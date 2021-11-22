from SensorData import SensorData
import serial


class Sensor:

    def __init__(self, port):
        self.port = serial.Serial('/dev/ttyUSB0')

    def start(self):
        output = 'c'.encode()
        self.port.write(output)
        return

    # should not have access to
    def read(self):
        ser_bytes = self.port.readline()
        decoded_bytes = ser_bytes[0:len(ser_bytes) - 2].decode("utf-8")
        return decoded_bytes

    def get(self):
        read = self.read()
        data = SensorData(read[0], read[1], read[2], read[3], read[4],
                          read[5], read[6], read[7], read[8], read[9],
                          read[10])
        return data

    def calibrate(self):
        output = 'Z'.encode()
        self.port.write(output)

    def reset(self):
        output = 'r'.encode()
        self.port.write(output)
        return

    def close(self):
        return
