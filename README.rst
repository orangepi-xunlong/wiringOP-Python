Note
~~~~

wiringOP for Python
===================

wiringOP: An implementation of most of the Arduino Wiring functions for
the Orange Pi.

Supported boards
===================
tested on:
``Orange Pi Zero2``
``Orange Pi 3 LTS``
``Orange Pi 4 LTS``

Manual Build
============

Get/setup repo
--------------

.. code:: bash

    git clone --recursive https://github.com/orangepi-xunlong/wiringOP-Python.git
    cd wiringOP-Python

Don't forget the --recursive; it is required to also pull in the WiringPi C code from its own repository.

Prerequisites
-------------

To rebuild the bindings you **must** first have installed ``swig``,
``python3-dev``, and ``python3-setuptools``. wiringOP should also be installed system-wide for access
to the ``gpio`` tool.

.. code:: bash

    sudo apt-get install swig python3-dev python3-setuptools

Build & install with
--------------------

``python3 generate-bindings.py > bindings.i``

``sudo python3 setup.py install``

Usage
=====

.. code:: python

    import wiringpi

    # One of the following MUST be called before using IO functions:
    wiringpi.wiringPiSetup()      # For sequential pin numbering

**General IO:**

.. code:: python

    wiringpi.pinMode(6, 1)       # Set pin 6 to 1 ( OUTPUT )
    wiringpi.digitalWrite(6, 1)  # Write 1 ( HIGH ) to pin 6
    wiringpi.digitalRead(6)      # Read pin 6
