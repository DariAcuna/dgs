import serial
import time

# default values match suggested paramaters
# baudrate=9600         ->  Baud: 9600
# bytesize=EIGHTBITS    ->  Data bits: 8
# stopbits=STOPBITS_ONE ->  Stop bits: 1
# parity=PARITY_NONE    ->  Parity: None
# xonxoff=False         ->  Flow Control: None
# adding timeout to avoid strokes
serialPort = serial.Serial('/dev/ttyUSB0', timeout=1)
print('\nSerial information:\n' + str(serialPort) + '\n')

# allow the port to open
time.sleep(3)

# sends a key to trigger a measurement
print('Sending TRIGGER key...')
dataTrigger = 't'.encode()
serialPort.write(dataTrigger)
serialPort.flush()

# within 5-seconds of a TRIGGER key stroke
time.sleep(3)

# starts continuous measurement
# entering command twice works well
print('Starting continuous measurement...')
dataOutput = 'c'.encode()
serialPort.write(dataOutput)
serialPort.flush()
serialPort.write(dataOutput)
serialPort.flush()

# allow flush() to finish
# strokes occur if set under 5 seconds
time.sleep(5)

try:
    while True:

        # wait until there is data waiting in the serial buffer
        if serialPort.in_waiting > 0:

            ser_bytes = serialPort.readline()

            # without this, first four strings are sent abruptly
            time.sleep(1)

            decoded_bytes = ser_bytes[0:len(ser_bytes) - 2].decode("utf-8")

            # if received ghost data, skip
            if not decoded_bytes:
                continue

            decoded_list = list(decoded_bytes.split(","))
            available_list = [int(item) for item in decoded_list]

            # if received incomplete data, skip
            if not len(available_list) == 11:
                continue

            print(available_list)

        serialPort.flush()

except KeyboardInterrupt:
    time.sleep(3)
    serialPort.flush()
    time.sleep(3)

    print('\nStopping continuous data output stream')
    dataStop = 'R'.encode()
    serialPort.write(dataStop)
    serialPort.flush()
    time.sleep(3)
    pass
