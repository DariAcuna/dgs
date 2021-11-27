# TODO: properly import class from utils file
from utils.Sensor import Sensor
import serial
import time

# opens port
sensor = Sensor(port='')

# allow the port to open
time.sleep(3)

# starts continuous measurement
sensor.start()

try:
    while True:

        # wait until there is data waiting in the serial buffer
        if sensor.port.in_waiting > 0:

            dataInput = sensor.get()

            # TODO: fix data reading
            print(dataInput)

        sensor.port.flush()

except KeyboardInterrupt:
    time.sleep(3)
    sensor.port.flush()

    print('\nStopping continuous data output stream')
    sensor.reset()
    pass
