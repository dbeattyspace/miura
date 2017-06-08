import os
import time
import smbus
import Adafruit_ADXL345
import RPi.GPIO as GPIO
import Adafruit_ADS1x15
import datetime
from zlib import adler32
import sys
import math
sys.path.append('/home/pi/miura')
from dwlk import dwlk

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)
os.system('modprobe w1-gpio')
os.system('modprobe w1-therm')
temp_sensor1 = '//sys/bus/w1/devices/28-000007a8d22b/w1_slave'
temp_sensor2 = '//sys/bus/w1/devices/28-000007a8c380/w1_slave'
temp_sensor3 = '//sys/bus/w1/devices/28-000007a8b7a1/w1_slave'

#accel = Adafruit_ADXL345.ADXL345()
adc = Adafruit_ADS1x15.ADS1115()
GAIN = 1
bus = smbus.SMBus(1)
#bus.write_byte_data(0x60, 0x26, 0x39) #pres

def temp_raw(temp_sensor):
	f = open(temp_sensor, 'r')
	lines = f.readlines()
	f.close()
	return lines

def read_temp(temp_sensor): #read temperature
	lines = temp_raw(temp_sensor)
	while lines[0].strip()[-3:] != 'YES':
		time.sleep(0.2)
		lines = temp_raw(temp_sensor)
	temp_output = lines[1].find('t=')
	if temp_output != -1:
		temp_string = lines[1].strip()[temp_output+2:]
		temp_c = float(temp_string) /1000.0
		temp_f = temp_c * 9.0 / 5.0 + 32.0
		return temp_f	

def read_humi(): #read humidity
	bus.write_byte(0x40, 0xF5)
	time.sleep(0.3)
	data0 = bus.read_byte(0x40)
	data1 = bus.read_byte(0x40)
	humidity = ((data0 * 256 + data1) * 125 / 65536.0) - 6
	time.sleep(0.3)
	return humidity

'''
def read_pres(): #read pressure
	data = bus.read_i2c_block_data(0x60, 0x00, 4)
	pres = ((data[1] * 65536) + (data[2] * 256) + (data[3] & 0xF0)) / 16
	pressure = (pres / 4.0) / 1000.0
	return pressure

def read_acc(): #read accelerometer
	x, y, z = accel.read()
	return x, y, z
'''

def blink(pin): #blink LEDs
	GPIO.setup(pin, GPIO.OUT)
	GPIO.output(pin,GPIO.HIGH)
	time.sleep(0.5)
	GPIO.output(pin,GPIO.LOW)
	time.sleep(0.5)
	return

def led_on(pin): #turn on LEDs
	GPIO.output(pin,GPIO.HIGH)

def led_off(pin): #turn off LEDs
	GPIO.output(pin,GPIO.LOW)

def read_adc(): #read ADC
	values = [0]*4
	for i in range(4):
		values[i] = adc.read_adc(i, gain=GAIN)
	#Rangefinder conversion factor
	values[0] = 130*math.pow(values[0]/1000,-1.1)
	#Ammeter Conversion factor
	Vref = 2500
	sensitivity = 100/500
	voltage = 4.88*(values[1]/1000)
	values[1] = (voltage - Vref) * sensitivity
	#values[1] = (values[1])/(100/500)
	#values[1] = (voltage-2500)*.2
	return values[0], values[1]

def main():
	counter = 1
	while True:
		#ranf, amm  = read_adc()
		#label = 'CU ' + 'MI ' + 'SE '
		#timestamp = "{0:.2f}".format(time.time())
		#data = ' ' + "{0:.4f}".format(ranf) + ' ' + "{0:.2f}".format(amm) + ' ' + "{0:.2f}".format(read_humi()) + ' ' +  "{0:.2f}".format(read_temp())
		#checksum = label + timestamp + data
		#checksum  = checksum.encode('utf-8')
		#checksum = adler32(checksum) & 0xffffffff
		#checksum = str(checksum)
		#packet = label + timestamp + ' ' + checksum + data		
		#packet = "{0:.4f}".format(ranf)
		#packet = str(amm)
		packet = str(read_temp(temp_sensor1)) + ' ' + str(read_temp(temp_sensor2)) + ' ' + str(read_temp(temp_sensor3))
		#packet = label + timestamp + ' ' + checksum + data
		print(packet)
		packet = packet + '\n'
		dwlk.q.put(packet)
		name = 'test{:d}.log'.format(counter)
		with open(name, "a") as f:
			f.write(packet)
		#counter += 1
main()
