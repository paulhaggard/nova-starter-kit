#define variables
import time
import RPi.GPIO as GPIO ## Import GPIO library
from myLED import lightOn, lightOff ## Import blink function
from myDHT import getTemp, getHum ## Import temperature and humidity functions
from myMCP import getLux ## Import photoresistor function
from myDHT import getTempString, getHumString, getTemp, getHum ## Import temperature and humidity functions
from myMCP import getLuxString, getLux ## Import photoresistor function
from Hologram.HologramCloud import HologramCloud ## Import Hologram cloud library
#tempBDC #check if celsius or fahrenheit
tempMinAlarm = 60           #temperature to set alarm bit
alarmBDC = 0

LED_PIN = 17 ## GPIO pin the LED is attached to
DHT_PIN = 21 ## GPIO pin the DHT sensor is attached to
LUX_MCP = 0 ## ADC pin the Photoresistor is attached to
BTN_PIN = 27 ## GPIO pin the button is attached to

def pollingFunction():
  global tempBDC
  global humBDC
  global luxBDC
  global tempMinAlarm
  global alarmBDC
  
  
  while alarmBDC == 0:
                time.sleep(10)
                tempBDC = getTemp(DHT_PIN)
                if tempBDC < tempMinAlarm:
                   alarmBDC = 1
                   sendSMS = True
                   return sendSMS
                   
                else:
                    
                    print 'Sleeping in non-alarm loop'
                    #tempBDC = getTemp(DHT_PIN)  #check if celsius or fahrenheit
                    #humBDC = getHum(DHT_PIN)
                    #luxBDC = getLux(LUX_MCP)
                    print tempBDC
                    print "temp is ok"
                    break
  else:
          print 'System Alarm!'
          print tempBDC
          
          
          if tempBDC > tempMinAlarm:
                   alarmBDC = 0
                   sendSMS = False
                   break
          else:
                    time.sleep(10)
                    print 'Sleeping in alarm loop'
                    tempBDC = getTemp(DHT_PIN)  #check if celsius or fahrenheit
                    #humBDC = getHum(DHT_PIN)
                    #luxBDC = getLux(LUX_MCP)
                    print tempBDC
                    break
                    
            
          
            #message = json.dumps({'h': getHumString(DHT_PIN), 't': getTempString(DHT_PIN), 'l': getLuxString(LUX_MCP)})
            #sent = hologram.sendMessage(message)

            #lightOff(LED_PIN)

            #if sent == 0:
                #print 'Success! Message sent to the cloud.'
                #print message
                
              
                
                
