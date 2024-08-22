import streamlit as st
import sqlite3
import os
from langchain_community.llms import Ollama

# Initialize Ollama
ollama = Ollama(model='llama3')

def get_aisle_from_db(item):
    # Get the absolute path to the database
    db_path = os.path.join(os.path.dirname(__file__), 'staples.db')
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # Use a SQL query to find a partial match
    cursor.execute("SELECT aisle FROM aisles WHERE ? LIKE '%' || item || '%'", (item,))
    result = cursor.fetchone()
    conn.close()
    return result[0] if result else None

def classify_aisle(item):
    aisle = get_aisle_from_db(item)
    if aisle:
        return f"**Suggested Aisle:** {aisle}\n\n**More details:** This item can be found in {aisle}. Please note that the exact location may vary depending on the store layout."

    # Call Ollama to infer the aisle if not found in the database
    response = ollama(f"Which aisle would you find '{item}' in a Staples store?")
    response = response.strip()
    
    # Provide a general suggestion
    return f"**Suggested Aisle:** {response}\n\n**More details:** The item might not be found in our database, but it should be located in a similar section of the store."

# Streamlit interface
st.title("Staples Store Guide")

# Add an admin login button on the top right
st.markdown(
    """
    <div style="text-align: right;">
        <a href="/admin" target="_self" style="text-decoration: none;">
            <button style="background-color:white; color: red; padding: 10px 20px; margin-top: 20px; border: 2px solid rgba(255, 0, 0, 0.7);">
                Admin Login
            </button>
        </a>
    </div>
    """,
    unsafe_allow_html=True
)

item = st.text_input("Enter item name")

# Style the search button with red background and white text
search_button_html = """
    <style>
    .stButton > button {
        background-color: red;
        color: white;
        border-radius: 5px;
        padding: 10px 20px;
    }
    </style>
    """
st.markdown(search_button_html, unsafe_allow_html=True)

if st.button("Search"):
    if item:
        try:
            aisle = classify_aisle(item)
            st.write(aisle)
        except Exception as e:
            st.write(f"Error: {e}")
    else:
        st.write("Please enter an item name.")
