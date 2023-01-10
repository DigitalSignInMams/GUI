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
			sql = mydb.cursor()
			print("connected")
			connected = True
		except:
			print("Not connected")
			sleep(10)
			continue

	while True:
		
		try:
			#print("I'm trying!")
			target = clf.sense(RemoteTarget('106A'))
			#print(target)
		except:
			print('Error.')
			continue
		
		if target is None:
			sleep(0.25)
			continue
		
		#serial = target.sdd_res.hex()
		tag = nfc.tag.activate(clf, target)
		try:
			command = f"INSERT INTO daily VALUES(get_id({str(binascii.hexlify(tag.identifier).decode())}), CURRENT_DATE(), CURRENT_TIME());"
			print("RFID: " + binascii.hexlify(tag.identifier).decode())
			last_rfid = str(binascii.hexlify(tag.identifier).decode())
			sql.execute(command)
			mydb.commit()
			sleep(5)
		except:
			print("RFID not found, please try something else")
			sleep(2)
		
		
	mydb.close()

	
	
