from SensorData import SensorData
import serial
import time


class Sensor:

    def __init__(self, port):
        self.port = serial.Serial('/dev/ttyUSB0')

    # private method
    def __read(self):
        ser_bytes = self.port.readline()
        decoded_bytes = ser_bytes[0:len(ser_bytes) - 2].decode("utf-8")
        return decoded_bytes

    # sends a key to trigger a measurement
    def __trigger(self):
        trigger = 't'.encode()
        self.port.write(trigger)
        self.port.flush()

        # within 5-seconds of a TRIGGER key stroke
        time.sleep(3)
        return

    def __send(self, character):
        self.__trigger()
        send = character.encode()

        # entering command twice works well
        self.port.write(send)
        self.port.flush()
        self.port.write(send)
        self.port.flush()

        # allow for a small delay in between characters
        time.sleep(5)
        return

    def start(self):
        self.__send('c')
        return

    def calibrate(self):
        self.__send('Z')

    def reset(self):
        self.__send('r')

    def get(self):
        read = self.__read()
        data = SensorData(read[0], read[1], read[2], read[3], read[4],
                          read[5], read[6], read[7], read[8], read[9],
                          read[10])
        return data
