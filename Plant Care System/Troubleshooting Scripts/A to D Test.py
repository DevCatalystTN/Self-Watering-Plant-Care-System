import spidev
import RPi.GPIO as GPIO
import time
GPIO.setmode(GPIO.BCM)
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

while True:
    print(moisture)
    time.sleep(1)
    moisture = readadc(0)
