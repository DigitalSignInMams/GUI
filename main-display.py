import nfc
from nfc.clf import RemoteTarget
from time import sleep
import time
import binascii
import mysql.connector

from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont
import ST7735


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
	displayInitialized = False
	disp = None
	img = None
	font = None
	draw = None

	
	while not displayInitialized:
		try:
			disp = ST7735.ST7735(port=0, cs=0, dc=24, backlight=None, rst=25, width=125, height=155, rotation=270, invert=False)
			disp.begin()

			WIDTH = disp.width
			HEIGHT = disp.height

			img = Image.new('RGB', (WIDTH, HEIGHT), color=(0,0,0))
			draw = ImageDraw.Draw(img)

			# Load default font.
			font = ImageFont.load_default()

			# Write some text
			draw.text((5, 5), "Connected to LCD", font=font, fill=(255, 255, 255))

			# Write buffer to display hardware, must be called to make things visible on the
			# display!
			disp.display(img)
			sleep(3)
			displayInitialized = True
		except:
			print("Display not connected. Try again")
			continue

				
	
	while not connected:
		try:
			mydb = mysql.connector.connect(
				host="mysql.wpi.edu",
				user="ctang5",
				password="CT@ng5",
				database="mams_siso",
				)
			sql = mydb.cursor(buffered=True)
			
			draw.rectangle((0, 0, disp.width, disp.height), (0,0,0))
			draw.text((5, 5), "Connected SQL Database", font=font, fill=(255, 255, 255))
			disp.display(img)
			
			print("Connected to MySQL Database.")
			connected = True
			sleep(2)
		except:
			print("Not connected. Trying again.")
			sleep(10)
			continue
	
	print("Scanning")
	draw.rectangle((0, 0, disp.width, disp.height), (0,0,0))
	draw.text((5, 5), "Scanning", font=font, fill=(255, 255, 255))
	disp.display(img)
	
	
	
	
	
	
	while True:
		try:
			target = clf.sense(RemoteTarget('106A'))
		except:
			print('Error in connecting to RFID module.')
			draw.text((5, 5), "Error in connecting to RFID module.", font=font, fill=(255, 255, 255))
			disp.display(img)
			
			continue
		if target is None:
			sleep(0.25)
			continue
		tag = nfc.tag.activate(clf, target)
		draw.rectangle((0, 0, disp.width, disp.height), (0,0,0))
		draw.text((5, 5), "Scanning", font=font, fill=(255, 255, 255))
		disp.display(img)
		try:
			print("———————————————————————————————")
			command = f"INSERT INTO daily VALUES(get_id(\"{str(binascii.hexlify(tag.identifier).decode())}\"), CURRENT_DATE(), CURRENT_TIME());"
			print("RFID ID: " + binascii.hexlify(tag.identifier).decode())
			sql.execute(command)
			mydb.commit()
			command = f"SELECT first_name, last_name FROM person WHERE student_id = get_id(\"{binascii.hexlify(tag.identifier).decode()}\")"
			sql.execute(command)
			result = sql.fetchall()
			
			msg = f"Welcome {result[0][0]} {result[0][1]}!"

			size_x, size_y = draw.textsize(msg, font)
			text_x = 160
			text_y = (80 - size_y) // 2
			t_start = time.time()
			t_end = time.time() + 5
			while time.time() < t_end:
				x = (time.time() - t_start) * 100
				x %= (size_x + 160)
				draw.rectangle((0, 0, disp.width, disp.height), (0,64,0))
				draw.text((int(text_x - x), text_y), msg, font=font, fill=(255, 255, 255))
				disp.display(img)
			
			print(f"Welcome {result[0][0]} {result[0][1]}!")
			print("———————————————————————————————")
			sleep(2)
			print("Scanning")
			draw.rectangle((0, 0, disp.width, disp.height), (0,0,0))
			draw.text((5, 5), "Scanning", font=font, fill=(255, 255, 255))
			disp.display(img)
		except:
			
			
			print("RFID ID not recognized, please try something else")
			msg = "RFID ID not recognized, please try something else"

			size_x, size_y = draw.textsize(msg, font)
			text_x = 160
			text_y = (80 - size_y) // 2

			t_start = time.time()

			t_end = time.time() + 5
			while time.time() < t_end:
				x = (time.time() - t_start) * 100
				x %= (size_x + 160)
				draw.rectangle((0, 0, disp.width, disp.height), (0,0,255))
				draw.text((int(text_x - x), text_y), msg, font=font, fill=(255, 255, 255))
				disp.display(img)
			print("Scanning")
			draw.rectangle((0, 0, disp.width, disp.height), (0,0,0))
			draw.text((5, 5), "Scanning", font=font, fill=(255, 255, 255))
			disp.display(img)
	mydb.close()

	
	
