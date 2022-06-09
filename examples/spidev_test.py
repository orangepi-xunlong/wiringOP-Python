import wiringpi
channel = 1
port = 0
speed = 500000
mode = 0

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

print("spi mode: 0x%x" % mode);
print("max speed: %d Hz (%d KHz)\n" %(speed, speed / 1000), end='');

wiringpi.wiringPiSPISetupMode(channel, port, speed, mode)
revlen, recvData = wiringpi.wiringPiSPIDataRW(channel, bytes(default_tx))

print(hexdump(bytes(default_tx), 32, "TX"))
print(hexdump(bytes(recvData), 32, "RX"))
