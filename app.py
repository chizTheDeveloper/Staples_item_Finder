import streamlit as st
import sqlite3
import os
from groq import Groq
from dotenv import load_dotenv
import os

load_dotenv("staples.env")
api_key = os.getenv("GROQ_API_KEY")

# Initialize Groq client
client = Groq(api_key=os.environ.get("GROQ_API_KEY"))

def get_aisle_from_db(item):
    conn = sqlite3.connect('staples.db')
    cursor = conn.cursor()
    cursor.execute('SELECT aisle FROM aisles WHERE item = ?', (item,))
    result = cursor.fetchone()
    conn.close()
    return result[0] if result else None

def classify_aisle(item):
    aisle = get_aisle_from_db(item)
    if aisle:
        return aisle
    
    # Call Groq to infer the aisle
    completion = client.chat.completions.create(
        model="llama3-8b-8192",
        messages=[
            {
                "role": "user",
                "content": f"Which aisle would you find '{item}' in a Staples store?",
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

    # Provide a general suggestion
    return response

# Streamlit interface
st.title("Staples Aisle Finder")
item = st.text_input("Enter item name")

if st.button("Search"):
    if item:
        try:
            aisle = classify_aisle(item)
            st.write(f"**Suggested Aisle:** {aisle}")
            st.write(f"**More details:** In a Staples store, {aisle}")
        except Exception as e:
            st.write(f"Error: {e}")
    else:
        st.write("Please enter an item name.")
