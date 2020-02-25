import sqlite3 as lite
import paho.mqtt.client as mqtt
import paho.mqtt.publish as publish
import paho.mqtt.subscribe as subscribe

con = None
broker = "192.168.43.249"

def Sub_callback(client, userdata, message):
    print("%s: %s" % (message.topic, message.payload))
        
#setup mqtt
client = mqtt.Client()
client.connect(broker, 1883, 60)
client.loop_start()
client.subscribe("UserList")
client.message_callback_add("UserList", Sub_callback)

path = "./userList"
con = lite.connect(path)

cur = con.cursor()
cur.execute('select * from list')

data = cur.fetchall()
dataSend = ""

for element in data:
    print(element)
    dataSend += (str(element[0])+'%'+element[1]+'%'+element[2]+'%'+str(element[3])+'%'+element[4]+'%'+str(element[5])+'%'+element[6]+'%'+str(element[7])+'%'+str(element[8])+'%')

publish.single("UserList", dataSend, hostname=broker)
print(dataSend)
    



