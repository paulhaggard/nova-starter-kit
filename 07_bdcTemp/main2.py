#define variables
import time
#tempBDC #check if celsius or fahrenheit
tempMinAlarm = 40           #temperature to set alarm bit
alarmBDC = 0

def pollingFunction():
  global tempBDC
  global humBDC
  global luxBDC
  global tempMinAlarm
  global alarmBDC
  while True:
        while alarmBDC == 0:
            while alarmBDC == 0:
              tempBDC = getTemp(DHT_PIN)
                if tempBDC < tempMinAlarm:
                   alarmBDC = 1
                   sendSMS = True
                   return sendSMS
                   continue
                else:
                    time.sleep(5)
                    print 'Sleeping in non-alarm loop'
                    tempBDC = getTemp(DHT_PIN)  #check if celsius or fahrenheit
                    humBDC = getHum(DHT_PIN)
                    luxBDC = getLux(LUX_MCP)
                    print tempBDC
                    print "temp is ok"
        else:
          print 'System Alarm!'
          print tempBDC
          
          while alarmBDC == 1:
                if tempBDC > tempMinAlarm:
                   alarmBDC = 0
                   sendSMS = False
                   continue
                else:
                    time.sleep(5)
                    print 'Sleeping in alarm loop'
                    tempBDC = getTemp(DHT_PIN)  #check if celsius or fahrenheit
                    humBDC = getHum(DHT_PIN)
                    luxBDC = getLux(LUX_MCP)
                    print tempBDC
                    
          continue
          
            #message = json.dumps({'h': getHumString(DHT_PIN), 't': getTempString(DHT_PIN), 'l': getLuxString(LUX_MCP)})
            #sent = hologram.sendMessage(message)

            #lightOff(LED_PIN)

            #if sent == 0:
                #print 'Success! Message sent to the cloud.'
                #print message
                
              
                
                
