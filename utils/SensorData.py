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

    # TODO: allow declaration only for parameters within the specified ranges
    # N [XXXXXXXXXXXX],
    # PPB [0 : 999999],
    # TEMP [-99 : 99],
    # RH [0 : 99],
    # RawSensor[ADCCount],
    # TempDigital, RHDigital,
    # Day [0 : 99],
    # Hour [0 : 23],
    # Minute [0 : 59],
    # Second [0 : 59
