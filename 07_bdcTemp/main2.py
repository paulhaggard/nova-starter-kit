#define variables
import time
import RPi.GPIO as GPIO ## Import GPIO library
from myLED import lightOn, lightOff ## Import blink function
from myDHT import getTempString, getHumString, getTemp, getHum ## Import temperature and humidity functions
from myMCP import getLuxString, getLux ## Import photoresistor function
from Hologram.HologramCloud import HologramCloud ## Import Hologram cloud library
#tempBDC #check if celsius or fahrenheit
tempMinAlarm = 61           #temperature to set alarm bit
alarmBDC = 0

LED_PIN = 17 ## GPIO pin the LED is attached to
DHT_PIN = 21 ## GPIO pin the DHT sensor is attached to
LUX_MCP = 0 ## ADC pin the Photoresistor is attached to
BTN_PIN = 27 ## GPIO pin the button is attached to

def heartbeatFunction():

  return True




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
                    
                    print 'Temperature monitor is not in alarm'
                    #tempBDC = getTemp(DHT_PIN)  #check if celsius or fahrenheit
                    #humBDC = getHum(DHT_PIN)
                    #luxBDC = getLux(LUX_MCP)
                    print tempBDC + " is higher than alarm setpoint of " + tempMinAlarm
                    break
          
  while alarmBDC == 1:        
                if tempBDC > tempMinAlarm:
                   alarmBDC = 0
                   sendSMS = False
                   return sendSMS
                else:
                    time.sleep(10)
                    print 'System temperature is in alarm loop'
                    tempBDC = getTemp(DHT_PIN)  #check if celsius or fahrenheit
                    #humBDC = getHum(DHT_PIN)
                    #luxBDC = getLux(LUX_MCP)
                    print tempBDC + " is (or was recently) lower than alarm setpoint of " + tempMinAlarm
                    break
                    
                    
            
          
            #message = json.dumps({'h': getHumString(DHT_PIN), 't': getTempString(DHT_PIN), 'l': getLuxString(LUX_MCP)})
            #sent = hologram.sendMessage(message)

            #lightOff(LED_PIN)

            #if sent == 0:
                #print 'Success! Message sent to the cloud.'
                #print message
                
              
                
                
