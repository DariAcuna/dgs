import time
import board
import busio
import adafruit_ads1x15.ads1115 as ADS
from adafruit_ads1x15.analog_in import AnalogIn

# Create the I2C bus
i2c = busio.I2C(board.SCL, board.SDA)

# Create the ADC object using the I2C bus
ads = ADS.ADS1115(i2c,address=0x49)

# Create single-ended input on channel 1
chan = AnalogIn(ads, ADS.P1)

# Create differential input between channel 0 and 1
#chan = AnalogIn(ads, ADS.P0, ADS.P1)

#print("{:>5}\t{:>5}".format('raw', 'v'))

while True:
    #print("{:>5}\t{:>5.3f}".format(chan.value, chan.voltage))
    value = chan.voltage
    if value < 0.7:
        print("Silencioso")
    elif value <2:
        print("Moderado")
    else:
        print("Muy bullicioso")
    time.sleep(0.5)
    