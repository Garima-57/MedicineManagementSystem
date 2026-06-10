import tkinter as tk
import sqlite3
from datetime import datetime
from plyer import notification

# -----------------------------
# Dashboard
# -----------------------------

def update_dashboard():

    conn = sqlite3.connect("medicines.db")
    cursor = conn.cursor()

    cursor.execute("SELECT COUNT(*) FROM medicines")
    total = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM medicines WHERE status='Taken'")
    taken = cursor.fetchone()[0]

    pending = total - taken

    if total == 0:
        adherence = 0
    else:
        adherence = round((taken / total) * 100, 2)

    total_label.config(text=f"Total Medicines: {total}")
    taken_label.config(text=f"Taken: {taken}")
    pending_label.config(text=f"Pending: {pending}")
    adherence_label.config(text=f"Adherence Rate: {adherence}%")

    conn.close()


# -----------------------------
# Load Medicines
# -----------------------------

def load_medicines():

    medicine_list.delete(0, tk.END)

    conn = sqlite3.connect("medicines.db")
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM medicines")

    rows = cursor.fetchall()

    for row in rows:
        medicine_list.insert(
            tk.END,
            f"{row[0]} | {row[1]} | {row[2]} | {row[3]} | {row[4]}"
        )

    conn.close()

    update_dashboard()


# -----------------------------
# Add Medicine
# -----------------------------

def add_medicine():

    name = medicine_entry.get()
    dosage = dosage_entry.get()
    med_time = time_entry.get()

    if name == "" or dosage == "" or med_time == "":
        return

    conn = sqlite3.connect("medicines.db")
    cursor = conn.cursor()

    cursor.execute("""
    INSERT INTO medicines(name,dosage,time,status,reminded)
    VALUES(?,?,?,?,?)
    """, (name, dosage, med_time, "Pending", "No"))

    conn.commit()
    conn.close()

    medicine_entry.delete(0, tk.END)
    dosage_entry.delete(0, tk.END)
    time_entry.delete(0, tk.END)

    load_medicines()


# -----------------------------
# Mark Taken
# -----------------------------

def mark_taken():

    selected = medicine_list.curselection()

    if not selected:
        return

    item = medicine_list.get(selected[0])

    medicine_id = item.split("|")[0].strip()

    conn = sqlite3.connect("medicines.db")
    cursor = conn.cursor()

    cursor.execute("""
    UPDATE medicines
    SET status='Taken'
    WHERE id=?
    """, (medicine_id,))

    conn.commit()
    conn.close()

    load_medicines()


# -----------------------------
# Delete Medicine
# -----------------------------

def delete_medicine():

    selected = medicine_list.curselection()

    if not selected:
        return

    item = medicine_list.get(selected[0])

    medicine_id = item.split("|")[0].strip()

    conn = sqlite3.connect("medicines.db")
    cursor = conn.cursor()

    cursor.execute(
        "DELETE FROM medicines WHERE id=?",
        (medicine_id,)
    )

    conn.commit()
    conn.close()

    load_medicines()
#-----------------------------  
# Check Reminders
#-----------------------------

def check_reminders():

    current_time = datetime.now().strftime("%H:%M")

    conn = sqlite3.connect("medicines.db")
    cursor = conn.cursor()

    cursor.execute("""
    SELECT id, name, dosage
    FROM medicines
    WHERE time=?
    AND status='Pending'
    AND reminded='No'
    """, (current_time,))

    medicines = cursor.fetchall()

    for medicine in medicines:

        notification.notify(
            title="Medicine Reminder",
            message=f"Time to take {medicine[1]}\nDosage: {medicine[2]}",
            timeout=10
        )

        cursor.execute("""
        UPDATE medicines
        SET reminded='Yes'
        WHERE id=?
        """, (medicine[0],))

    conn.commit()
    conn.close()

    root.after(10000, check_reminders)

# -----------------------------
# GUI
# -----------------------------

root = tk.Tk()

root.title("Medicine Management System")
root.geometry("900x750")

title = tk.Label(
    root,
    text="Medicine Management System",
    font=("Arial", 22, "bold")
)
title.pack(pady=10)

# Dashboard

dashboard_heading = tk.Label(
    root,
    text="📊 Dashboard",
    font=("Arial", 14, "bold")
)
dashboard_heading.pack(pady=5)

total_label = tk.Label(root, text="Total Medicines: 0")
total_label.pack()

taken_label = tk.Label(root, text="Taken: 0")
taken_label.pack()

pending_label = tk.Label(root, text="Pending: 0")
pending_label.pack()

adherence_label = tk.Label(root, text="Adherence Rate: 0%")
adherence_label.pack(pady=10)

# Input Fields

medicine_heading = tk.Label(
    root,
    text="💊 Add New Medicine",
    font=("Arial", 14, "bold")
)
medicine_heading.pack(pady=10)

tk.Label(root, text="Medicine Name").pack()
medicine_entry = tk.Entry(root, width=40)
medicine_entry.pack(pady=5)

tk.Label(root, text="Dosage").pack()
dosage_entry = tk.Entry(root, width=40)
dosage_entry.pack(pady=5)

tk.Label(root, text="Time (HH:MM)").pack()
time_entry = tk.Entry(root, width=40)
time_entry.pack(pady=5)

# Buttons

tk.Button(
    root,
    text="Add Medicine",
    command=add_medicine
).pack(pady=5)

tk.Button(
    root,
    text="Mark as Taken",
    command=mark_taken
).pack(pady=5)

tk.Button(
    root,
    text="Delete Medicine",
    command=delete_medicine
).pack(pady=5)

# Medicine List

tk.Label(
    root,
    text="Saved Medicines",
    font=("Arial", 12, "bold")
).pack(pady=10)

medicine_list = tk.Listbox(
    root,
    width=90,
    height=15
)

medicine_list.pack()

load_medicines()

check_reminders()

root.mainloop()