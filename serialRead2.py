import serial
import time

# default values match suggested paramaters
# baudrate=9600         ->  Baud: 9600
# bytesize=EIGHTBITS    ->  Data bits: 8
# stopbits=STOPBITS_ONE ->  Stop bits: 1
# parity=PARITY_NONE    ->  Parity: None
# xonxoff=False         ->  Flow Control: None
serialPort = serial.Serial('/dev/ttyUSB0')
print('\nSerial information:\n' + str(serialPort) + '\n')

# clean buffers
print('Cleaning buffers...\n')
time.sleep(1)
serialPort.reset_output_buffer()
time.sleep(1)
serialPort.reset_input_buffer()

# set delay
time.sleep(2)
# sends a key to trigger a measurement
dataTrigger = 't'.encode()
serialPort.write(dataTrigger)
# sets delay to make sure character 't' is read
time.sleep(2)
# starts continuous measurement
dataOutput = 'c'.encode()
serialPort.write(dataOutput)

try:
    while True:
        # wait until there is data waiting in the serial buffer
        if serialPort.in_waiting > 0:

            ser_bytes = serialPort.readline()
            decoded_bytes = ser_bytes[0:len(ser_bytes) - 2].decode("utf-8")
            print(decoded_bytes)

except KeyboardInterrupt:
    dataStop = 'R'.encode()
    serialPort.write(dataStop)
    serialPort.flush()
    print('\nStopping continuous data output stream')
    time.sleep(2)
    pass
