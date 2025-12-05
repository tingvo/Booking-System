import sqlite3
from tkinter import *
from tkinter import ttk
from tkinter import messagebox
import datetime

root = Tk()
conn = sqlite3.connect("bookings.db")
cursor = conn.cursor()

cursor.execute("CREATE TABLE IF NOT EXISTS drivers ('first_name' TEXT, 'last_name' TEXT, 'car_reg' TEXT)")
cursor.execute("CREATE TABLE IF NOT EXISTS bookings ('driver' TEXT, 'date' TEXT, 'time' TEXT)")

def submit():
    pass

## Widgets ##
driverTitle = Label(root, text="Add driver:")
driverTitle.grid(row=0, column=0)

fname_entry = Entry(root)
fname_entry.insert(0, "First Name")
fname_entry.grid(row=1, column=0)

lname_entry = Entry(root)
lname_entry.insert(0, "Last Name")
lname_entry.grid(row=2, column=0)

submit_driver = Button(root, padx=60, text="Submit", command=submit)
submit_driver.grid(row=3, column=0)

conn.commit()
root.mainloop()
conn.close()