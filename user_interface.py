
import mysql.connector
from tkinter import *
from tkinter import ttk
import tkinter as tk

def insert_daily_id(ID):
  mydb = mysql.connector.connect(
    host="mysql.wpi.edu",
    user="ctang5",
    password="CT@ng5",
    database="mams_siso",
  )
  sql = mydb.cursor()

  command = f"INSERT INTO daily VALUES ({ID}, CURRENT_DATE(), CURRENT_TIME());"
  sql.execute(command)
  mydb.commit()
  mydb.close()

def insert_daily_name(FName, LName):
  mydb = mysql.connector.connect(
  host="mysql.wpi.edu",
  user="ctang5",
  password="CT@ng5",
  database="mams_siso",
  )
  sql = mydb.cursor()
  command = f"INSERT INTO daily VALUES (return_id('{FName}', '{LName}'), CURRENT_DATE(), CURRENT_TIME());"
  sql.execute(command) 
  mydb.commit()
  mydb.close()
 
root = Tk()
root.title("Sign In / Sign Out")
root.geometry('500x500')
#root.attributes ('-fullscreen', True)
a = Label(root, text="Enter Name",font=("calibre", 25))
#a.pack()
a.place(relx=0.5, rely=0.05, anchor=CENTER)

f_name_var=tk.StringVar()
l_name_var=tk.StringVar()

def submit():
    fname=f_name_var.get().strip()
    lname=l_name_var.get().strip()    
    f_name_var.set("")
    l_name_var.set("")
    try:
        insert_daily_name(fname, lname)
        success = tk.Label(root, text = 'Signed In!', font=('calibre',10, 'bold'))
        success.place(relx=0.5, rely=0.72)
    except:
        success = tk.Label(root, text = 'Name Not Found!', font=('calibre',10, 'bold'))
        success.place(relx=0.5, rely=0.72)

f_name_label = tk.Label(root, text = 'First Name', font=('calibre',15, 'bold'))
f_name_entry = tk.Entry(root, textvariable= f_name_var, relief=SUNKEN, font=("calibre", 15))
l_name_label = tk.Label(root, text = 'Last Name', font=('calibre',15, 'bold'))
l_name_entry = tk.Entry(root, textvariable= l_name_var, relief=SUNKEN, font=("calibre", 15))
f_name_label.place(relx=0.1, rely=0.4)
f_name_entry.place(relx=0.4, rely=0.4)
l_name_label.place(relx=0.1, rely=0.6)
l_name_entry.place(relx=0.4, rely=0.6)

sub_btn=tk.Button(root,text = 'Submit', bd='5', command = submit)
sub_btn.place(relx=0.5, rely=0.8, anchor=CENTER)

btn = Button(root, text = 'Exit Window', bd = '5',
                          command = root.destroy)
btn.place(relx=0.5, rely=0.95, anchor=CENTER)

root.mainloop()

