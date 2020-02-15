import time
import RPi.GPIO as GPIO
import board
import busio
import digitalio
import adafruit_ads1x15.ads1115 as ADS
from adafruit_ads1x15.analog_in import AnalogIn

# Create the I2C bus
i2c = busio.I2C(board.SCL, board.SDA)

# Create the ADC object using the I2C bus
ads = ADS.ADS1115(i2c,address=0x49)
ads.gain =2/3

# Create single-ended input on channel 1
channel = AnalogIn(ads, ADS.P0)

print('Weather Shield online!')

GPIO.setmode(GPIO.BCM)
    
GPIO.setup(WSPEED, GPIO.IN)
GPIO.setup(RAIN, GPIO.IN)

seconds = 0; seconds_2m = 0; lastWindCheck=0; windClicks=0; windspdavg = [0] * 120; WIND_DIR_AVG_SIZE = 120; winddiravg = [0] * WIND_DIR_AVG_SIZE
windgust_10m = [0] * 10; windgustdirection_10m = [0] * 10; minutes_10m = 0; windgustmph = 0; windgustdir = 0; minutes = 0; rainHour = [0] * 60



lastSecond = millis()


#LOOP
while True:
    tiempo = millis() - lastSecond
    #print(tiempo)
    if tiempo >= 1000:
        lastSecond += 1000

        seconds_2m += 1
        if seconds_2m > 119:
            seconds_2m = 0
            
        ######## get_wind_speed
        deltaTime = millis() - lastWindCheck  #750ms
        deltaTime /= 1000.0     #Covert to seconds
        windSpeed = windClicks / deltaTime     #3 / 0.750s = 4
        windClicks = 0    #Reset and start watching for new wind
        lastWindCheck = millis()
        windSpeed *= 1.492    #4 * 1.492 = 5.968MPH
        currentSpeed = windSpeed
        
        windspeedmph = currentSpeed
        
        ######## get_wind_direction
        ads1 = channel.value
        adc = ads1*1023/32767
        print(adc)
        print(channel.voltage)
        if adc < 380: currentDirection = 113
        elif adc < 393: currentDirection = 68
        elif adc < 414: currentDirection = 90
        elif adc < 456: currentDirection = 158
        elif adc < 508: currentDirection = 135
        elif adc < 551: currentDirection = 203
        elif adc < 615: currentDirection = 180
        elif adc < 680: currentDirection = 23
        elif adc < 746: currentDirection = 45
        elif adc < 801: currentDirection = 248
        elif adc < 833: currentDirection = 225
        elif adc < 878: currentDirection = 338
        elif adc < 913: currentDirection = 0
        elif adc < 940: currentDirection = 293
        elif adc < 967: currentDirection = 315
        elif adc < 990: currentDirection = 270
        else: currentDirection = -1 #error, disconnected?
        
        windspdavg[seconds_2m] = int(currentSpeed)
        winddiravg[seconds_2m] = currentDirection

        # Check to see if this is a gust for the minute
        if currentSpeed > windgust_10m[minutes_10m]:
            windgust_10m[minutes_10m] = currentSpeed
            windgustdirection_10m[minutes_10m] = currentDirection

        # Check to see if this is a gust for the day
        if currentSpeed > windgustmph:
            windgustmph = currentSpeed
            windgustdir = currentDirection

        seconds = seconds + 1
        if seconds > 59:
            seconds = 0

            minutes = minutes + 1
            minutes_10m = minutes_10m + 1
            if minutes > 59:
                minutes = 0
            if minutes_10m > 9:
                minutes_10m = 0

            rainHour[minutes] = 0           #Zero out this minute's rainfall amount
            windgust_10m[minutes_10m] = 0   #Zero out this minute's gust
        # falta calcWeather()
        print('winddir='+str(winddir), end="")
        print(',windspeedmph='+str(windspeedmph), end="")
        print(',windgustmph='+str(windgustmph), end="")
        print(',windgustdir='+str(windgustdir), end="")
        print(',windspdmph_avg2m='+str(windspdmph_avg2m), end="")
        print(',winddir_avg2m='+str(winddir_avg2m), end="")
        print(',windgustmph_10m='+str(windgustmph_10m), end="")
        print(',windgustdir_10m='+str(windgustdir_10m), end="")
        print(',rainin='+str(rainin), end="")
        print(',dailyrainin='+str(dailyrainin))
    time.sleep(0.1)

