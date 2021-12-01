from utils.sensor import Sensor
import time

# output from ports.sh
# TODO: figure out why eeprom data and sensor readout are not being flushed properly
# TODO: print sensor readout all at once per second
# TODO: write new class for multiple sensors
ports = [0, 1, 2, 3]
sensors = []

# opens ports
for port in ports:
    sensors.append(Sensor(port=port))

for sensor in sensors:
    sensor.ser.reset_input_buffer()
    sensor.ser.reset_output_buffer()

# allow the port to open
time.sleep(3)

gases = []

for sensor in sensors:
    gases.append(sensor.gas())
    sensor.ser.flush()

# it takes about 40 seconds to get here
# if using 4 sensors
print(gases)

# include in prior for?
# for idx, _ in range(5):
#     sensors[idx].ser.flush()

# starts continuous measurement
for sensor in sensors:
    sensor.start()

idx = 0

try:
    while True:
        for sensor in sensors:
            # wait until there is data waiting in the serial buffer
            if sensor.ser.in_waiting > 0:
                dataInput = sensor.get()
                print(str(gases[idx]) + ': ' + str(dataInput))

            sensor.ser.flush()
            idx = idx + 1
        idx = 0
        print('')

except KeyboardInterrupt:
    time.sleep(3)

    for sensor in sensors:
        sensor.ser.flush()

    print('\nStopping continuous data output stream')

    for sensor in sensors:
        sensor.reset()

    pass
