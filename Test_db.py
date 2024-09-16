import sqlite3

def search_item(item_name):
    conn = sqlite3.connect('staples.db')
    cursor = conn.cursor()

    # Query the database for the item
    cursor.execute('SELECT aisle_loc FROM aisles WHERE item_name = ?', (item_name,))
    result = cursor.fetchone()
    
    if result:
        print(f"Item '{item_name}' is located in: {result[0]}")
    else:
        print(f"Item '{item_name}' not found in database.")
    
    conn.close()

if __name__ == "__main__":
    search_item("Laser paper")
