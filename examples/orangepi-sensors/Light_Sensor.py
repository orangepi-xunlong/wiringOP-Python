import sys
import time
import wiringpi
from wiringpi import GPIO

I2C_ADDR = 0x48
BASE = 64
A0 = BASE+0

wiringpi.wiringPiSetup()
wiringpi.pcf8591Setup(BASE, I2C_ADDR)
while True:
	try:
		value = wiringpi.analogRead(A0)
		print("value: %d"%value)
		time.sleep(2)
	except KeyboardInterrupt:
		print('\nExit')
		sys.exit(0)
