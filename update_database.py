import sqlite3

conn = sqlite3.connect("medicines.db")
cursor = conn.cursor()

try:
    cursor.execute("""
    ALTER TABLE medicines
    ADD COLUMN reminded TEXT DEFAULT 'No'
    """)
    print("Column added successfully")
except Exception as e:
    print("Column may already exist")

conn.commit()
conn.close()