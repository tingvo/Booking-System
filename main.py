import sqlite3
from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from datemanager import *

root = Tk()
root.title("Booking System")
conn = sqlite3.connect("bookings.db")
cursor = conn.cursor()

cursor.execute("""CREATE TABLE IF NOT EXISTS drivers 
               ('first_name' TEXT, 'last_name' TEXT, 'phone_number' TEXT, 'day_exceptions' TEXT)""")
cursor.execute("""CREATE TABLE IF NOT EXISTS clients 
               ('first_name' TEXT, 'last_name' TEXT, 'address' TEXT, phone_number TEXT, 'disability_support' TEXT)""")
cursor.execute("CREATE TABLE IF NOT EXISTS bookings ('driver' TEXT, 'client' TEXT, 'date' TEXT, 'time' TEXT)")

driver_names = []
client_names = []
week = get_week()
drivers_set = False
clients_set = False

#Deletes expired bookings
cursor.execute("SELECT date FROM bookings")
dates = cursor.fetchall()
for day in dates:
    if inPast(day[0]) == True:
        cursor.execute("DELETE FROM bookings WHERE date=?", day)
    else:
        pass

def add_driver():
    global fname_entry
    global lname_entry
    global phone_entry
    global dexc_entry
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

    phone_entry = Entry(top)
    phone_entry.insert(0, "Phone Number")
    phone_entry.grid(row=3, column=0)

    dexc_label = Label(top, text="Please list any day exceptions:").grid(row=4, column=0)
    dexc_entry = Entry(top)
    dexc_entry.grid(row=5, column=0)

    submit_driver = Button(top, padx=60, text="Submit", command=func_subDr)
    submit_driver.grid(row=6, column=0)


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

def book_or_edit(state):
    global day_slots
    global select_day
    global time_slots
    global select_time
    global top
    dateAndTime = pres_bookings.get(ACTIVE)
    date = dateAndTime[0]
    time = dateAndTime[1]
    top = Toplevel()
    if state == 0:
        current_dr = current_cl = "0"
    if state == 1:
        cursor.execute("SELECT * FROM bookings WHERE date=? AND time=?", (date, time))
        details = cursor.fetchone()
        current_dr = details[0]
        current_cl = details[1]
    set_drivers(top, current_dr)
    set_clients(top, current_cl)
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


def set_drivers(top, current_dr):
    global drivers
    global driver_names
    global select_driver
    global drivers_set
    if current_dr == "0":
        current_dr = "Select a Driver"
    if drivers_set == True:
        driver_names.clear()
    cursor.execute("SELECT first_name, last_name FROM drivers")
    drivers = cursor.fetchall()
    for x in drivers:
        driver_name = x[0] + " " + x[1]
        driver_names.append(driver_name)
    drivers_set = True
    select_driver = ttk.Combobox(top, values=driver_names)
    select_driver.set(current_dr)
    select_driver.grid(row=0, column=0)

def set_clients(top, current_cl):
    global clients
    global client_names
    global select_client
    global clients_set
    if current_cl == "0":
        current_cl = "Select a Client"
    if clients_set == True:
        client_names.clear()
    cursor.execute("SELECT first_name, last_name FROM clients")
    clients = cursor.fetchall()
    for x in clients:
        client_name = x[0] + " " + x[1]
        client_names.append(client_name)
    clients_set = True
    select_client = ttk.Combobox(top, values=client_names)
    select_client.set(current_cl)
    select_client.grid(row=1, column=0)

def func_subDr():
    fname = fname_entry.get()
    lname =lname_entry.get()
    phone = phone_entry.get()
    day_exc = dexc_entry.get()
    incorrect = [fname == "First Name", fname == "", lname == "Last Name", 
                 lname == "", phone == "Phone Number", phone == ""]
    if any(incorrect):
        messagebox.showerror("Error", "Please complete driver details")
    else:
        driver_details = fname, lname, phone, day_exc
        cursor.execute("INSERT INTO drivers VALUES (?,?,?,?)", driver_details)
        conn.commit()
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
        top.destroy()
        messagebox.showinfo("Success", "Details submitted successfully")

