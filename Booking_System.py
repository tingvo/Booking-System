import sqlite3
from tkinter import *
from tkinter import ttk
from tkinter import messagebox
import calendar
import datetime

root = Tk()
root.title("Booking System")
conn = sqlite3.connect("bookings.db")
cursor = conn.cursor()

cursor.execute("CREATE TABLE IF NOT EXISTS drivers ('first_name' TEXT, 'last_name' TEXT, 'car_reg' TEXT)")
cursor.execute("CREATE TABLE IF NOT EXISTS bookings ('driver' TEXT, 'date' TEXT, 'time' TEXT)")

def set_drivers():
    global drivers
    global driver_names
    global select_driver
    cursor.execute("SELECT first_name, last_name FROM drivers")
    drivers = cursor.fetchall()
    for x in drivers:
        driver_name = x[0] + " " + x[1]
        driver_names.append(driver_name)
    select_driver = ttk.Combobox(root, values=driver_names)
    select_driver.set("Select a Driver")
    select_driver.grid(row=5, column=0)

def submit():
    fname = fname_entry.get()
    lname =lname_entry.get()
    reg = reg_entry.get()
    if fname == "First Name" or fname == "" or lname == "Last Name" or lname == "" or reg == "Car Registration Number" or reg == "":
        messagebox.showerror("Error", "Please complete driver details")
    else:
        driver_details = fname, lname, reg
        cursor.execute("INSERT INTO drivers VALUES (?,?,?)", driver_details)
        conn.commit()
        set_drivers()
        messagebox.showinfo("Success", "Details submitted successfully")

def day_sel():
    global s_day
    global day_slots
    global select_day
    s_day = day_slots.get(ACTIVE)
    day_slots.destroy()
    select_day.destroy()
    time_slots.grid(row=0, column=1, rowspan=5)
    select_time.grid(row=5, column=1)

def time_sel():
    global s_time
    global time_slots
    global select_time
    s_time = time_slots.get(ACTIVE)
    s_driver = select_driver.get()
    if s_driver == "Select a Driver":
        messagebox.showerror("Error", "Please select a driver")
    else:
        choice = messagebox.askyesno("Details", "Are these the correct details for the booking?\n\n" + s_driver + ", " + s_day + ", " + s_time)
        if choice == True:
            booking = s_driver, s_day, s_time
            cursor.execute("INSERT INTO bookings VALUES (?,?,?)", booking)
            messagebox.showinfo("Booking Confirmed", "Confirmed Booking:\n\n" + s_driver + ", " + s_day + ", " + s_time)

## Widgets ##
driverTitle = Label(root, text="Add driver:")
driverTitle.grid(row=0, column=0)

fname_entry = Entry(root)
fname_entry.insert(0, "First Name")
fname_entry.grid(row=1, column=0)

lname_entry = Entry(root)
lname_entry.insert(0, "Last Name")
lname_entry.grid(row=2, column=0)

reg_entry = Entry(root)
reg_entry.insert(0, "Car Registration Number")
reg_entry.grid(row=3, column=0)

submit_driver = Button(root, padx=60, text="Submit", command=submit)
submit_driver.grid(row=4, column=0)

driver_names = []
set_drivers()

day_slots = Listbox()
days = ["Monday","Tuesday","Wednesday","Thursday","Friday","Saturday","Sunday"]
for day in days:
    day_slots.insert(END, day)
day_slots.grid(row=0, column=1, rowspan=5)
Scrollbar(day_slots, orient="vertical")

select_day = Button(root, padx=45, text="Select Day", command=day_sel)
select_day.grid(row=5, column=1)

time_slots = Listbox()
times = ["09:00am","09:30am","10:00am","10:30am","11:00am","11:30am","12:00pm",
         "12:30pm","13:00pm","13:30pm","14:00pm","14:30pm","15:00pm","15:30pm"]
for time in times:
    time_slots.insert(END, time)
Scrollbar(time_slots, orient="vertical")

select_time = Button(root, padx=40, text="Select Time", command=time_sel)
## End of Widgets ##

conn.commit()
root.mainloop()
conn.close()