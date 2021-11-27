import serial
import time

# default values match suggested paramaters
# baudrate=9600         ->  Baud: 9600
# bytesize=EIGHTBITS    ->  Data bits: 8
# stopbits=STOPBITS_ONE ->  Stop bits: 1
# parity=PARITY_NONE    ->  Parity: None
# xonxoff=False         ->  Flow Control: None
serialPort = serial.Serial('/dev/ttyUSB0', timeout=1)
print('\nSerial information:\n' + str(serialPort) + '\n')

# clean buffers
print('Cleaning buffers...\n')
# time.sleep(1)
# serialPort.reset_output_buffer()
time.sleep(3)
# serialPort.reset_input_buffer()

# sends a key to trigger a measurement
dataTrigger = 't'.encode()
serialPort.write(dataTrigger)
serialPort.flush()
# sets delay to make sure character 't' is read

# within 5-seconds of a TRIGGER key stroke
time.sleep(3)

# starts continuous measurement
dataOutput = 'c'.encode()
serialPort.write(dataOutput)
serialPort.flush()
serialPort.write(dataOutput)
serialPort.flush()

time.sleep(5)

try:
    while True:
        # wait until there is data waiting in the serial buffer

        if serialPort.in_waiting > 0:

            ser_bytes = serialPort.readline()
            time.sleep(1)
            decoded_bytes = ser_bytes[0:len(ser_bytes) - 2].decode("utf-8")

            if not decoded_bytes:
                continue

            print(decoded_bytes)

        serialPort.flush()

except KeyboardInterrupt:
    time.sleep(3)
    serialPort.flush()
    time.sleep(1)
    dataStop = 'R'.encode()
    serialPort.write(dataStop)
    serialPort.flush()
    print('\nStopping continuous data output stream')
    time.sleep(3)
    pass
