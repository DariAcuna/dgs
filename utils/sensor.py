import serial
import time


class Sensor:

    def __init__(self, port):
        # default values match suggested paramaters
        # baudrate=9600         ->  Baud: 9600
        # bytesize=EIGHTBITS    ->  Data bits: 8
        # stopbits=STOPBITS_ONE ->  Stop bits: 1
        # parity=PARITY_NONE    ->  Parity: None
        # xonxoff=False         ->  Flow Control: None
        # adding timeout to avoid strokes
        self.ser = serial.Serial('/dev/ttyUSB' + str(port))

    # private method
    def __read(self):
        ser_bytes = self.ser.readline()
        time.sleep(1)
        decoded_bytes = ser_bytes[0:len(ser_bytes) - 2].decode("utf-8")

        # if received ghost data, skip
        if not decoded_bytes:
            return

        decoded_list = list(decoded_bytes.split(","))
        available_list = [int(item) for item in decoded_list]

        # if received incomplete data, skip
        if not len(available_list) == 11:
            print('invalid')
            return

        return available_list

    # private method
    # TODO: write method that gets all lines from EEPROM readout

    # private method
    # TODO: get gas code from method above
    def __eeprom(self):
        # gases = {'H2S', 'NO2', 'SO2', 'O3', 'CO'}

        ser_bytes = self.ser.read_until('Date_Code'.encode())
        time.sleep(1)
        decoded_bytes = ser_bytes[0:len(ser_bytes)].decode("utf-8")

        # 18 lines counting the Date_Code readout
        gas = decoded_bytes.split('\n', 18)[17]
        gas_type = gas.split(' ', 1)[1]

        return gas_type

    # sends a key to trigger a measurement
    def __trigger(self):
        trigger = 't'.encode()
        self.ser.write(trigger)
        self.ser.flush()

        # within 5-seconds of a TRIGGER key stroke
        time.sleep(3)
        return

    def __send(self, character):
        self.__trigger()
        send = character.encode()

        # entering command twice works well
        self.ser.write(send)
        self.ser.flush()
        self.ser.write(send)
        self.ser.flush()

        # allow for a small delay in between characters
        time.sleep(5)
        return

    def start(self):
        self.__send('c')
        return

    def gas(self):
        self.__send('e')
        gas = self.__eeprom()
        return gas

    # TODO: test calibrate method
    def calibrate(self):
        self.__send('Z')
        return

    # TODO: test reset method
    def reset(self):
        self.__send('r')
        return

    def get(self):
        read = self.__read()
        return read
