import RPi.GPIO as GPIO ## Import GPIO library
from myLED import lightOn, lightOff ## Import blink function
from myDHT import getTempString, getHumString, getTemp, getHum ## Import temperature and humidity functions
from myMCP import getLuxString, getLux ## Import photoresistor function
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
## hologram = HologramCloud(devicekey, enable_inbound=False)

## Exercise 06 - send data to Hologram's cloud through Cellular
hologram = HologramCloud(dict(), network='cellular', enable_inbound=False)
#hologram.network.connect() ## connect from the cellular netowork

#define variables
tempBDC = getTemp(DHT_PIN)  #check if celsius or fahrenheit
humBDC = getHum(DHT_PIN)
luxBDC = getLux(LUX_MCP)
tempMinAlarm           #temperature to set alarm bit
alarmBDC = 0



from time import gmtime, strftime
strftime("%a, %d %b %Y %H:%M:%S +0000", gmtime())

###################
#Initialize Message
#hologram.sendMessage('BDC Temperature monitoring is now online.')

try:
    while True:
        while alarmBDC == 0:
            while alarmBDC == 0:
                if tempBDC <= tempMinAlarm:
                   alarmBDC = 1
                   break
                else:
                    time.sleep(5)
                    print 'Sleeping'
                    tempBDC = getTemp(DHT_PIN)  #check if celsius or fahrenheit
                    humBDC = getHum(DHT_PIN)
                    luxBDC = getLux(LUX_MCP)
                    print tempBDC + humBDC + luxBDC
        else:
          print 'System Alarm!'
          print tempBDC
          while alarmBDC == 1:
                if tempBDC >= tempMinAlarm:
                   alarmBDC = 0
                   break
                else:
                    time.sleep(5)
                    print 'Sleeping'
                    tempBDC = getTemp(DHT_PIN)  #check if celsius or fahrenheit
                    humBDC = getHum(DHT_PIN)
                    luxBDC = getLux(LUX_MCP)
                    print tempBDC + humBDC + luxBDC
          
            #message = json.dumps({'h': getHumString(DHT_PIN), 't': getTempString(DHT_PIN), 'l': getLuxString(LUX_MCP)})
            #sent = hologram.sendMessage(message)

            #lightOff(LED_PIN)

            #if sent == 0:
                #print 'Success! Message sent to the cloud.'
                #print message
except: 
    hologram.sendMessage('Error type [' + sent + ']')
    hologram.sendMessage('Error descriptions: https://hologram.io/docs/reference/cloud/python-sdk/#-sendmessage-message-topics-none-timeout-5-')
    hologram.sendMessage('BDC Temperature Monitoring System has gone down.')

finally:
    GPIO.output(LED_PIN,False) ## Switch off LED
    GPIO.cleanup()  ## reset all pins
    hologram.network.disconnect() ## disconnect from the cellular network - likely unnecessary, but leaving for now
    
    
    
    
    
    #Notes:
    #need to monitor signal strength, be able to verify log occasionally or alert if signal is lost and regained
    #need to send 1 message and confirm sent when temp drops below tempMinAlarm
    #need to not send multiple messages each time temp is checked
    #need to run constantly, not overheat sensor, and be on a small UPS
