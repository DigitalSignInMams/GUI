import nfc
from nfc.clf import RemoteTarget
from time import sleep
import time
import binascii
import mysql.connector


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


with nfc.ContactlessFrontend('tty:S0:pn532') as clf:
	connected = False
	
	while not connected:
		try:
			mydb = mysql.connector.connect(
				host="mysql.wpi.edu",
				user="ctang5",
				password="CT@ng5",
				database="mams_siso",
				)
			sql = mydb.cursor(buffered=True)
			print("connected")
			connected = True
		except:
			print("Not connected. Trying again.")
			sleep(10)
			continue

	while True:
		try:
			target = clf.sense(RemoteTarget('106A'))
		except:
			print('Error in connecting to RFID module.')
			continue
		if target is None:
			print("Scanning")
			sleep(0.25)
			continue
		tag = nfc.tag.activate(clf, target)
		try:
			print("———————————————————————————————")
			command = f"INSERT INTO daily VALUES(get_id({str(binascii.hexlify(tag.identifier).decode())}), CURRENT_DATE(), CURRENT_TIME());"
			print("RFID ID: " + binascii.hexlify(tag.identifier).decode())
			sql.execute(command)
			mydb.commit()
			command = f"SELECT first_name, last_name FROM person WHERE student_id = get_id({binascii.hexlify(tag.identifier).decode()})"
			sql.execute(command)
			result = sql.fetchall()
			print(f"Welcome {result[0]} {result[1]}")
			print("———————————————————————————————")
			sleep(5)
		except:
			print("RFID ID not recognized, please try something else")
			sleep(2)
	mydb.close()

	
	
