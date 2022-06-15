#!/usr/bin/env python
import os
import sys
from setuptools import setup, Extension
from setuptools.command.build_py import build_py
from setuptools.command.sdist import sdist
from distutils.spawn import find_executable
from glob import glob
from subprocess import Popen, PIPE
import re

sources = glob('wiringOP/devLib/*.c')
sources += glob('wiringOP/wiringPi/*.c')
sources += ['wiringpi.i']
sources += ['fixUndefFunc.c']
try:
    sources.remove('wiringOP/devLib/piFaceOld.c')
except ValueError:
    # the file is already excluded in the source distribution
    pass

# Fix so that build_ext runs before build_py
# Without this, wiringpi.py is generated too late and doesn't
# end up in the distribution when running setup.py bdist or bdist_wheel.
# Based on:
#  https://stackoverflow.com/a/29551581/7938656
#  and
#  https://blog.niteoweb.com/setuptools-run-custom-code-in-setup-py/


class build_py_ext_first(build_py):
    def run(self):
        self.run_command("build_ext")
        return build_py.run(self)

# Make sure wiringpi_wrap.c is available for the source dist, also.


class sdist_ext_first(sdist):
    def run(self):
        self.run_command("build_ext")
        return sdist.run(self)

def cmdline(command, arguments):
    process = Popen(args=[command, arguments],stdin=PIPE, stdout=PIPE, stderr=PIPE)
    return process.communicate()[0]

BOARD = ""
boards = ["orangepir1", "orangepizero", "orangepizero-lts", "orangepipc", "orangepipch5", "orangepipcplus",
          "orangepiplus2e", "orangepione", "orangepioneh5", "orangepilite", "orangepiplus", "orangepizeroplus2h3",
          "orangepizeroplus", "orangepipc2", "orangepiprime", "orangepizeroplus2h5", "orangepiwin", "orangepiwinplus",
          "orangepi3", "orangepi3-lts", "orangepilite2", "orangepioneplus", "orangepi4", "orangepi4-lts", "orangepirk3399",
          "orangepi800", "orangepizero2", "orangepizero2-lts", "orangepizero2-b", "orangepir1plus-lts", "orangepir1plus"]

inf_orangepi = cmdline('cat','/etc/orangepi-release')
inf_armbian = cmdline('cat','/etc/armbian-release')
if inf_orangepi != b'':
    match = re.search(r"(?<=^BOARD=).*", inf_orangepi.decode("utf-8"), re.MULTILINE)
    if match == None: sys.exit(1) #something went wrong
    BOARD = match.group()
elif inf_armbian != b'':
    match = re.search(r"(?<=^BOARD=).*", inf_armbian.decode("utf-8"), re.MULTILINE)
    if match == None: sys.exit(1) #something went wrong
    BOARD = match.group()
    if BOARD == "orangepi-r1": EXTRA_CFLAGS = "orangepir1"
    elif BOARD == "orangepi-rk3399": EXTRA_CFLAGS = "orangepirk3399"
    elif BOARD == "orangepizeroplus2-h3": EXTRA_CFLAGS = "orangepizeroplus2h3"
    elif BOARD == "orangepizeroplus2-h5": EXTRA_CFLAGS = "orangepizeroplus2h5"
else:
    print("All available boards:\n")
    cnt = 0
    for board in boards:
        print("%4d. %s\n", cnt, board)
    while True:
        choice = input("Choice: ")
        if choice == None or choice.isdigit() != True:
            continue
        if 0 <= int(choice) <= 10:
            BOARD = boards[choice]
            break
        print("Invalid input ...\n")

