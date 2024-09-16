import sqlite3

def create_table():
    conn = sqlite3.connect('staples.db')
    cursor = conn.cursor()
    
    # Drop the table if it exists to avoid schema conflicts
    cursor.execute('DROP TABLE IF EXISTS aisles')
    
    # Create the table with correct column names
    cursor.execute('''
        CREATE TABLE aisles (
            item_name TEXT,
            aisle_loc TEXT
        )
    ''')
    
    conn.commit()
    conn.close()

if __name__ == "__main__":
    create_table()