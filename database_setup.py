import sqlite3

conn = sqlite3.connect("medicines.db")

cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS medicines(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    dosage TEXT,
    time TEXT,
    status TEXT
)
""")

conn.commit()
conn.close()

print("Database Created Successfully")