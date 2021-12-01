from utils.sensor import Sensor
import time

# output from ports.sh
ports = [0, 1, 2, 3]
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
