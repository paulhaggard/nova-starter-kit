def pollingFunction(alarmBDC):
  while True:
        while alarmBDC == 0:
            while alarmBDC == 0:
                if tempBDC <= tempMinAlarm:
                   alarmBDC = 1
                   break
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
                if tempBDC >= tempMinAlarm:
                   alarmBDC = 0
                   break
                else:
                    time.sleep(5)
                    print 'Sleeping'
                    #tempBDC = getTemp(DHT_PIN)  #check if celsius or fahrenheit
                    #humBDC = getHum(DHT_PIN)
                    #luxBDC = getLux(LUX_MCP)
                    #print tempBDC + humBDC + luxBDC
                    print "temp is too low! incrementing temp!"
                    tempBDC = tempBDC + 1
          break
