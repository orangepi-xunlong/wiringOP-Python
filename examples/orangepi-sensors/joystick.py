import sys
import time
import wiringpi
from wiringpi import GPIO

I2C_ADDR = 0x48
BASE = 64
A0 = BASE+0
A1 = BASE+1

wiringpi.wiringPiSetup()
wiringpi.pcf8591Setup(BASE, I2C_ADDR)

while True:
	try:
		i = 0
		while i < 2:
			if 0 == i:
				x = wiringpi.analogRead(A0)
			if 1 == i:
				y = wiringpi.analogRead(A1)
			i += 1
		print("X=%d Y=%d"%(x,y))
		time.sleep(1)
	except KeyboardInterrupt:
		print('\nExit')
		sys.exit(0)
