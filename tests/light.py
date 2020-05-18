import sys
import time
import wiringpi
from wiringpi import GPIO

PIN = 2 

wiringpi.wiringPiSetup()
wiringpi.pinMode(PIN, GPIO.OUTPUT)

while True:
	try:
		wiringpi.digitalWrite(PIN, GPIO.HIGH)
		print(wiringpi.digitalRead(PIN))
		time.sleep(1)
		wiringpi.digitalWrite(PIN, GPIO.LOW)
		print(wiringpi.digitalRead(PIN))
		time.sleep(1)
	except KeyboardInterrupt:
		print("\nexit")
		sys.exit(0)
