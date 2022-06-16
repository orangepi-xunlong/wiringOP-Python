import sys
import time
import wiringpi
from datetime import datetime
import operator
import argparse

parser = argparse.ArgumentParser(description='i2c')
parser.add_argument("--device", type=str, default="/dev/i2c-0", help='specify the i2c node')
args = parser.parse_args()

i2caddr = 0x68

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

def ds1302_write_byte(fd, reg, byte):
	if wiringpi.wiringPiI2CWriteReg8(fd, reg, byte) < 0:
		print("Error write byte to ds1302")
		return -1
	return 0

def ds1302_read_byte(fd, reg):
    byte = wiringpi.wiringPiI2CReadReg8(fd, reg)
    if byte < 0:
        print("Error read byte from ds1302")
        return -1
    return byte

def sys2rtcSet(fd):
	ds1302_write_byte(fd, 0x02, getHours())
	ds1302_write_byte(fd, 0x01, getMins())
	ds1302_write_byte(fd, 0x00, getSecs())
	ds1302_write_byte(fd, 0x03, getWeeks())
	ds1302_write_byte(fd, 0x04, getDays())
	ds1302_write_byte(fd, 0x05, getMons())
	ds1302_write_byte(fd, 0x06, getYear())

def read_register(fd):
	byte = ds1302_read_byte(fd, 0x0)
	if byte >> 7:
		ds1302_write_byte(fd, 0x0, 0x0)
	second = operator.mod(byte, 16) + operator.floordiv(byte, 16) * 10

	byte = ds1302_read_byte(fd, 0x01)
	minute = operator.mod(byte, 16) + operator.floordiv(byte, 16) * 10

	byte = ds1302_read_byte(fd, 0x02)
	hour = operator.mod(byte, 16) + operator.floordiv(byte, 16) * 10

	week = ds1302_read_byte(fd, 0x03)

	byte = ds1302_read_byte(fd, 0x04)
	day = operator.mod(byte, 16) + operator.floordiv(byte, 16) * 10

	byte = ds1302_read_byte(fd, 0x05)
	month = operator.mod(byte, 16) + operator.floordiv(byte, 16) * 10

	byte = ds1302_read_byte(fd, 0x06)
	year = operator.mod(byte, 16) + operator.floordiv(byte, 16) * 10 + 1970

	if year == 2000 or month > 12 or month<1 or day < 1 or day > 31:
		return False

	if second > 59:
		return False
	return datetime(year,month,day,hour,minute,second)

def main():
    wiringpi.wiringPiSetup()
    fd = wiringpi.wiringPiI2CSetupInterface(args.device, i2caddr)
    try:
        sys2rtcSet(fd)
        while True:
            time.sleep(1)
            dt = read_register(fd)
            if not dt:
                continue
            else:
                str_time = dt.strftime("%a %Y-%m-%d  %H:%M:%S")
                print("%s"%(str_time))
    except KeyboardInterrupt:
        print("\nexit")
        sys.exit(0)

if __name__ == '__main__':
	main()

