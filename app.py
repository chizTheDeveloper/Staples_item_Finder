import streamlit as st
import sqlite3
import re
from groq import Groq
import os

# Set the API key from either the environment variable or Streamlit secrets
api_key = os.getenv("GROQ_API_KEY") or st.secrets["groq"]["api_key"]
client = Groq(api_key=api_key)

# Function to preprocess and normalize item names
def normalize_item_name(item):
    doc = nlp(item)
    return " ".join([token.lemma_ for token in doc])

# Function to remove common words and extract the main item
def extract_item_from_query(query):
    stop_words = set(["where", "can", "i", "find", "the", "in", "a", "an", "at"])
    words = re.findall(r'\b\w+\b', query.lower())
    keywords = [word for word in words if word not in stop_words]
    return ' '.join(keywords)

# Function to get the aisle from the database
def get_aisle_from_db(item):
    conn = sqlite3.connect('staples.db')
    cursor = conn.cursor()

    # Normalize item before querying database
    normalized_item = normalize_item_name(item)
    
    # Perform a case-insensitive LIKE query with normalized item name
    cursor.execute('SELECT aisle FROM aisles WHERE item LIKE ?', ('%' + normalized_item + '%',))
    result = cursor.fetchone()
    conn.close()
    
    return result[0] if result else None

# Function to classify the aisle
def classify_aisle(item):
    keyword = extract_item_from_query(item)
    
    # Step 1: Attempt to fetch the aisle from the database
    aisle = get_aisle_from_db(keyword)
    if aisle:
        return aisle

    # Step 2: Call Groq if not found in the database
    completion = client.chat.completions.create(
        model="llama3-8b-8192",
        messages=[
            {
                "role": "user",
                "content": f"Which aisle would you find '{keyword}' in a Staples store?",
            }
        ],
        temperature=1,
        max_tokens=1024,
        top_p=1,
        stream=True,
        stop=None,
    )

    response = ""
    for chunk in completion:
        response += chunk.choices[0].delta.content or ""

    response = response.strip()
    return response

# Initialize conversation history in Streamlit session state
if 'conversation' not in st.session_state:
    st.session_state.conversation = []
if 'latest_response' not in st.session_state:
    st.session_state.latest_response = ""

# Streamlit interface
st.title("🛒 Staples Aisle Finder Chatbot")

# Display chat history
for message in st.session_state.conversation:
    if message['role'] == 'user':
        # User message with black icon
        st.markdown(f"""
            <div style="display: flex; align-items: flex-start; margin-bottom: 10px;">
                <div style="width: 20px; height: 20px; background-color: black; border-radius: 50%; margin-right: 10px;"></div>
                <div style="background-color: #f1f1f1; padding: 10px; border-radius: 10px; max-width: 80%;">
                    {message["content"]}
                </div>
            </div>
        """, unsafe_allow_html=True)
    else:
        # Staples message with red icon
        st.markdown(f"""
            <div style="display: flex; align-items: flex-start; margin-bottom: 10px;">
                <div style="width: 20px; height: 20px; background-color: red; border-radius: 50%; margin-right: 10px;"></div>
                <div style="background-color: #ffe6e6; padding: 10px; border-radius: 10px; max-width: 80%;">
                    {message["content"]}
                </div>
            </div>
        """, unsafe_allow_html=True)

# Use a form to keep input at the bottom
with st.form(key='input_form', clear_on_submit=True):
    user_input = st.text_input("🔍 What are you looking for...", placeholder="e.g., Where can I find pens?", key='input')
    submit_button = st.form_submit_button(label='Send')

    if submit_button and user_input:
        # Add user query to chat history
        st.session_state.conversation.append({"role": "user", "content": user_input})

        # Get the aisle information
        try:
            aisle = classify_aisle(user_input)
            response = f"**Suggested Aisle:** {aisle}"
            nresponse = f" {aisle}"
            nuser = f"**You** {user_input}" 
            
            # Add Staples response to conversation history
            st.session_state.conversation.append({"role": "staples", "content": nresponse})
            st.session_state.latest_response = response
            st.session_state.user_input = nuser
        except Exception as e:
            st.session_state.conversation.append({"role": "staples", "content": f"Error: {e}"})
            st.session_state.latest_response = f"Error: {e}"

# Display the latest response directly
if st.session_state.latest_response:
    st.write(st.session_state.user_input)
    st.write(st.session_state.latest_response)

# Optional: Add some spacing at the bottom
st.markdown("<br>" * 3, unsafe_allow_html=True)
