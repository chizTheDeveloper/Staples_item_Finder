import sqlite3
from aisle_data import aisles

def populate_db():
    conn = sqlite3.connect('staples.db')
    cursor = conn.cursor()
    
    for item, aisle in aisles.items():
        cursor.execute('''
            INSERT INTO aisles (item, aisle) VALUES (?, ?)
        ''', (item, aisle))
    
    conn.commit()
    conn.close()

if __name__ == "__main__":
    populate_db()
