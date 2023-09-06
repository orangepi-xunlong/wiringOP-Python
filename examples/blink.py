import wiringpi
import time
import sys
from wiringpi import GPIO

wiringpi.wiringPiSetup()
NUM = wiringpi.getGpioNum()

for i in range(0, NUM):
    wiringpi.pinMode(i, GPIO.OUTPUT) ;

while True:
    try:
        for i in range(0, NUM):
            wiringpi.digitalWrite(i, GPIO.HIGH)
        time.sleep(1)
        for i in range(0, NUM):
            wiringpi.digitalWrite(i, GPIO.LOW)
        time.sleep(1)
    except KeyboardInterrupt:
        print("\nexit")
        sys.exit(0)
