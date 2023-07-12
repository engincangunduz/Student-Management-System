import pymysql
from tkinter import *
from tkinter import ttk
from tkinter import messagebox
import tkinter as tk

#connection late
def connection():
    conn = pymysql.connect(
        host='localhost', user='root', password='', db='student.db',port=3307
    )
    return conn


def refreshTable():
    for data in my_tree.get_children():
        my_tree.delete(data)

    for array in read():
        my_tree.insert(parent='', index='end', iid=array, text="", values=(array), tag='orow')

    my_tree.tag_configure('orow', background="#EEEEEE", font="Arial 12")
    my_tree.grid(row=8, column=0, columnspan=5, rowspan=11, padx=10, pady=20)


root = Tk()
root.title("Student Registration System")
root.geometry("1400x800")
my_tree = ttk.Treeview(root)
# root.attributes("-fullscreen", True)
# root.bind("<Escape>", lambda event: root.attributes("-fullscreen", False))

#functions later

#placeholders for entry
ph1 = tk.StringVar()
ph2 = tk.StringVar()
ph3 = tk.StringVar()
ph4 = tk.StringVar()
ph5 = tk.StringVar()
ph6 = tk.StringVar()

def setph(word, num):
    if num == 1:
        ph1.set(word)
    if num == 2:
        ph2.set(word)
    if num == 3:
        ph3.set(word)
    if num == 4:
        ph4.set(word)
    if num == 5:
        ph5.set(word)
    if num == 6:
        ph6.set(word)


def read():
    conn = connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM student")
    results = cursor.fetchall()
    conn.commit()
    conn.close()
    return results


def add():
    studid = str(studident.get())
    fname = str(fnameent.get())
    lname = str(lnameent.get())
    adrees = str(adressent.get())
    phone = str(phoneent.get())
    depart = str(departent.get())

    if(studid == "" or studid == " ") or (fname == "" or fname == " ") or (lname == "" or lname == " ") or (adrees == "" or adrees == " ") or (phone == "" or phone == " ") or (depart == "" or depart == " "):
        messagebox.showinfo("Error", "Please fill up the blank entry")
        return
    else:
        try:
            conn = connection()
            cursor = conn.cursor()
            cursor.execute("INSERT INTO student VALUES ('"+studid+"','"+fname+"','"+lname+"','"+adrees+"','"+phone+"','"+depart+"')")
            conn.commit()
            conn.close()
        except:
            messagebox.showinfo("Error", "Stud ID already exist")
            return

    refreshTable()


def reset():
    desicion = messagebox.askquestion("Warning!", "Delete all data?")
    if desicion != "yes":
        return
    else:
        try:
            conn = connection()
            cursor = conn.cursor()
            cursor.execute("DELETE FROM student")
            conn.commit()
            conn.close()
        except:
            messagebox.showinfo("Error", "Sorry an error occured")
            return

    refreshTable()


def delete():
    desicion = messagebox.askquestion("Warning!", "Delete the selected data?")
    if desicion != "yes":
        return
    else:
        selected_item = my_tree.selection()[0]
        deleteData = str(my_tree.item(selected_item)['values'][0])
        try:
            conn = connection()
            cursor = conn.cursor()
            cursor.execute("DELETE FROM student WHERE STUDID='"+str(deleteData)+"'")
            conn.commit()
            conn.close()
        except:
            messagebox.showinfo("Error", "Sorry an error occured")
            return

    refreshTable()


def select():
    try:
        selected_item = my_tree.selection()[0]
        studid = str(my_tree.item(selected_item)['values'][0])
        fname = str(my_tree.item(selected_item)['values'][1])
        lname = str(my_tree.item(selected_item)['values'][2])
        address = str(my_tree.item(selected_item)['values'][3])
        phone = str(my_tree.item(selected_item)['values'][4])
        depart = str(my_tree.item(selected_item)['values'][5])

        setph(studid, 1)
        setph(fname, 2)
        setph(lname, 3)
        setph(address, 4)
        setph(phone, 5)
        setph(depart,6)
    except:
        messagebox.showinfo("Error", "Please select a data row")


def search():
    studid = str(studident.get())
    fname = str(fnameent.get())
    lname = str(lnameent.get())
    address = str(adressent.get())
    phone = str(phoneent.get())
    depart = str(departent.get())

    conn = connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM student WHERE STUDID='"+
                   studid+"'or FNAME='" +
                   fname+"'or LNAME='" +
                   lname+"'or ADDRESS='" +
                   address+"'or PHONE='" +
                   phone+"'or DEPARTMENT='" +
                   depart+"' ")

    try:
        result = cursor.fetchall()
        for num in range(0, 6):
            setph(result[0][num], (num+1))

        conn.commit()
        conn.close()
    except:
        messagebox.showinfo("Error", "No data found")


