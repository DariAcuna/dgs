from utils.sensor import Sensor
import time

# opens port ttyUSB0
sensor = Sensor(port=0)

# allow the port to open
time.sleep(3)

# starts continuous measurement
sensor.start()

try:
    while True:

        # wait until there is data waiting in the serial buffer
        if sensor.ser.in_waiting > 0:

            dataInput = sensor.get()

            print(dataInput)

        sensor.ser.flush()

except KeyboardInterrupt:
    time.sleep(3)
    sensor.ser.flush()

    print('\nStopping continuous data output stream')
    sensor.reset()
    pass
