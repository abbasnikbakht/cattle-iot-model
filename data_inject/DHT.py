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
    humidity, temperature = Adafruit_DHT.read_retry(sensor, pin)
    print('Temp={0:0.1f}*C  Humidity={1:0.1f}%'.format(temperature, humidity))
    time.sleep(30)
    
'''
    print('Temp={0:0.1f}*C  Humidity={1:0.1f}%'.format(temperature, humidity))
else:
    print('Failed to get reading. Try again!')
'''