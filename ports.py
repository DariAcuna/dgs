from utils.sensor import Sensor
import time

# output from ports.sh
# fails for ports different than 0 and 1
# TODO: look for permanent fix to ubuntu denying root permission to ports 2-4
ports = [0, 1, 2]
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
