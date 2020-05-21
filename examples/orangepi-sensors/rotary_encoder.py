import sys
import time
import wiringpi
from wiringpi import GPIO

SIA = 9
SIB= 10
SW = 6

wiringpi.wiringPiSetup()
wiringpi.pinMode(SW, GPIO.INPUT)
wiringpi.pinMode(SIA, GPIO.INPUT)
wiringpi.pinMode(SIB, GPIO.INPUT)

flag = 0
resetflag = 0
globalCount = 0

while True:
	try:
		lastSib = wiringpi.digitalRead(SIB)
		while not wiringpi.digitalRead(SW):
			resetflag = 1
		while not wiringpi.digitalRead(SIA):
			currentSib = wiringpi.digitalRead(SIB)
			flag =1
		
		if resetflag:
			globalCount = 0
			resetflag = 0
			print ('Count reset\ncurrent = 0')
			continue
		if flag:
			if lastSib == 0 and currentSib == 1:
				print ('Anticlockwise rotation')
				globalCount += 1
			if lastSib == 1 and currentSib == 0:
				print ('clockwise rotation')
				globalCount -=1
			
			flag =0
			print ('current = %s' % globalCount)
	except KeyboardInterrupt:
		print('\nExit')
		sys.exit(0)

