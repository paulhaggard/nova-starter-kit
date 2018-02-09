import RPi.GPIO as GPIO ## Import GPIO library
from myLED import blink ## Import blink function
from myDHT import getTempString, getHumString, getTemp ## Import temperature and humidity functions
from myMCP import getLuxString ## Import photoresistor function

GPIO.setmode(GPIO.BCM) ## Use broadcom pin numbering

LED_PIN = 17 ## GPIO pin the LED is attached to
DHT_PIN = 21 ## GPIO pin the DHT sensor is attached to
LUX_MCP = 0 ## ADC pin the Photoresistor is attached to
BTN_PIN = 27 ## GPIO pin the button is attached to

## Exercise 04 - triggered by a button press
GPIO.setup(BTN_PIN,GPIO.IN,pull_up_down=GPIO.PUD_UP) ## Setup GPIO pin as an input

try:
    while True:
        if GPIO.input(BTN_PIN) == False:

            ## Exercise 01 - blink an LED
            ## blinkTimes(LED_PIN) ## blink the LED

            ## Exercise 02 - read a digital sensor
            blink(LED_PIN) ## blink the LED
            print getTemp(DHT_PIN) ## print temp string to terminal
            blink(LED_PIN)
            print getHumString(DHT_PIN) ## print hum string to terminal
            blink(LED_PIN)

            ## Exercise 03 - read an analog sensor
            print getLuxString(LUX_MCP) ## print lumenance string to terminal
            blink(LED_PIN)

finally:
    GPIO.output(LED_PIN,False) ## Switch off LED
    GPIO.cleanup()  ## reset all pins
