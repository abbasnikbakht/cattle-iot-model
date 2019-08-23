#!/usr/bin/python
 
import Adafruit_DHT
import time
# Sensor should be set to Adafruit_DHT.DHT11
 
sensor = Adafruit_DHT.DHT11

# connected to GPIO4(any pin as u wish sir).
pin = 4

# Try to grab a sensor reading.  Use the read_retry method which will retry  multiple times.
#  15 times to get a sensor reading (waiting 2 seconds between each retry).
while True:
    h, t = Adafruit_DHT.read_retry(sensor, pin)
    if(h is not "None" and t is not 'None'):
        print 'Temp={0:0.1f}*C Humidity={1:0.1f}%'.format(t,h)
    else:
        print "no input found"
    time.sleep(3)
    