def update():
    selectedStudid = ""
    try:
        selected_item = my_tree.selection()[0]
        selectedStudid = str(my_tree.item(selected_item)['values'][0])
    except:
        messagebox.showinfo("Error", "No data found")

    studid = str(studident.get())
    fname = str(fnameent.get())
    lname = str(lnameent.get())
    address = str(adressent.get())
    phone = str(phoneent.get())
    depart = str(departent.get())

    if (studid == "" or studid == " ") or (fname == "" or fname == " ") or (lname == "" or lname == " ") or (address == "" or address == " ") or (phone == "" or phone == " ") or (depart == "" or depart == " "):
        messagebox.showinfo("Error", "Please fill up the blank entry")
        return
    else:
        try:
            conn = connection()
            cursor = conn.cursor()
            cursor.execute("UPDATE student SET STUDID='" +
                           studid+"', FNAME='" +
                           fname+"', LNAME='" +
                           lname+"', ADDRESS='" +
                           address+"', PHONE='" +
                           phone+"' WHERE STUDID='" +
                           selectedStudid+"' ")
            conn.commit()
            conn.close()
        except:
            messagebox.showinfo("Error", "Stud ID already exist")
            return

    refreshTable()


lbl = Label(root, text="Student Registration System", font="Arial 30 bold")
lbl.grid(row=0, column=1, columnspan=1, rowspan=2, padx=50, pady=40)

studidlbl = Label(root, text="Stud ID", font="Arial 15")
fnamelbl = Label(root, text="Firstname", font="Arial 15")
lnamelbl = Label(root, text="Lastname", font="Arial 15")
adresslbl = Label(root, text="Adress", font="Arial 15")
phonelbl = Label(root, text="Phone", font="Arial 15")
departlbl = Label(root, text="Department",font="Arial 15")

studidlbl.grid(row=3, column=0, columnspan=1, padx=50, pady=5)
fnamelbl.grid(row=4, column=0, columnspan=1, padx=50, pady=5)
lnamelbl.grid(row=5, column=0, columnspan=1, padx=50, pady=5)
adresslbl.grid(row=6, column=0, columnspan=1, padx=50, pady=5)
phonelbl.grid(row=7, column=0, columnspan=1, padx=50, pady=5)
departlbl.grid(row=8, column=0, columnspan=1, padx=50, pady=5)

#text variable later
studident = Entry(root, width=55, bd=5, font="Arial 15", textvariable=ph1)
fnameent = Entry(root, width=55, bd=5, font="Arial 15", textvariable=ph2)
lnameent = Entry(root, width=55, bd=5, font="Arial 15", textvariable=ph3)
adressent = Entry(root, width=55, bd=5, font="Arial 15", textvariable=ph4)
phoneent = Entry(root, width=55, bd=5, font="Arial 15", textvariable=ph5)
departent = Entry(root, width=55, bd=5, font="Arial 15", textvariable=ph6)

studident.grid(row=3, column=1, columnspan=4, padx=5, pady=0)
fnameent.grid(row=4, column=1, columnspan=4, padx=5, pady=0)
lnameent.grid(row=5, column=1, columnspan=4, padx=5, pady=0)
adressent.grid(row=6, column=1, columnspan=4, padx=5, pady=0)
phoneent.grid(row=7, column=1, columnspan=4, padx=5, pady=0)
departent.grid(row=8, column=1, columnspan=4, padx=5, pady=0)

#command later
addBtn = Button(
    root, text="Add", padx=65, pady=25, width=10, bd=5, font="Arial 15", bg="#84F894", command=add
)
updateBtn = Button(
    root, text="Update", padx=65, pady=25, width=10, bd=5, font="Arial 15", bg="#84E8F8", command=update
)
deleteBtn = Button(
    root, text="Delete", padx=65, pady=25, width=10, bd=5, font="Arial 15", bg="#FF9999", command=delete
)
searchBtn = Button(
    root, text="Search", padx=65, pady=25, width=10, bd=5, font="Arial 15", bg="#F4FE82", command=search
)
resetBtn = Button(
    root, text="Reset", padx=65, pady=25, width=10, bd=5, font="Arial 15", bg="#F398FF", command=reset
)
selectBtn = Button(
    root, text="Select", padx=65, pady=25, width=10, bd=5, font="Arial 15", bg="#EEEEEE", command=select
)

addBtn.grid(row=3, column=5, columnspan=1, rowspan=2)
updateBtn.grid(row=5, column=5, columnspan=1, rowspan=2)
deleteBtn.grid(row=7, column=5, columnspan=1, rowspan=2)
searchBtn.grid(row=9, column=5, columnspan=1, rowspan=2)
resetBtn.grid(row=11, column=5, columnspan=1, rowspan=2)
selectBtn.grid(row=13, column=5, columnspan=1, rowspan=2)

style = ttk.Style()
style.configure("Treeview.Heading", font="Arial 15 bold")
my_tree['columns'] = ("Stud ID", "Firstname", "Lastname", "Address", "Phone", "Department")

my_tree.column("#0", width=0, stretch=NO)
my_tree.column("Stud ID", anchor=W, width=170)
my_tree.column("Firstname", anchor=W, width=150)
my_tree.column("Lastname", anchor=W, width=150)
my_tree.column("Address", anchor=W, width=165)
my_tree.column("Phone", anchor=W, width=150)
my_tree.column("Department", anchor=W, width=160)

my_tree.heading("Stud ID", text="Student ID", anchor=W)
my_tree.heading("Firstname", text="Firstname", anchor=W)
my_tree.heading("Lastname", text="Lastname", anchor=W)
my_tree.heading("Address", text="Address", anchor=W)
my_tree.heading("Phone", text="Phone", anchor=W)
my_tree.heading("Department", text="Department", anchor=W)

refreshTable()

root.mainloop()
