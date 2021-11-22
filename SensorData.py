class SensorData:
    def __init__(self, sn, ppb, temp, rh, rawsensor, tempdigital, rhdigital, day, hour, minute, second):
        self.SN = sn
        self.PPB = ppb
        self.TEMP = temp
        self.RH = rh
        self.RAW = rawsensor
        self.TEMP_DIGITAL = tempdigital
        self.RH_DIGITAL = rhdigital
        self.DAY = day
        self.HOUR = hour
        self.MINUTE = minute
        self.SECOND = second
