Note
~~~~

This is an unofficial port of Gordon's wiringPi library. Please do not
email Gordon if you have issues, he will not be able to help.

wiringOP for Python
===================

wiringOP: An implementation of most of the Arduino Wiring functions for
the Orange Pi.

Manual Build
============

Get/setup repo
--------------

.. code:: bash

    git clone https://github.com/orangepi-xunlong/wiringOP-Python.git
    cd wiringOP-Python

Prerequisites
-------------

To rebuild the bindings you **must** first have installed ``swig``,
``python-dev``, and ``python-setuptools`` (or their ``python3-``
equivalents). wiringOP should also be installed system-wide for access
to the ``gpio`` tool.

.. code:: bash

    sudo apt-get install python-dev python-setuptools swig python-pip

Build & install with
--------------------

``sudo python setup.py install``

Or Python 3:

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
