import sqlite3

conn = sqlite3.connect("medicines.db")
cursor = conn.cursor()

cursor.execute("SELECT * FROM medicines")

rows = cursor.fetchall()

for row in rows:
    print(row)

conn.close()