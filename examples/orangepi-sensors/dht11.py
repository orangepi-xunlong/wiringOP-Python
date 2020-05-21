import wiringpi
from wiringpi import GPIO

pin = 6

def getval(pin):
	tl=[]
	tb=[]
	wiringpi.wiringPiSetup()
	wiringpi.pinMode(pin, GPIO.OUTPUT)
	wiringpi.digitalWrite(pin, GPIO.HIGH)
	wiringpi.delay(1)
	wiringpi.digitalWrite(pin, GPIO.LOW)
	wiringpi.delay(25)
	wiringpi.digitalWrite(pin, GPIO.HIGH)
	wiringpi.delayMicroseconds(20)
	wiringpi.pinMode(pin, GPIO.INPUT)
	while(wiringpi.digitalRead(pin)==1): pass
	
	for i in range(45):
		tc=wiringpi.micros()
		'''
		'''
		while(wiringpi.digitalRead(pin)==0): pass
		while(wiringpi.digitalRead(pin)==1):
			if wiringpi.micros()-tc>500:
				break
		if wiringpi.micros()-tc>500:
			break
		tl.append(wiringpi.micros()-tc)

	tl=tl[1:]
	for i in tl:
		if i>100:
			tb.append(1)
		else:
			tb.append(0)
	
	return tb

def GetResult(pin):
	for i in range(10):
		SH=0;SL=0;TH=0;TL=0;C=0
		result=getval(pin)

		if len(result)==40:
			for i in range(8):
				SH*=2;SH+=result[i]    # humi Integer
				SL*=2;SL+=result[i+8]  # humi decimal
				TH*=2;TH+=result[i+16] # temp Integer
				TL*=2;TL+=result[i+24] # temp decimal
				C*=2;C+=result[i+32]   # Checksum
			if ((SH+SL+TH+TL)%256)==C and C!=0:
				break
			else:
				print("Read Sucess,But checksum error! retrying")

		else:
			print("Read failer! Retrying")
			break
		wiringpi.delay(200)
	return SH,SL,TH,TL

SH,SL,TH,TL=GetResult(pin)
print("humi:",SH,SL,"temp:",TH,TL)


