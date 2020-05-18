import wiringpi
from wiringpi import GPIO

PIN = 6

def oneWireReset(pin):
	wiringpi.pinMode(pin, GPIO.OUTPUT)
	wiringpi.digitalWrite(pin, GPIO.HIGH)
	wiringpi.digitalWrite(pin, GPIO.LOW)
	wiringpi.delayMicroseconds(500)
	wiringpi.digitalWrite(pin, GPIO.HIGH)
	wiringpi.delayMicroseconds(60)
	wiringpi.pinMode(pin, GPIO.INPUT)
	if not wiringpi.digitalRead(pin):
		ack = 1
	else:
		ack = 0
	wiringpi.delayMicroseconds(500)
	return ack
	
def writeBit(pin, bit):
	wiringpi.pinMode(pin, GPIO.OUTPUT)
	wiringpi.digitalWrite(pin, GPIO.LOW)
	wiringpi.delayMicroseconds(2)
	wiringpi.digitalWrite(pin, bit)
	wiringpi.delayMicroseconds(80)
	wiringpi.digitalWrite(pin, GPIO.HIGH)
	wiringpi.delayMicroseconds(1)

def oneWireSendComm(pin, byte):
	i = 0
	while i < 8:
		sta = byte & 0x01
		writeBit(pin, sta)
		byte >>= 1
		i += 1

def readBit(pin):
	wiringpi.pinMode(pin, GPIO.OUTPUT)
	wiringpi.digitalWrite(pin, GPIO.HIGH)
	wiringpi.digitalWrite(pin, GPIO.LOW)
	wiringpi.delayMicroseconds(2)
	wiringpi.digitalWrite(pin, GPIO.HIGH)
	
	wiringpi.pinMode(pin, GPIO.INPUT)
	wiringpi.delayMicroseconds(2)

	tmp = wiringpi.digitalRead(pin)
	wiringpi.delayMicroseconds(40)
	return tmp

def oneWireReceive(pin):
	i = 0
	k = 0
	while i < 8:
		j = readBit(pin)
		k = (j << 7) | (k >> 1)
		i += 1
	k = k & 0x00FF
	return k

def tempchange(lsb, msb):
	if (msb >= 0xF0):
		msb = 255 - msb
		lsb = 256 - lsb
		tem = -(msb*16*16 + lsb)
	else:
		tem = (msb*16*16 + lsb)
	temp = tem*0.0625
	print("Current Temp: %.2f"%(temp))

def main():
	wiringpi.wiringPiSetup()
	if oneWireReset(PIN):
		oneWireSendComm(PIN, 0xcc)
		oneWireSendComm(PIN, 0x44)
	if oneWireReset(PIN):
		oneWireSendComm(PIN, 0xcc)
		oneWireSendComm(PIN, 0xbe)
		lsb = oneWireReceive(PIN)
		msb = oneWireReceive(PIN)
	tempchange(lsb, msb)

if __name__ == '__main__':
	main()
