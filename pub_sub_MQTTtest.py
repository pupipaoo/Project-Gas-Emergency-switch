import network
import time
from machine import Pin
from mqttlib import MQTTClient


#Run過一次後，須至少隔60秒才能再跑程式，這是板子內部的Wifi Internal設定
wlan = network.WLAN(network.STA_IF)
wlan.active(True)
wlan.connect("My ASUS","jade1234")
time.sleep(10)
print('wifi OK:',wlan.isconnected())
print(wlan.ifconfig())

mqtt_server = 'hq.ittraining.com.tw'
#mqtt_server = 'hq.ittraining.com.tw'
client_id = 'pico_mqtt_iot' #裝置上(pico)的ID，自己隨便取，假設有多個裝置下，可以用來做區別
topic_pub = b'sensor/fire'   #b是指binary 
topic_sub=b'sensor/switch'
led=Pin(2,Pin.OUT)

def mqtt_connect():
    client = MQTTClient(client_id, mqtt_server, port=1883, keepalive=3600)
    client.connect()
    print('Connected to %s MQTT Broker'%(mqtt_server))
    return client

def reconnect():
    print('Failed to connect to the MQTT Broker. Reconnecting...')
    time.sleep(5)
    machine.reset()

def on_message(topic, msg):
    print(topic,msg)
    if topic==topic_sub:
        on=msg.decode('utf-8')
        print(on)
        if on=='1':
            led.value(1)
        elif on=='0':
            led.value(0)       


try:
    client = mqtt_connect()
    client.set_callback(on_message)
    client.subscribe(topic_sub)
    #print(client.subscribe(topic_sub))
    led.value(1)
except OSError as e:
    reconnect()

led.value(1)
while True:
    client.publish(topic_pub,"on1")
    time.sleep(0.5)
    #led.value(1)
    #time.sleep_ms(1000)
 
    #time.sleep_ms(1000)
    #led.value(0)
    client.check_msg()#透過語法讓程式主動檢查socket，也就是檢查底層有沒有訊息過來 ，因為mqtt架構無法再有訊息丟來時自主通知

    