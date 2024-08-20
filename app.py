import streamlit as st
import sqlite3
from langchain_community.llms import Ollama

# Initialize Ollama
ollama = Ollama(model='llama3')

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
    
    # If the item isn't found in the database, handle accordingly
    # You could prompt to add the item to the database, or give a different response
    st.write(f"The item '{item}' was not found in the database.")
    return "Aisle information not available"

# Streamlit interface
st.title("Staples Aisle Finder")
item = st.text_input("Enter item name")

if st.button("Search"):
    if item:
        try:
            aisle = classify_aisle(item)
            st.write(f"Aisle: {aisle}")
        except Exception as e:
            st.write(f"Error: {e}")
    else:
        st.write("Please enter an item name.")
