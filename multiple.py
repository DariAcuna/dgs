from utils.sensor import Sensor
import time

# output from ports.sh
# TODO: look for permanent fix to ubuntu denying root permission to ports 2-4
ports = [1, 2]
sensors = []

# opens ports
for port in ports:
    sensors.append(Sensor(port=port))

# allow the port to open
time.sleep(3)

gases = []

for sensor in sensors:
    gases.append(sensor.gas())
    sensor.ser.flush()

print(gases)

# include in prior for?
# for idx, _ in range(5):
#     sensors[idx].ser.flush()

# starts continuous measurement
for sensor in sensors:
    sensor.start()

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
