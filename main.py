import serial
import spidev
from time import *
import RPi.GPIO as GPIO
import os
import subprocess
GPIO.setmode(GPIO.BCM)
GPIO.setup(17, GPIO.IN)
GPIO.setup(18, GPIO.IN)
GPIO.setup(4, GPIO.IN)
preset = 0
preset_old = 0
name_file = open ("/ben/Desktop/rpieffectbox/names.txt")
names = name_file.read().splitlines()
print names
function_file = open ("/ben/Desktop/rpieffectbox/functions.txt")
functions = function_file.read().splitlines()
print functions
ser = serial.Serial('/dev/ttyAMA0')
spi = spidev.SpiDev()
spi.open(0, 0)
def readadc(adcnum):
# read SPI data from MCP3008 chip, 8 possible adc's (0 thru 7)
    if adcnum > 7 or adcnum < 0:
        return -1
    r = spi.xfer2([1, 8 + adcnum << 4, 0])
    adcout = ((r[1] & 3) << 8) + r[2]
    return adcout
ser.write("?fRaspberry Pi?nEffects Module")
sleep(1)
ser.write("?fBuilt By ?nBen Jacobs")
sleep(2)
ser.write("?fOpening PD...")
sleep(2)
subprocess.call("pd -nogui server.pd &", shell=True)
ser.write("?f" + str(names[preset]) + "?n" + str(functions[preset]))
while True:
 sleep(.01)
 if (GPIO.input(17) and preset > 0):
  preset_old = preset
  preset = preset - 1
  os.system("echo '1 "+ str(preset_old) +";' | pdsend 5000 localhost")
  os.system("echo '0 "+ str(preset) +";' | pdsend 5000 localhost")
  ser.write("?f" + str(names[preset]) + "?n" + str(functions[preset]))
 elif (GPIO.input(18) and preset < len(names) - 1):
  preset_old = preset
  preset = preset + 1
  os.system("echo '1 "+ str(preset_old) +";' | pdsend 5000 localhost")
  os.system("echo '0 "+ str(preset) +";' | pdsend 5000 localhost")
  ser.write("?f" + str(names[preset]) + "?n" + str(functions[preset]))
 elif (GPIO.input(4)):
  ser.write("?f")
  sleep(.2)
  while True:
   value0 = readadc(0)
   value1 = readadc(1)
   value2 = readadc(2)
   value3 = readadc(3)
   os.system("echo '3 " + str(value0) + ";' | pdsend 5001 localhost udp")
   os.system("echo '0 " + str(value1) + ";' | pdsend 5001 localhost udp")
   os.system("echo '1 " + str(value2) + ";' | pdsend 5001 localhost udp")
   os.system("echo '2 " + str(value3) + ";' | pdsend 5001 localhost udp")
   ser.write("?fE1:" + str(value3) + " E2:" + str(value2) + "?nE3:" + str(value1) + " E4:" + str(value0))
   if (GPIO.input(4) > 0):
    sleep(.2)
    ser.write("?f" + str(names[preset]) + "?n" + str(functions[preset]))
    break
