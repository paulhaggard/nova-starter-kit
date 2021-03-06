import time
import os
import RPi.GPIO as GPIO ## Import GPIO library
from main2 import pollingFunction, heartbeatFunction ## Import temperature polling
from myLED import lightOn, lightOff ## Import blink function
from Hologram.HologramCloud import HologramCloud ## Import Hologram cloud library
from Hologram.CustomCloud import CustomCloud #cellular library        
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
#time.sleep(45)
#sent = hologram.sendMessage('Startup.')
x = 0
try: 
    while True:
      x += 1
      os.system("sudo hologram modem signal >> /home/signalfile.hologram")
      signalFile = open('/home/signalfile.hologram')
      print "X is at " + str(x) + ' with a signal of ' + signalFile.read()
      for i in range (0, 1):
        smsMessages = hologram.popReceivedSMS()
      
        if smsMessages != smsNone:
          print smsMessages
          smsMessageString = smsMessages.message
        
          if smsMessageString.find("update"):
            print type(smsMessages)
	    hologram.network.connect()
            time.sleep(20)
            os.system("cd /home/pi/nova-starter-kit/")
            os.system("sudo git pull")
            sent = hologram.sendMessage("Update Pulled!")
            os.system("sudo reboot")
            time.sleep(15)
          elif smsMessageString.find("ping"):
            sent = hologram.sendMessage("Ping received.")



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
      if x > 2400:
        sendHeartBeat = heartbeatFunction() 
        if sendHeartBeat == True:
            localTime = time.localtime()
            os.system("sudo hologram modem signal > /home/latestsignal.hologram")
            signalStrength = open('/home/latestsignal.hologram')
            sent = hologram.sendMessage("HeartBeat Verification at " + time.strftime("%a %b %d, %I:%M %P ", ) + "where " + getTempString(DHT_PIN) + ' and ' + signalStrength.read())
            if sent == 0:
                print 'Success! Message sent to the cloud.'
                sendHeartBeat = False
            else:
                #add ability to write error to log file, pull remotely
                print 'Error type [' + str(sent) + ']'
                print 'Error descriptions: https://hologram.io/docs/reference/cloud/python-sdk/#-sendmessage-message-topics-none-timeout-5-'
            sendHeartBeat = False
            x = 0

finally:
    #GPIO.output(LED_PIN,False) ## Switch off LED
    GPIO.cleanup()  ## reset all pins
    hologram.network.disconnect() ## Exercise 06 - disconnect from the cellular network
