import sqlite3
from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from datemanager import *

root = Tk()
root.title("Booking System")
conn = sqlite3.connect("bookings.db")
cursor = conn.cursor()

cursor.execute("CREATE TABLE IF NOT EXISTS drivers ('first_name' TEXT, 'last_name' TEXT, 'car_reg' TEXT)")
cursor.execute("""CREATE TABLE IF NOT EXISTS clients 
               ('first_name' TEXT, 'last_name' TEXT, 'address' TEXT, phone_number TEXT, 'disability_support' TEXT)""")
cursor.execute("CREATE TABLE IF NOT EXISTS bookings ('driver' TEXT, 'date' TEXT, 'time' TEXT)")

driver_names = []
client_names = []
week = get_week()

cursor.execute("SELECT date FROM bookings")
dates = cursor.fetchall()
for day in dates:
    if inPast(day) == True:
        cursor.execute("DELETE FROM bookings WHERE date=?", day)
    else:
        pass

def add_driver():
    global fname_entry
    global lname_entry
    global reg_entry
    global top
    top = Toplevel()
    top.title("Add a new driver")
    driverTitle = Label(top, text="Add driver:")
    driverTitle.grid(row=0, column=0)

    fname_entry = Entry(top)
    fname_entry.insert(0, "First Name")
    fname_entry.grid(row=1, column=0)

    lname_entry = Entry(top)
    lname_entry.insert(0, "Last Name")
    lname_entry.grid(row=2, column=0)

    reg_entry = Entry(top)
    reg_entry.insert(0, "Car Registration Number")
    reg_entry.grid(row=3, column=0)

    submit_driver = Button(top, padx=60, text="Submit", command=func_subDr)
    submit_driver.grid(row=4, column=0)


def add_client():
    global fname_entry
    global lname_entry
    global line1Entry
    global line2Entry
    global line3Entry
    global pcEntry
    global phone_entry
    global dis_entry
    global top
    top = Toplevel()
    top.title("Add a new client")
    clientTitle = Label(top, text="Add client:")
    clientTitle.grid(row=0, column=0)

    fname_entry = Entry(top)
    fname_entry.insert(0, "First Name")
    fname_entry.grid(row=1, column=0)

    lname_entry = Entry(top)
    lname_entry.insert(0, "Last Name")
    lname_entry.grid(row=2, column=0)
    
    line1Label = Label(top, text="Address:").grid(row=3, column=0)
    line1Entry = Entry(top)
    line1Entry.insert(0, "Line 1")
    line1Entry.grid(row=4, column=0)
    line2Entry = Entry(top)
    line2Entry.insert(0, "Line 2")
    line2Entry.grid(row=5, column=0)
    line3Entry = Entry(top)
    line3Entry.insert(0, "Line 3")
    line3Entry.grid(row=6, column=0)
    pcEntry = Entry(top)
    pcEntry.insert(0, "Post Code")
    pcEntry.grid(row=7, column=0)
    placeholder = Label(top, text="").grid(row=8, column=0)

    phone_entry = Entry(top)
    phone_entry.insert(0, "Phone Number")
    phone_entry.grid(row=9, column=0)

    yesno = ["Yes", "No"]
    dis_entry = ttk.Combobox(top, values=yesno)
    dis_entry.set("Disability Support Required")
    dis_entry.grid(row=10, column=0)

    submit_client = Button(top, padx=60, text="Submit", command=func_subCl)
    submit_client.grid(row=11, column=0)


def make_booking():
    global day_slots
    global select_day
    global time_slots
    global select_time
    top = Toplevel()
    set_drivers(top)
    set_clients(top)
    top.title("Make a booking")
    day_slots = Listbox(top)
    for day in week:
        day_slots.insert(END, day)
    day_slots.grid(row=0, column=1, rowspan=5)
    Scrollbar(day_slots, orient="vertical")

    select_day = Button(top, padx=45, text="Select Day", command=day_sel)
    select_day.grid(row=5, column=1)

    time_slots = Listbox(top)
    times = ["09:00am","09:30am","10:00am","10:30am","11:00am","11:30am","12:00pm",
         "12:30pm","13:00pm","13:30pm","14:00pm","14:30pm","15:00pm","15:30pm"]
    for time in times:
        time_slots.insert(END, time)
    Scrollbar(time_slots, orient="vertical")

    select_time = Button(top, padx=40, text="Select Time", command=time_sel)


