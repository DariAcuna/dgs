import RPi.GPIO as GPIO
import time

pin = [36,38,32,26]
delay = 0.08

GPIO.setmode(GPIO.BOARD)

for pincito in pin:
    GPIO.setup(pincito,GPIO.OUT)
    GPIO.output(pincito,False)

while True:    
    for i in range(4):
        GPIO.output(pin[i],True)
        time.sleep(delay)
        GPIO.output(pin[i],False)
        time.sleep(delay)
    for i in range(3,-1,-1):
        GPIO.output(pin[i],True)
        time.sleep(delay)
        GPIO.output(pin[i],False)
        time.sleep(delay)
    GPIO.output(pin[3],True)
    time.sleep(delay)
    GPIO.output(pin[3],False)
    time.sleep(delay)
        
    
''' 
GPIO.output(pin[3],False)
GPIO.output(pin[0],True)
time.sleep(delay)
GPIO.output(pin[0],False)
GPIO.output(pin[1],True)
time.sleep(delay)
GPIO.output(pin[1],False)
GPIO.output(pin[2],True)
time.sleep(delay)
GPIO.output(pin[2],False)
GPIO.output(pin[3],True)
time.sleep(delay)
'''