if BOARD == "orangepir1": BOARD = "orangepir1-h2"
elif BOARD == "orangepizero" or BOARD == "orangepizero-lts": BOARD = "orangepizero-h2"
elif BOARD == "orangepipc" or BOARD == "orangepipch5": BOARD = "orangepipc-h3"
elif BOARD == "orangepipcplus": BOARD = "orangepipcplus-h3"
elif BOARD == "orangepiplus2e": BOARD = "orangepiplus2e-h3"
elif BOARD == "orangepione" or BOARD == "orangepioneh5": BOARD = "orangepione-h3"
elif BOARD == "orangepilite": BOARD = "orangepilite-h3"
elif BOARD == "orangepiplus": BOARD = "orangepiplus-h3"
elif BOARD == "orangepizeroplus": BOARD = "orangepizeroplus-h5"
elif BOARD == "orangepipc2": BOARD = "orangepipc2-h5"
elif BOARD == "orangepiprime": BOARD = "orangepiprime-h5"
elif BOARD == "orangepiwin": BOARD = "orangepiwin-a64"
elif BOARD == "orangepiwinplus": BOARD = "orangepiwinplus-a64"
elif BOARD == "orangepi3" or BOARD == "orangepi3-lts": BOARD = "orangepi3-h6"
elif BOARD == "orangepilite2": BOARD = "orangepilite2-h6"
elif BOARD == "orangepioneplus": BOARD = "orangepioneplus-h6"
elif BOARD == "orangepizero2" or BOARD == "orangepizero2-lts" or BOARD == "orangepizero2-b": BOARD = "orangepizero2-h616"
elif BOARD == "orangepir1plus" or BOARD == "orangepir1plus-lts": BOARD = "orangepir1plus-rk3328"

if BOARD == "": BOARD = "orangepioneplus-h6"

EXTRA_CFLAGS = ""

if BOARD == "orangepi2giot": EXTRA_CFLAGS = "-DCONFIG_ORANGEPI_2G_IOT"
elif BOARD == "orangepipc2-h5": EXTRA_CFLAGS = "-DCONFIG_ORANGEPI_PC2"
elif BOARD == "orangepiprime-h5": EXTRA_CFLAGS = "-DCONFIG_ORANGEPI_PRIME"
elif BOARD == "orangepizeroplus-h5": EXTRA_CFLAGS = "-DCONFIG_ORANGEPI_ZEROPLUS"
elif BOARD == "orangepiwin-a64" or BOARD == "orangepiwinplus-a64": EXTRA_CFLAGS = "-DCONFIG_ORANGEPI_WIN"
elif BOARD == "orangepione-h3" or BOARD == "orangepilite-h3" or BOARD == "orangepipc-h3" or BOARD == "orangepiplus-h3" or BOARD == "orangepipcplus-h3" or BOARD == "orangepiplus2e-h3": EXTRA_CFLAGS = "-DCONFIG_ORANGEPI_H3"
elif BOARD == "orangepizero-h2" or BOARD == "orangepir1-h2": EXTRA_CFLAGS = "-DCONFIG_ORANGEPI_ZERO"
elif BOARD == "orangepioneplus-h6" or BOARD == "orangepilite2-h6": EXTRA_CFLAGS = "-DCONFIG_ORANGEPI_LITE2"
elif BOARD == "orangepi3-h6": EXTRA_CFLAGS = "-DCONFIG_ORANGEPI_3"
elif BOARD == "orangepizero2-h616": EXTRA_CFLAGS = "-DCONFIG_ORANGEPI_ZERO2"
elif BOARD == "orangepizeroplus2h3": EXTRA_CFLAGS = "-DCONFIG_ORANGEPI_ZEROPLUS2_H3"
elif BOARD == "orangepizeroplus2h5": EXTRA_CFLAGS = "-DCONFIG_ORANGEPI_ZEROPLUS2_H5"
elif BOARD == "orangepirk3399": EXTRA_CFLAGS = "-DCONFIG_ORANGEPI_RK3399"
elif BOARD == "orangepi4": EXTRA_CFLAGS = "-DCONFIG_ORANGEPI_4"
elif BOARD == "orangepi4-lts": EXTRA_CFLAGS = "-DCONFIG_ORANGEPI_4_LTS"
elif BOARD == "orangepi800": EXTRA_CFLAGS = "-DCONFIG_ORANGEPI_800"
elif BOARD == "orangepir1plus-rk3328": EXTRA_CFLAGS = "-DCONFIG_ORANGEPI_R1PLUS"

_wiringpi = Extension(
    '_wiringpi',
    include_dirs=['wiringOP', 'wiringOP/wiringPi', 'wiringOP/devLib'],
    extra_compile_args=[EXTRA_CFLAGS, "-DCONFIG_ORANGEPI"],
    swig_opts=['-threads'],
    extra_link_args=['-lcrypt', '-lrt'],
    sources=sources
)

setup(
    name='wiringpi',
    version='2.60.1',
    ext_modules=[_wiringpi],
    py_modules=["wiringpi"],
    install_requires=[],
    cmdclass={'build_py': build_py_ext_first, 'sdist': sdist_ext_first}
)
