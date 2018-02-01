#define variables
import time
global tempBDC
global humBDC
global luxBDC
global tempMinAlarm
global alarmBDC
tempBDC = 30  #check if celsius or fahrenheit
humBDC = 39
luxBDC = 1000
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
                if tempBDC < tempMinAlarm:
                   alarmBDC = 1
                   continue
                else:
                    time.sleep(5)
                    print 'Sleeping'
                    #tempBDC = getTemp(DHT_PIN)  #check if celsius or fahrenheit
                    #humBDC = getHum(DHT_PIN)
                    #luxBDC = getLux(LUX_MCP)
                    #print tempBDC + humBDC + luxBDC
                    print "temp is ok"
        else:
          print 'System Alarm!'
          print tempBDC
          
          while alarmBDC == 1:
                if tempBDC > tempMinAlarm:
                   alarmBDC = 0
                   continue
                else:
                    time.sleep(5)
                    print 'Sleeping'
                    #tempBDC = getTemp(DHT_PIN)  #check if celsius or fahrenheit
                    #humBDC = getHum(DHT_PIN)
                    #luxBDC = getLux(LUX_MCP)
                    #print tempBDC + humBDC + luxBDC
                    print "temp is too low! incrementing temp!"
                    tempBDC = tempBDC + 1
          continue
          
            #message = json.dumps({'h': getHumString(DHT_PIN), 't': getTempString(DHT_PIN), 'l': getLuxString(LUX_MCP)})
            #sent = hologram.sendMessage(message)

            #lightOff(LED_PIN)

            #if sent == 0:
                #print 'Success! Message sent to the cloud.'
                #print message
                
pollingFunction()                
                
                
