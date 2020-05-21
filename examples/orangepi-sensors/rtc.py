import sys
import time
import wiringpi
#from wiringpi import GPIO

I2C_ADDR = 0x68

def b2s(bcd, mask):
	bcd &= mask
	b1 = bcd & 0x0F
	b2 = ((bcd >> 4) & 0x0F)*10
	return b1 + b2

def decCompensation(units):
	unitsU = units%10
	if units >= 50:
		units = 0x50 + unitsU
	elif units >= 40:
		units = 0x40 + unitsU
	elif units >= 30:
		units = 0x30 + unitsU
	elif units >= 20:
		units = 0x20 + unitsU
	elif units >= 10:
		units = 0x10 + unitsU
	return units

def getHours():
	HH = time.strftime("%H")
	return decCompensation(int(HH))

def getMins():
	MM = time.strftime("%M")
	return decCompensation(int(MM))

def getSecs():
	SS = time.strftime("%S")
	return decCompensation(int(SS))

def getWeeks():
	WW = time.strftime("%w")
	return decCompensation(int(WW))

def getDays():
	DD = time.strftime("%d")
	return decCompensation(int(DD))

def getMons():
	MON = time.strftime("%m")
	return decCompensation(int(MON))

def getYear():
	YY = time.strftime("%Y")
	return decCompensation(int(YY))

def clear_register(fd):
	wiringpi.wiringPiI2CWriteReg8(fd, 0x02, 0b0)        # hours
	wiringpi.wiringPiI2CWriteReg8(fd, 0x01, 0b0)        # mins
	wiringpi.wiringPiI2CWriteReg8(fd, 0x00, 0b10000000) # secs
	wiringpi.wiringPiI2CWriteReg8(fd, 0x03, 0b0)        # weeks
	wiringpi.wiringPiI2CWriteReg8(fd, 0x04, 0b0)        # days
	wiringpi.wiringPiI2CWriteReg8(fd, 0x05, 0b0)        # mons

def sys2rtcSet(fd):
	wiringpi.wiringPiI2CWriteReg8(fd, 0x02, getHours()) 
	wiringpi.wiringPiI2CWriteReg8(fd, 0x01, getMins())
	wiringpi.wiringPiI2CWriteReg8(fd, 0x00, getSecs()+0b10000000)
	wiringpi.wiringPiI2CWriteReg8(fd, 0x03, getWeeks())
	wiringpi.wiringPiI2CWriteReg8(fd, 0x04, getDays())
	wiringpi.wiringPiI2CWriteReg8(fd, 0x05, getMons())
	wiringpi.wiringPiI2CWriteReg8(fd, 0x06, getYear())

def read_register(fd):
	secs = b2s(wiringpi.wiringPiI2CReadReg8(fd, 0x00), 0x7F)
	mins = b2s(wiringpi.wiringPiI2CReadReg8(fd, 0x01), 0x7F)
	hours = b2s(wiringpi.wiringPiI2CReadReg8(fd, 0x02) - 0b10000000, 0x3F)
	week = b2s(wiringpi.wiringPiI2CReadReg8(fd, 0x03), 0x3F)
	day = b2s(wiringpi.wiringPiI2CReadReg8(fd, 0x04), 0x1F)
	mon = b2s(wiringpi.wiringPiI2CReadReg8(fd, 0x05), 0x07)
	year = b2s(wiringpi.wiringPiI2CReadReg8(fd, 0x06), 0xFF) + 1970
	print("week:%d mon:%d day:%d hours:%d mins:%d secs:%d year:%d"%(week,mon,day,hours,mins,secs,year))

def main():
	wiringpi.wiringPiSetup()
	fd = wiringpi.wiringPiI2CSetup(I2C_ADDR)
	if not fd:
		return False;
	while True:
		try:
			# clear RTC Register
			clear_register(fd)
			# set sys time to RTC Register
			sys2rtcSet(fd)
			# read RTC Register
			read_register(fd)
			time.sleep(1)
		except KeyboardInterrupt:
			print("\nexit")
			sys.exit(0)

if __name__ == '__main__':
	main()

