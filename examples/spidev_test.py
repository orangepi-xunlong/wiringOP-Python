import wiringpi
import argparse

parser = argparse.ArgumentParser(description='')
parser.add_argument("--channel", type=int, default=1, help='specify the spi channel')
parser.add_argument("--port", type=int, default=0, help='specify the spi port')
parser.add_argument("--speed", type=int, default=500000, help='specify the spi speed')
parser.add_argument("--mode", type=int, default=0, help='specify the spi mode')
args = parser.parse_args()

default_tx = [
        0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF,
        0x40, 0x00, 0x00, 0x00, 0x00, 0x95,
        0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF,
        0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF,
        0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF,
        0xF0, 0x0D,
]

def hexdump(src, line_size, prefix):
    result = []
    digits = 4 if isinstance(src, str) else 2

    for i in range(0, len(src), line_size):
        s = src[i:i + line_size]
        hexa = ' '.join([hex(x)[2:].upper().zfill(digits) for x in s])
        text = ''.join([chr(x) if 0x20 <= x < 0x7F else '.' for x in s])
        result.append(prefix + ' | ' + hexa.ljust(line_size * (digits + 1)) + ' |' + "{0}".format(text) + '|')

    return '\n'.join(result)

print("spi mode: 0x%x" % args.mode);
print("max speed: %d Hz (%d KHz)\n" %(args.speed, args.speed / 1000), end='');

wiringpi.wiringPiSPISetupMode(args.channel, args.port, args.speed, args.mode)
revlen, recvData = wiringpi.wiringPiSPIDataRW(args.channel, bytes(default_tx))

print(hexdump(bytes(default_tx), 32, "TX"))
print(hexdump(bytes(recvData), 32, "RX"))
