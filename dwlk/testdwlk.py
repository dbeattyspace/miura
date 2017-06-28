import serial
import time

ser = serial.Serial(
	port = '/dev/serial0',
	baudrate = 4800,
	parity = serial.PARITY_NONE,
	stopbits = serial.STOPBITS_ONE,
	bytesize = serial.EIGHTBITS,
	timeout = 1
)

ser.close()
ser.open()

def main(downlink):
	counter = 0
	while True:
#		a = downlink.get()
		a = ("hi micah\n")
		print('message: ' + a)
		ser.write(a.encode('utf-8'))
#		print("packet sent",counter)
		time.sleep(1)
		counter+=1