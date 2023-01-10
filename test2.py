import nfc
import binascii
from time import sleep


def on_startup(targets):
	return targets

def on_connect(tag):
	print(binascii.hexlify(tag.identifier).decode())
	print("connect")
	return True

def on_release(tag):
	print('Released')
	return tag

rdwr_options = {
	'on-startup': on_startup,
	'on-connect': on_connect,
	'on-release': on_release,
	'beep-on-connect': True,
}

with nfc.ContactlessFrontend('tty:S0:pn532') as clf:
	while True:
		tag = clf.connect(rdwr=rdwr_options)
		sleep(1)
