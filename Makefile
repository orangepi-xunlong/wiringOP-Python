all: bindings
	python3 setup.py build

bindings:
	python3 generate-bindings.py > bindings.i

clean:
	rm -rf build dist wiringpi.egg-info
	rm -rf wiringpi.py wiringpi_wrap.c

install: bindings
	sudo python3 setup.py install

test:
	pytest tests
