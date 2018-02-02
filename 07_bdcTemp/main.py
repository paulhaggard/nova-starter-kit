import time
import os
import RPi.GPIO as GPIO ## Import GPIO library
from myLED import lightOn, lightOff ## Import blink function
from myDHT import getTempString, getHumString ## Import temperature and humidity functions
from myMCP import getLuxString ## Import photoresistor function
from Hologram.HologramCloud import HologramCloud ## Import Hologram cloud library
import json ## Import library to create and read JSON

GPIO.setmode(GPIO.BCM) ## Use broadcom pin numbering

LED_PIN = 17 ## GPIO pin the LED is attached to
DHT_PIN = 21 ## GPIO pin the DHT sensor is attached to
LUX_MCP = 0 ## ADC pin the Photoresistor is attached to
BTN_PIN = 27 ## GPIO pin the button is attached to

## Exercise 04 - triggered by a button press
GPIO.setup(BTN_PIN,GPIO.IN,pull_up_down=GPIO.PUD_UP) ## Setup GPIO pin as an input

## Exercise 05 - send data to Hologram's cloud through WiFi
#with open('../credentials.json') as key_file:
#    devicekey = json.load(key_file)
#hologram = HologramCloud(dict(), enable_inbound=True)

## Exercise 06 - send data to Hologram's cloud through Cellular
hologram = HologramCloud(dict(), network='cellular', enable_inbound=True)
#hologram.enableSMS()
#hologram.network.connect() ## connect from the cellular netowork
smsNone = hologram.popReceivedSMS()
print type(smsNone)
while True:
    smsMessages = hologram.popReceivedSMS()
    if smsMessages != smsNone:
        print smsMessages
        smsMessageString = smsMessages.message
        print type(smsMessages)
        if smsMessageString.find("update"):
            os.system("cd ~/nova-starter-kit/")
            os.system("git pull")
            os.system("sudo restart")

        time.sleep(15)
    else:
        time.sleep(15)
        print "sleeping smsMessages"
try:
    while True:
        if GPIO.input(BTN_PIN) == False:

            ## Exercise 05 - send data to Hologram's cloud through WiFi
            lightOn(LED_PIN)

            message = json.dumps({'h': getHumString(DHT_PIN), 't': getTempString(DHT_PIN), 'l': getLuxString(LUX_MCP)})
            sent = hologram.sendMessage(message)

            lightOff(LED_PIN)

            if sent == 0:
                print 'Success! Message sent to the cloud.'
                print message
            else:
                print 'Error type [' + sent + ']'
                print 'Error descriptions: https://hologram.io/docs/reference/cloud/python-sdk/#-sendmessage-message-topics-none-timeout-5-'

finally:
    GPIO.output(LED_PIN,False) ## Switch off LED
    GPIO.cleanup()  ## reset all pins
    hologram.network.disconnect() ## Exercise 06 - disconnect from the cellular network
