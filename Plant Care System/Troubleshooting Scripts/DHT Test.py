import Adafruit_DHT
import time
pin = 4
sensor = Adafruit_DHT.DHT22
humidity, temperature = Adafruit_DHT.read_retry(sensor, pin)
temperature = temperature * 1.8 + 32 
while(True):
    time.sleep(1)
    print("Humidity: %s" % (humidity))
    print("Temperature: %s F" % (temperature))
    humidity, temperature = Adafruit_DHT.read_retry(sensor, pin)
    temperature = temperature * 1.8 + 32 
