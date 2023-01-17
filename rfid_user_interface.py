import nfc
from nfc.clf import RemoteTarget
from time import sleep
import time
import binascii
import mysql.connector
from tkinter import *
from tkinter import ttk
import tkinter as tk

connected = False
while not connected:
	try:
		print("Trying to connect")
		mydb = mysql.connector.connect(
				host="mysql.wpi.edu",
				user="ctang5",
				password="CT@ng5",
				database="mams_siso",
			)
		sql = mydb.cursor()
		print("Connected to WPI SQL database!")
		connected = True
	except:
		print("Not connected! Trying again to connect.")
		sleep(4)
		continue

def on_connect(target):
		serial = target.sdd_res.hex()
		tag = nfc.tag.activate(clf, target)
		print(binascii.hexlify(tag.identifier).decode())
	
def on_startup(targets):
	return targets

rdwr_options = {
	'targets': ['106A'],
	'on_startup': on_startup,
	'on_connect': lambda tag: False,
	} 
		
root = Tk()
root.title("Sign In / Sign Out")
root.geometry('500x500')
a = Label(root, text="Scan RFID Here",font=("calibre", 40))
a.place(relx=0.5, rely=0.05, anchor=CENTER)

def submit(id):
    success = tk.Label(root, text = f'Recorded! ID: {id}', font=('calibre',20, 'bold'))
    success.place(relx=0.1, rely=0.5)
    root.after(500, success.destroy)

btn = Button(root, text = 'Exit Window', bd = '5',
                          command = root.destroy)
btn.place(relx=0.5, rely=0.95, anchor=CENTER)

def scan():
	with nfc.ContactlessFrontend('tty:S0:pn532') as clf:
		try:
			target = clf.sense(RemoteTarget('106A'))
		except:
			print('Error connecting to RFID module')
		if target is None:
			print("-")
		else:
			print("Detected RFID")
			tag = nfc.tag.activate(clf, target)
			try:
				command = f"INSERT INTO daily VALUES(get_id({str(binascii.hexlify(tag.identifier).decode())}), CURRENT_DATE(), CURRENT_TIME());"
				print("RFID: " + binascii.hexlify(tag.identifier).decode())
				submit(str(binascii.hexlify(tag.identifier).decode()))
				sql.execute(command)
				mydb.commit()
				root.configure(bg="green")
			except:
				print("RFID not found, please try again.")
				root.configure(bg="red")

def run_periodically(func):
	scan()
	root.configure(bg="white")
	root.after(25, run_periodically, func)

run_periodically(scan)

root.mainloop()