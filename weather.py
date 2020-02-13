import time
#import smbus
import RPi.GPIO as io
import board
import busio
import digitalio
import adafruit_ads1x15.ads1115 as ADS
from adafruit_ads1x15.analog_in import AnalogIn

# Create the I2C bus
i2c = busio.I2C(board.SCL, board.SDA)

# Create the ADC object using the I2C bus
ads = ADS.ADS1115(i2c,address=0x49)
print(ads)
# Create single-ended input on channel 0
#while True:
#    channel = AnalogIn(ads, ADS.P1)
#    print(channel.voltage)

# digital I/O pins
WSPEED = 23
RAIN = 24

lastSecond = 0
seconds = 0
seconds_2m = 0
minutes = 0
minutes_10m = 0

lastWindCheck = 0
lastWindIRQ = 0
windClicks = 0

windspdavg = [0] * 120

WIND_DIR_AVG_SIZE = 120

winddiravg = [0] * WIND_DIR_AVG_SIZE

windgust_10m = [0] * 10
windgustdirection_10m = [0] * 10
rainHour = [0] * 60

winddir = 0
windspeedmph = 0
windgustmph = 0
windgustdir = 0 
windspdmph_avg2m = 0
winddir_avg2m = 0
windgustmph_10m = 0
windgustdir_10m = 0

humidity = 0
tempf = 0

rainin = 0
dailyrainin = 0

raintime = 0
rainlast = 0
raininterval = 0
rain = 0

def millis():
  milliseconds = int(round(time.time() * 1000))
  return milliseconds

def rainIRQ():
  global raintime, raininterval, rainlast, dailyrainin, rainHour

  raintime = millis()
  raininterval = raintime - rainlast

  if raininterval > 10:
    dailyrainin += 0.011
    rainHour[minutes] += 0.011 

    rainlast = raintime

def wspeedIRQ():
  global lastWindIRQ, windClicks

  if millis() - lastWindIRQ > 10:
    lastWindIRQ = millis()
    windClicks += 1

def calcWeather():
  global winddir, windspdavg, windspdmph_avg2m, winddiravg, WIND_DIR_AVG_SIZE, winddir_avg2m, windgustmph_10m, windgust_10m, windgustdir_10m, rainin, rainHour

  #Calc winddir
  winddir = get_wind_direction()

  #Calc windspeed
  #windspeedmph = get_wind_speed() #This is calculated in the main loop on line ---
  
  temp = 0
  for i in range(120):
    temp += windspdavg[i]

  temp /= 120.0
  windspdmph_avg2m = temp
  
  sum = winddiravg[0]
  D = winddiravg[0]

  for i in range(WIND_DIR_AVG_SIZE):
    delta = winddiravg[i] - D

    if delta < -180:
      D += delta + 360

    elif delta > 180:
      D += delta - 360
    else:
      D += delta

    sum += D
  
  winddir_avg2m = sum / WIND_DIR_AVG_SIZE
  
  if winddir_avg2m >= 360:
     winddir_avg2m -= 360
  
  if winddir_avg2m < 0:
    winddir_avg2m += 360

  windgustmph_10m = 0
  windgustdir_10m = 0

  for i in range(10):
    if windgust_10m[i] > windgustmph_10m:
      windgustmph_10m = windgust_10m[i]
      windgustdir_10m = windgustdirection_10m[i]

  rainin = 0

  for i in range(60):
    rainin += rainHour[i]

def get_wind_speed():
  global lastWindCheck, windSpeed, windClicks

  deltaTime = millis() - lastWindCheck  #750ms

  deltaTime /= 1000.0     #Covert to seconds

  windSpeed = windClicks / deltaTime     #3 / 0.750s = 4

  windClicks = 0    #Reset and start watching for new wind
  lastWindCheck = millis()

  windSpeed *= 1.492    #4 * 1.492 = 5.968MPH

  #print("Windspeed: "+str(windSpeed))

  return windSpeed

def get_wind_direction():
  global WDIR
  

  calcWeather()
  #adc = WDIR #analogRead(WDIR) <<<<
  adc = WDIR
  if adc < 380: return 113
  if adc < 393: return 68
  if adc < 414: return 90
  if adc < 456: return 158
  if adc < 508: return 135
  if adc < 551: return 203
  if adc < 615: return 180
  if adc < 680: return 23
  if adc < 746: return 45
  if adc < 801: return 248
  if adc < 833: return 225
  if adc < 878: return 338
  if adc < 913: return 0
  if adc < 940: return 293
  if adc < 967: return 315
  if adc < 990: return 270

  return -1 #error, disconnected?

def printWeather():
  print ('Holi$,winddir='+str(winddir)+',windspeedmph='+str(windspeedmph)+',windgustmph='+str(windgustmph)+',windgustdir='+str(windgustdir)+',windspdmph_avg2m='+str(windspdmph_avg2m)+',winddir_avg2m='+str(winddir_avg2m)+',windgustmph_10m='+str(windgustmph_10m)+',windgustdir_10m='+str(windgustdir_10m)+',rainin='+str(rainin)+',dailyrainin='+str(dailyrainin)+',#')

#WSPEED = digitalio.DigitalInOut(board.D23)
#WSPEED.direction = digitalio.Direction.INPUT

#RAIN = digitalio.DigitalInOut(board.D24)
#RAIN.direction = digitalio.Direction.INPUT
  
io.setup(WSPEED, io.IN)
io.setup(RAIN, io.IN)

seconds = 0
lastSecond = millis()
print('Weather Shield online!########################################')

#LOOP
while True:
    print("=========================================================")
    if millis() - lastSecond >= 1000:
        lastSecond += 1000

    seconds_2m += 1
    if seconds_2m > 119:
      seconds_2m = 0

    currentSpeed = get_wind_speed()
    windspeedmph = currentSpeed
    currentDirection = get_wind_direction()
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

    printWeather()

    time.sleep(100)
