import wiringpi
import time
import sys
from wiringpi import GPIO

NUM = 17    #26pin
#NUM = 18   #26pin
#NUM = 20   #for Orange Pi Zero 2
#NUM = 19   #for Orange Pi 4
#NUM = 28   #40pin

wiringpi.wiringPiSetup()

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
