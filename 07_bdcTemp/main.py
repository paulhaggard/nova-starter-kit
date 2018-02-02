import time
import os
import RPi.GPIO as GPIO ## Import GPIO library
from main2 import pollingFunction, heartbeatFunction ## Import temperature polling
from myLED import lightOn, lightOff ## Import blink function
from Hologram.HologramCloud import HologramCloud ## Import Hologram cloud library
import json ## Import library to create and read JSON
from myDHT import getTempString, getHumString, getTemp, getHum ## Import temperature and humidity functions
from myMCP import getLuxString, getLux ## Import photoresistor function

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
sendSMS = False
x = 0
try: 
    while True:
      signalStrength = HologramCloud.getSignalStrength()
      x += 1
      print "X is at " + str(x) + ' with a signal of ' + str(signalStrength)
      for i in range (0, 1):
        smsMessages = hologram.popReceivedSMS()
      
        if smsMessages != smsNone:
          print smsMessages
          smsMessageString = smsMessages.message
        
          if smsMessageString.find("update"):
            print type(smsMessages)
            os.system("cd /home/pi/nova-starter-kit/")
            os.system("sudo git pull")
            os.system("sudo reboot")
            time.sleep(15)
      
      else:
            time.sleep(15)
            print "...waiting for smsMessages.  None to report."
      i += 2

      for i in range (2, 3):
          
          if sendSMS == True:

            ## Exercise 05 - send data to Hologram's cloud through WiFi
            lightOn(LED_PIN)

            message = json.dumps({'h': getHumString(DHT_PIN), 'System Alarm!': getTempString(DHT_PIN), 'l': getLuxString(LUX_MCP)})
            sent = hologram.sendMessage(message)

            lightOff(LED_PIN)

            if sent == 0:
                print 'Success! Message sent to the cloud.'
                print message
            else:
                print 'Error type [' + sent + ']'
                print 'Error descriptions: https://hologram.io/docs/reference/cloud/python-sdk/#-sendmessage-message-topics-none-timeout-5-'
          i += 2
      for i in range (4,5):
            sendSMS = pollingFunction()
            i = 0
      if x > 10000:
        sendHeartBeat = heartbeatFunction() 
        if sendHeartBeat == True:
            localTime = time.localtime()
            signalStrength = HologramCloud.getSignalStrength()
            sent = hologram.sendMessage("HeartBeat Verification at " + str(time.localTime) + "with temperature of " + getTempString(DHT_PIN) + ' and a signal of ' + str(signalStrength))
            if sent == 0:
                print 'Success! Message sent to the cloud.'
                print message
                sendHeartBeat = False
            else:
                print 'Error type [' + sent + ']'
                print 'Error descriptions: https://hologram.io/docs/reference/cloud/python-sdk/#-sendmessage-message-topics-none-timeout-5-'
            sendHeartBeat = False
            x = 0

finally:
    #GPIO.output(LED_PIN,False) ## Switch off LED
    GPIO.cleanup()  ## reset all pins
    hologram.network.disconnect() ## Exercise 06 - disconnect from the cellular network
