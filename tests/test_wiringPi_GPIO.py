import wiringpi

def test_wiringPiSetup():
    assert wiringpi.wiringPiSetup() == 0

def test_digitalRead():
    assert wiringpi.digitalRead(1) != None
def test_digitalWrite():
    assert wiringpi.digitalWrite(1,0) == None