import sys
import wiringpi
from wiringpi import GPIO

LED = 6
PIN = 16

wiringpi.wiringPiSetup()
wiringpi.pinMode(LED, GPIO.OUTPUT)
wiringpi.pinMode(PIN, GPIO.INPUT)

while True:
	try:
		if wiringpi.digitalRead(PIN):
			wiringpi.digitalWrite(LED, GPIO.LOW)
		else:
			wiringpi.digitalWrite(LED, GPIO.HIGH)
	except KeyboardInterrupt:
		print("\nexit")
		sys.exit(0)

