import RPi.GPIO as GPIO
import serial
import MIC
import time
import paho.mqtt.client as mqtt
import paho.mqtt.publish as publish
import paho.mqtt.subscribe as subscribe
import sqlite3 as lite
import sys
import os
broker = "broker.hivemq.com"
#path = "./modbusData.db" #Use internal memory
path = "/meida/usb/modbusData.db" #Use external memory
con = lite.connect(path)
cur = con.cursor()

#Pin definitions
control_pin = 18

#Use BCM pin numbering
GPIO.setmode(GPIO.BCM)

#Turn off warnings
GPIO.setwarnings(False)

#Control pin as an output
GPIO.setup(control_pin, GPIO.OUT)

#Announcement
print("Program was written by P.M.Nhat")
print("ver 2.0")
print("MODBUS converter: MAX485")
print("MODBUS slave: MIC1")

#Declare slave(s)
#meter1 = MIC.MIC2(0x01, control_pin)

meter1 = MIC.MIC1(0x01, control_pin)
meter2 = MIC.MIC1(0x02, control_pin)
meter3 = MIC.MIC1(0x03, control_pin)
meter4 = MIC.MIC1(0x04, control_pin)
meter5 = MIC.MIC1(0x05, control_pin)

while True:
    print("E1:")
    #Read PHASE VOLTAGE
    reading = meter1.readPhaseVoltage()
    if (reading == 0):
        current_time = time.ctime(time.time())
        Message = current_time + """
    V1: %.2f   V2: %.2f   V3: %.2f
    """%(meter1._MIC1__V1, meter1._MIC1__V2, meter1._MIC1__V3)
        print(Message)
    else:
        print("Measuring failed. Error code: " + str(reading))
    #Read PHASE CURRENT
    reading = meter1.readPhaseCurrent()
    if (reading == 0):
        current_time = time.ctime(time.time())
        Message = current_time + """
    I1: %.2f   I2: %.2f   I3: %.2f
    """%(meter1._MIC1__I1, meter1._MIC1__I2, meter1._MIC1__I3)
        print(Message)
    else:
        print("Measuring failed. Error code: " + str(reading))
    #Read PHASE POWER
    reading = meter1.readPhasePower()
    if (reading == 0):
        current_time = time.ctime(time.time())
        Message = current_time + """
    P1: %.2f   P2: %.2f   P3: %.2f
    """%(meter1._MIC1__P1, meter1._MIC1__P2, meter1._MIC1__P3)
        print(Message)
    else:
        print("Measuring failed. Error code: " + str(reading))
    #Read FREQUENCY
    reading = meter1.readFrequency()
    if (reading == 0):
        current_time = time.ctime(time.time())
        Message = current_time + """
    F: %.2f
    """%(meter1._MIC1__F)
        print(Message)
    else:
        print("Measuring failed. Error code: " + str(reading))
    cur.execute("INSERT INTO meter1 VALUES(?,?,?,?,?,?,?,?,?,?,?)",
                (time.time(),
                 meter1._MIC1__V1, meter1._MIC1__V2, meter1._MIC1__V3,
                 meter1._MIC1__I1, meter1._MIC1__I2, meter1._MIC1__I3,
                 meter1._MIC1__P1, meter1._MIC1__P2, meter1._MIC1__P3,
                 meter1._MIC1__F))
    
    #Read meter 2----------------------------------------------
    print("E2:")
    #Read PHASE VOLTAGE
    reading = meter2.readPhaseVoltage()
    if (reading == 0):
        current_time = time.ctime(time.time())
        Message = current_time + """
    V1: %.2f   V2: %.2f   V3: %.2f
    """%(meter2._MIC1__V1, meter2._MIC1__V2, meter2._MIC1__V3)
        print(Message)
    else:
        print("Measuring failed. Error code: " + str(reading))
    #Read PHASE CURRENT
    reading = meter2.readPhaseCurrent()
    if (reading == 0):
        current_time = time.ctime(time.time())
        Message = current_time + """
    I1: %.2f   I2: %.2f   I3: %.2f
    """%(meter2._MIC1__I1, meter2._MIC1__I2, meter2._MIC1__I3)
        print(Message)
    else:
        print("Measuring failed. Error code: " + str(reading))
    #Read PHASE POWER
    reading = meter2.readPhasePower()
    if (reading == 0):
        current_time = time.ctime(time.time())
        Message = current_time + """
    P1: %.2f   P2: %.2f   P3: %.2f
    """%(meter2._MIC1__P1, meter2._MIC1__P2, meter2._MIC1__P3)
        print(Message)
    else:
        print("Measuring failed. Error code: " + str(reading))
    #Read FREQUENCY
    reading = meter2.readFrequency()
    if (reading == 0):
        current_time = time.ctime(time.time())
        Message = current_time + """
    F: %.2f
    """%(meter2._MIC1__F)
        print(Message)
    else:
        print("Measuring failed. Error code: " + str(reading))
    cur.execute("INSERT INTO meter2 VALUES(?,?,?,?,?,?,?,?,?,?,?)",
                (time.time(),
                 meter2._MIC1__V1, meter2._MIC1__V2, meter2._MIC1__V3,
                 meter2._MIC1__I1, meter2._MIC1__I2, meter2._MIC1__I3,
                 meter2._MIC1__P1, meter2._MIC1__P2, meter2._MIC1__P3,
                 meter2._MIC1__F))
    
    #Read meter 3----------------------------------------------
    print("E3:")
    #Read PHASE VOLTAGE
    reading = meter3.readPhaseVoltage()
    if (reading == 0):
        current_time = time.ctime(time.time())
        Message = current_time + """
    V1: %.2f   V2: %.2f   V3: %.2f
    """%(meter3._MIC1__V1, meter3._MIC1__V2, meter3._MIC1__V3)
        print(Message)
    else:
        print("Measuring failed. Error code: " + str(reading))
    #Read PHASE CURRENT
    reading = meter3.readPhaseCurrent()
    if (reading == 0):
        current_time = time.ctime(time.time())
        Message = current_time + """
    I1: %.2f   I2: %.2f   I3: %.2f
    """%(meter3._MIC1__I1, meter3._MIC1__I2, meter3._MIC1__I3)
        print(Message)
    else:
        print("Measuring failed. Error code: " + str(reading))
    #Read PHASE POWER
    reading = meter3.readPhasePower()
    if (reading == 0):
        current_time = time.ctime(time.time())
        Message = current_time + """
    P1: %.2f   P2: %.2f   P3: %.2f
    """%(meter3._MIC1__P1, meter3._MIC1__P2, meter3._MIC1__P3)
        print(Message)
    else:
        print("Measuring failed. Error code: " + str(reading))
    #Read FREQUENCY
    reading = meter3.readFrequency()
    if (reading == 0):
        current_time = time.ctime(time.time())
        Message = current_time + """
    F: %.2f
    """%(meter3._MIC1__F)
        print(Message)
    else:
        print("Measuring failed. Error code: " + str(reading))
    cur.execute("INSERT INTO meter3 VALUES(?,?,?,?,?,?,?,?,?,?,?)",
                (time.time(),
                 meter3._MIC1__V1, meter3._MIC1__V2, meter3._MIC1__V3,
                 meter3._MIC1__I1, meter3._MIC1__I2, meter3._MIC1__I3,
                 meter3._MIC1__P1, meter3._MIC1__P2, meter3._MIC1__P3,
                 meter3._MIC1__F))
    
    #Read meter 4----------------------------------------------
    print("E4:")
    #Read PHASE VOLTAGE
    reading = meter4.readPhaseVoltage()
    if (reading == 0):
        current_time = time.ctime(time.time())
        Message = current_time + """
    V1: %.2f   V2: %.2f   V3: %.2f
    """%(meter4._MIC1__V1, meter4._MIC1__V2, meter4._MIC1__V3)
        print(Message)
    else:
        print("Measuring failed. Error code: " + str(reading))
    #Read PHASE CURRENT
    reading = meter4.readPhaseCurrent()
    if (reading == 0):
        current_time = time.ctime(time.time())
        Message = current_time + """
    I1: %.2f   I2: %.2f   I3: %.2f
    """%(meter4._MIC1__I1, meter4._MIC1__I2, meter4._MIC1__I3)
        print(Message)
    else:
        print("Measuring failed. Error code: " + str(reading))
    #Read PHASE POWER
    reading = meter4.readPhasePower()
    if (reading == 0):
        current_time = time.ctime(time.time())
        Message = current_time + """
    P1: %.2f   P2: %.2f   P3: %.2f
    """%(meter4._MIC1__P1, meter4._MIC1__P2, meter4._MIC1__P3)
        print(Message)
    else:
        print("Measuring failed. Error code: " + str(reading))
    #Read FREQUENCY
    reading = meter4.readFrequency()
    if (reading == 0):
        current_time = time.ctime(time.time())
        Message = current_time + """
    F: %.2f
    """%(meter4._MIC1__F)
        print(Message)
    else:
        print("Measuring failed. Error code: " + str(reading))
    cur.execute("INSERT INTO meter4 VALUES(?,?,?,?,?,?,?,?,?,?,?)",
                (time.time(),
                 meter4._MIC1__V1, meter4._MIC1__V2, meter4._MIC1__V3,
                 meter4._MIC1__I1, meter4._MIC1__I2, meter4._MIC1__I3,
                 meter4._MIC1__P1, meter4._MIC1__P2, meter4._MIC1__P3,
                 meter4._MIC1__F))
    
    #Read meter 5----------------------------------------------
    print("E5:")
    #Read PHASE VOLTAGE
    reading = meter5.readPhaseVoltage()
    if (reading == 0):
        current_time = time.ctime(time.time())
        Message = current_time + """
    V1: %.2f   V2: %.2f   V3: %.2f
    """%(meter5._MIC1__V1, meter5._MIC1__V2, meter5._MIC1__V3)
        print(Message)
    else:
        print("Measuring failed. Error code: " + str(reading))
    #Read PHASE CURRENT
    reading = meter5.readPhaseCurrent()
    if (reading == 0):
        current_time = time.ctime(time.time())
        Message = current_time + """
    I1: %.2f   I2: %.2f   I3: %.2f
    """%(meter5._MIC1__I1, meter5._MIC1__I2, meter5._MIC1__I3)
        print(Message)
    else:
        print("Measuring failed. Error code: " + str(reading))
    #Read PHASE POWER
    reading = meter5.readPhasePower()
    if (reading == 0):
        current_time = time.ctime(time.time())
        Message = current_time + """
    P1: %.2f   P2: %.2f   P3: %.2f
    """%(meter5._MIC1__P1, meter5._MIC1__P2, meter5._MIC1__P3)
        print(Message)
    else:
        print("Measuring failed. Error code: " + str(reading))
    #Read FREQUENCY
    reading = meter5.readFrequency()
    if (reading == 0):
        current_time = time.ctime(time.time())
        Message = current_time + """
    F: %.2f
    """%(meter5._MIC1__F)
        print(Message)
    else:
        print("Measuring failed. Error code: " + str(reading))
    cur.execute("INSERT INTO meter5 VALUES(?,?,?,?,?,?,?,?,?,?,?)",
                (time.time(),
                 meter5._MIC1__V1, meter5._MIC1__V2, meter5._MIC1__V3,
                 meter5._MIC1__I1, meter5._MIC1__I2, meter5._MIC1__I3,
                 meter5._MIC1__P1, meter5._MIC1__P2, meter5._MIC1__P3,
                 meter5._MIC1__F))        
    #Send data to broker
    dataSend = ""
    cur.execute("SELECT * FROM meter1 ORDER BY No DESC LIMIT 1")
    data = cur.fetchone()
    dataSend += (str(data[2])+'%'+str(data[3])+'%'+str(data[4])+'%'+str(data[5])+'%'+str(data[6])+'%'+str(data[7])+'%'+str(data[8])+'%'+str(data[9])+'%'+str(data[10])+'%'+str(data[11])+'%'+str(data[1])+'%')   
    cur.execute("SELECT * FROM meter2 ORDER BY No DESC LIMIT 1")
    data = cur.fetchone()
    dataSend += (str(data[2])+'%'+str(data[3])+'%'+str(data[4])+'%'+str(data[5])+'%'+str(data[6])+'%'+str(data[7])+'%'+str(data[8])+'%'+str(data[9])+'%'+str(data[10])+'%'+str(data[11])+'%'+str(data[1])+'%')
    cur.execute("SELECT * FROM meter3 ORDER BY No DESC LIMIT 1")
    data = cur.fetchone()
    dataSend += (str(data[2])+'%'+str(data[3])+'%'+str(data[4])+'%'+str(data[5])+'%'+str(data[6])+'%'+str(data[7])+'%'+str(data[8])+'%'+str(data[9])+'%'+str(data[10])+'%'+str(data[11])+'%'+str(data[1])+'%')
    cur.execute("SELECT * FROM meter4 ORDER BY No DESC LIMIT 1")
    data = cur.fetchone()
    dataSend += (str(data[2])+'%'+str(data[3])+'%'+str(data[4])+'%'+str(data[5])+'%'+str(data[6])+'%'+str(data[7])+'%'+str(data[8])+'%'+str(data[9])+'%'+str(data[10])+'%'+str(data[11])+'%'+str(data[1])+'%')
    cur.execute("SELECT * FROM meter5 ORDER BY No DESC LIMIT 1")
    data = cur.fetchone()
    dataSend += (str(data[2])+'%'+str(data[3])+'%'+str(data[4])+'%'+str(data[5])+'%'+str(data[6])+'%'+str(data[7])+'%'+str(data[8])+'%'+str(data[9])+'%'+str(data[10])+'%'+str(data[11])+'%'+str(data[1])+'%')
    
    publish.single("EnergyMeter", dataSend, hostname=broker)
    
    time.sleep(10)
    