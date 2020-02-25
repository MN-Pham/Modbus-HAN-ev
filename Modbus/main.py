import RPi.GPIO as GPIO
import serial
import MIC
import time
import paho.mqtt.client as mqtt
import paho.mqtt.publish as publish
import paho.mqtt.subscribe as subscribe

#broker = "145.74.153.23"

#def Sub_callback(client, userdata, message):
#    print("%s: %s" % (message.topic, message.payload))
#    if (UserData.CheckID(message.payload) == True):
#        publish.single("IDStatus", "True", hostname=broker)
#        print("ID exists")
#    else:
#        publish.single("IDStatus", "False", hostname=broker)
#        print("ID does not exist")

#setup mqtt
#client = mqtt.Client()
#client.connect(broker, 1883, 60)
#client.loop_start()
#client.subscribe("clientID")
#client.message_callback_add("clientID", Sub_callback)

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
print("ver 1.6")
print("MODBUS converter: MAX485")
print("MODBUS slave: MIC2-Mk II")
#print("Broker: " + broker)

#Declare slave(s)
#meter1 = MIC.MIC2(0x01, control_pin)

meter1 = MIC.MIC1(0x01, control_pin)
meter2 = MIC.MIC1(0x02, control_pin)
meter3 = MIC.MIC1(0x03, control_pin)
meter4 = MIC.MIC1(0x04, control_pin)
meter5 = MIC.MIC1(0x05, control_pin)

while True:
    print("E1:")
    reading1 = meter1.readPhaseVoltage()
    if (reading1 == 0):
        current_time = time.ctime(time.time())
        Message = current_time + """
    V1: %.2f   V2: %.2f   V3: %.2f
    """%(meter1._MIC1__V1, meter1._MIC1__V2, meter1._MIC1__V3)
        print(Message)
        #publish.single("TestData", Message, hostname=broker)
    else:
        print("Measuring failed. Error code: " + str(reading1))
        #print("sending result to broker...")
        #print("""
    #V1: %.2f
    #V2: %.2f
    #V3: %.2f"""%(V1, V2, V3))
        #print("""
    #I1: %.2f
    #I2: %.2f
    #I3: %.2f"""%(I1, I2, I3))
        #publish.single("V1", V1, hostname=broker)
        #publish.single("V2", V2, hostname=broker)
        #publish.single("V3", V3, hostname=broker)
        #publish.single("I1", I1, hostname=broker)
        #publish.single("I2", I2, hostname=broker)
        #publish.single("I3", I3, hostname=broker)
    
    print("E2:")
    reading2 = meter2.readPhaseVoltage()
    if (reading2 == 0):
        current_time = time.ctime(time.time())
        Message = current_time + """
    V1: %.2f   V2: %.2f   V3: %.2f
    """%(meter2._MIC1__V1, meter2._MIC1__V2, meter2._MIC1__V3)
        print(Message)
        #publish.single("TestData", Message, hostname=broker)
    else:
        print("Measuring failed. Error code: " + str(reading2))
    
    print("E3:")
    reading3 = meter3.readPhaseVoltage()
    if (reading3 == 0):
        current_time = time.ctime(time.time())
        Message = current_time + """
    V1: %.2f   V2: %.2f   V3: %.2f
    """%(meter3._MIC1__V1, meter3._MIC1__V2, meter3._MIC1__V3)
        print(Message)
        #publish.single("TestData", Message, hostname=broker)
    else:
        print("Measuring failed. Error code: " + str(reading3))
    
    print("E4:")
    reading4 = meter4.readPhaseVoltage()
    if (reading4 == 0):
        current_time = time.ctime(time.time())
        Message = current_time + """
    V1: %.2f   V2: %.2f   V3: %.2f
    """%(meter4._MIC1__V1, meter4._MIC1__V2, meter4._MIC1__V3)
        print(Message)
        #publish.single("TestData", Message, hostname=broker)
    else:
        print("Measuring failed. Error code: " + str(reading4))
    
    print("E5:")
    reading5 = meter5.readPhaseVoltage()
    if (reading5 == 0):
        current_time = time.ctime(time.time())
        Message = current_time + """
    V1: %.2f   V2: %.2f   V3: %.2f
    """%(meter5._MIC1__V1, meter5._MIC1__V2, meter5._MIC1__V3)
        print(Message)
        #publish.single("TestData", Message, hostname=broker)
    else:
        print("Measuring failed. Error code: " + str(reading5))
        
    time.sleep(10)
    