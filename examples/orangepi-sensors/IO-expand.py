import sys
import time
import wiringpi
from wiringpi import GPIO

I2C_ADDR = 0x38
BASE = 100

wiringpi.wiringPiSetup()
wiringpi.pcf8574Setup(BASE, I2C_ADDR)

i = 0
while i < 8:
	wiringpi.pinMode(BASE + i, GPIO.OUTPUT)
	i += 1

wiringpi.pinMode(BASE + 0, GPIO.OUTPUT)

while True:
	try:
		wiringpi.digitalWrite(BASE + 0, GPIO.HIGH)
		time.sleep(1)
		wiringpi.digitalWrite(BASE + 0, GPIO.LOW)
		time.sleep(1)
	except KeyboardInterrupt:
		print('\nExit')
		sys.exit(0)

