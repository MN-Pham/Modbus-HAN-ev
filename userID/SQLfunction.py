import time
import sqlite3 as lite
import paho.mqtt.client as mqtt
import paho.mqtt.publish as publish
import paho.mqtt.subscribe as subscribe

con = None
broker = "broker.hivemq.com"
#broker = "192.168.43.249"

path = "./userList"

def SendUser_callback(client, userdata, message):
    con = lite.connect(path)
    cur = con.cursor()
    cur.execute('select * from list')

    data = cur.fetchall()
    dataSend = ""

    for element in data:
        print(element)
        dataSend += (str(element[0])+'%'+element[1]+'%'+element[2]+'%'+str(element[3])+'%'+element[4]+'%'+str(element[5])+'%'+element[6]+'%'+str(element[7])+'%'+str(element[8])+'%')

    publish.single("UserList", dataSend, hostname=broker)
    #print(dataSend)

def Update_callback(client, userdata, message):
    con = lite.connect(path)
    cur = con.cursor()
    data = message.payload
    index = []
    for i in range(len(data)):
        if (data[i] == '%'):
            index.append(i)
    UserId = int(data[:index[0]])
    PendingCharger = int(data[index[0]+1:index[1]])
    StartTime = int(data[index[1]+1:index[2]])
    cur.execute("UPDATE list SET PendingCharger=? WHERE Id=?", (PendingCharger, UserId))
    cur.execute("UPDATE list SET StartTime=? WHERE Id=?", (StartTime, UserId))
    
#setup mqtt
client = mqtt.Client()
client.connect(broker, 1883, 60)
client.loop_start()
client.subscribe("getUsers")
client.message_callback_add("getUsers", SendUser_callback)
   
while True:
    time.sleep(1)




