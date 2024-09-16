import sqlite3

def check_table():
    conn = sqlite3.connect('staples.db')
    cursor = conn.cursor()
    
    # Run the PRAGMA command to check the table structure
    cursor.execute('PRAGMA table_info(aisles)')
    result = cursor.fetchall()
    for row in result:
        print(row)

    conn.close()

if __name__ == "__main__":
    check_table()