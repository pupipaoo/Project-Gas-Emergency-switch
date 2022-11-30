import network
import time
from machine import Pin,Timer
from mqttlib import MQTTClient

wlan = network.WLAN(network.STA_IF)
wlan.active(True)
wlan.connect("My ASUS","jade1234")
time.sleep(10)
print('wifi OK:',wlan.isconnected())
print(wlan.ifconfig())

mqtt_server = 'test.mosquitto.org'
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
    time.sleep(10)
    machine.reset()

def check_socket(x):
    client.check_msg()

def on_message(topic, msg): #MQTT發布功能不能選保留訊息
    print(topic,msg)
    if topic==topic_sub:
        on=msg.decode('utf-8')
        print(on)
        if on=='0':
            led.value(0)
        if on=='1':
            led.value(1)

try:
    client = mqtt_connect()
    client.set_callback(on_message)
    client.subscribe(topic_sub)
    #print(client.subscribe(topic_sub))
    
    led.value(1)
except OSError as e:
    reconnect()

tim2=Timer(1)
tim2.init(period=500,mode=Timer.PERIODIC,callback=check_socket) #設置有Timer的thread去跑確認socket函示
led.value(1)
while True:
    client.publish(topic_pub,"on1")
    time.sleep(0.5)