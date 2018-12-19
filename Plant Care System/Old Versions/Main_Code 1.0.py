#Start Setup
import RPi.GPIO as GPIO
import time
import Adafruit_CharLCD as LCD
import Adafruit_DHT
import spidev
threshold = 511
check = 1000000
lcd_rs = 25 #LCD Setup
lcd_en = 24
lcd_d4 = 23
lcd_d5 = 17
lcd_d6 = 18
lcd_d7 = 22
lcd_backlight = 2
lcd_columns = 16
lcd_rows = 2
lcd = LCD.Adafruit_CharLCD(lcd_rs, lcd_en, lcd_d4, lcd_d5, lcd_d6, lcd_d7, lcd_columns, lcd_rows, lcd_backlight)
#End LCD Setup
sensor = Adafruit_DHT.DHT22                 #Temp Sensor Setup
pin = 4
humidity, temperature = Adafruit_DHT.read_retry(sensor, pin)
temperature = temperature * 1.8 + 32        #End Temp Sensor Setup
GPIO.setmode(GPIO.BCM)                      #GPIO Pins Setup
GPIO.setup(21, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(26, GPIO.OUT)
GPIO.output(26, GPIO.LOW)
input_state = GPIO.input(21)
button = 1                                  #End GPIO Pins Setup
lcd_update = 0                              #Update varible
moisture = 0                                #Soil Moisture sensor value
ldr_channel = 0                             #Analog to Digital Chip Setup
spi = spidev.SpiDev()
spi.open(0, 0)
#Chip-Pin 11 (DIN) to Pi MOSI or BCM Pin 19
#Chip-Pin 12 (DOUT) to Pi MISO or BCM Pin 21
#Chip-Pin 13 (CLK) to Pi SCLK or BCM Pin 23
def readadc(adcnum):
    # read SPI data from the MCP3008, 8 channels in total
    if adcnum > 7 or adcnum < 0:
        return -1
    r = spi.xfer2([1, 8 + adcnum << 4, 0])
    data = ((r[1] & 3) << 8) + r[2]
    return data
moisture = readadc(0)
moisture = moisture * 100
moisture = moisture  / 1023
#End Setup


while(True):
    if lcd_update == check: #In ~10 seconds the LCD will update with new data
        humidity, temperature = Adafruit_DHT.read_retry(sensor, pin)
        temperature = temperature * 1.8 + 32
        moisture = readadc(0)
        moisture = moisture * 100    #Converts Celsius
        moisture = moisture  / 1023  #to Farenheit

        if button == 1:
            lcd.clear()
            lcd.message("Temperature:\n{0:0.1f}*F".format(temperature))

        elif button == 2:
            lcd.clear()
            lcd.message("Air Humidity:\n{0:0.1f}%".format(humidity))

        elif button == 3:
            lcd.clear()
            lcd.message("Soil Moisture:\n{0:0.1f}%".format(moisture))
            
        if moisture <= 50:
            GPIO.output(26, GPIO.HIGH)
            while moisture <= threshold: 
                moisture = readadc(0)
                #fallback = fallback + 1
                #if fallback <= 

        else:
            lcd_update = 0
            #Uncomment below for debugging.
            print("Update Successful")
        GPIO.output(26, GPIO.LOW)
        
        
    if button == 1:                          #Display Temperature
        lcd.clear()
        lcd.message("Temperature:\n{0:0.1f}*F".format(temperature))
        while(lcd_update < check and button == 1):
            input_state = GPIO.input(21)
            #Uncomment below for debugging. You may need to change the counter value to a lower number!
            #print(lcd_update)
            lcd_update = lcd_update + 1
            if input_state == False:
                time.sleep(0.2)
                button = button + 1
                break

    elif button == 2:                         #Display Humidity
        lcd.clear()
        lcd.message("Humidity:\n{0:0.1f}%".format(humidity))
        while(lcd_update < check and button == 2):
            input_state = GPIO.input(21)
            #Uncomment below for debugging. You may need to change the counter value to a lower number!
            #print(lcd_update)
            lcd_update = lcd_update + 1
            if input_state == False:
                time.sleep(0.2)
                button = button + 1
                break
                        
    elif button == 3:                          #Display Soil Moisture
        lcd.clear()
        lcd.message("Soil Moisture:\n{0:0.1f}%".format(moisture))
        while(lcd_update < check and button == 3):
            input_state = GPIO.input(21)
            #Uncomment below for debugging. You may need to change the counter value to a lower number!
            #print(lcd_update)
            lcd_update = lcd_update + 1
            if input_state == False:
                time.sleep(0.2)
                button = button - 2
                break
                        
    
        



