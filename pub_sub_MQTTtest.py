import network
import time
from machine import Pin
from mqttlib import MQTTClient


#Run過一次後，須至少隔60秒才能再跑程式，這是板子內部的Wifi Internal設定
wlan = network.WLAN(network.STA_IF)
wlan.active(True)
wlan.connect("My ASUS","jade1234")
time.sleep(5)
print('wifi OK:',wlan.isconnected())


mqtt_server = 'test.mosquitto.org'
client_id = 'pico_mqtt_iot' #裝置上(pico)的ID，自己隨便取，假設有多個裝置下，可以用來做區別
topic_pub = 'sensor/fire'
topic_sub='sensor/fire'
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

def onMessage():
    client.on_message = message
    msg=message.payloadString
    if msg.topic=='sensor/fire':
        print('got off from sensor/fire')
        led.value(0)
        time.sleep_ms(1000)


try:
    client = mqtt_connect()
    client.subscribe('sensor/fire')
    client.on_message = on_message
except OSError as e:
    reconnect()

while True:
    client.publish(topic_pub,"on1")
    time.sleep(0.5)
    led.value(1)
    time.sleep_ms(1000)
    client.publish(topic_pub,"on2")
    time.sleep_ms(1000)

    