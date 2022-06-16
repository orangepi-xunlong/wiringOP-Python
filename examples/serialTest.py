import wiringpi
import sys
import argparse

parser = argparse.ArgumentParser(description='')
parser.add_argument("--device", type=str, default="/dev/ttyS4", help='specify the serial node')
args = parser.parse_args()

wiringpi.wiringPiSetup()
serial = wiringpi.serialOpen(args.device, 115200)
if serial < 0:
    print("Unable to open serial device: %s"% args.device)
    sys.exit(-1)

for count in range(0, 256):
    try:
        print("\nOut: %3d:" % count, end="")
        wiringpi.serialFlush(serial)
        wiringpi.serialPutchar(serial, count)
        wiringpi.delayMicroseconds(300000)

        while wiringpi.serialDataAvail(serial):
            print(" -> %3d" % wiringpi.serialGetchar(serial), end="")
            wiringpi.serialFlush(serial)
    except KeyboardInterrupt:
        print("\nexit")
        sys.exit(0)

wiringpi.serialClose(serial)  # Pass in ID