def set_drivers(top):
    global drivers
    global driver_names
    global select_driver
    cursor.execute("SELECT first_name, last_name FROM drivers")
    drivers = cursor.fetchall()
    for x in drivers:
        driver_name = x[0] + " " + x[1]
        driver_names.append(driver_name)
    select_driver = ttk.Combobox(top, values=driver_names)
    select_driver.set("Select a Driver")
    select_driver.grid(row=0, column=0)

def set_clients(top):
    global clients
    global client_names
    global select_client
    cursor.execute("SELECT first_name, last_name FROM clients")
    clients = cursor.fetchall()
    for x in clients:
        client_name = x[0] + " " + x[1]
        client_names.append(client_name)
    select_client = ttk.Combobox(top, values=client_names)
    select_client.set("Select a Client")
    select_client.grid(row=1, column=0)

def func_subDr():
    fname = fname_entry.get()
    lname =lname_entry.get()
    reg = reg_entry.get()
    incorrect = [fname == "First Name", fname == "", lname == "Last Name", 
                 lname == "", reg == "Car Registration Number", reg == ""]
    if any(incorrect):
        messagebox.showerror("Error", "Please complete driver details")
    else:
        driver_details = fname, lname, reg
        cursor.execute("INSERT INTO drivers VALUES (?,?,?)", driver_details)
        conn.commit()
        set_drivers(top)
        top.destroy()
        messagebox.showinfo("Success", "Details submitted successfully")

def func_subCl():
    fname = fname_entry.get()
    lname = lname_entry.get()
    line1 = line1Entry.get()
    line2 = line2Entry.get()
    line3 = line3Entry.get()
    postcode = pcEntry.get()
    phone = phone_entry.get()
    disability = dis_entry.get()
    incorrect = [fname == "First Name", fname == "", lname == "Last Name", lname == "", 
                 line1 == "", line2 == "", line3 == "", postcode == "", phone == "Phone Number", 
                 phone == "", disability == "Disability Support Required"]
    if any(incorrect):
        messagebox.showerror("Error", "Please complete client details")
    else:
        address = line1 + ", " + line2 + ", " + line3 + ", " + postcode
        client_details = fname, lname, address, phone, disability
        cursor.execute("INSERT INTO clients VALUES (?,?,?,?,?)", client_details)
        conn.commit()
        set_clients(top)
        top.destroy()
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
            conn.commit()
            show_bookings()
            messagebox.showinfo("Booking Confirmed", "Confirmed Booking:\n\n" + s_driver + ", " + s_day + ", " + s_time)

def show_bookings():
    global accounts
    global acc_sel
    cursor.execute("SELECT date, time FROM bookings")
    bookings = cursor.fetchall()
    pres_bookings = Listbox(root)
    for booking in bookings:
        pres_bookings.insert(END, booking)
        pres_bookings.grid(row=0, column=1, rowspan=4)
    Scrollbar(pres_bookings, orient="vertical")

def show_details():
    pass

def edit_booking():
    pass

## Home Widgets ##
show_bookings()

optionsLabel = Label(root, text="Options:").grid(row=0, column=0)

drivers_button = Button(root, padx=10, text="Add new driver details", command=add_driver)
drivers_button.grid(row=1, column=0)

client_button = Button(root, padx=10, text="Add new client details", command=add_client)
client_button.grid(row=2, column=0)

book_button = Button(root, padx=15, text="Make a new booking", command=make_booking)
book_button.grid(row=3, column=0)

edit_button = Button(root, padx=40, text="Edit booking", command=edit_booking)
edit_button.grid(row=4, column=0)

details_button = Button(root, padx=10, text="Show booking details", command=show_details)
details_button.grid(row=4, column=1)


## End of Home Widgets ##

conn.commit()
root.mainloop()
conn.close()