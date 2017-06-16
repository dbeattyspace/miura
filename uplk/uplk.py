import time
import serial

ser = serial.Serial(
	port = '/dev/serial0',
	baudrate = 4800,
	parity = serial.PARITY_NONE,
	stopbits = serial.STOPBITS_ONE,
	bytesize = serial.EIGHTBITS,
	timeout = 1
)

def main(downlink,run_exp):
	while True:
		x = ser.readline().decode("utf-8")
		if x == "start":
			
		time.sleep(1)
