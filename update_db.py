import sqlite3
import csv

def populate_db():
    conn = sqlite3.connect('staples.db')
    cursor = conn.cursor()
    
    # Open the CSV file and insert its data into the table
    with open('AisleData.csv', 'r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            cursor.execute('''
                INSERT INTO aisles (item_name, aisle_loc) VALUES (?, ?)
            ''', (row['Item Name'], row['Aisle_Loc']))
    
    conn.commit()
    conn.close()

if __name__ == "__main__":
    populate_db()
