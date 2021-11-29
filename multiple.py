from utils.sensor import Sensor
import time

# output from ports.sh
ports = [0, 1, 2, 3, 4]
sensors = []

# opens ports
for port in ports:
    sensors.append(Sensor(port=port))

# allow the port to open
time.sleep(3)

gases = []

for idx in range(5):
    gases.append(sensors[idx].gas())
    sensors[idx].ser.flush()

# include in prior for?
# for idx, _ in range(5):
#     sensors[idx].ser.flush()

# starts continuous measurement
for idx in range(5):
    sensors[idx].start()

try:
    while True:
        for idx, sensor in sensors:
            # wait until there is data waiting in the serial buffer
            if sensor.ser.in_waiting > 0:
                dataInput = sensor.get()
                print(str(gases[idx]) + ': ' + str(dataInput))

            sensor.ser.flush()
        print('\n')

except KeyboardInterrupt:
    time.sleep(3)

    for sensor in sensors:
        sensor.ser.flush()

    print('\nStopping continuous data output stream')

    for sensor in sensors:
        sensor.reset()

    pass
