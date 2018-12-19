import RPi.GPIO as GPIO
import time
GPIO.setmode(GPIO.BCM)
GPIO.setup(26, GPIO.OUT)
GPIO.output(26, GPIO.LOW)
x = 2

while(True):
    GPIO.output(26, GPIO.HIGH)
    print("ON")
    time.sleep(x)
    GPIO.output(26, GPIO.LOW)
    print("OFF")
    time.sleep(x)