def available(s_driverx):
    cursor.execute("SELECT day_exceptions FROM drivers WHERE first_name=? AND last_name=?", (s_driverx[0], s_driverx[1]))
    exceptions = cursor.fetchone()
    if isDayException(s_day, exceptions):
        messagebox.showerror("Error", "That driver is not available on that day")
        return False
    else:
        return True

def day_sel():
    global s_day
    global day_slots
    global select_day
    global s_driver
    global s_client
    s_driver = select_driver.get()
    s_client = select_client.get()
    s_driverx = s_driver.split()
    s_day = day_slots.get(ACTIVE)
    if s_driver == "Select a Driver" and s_client == "Select a Client":
        messagebox.showerror("Error", "Please select a driver and client")
    elif s_driver == "Select a Driver":
        messagebox.showerror("Error", "Please select a driver")
    elif s_client == "Select a Client":
        messagebox.showerror("Error", "Please select a client")
    else:
        if available(s_driverx):
            day_slots.destroy()
            select_day.destroy()
            time_slots.grid(row=0, column=1, rowspan=5)
            select_time.grid(row=5, column=1)

def time_sel():
    global s_time
    global time_slots
    global select_time
    s_time = time_slots.get(ACTIVE)
    choice = messagebox.askyesno("Details", "Are these the correct details for the booking?\n\n" 
                                 + s_driver + ", " + s_day + ", " + s_time)
    if choice == True:
        booking = s_driver, s_client, s_day, s_time
        cursor.execute("INSERT INTO bookings VALUES (?,?,?,?)", booking)
        conn.commit()
        show_bookings()
        top.destroy()
        messagebox.showinfo("Booking Confirmed", "Confirmed Booking:\n\n" 
                             + s_driver + ", " + s_client + ", " + s_day + ", " + s_time)

def show_bookings():
    global pres_bookings
    cursor.execute("SELECT date, time FROM bookings")
    bookings = cursor.fetchall()
    pres_bookings = Listbox(root)
    for booking in bookings:
        pres_bookings.insert(END, booking)
        pres_bookings.grid(row=0, column=1, rowspan=4)
    Scrollbar(pres_bookings, orient="vertical")

def format_address(addressY):
    address = ""
    for addressZ in addressY:
        address += " " + addressZ
    return address

def show_details():
    dateAndTime = pres_bookings.get(ACTIVE)
    date = dateAndTime[0]
    time = dateAndTime[1]
    cursor.execute("SELECT * FROM bookings WHERE date=? AND time=?", (date, time))
    details = cursor.fetchone()
    cursor.execute("SELECT client FROM bookings WHERE date=? AND time=?", (date, time))
    clientx = cursor.fetchone()
    client = clientx[0].split()
    cursor.execute("SELECT address FROM clients WHERE first_name=? AND last_name=?", (client[0], client[1]))
    addressX = cursor.fetchone()
    addressY = addressX[0].split()
    address = format_address(addressY)
    cursor.execute("SELECT phone_number FROM clients WHERE first_name=? AND last_name=?", (client[0], client[1]))
    phone = cursor.fetchone()
    messagebox.showinfo("Booking Details", "Driver: " + details[0] + "\n\n" + "Client: " 
                        + details[1] + "\n" + "Client Phone: " + phone[0] + "\n\n" + "Date: " 
                        + details[2] + "\n\n" + "Time: " + details[3] + "\n\n"
                        + "Address: " + address)

## Home Widgets ##
show_bookings()

optionsLabel = Label(root, text="Options:").grid(row=0, column=0)

drivers_button = Button(root, padx=10, text="Add new driver details", command=add_driver)
drivers_button.grid(row=1, column=0)

client_button = Button(root, padx=10, text="Add new client details", command=add_client)
client_button.grid(row=2, column=0)

book_button = Button(root, padx=15, text="Make a new booking", command=lambda:book_or_edit(0))
book_button.grid(row=3, column=0)

edit_button = Button(root, padx=40, text="Edit booking", command=lambda:book_or_edit(1))
edit_button.grid(row=4, column=0)

details_button = Button(root, padx=10, text="Show booking details", command=show_details)
details_button.grid(row=4, column=1)
## End of Home Widgets ##

conn.commit()
root.mainloop()
conn.close()