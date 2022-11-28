#距離聲波產生器大於60公分，旋鈕回到12點鐘
import urequests
import network
import time,math
from machine import Pin, PWM
from time import sleep
from mqttlib import MQTTClient

pin_led = Pin(2, Pin.OUT)
trig = Pin(17, Pin.OUT)
echo = Pin(16, Pin.IN,Pin.PULL_DOWN)
servo_1 = PWM(Pin(23))
servo_1.freq(50)
servoSwitch=Pin(22,Pin.OUT)
flame_sensor = Pin(21, Pin.IN)

wlan = network.WLAN(network.STA_IF)
wlan.active(True)
wlan.connect("My ASUS","jade1234")
time.sleep(5)
print('wifi OK:',wlan.isconnected())

mqtt_server = 'test.mosquitto.org'
client_id = 'pico_mqtt_iot' #裝置上(pico)的ID，自己隨便取，假設有多個裝置下，可以用來做區別
topic_pub = 'sensor/fire'



def ping():
    trig.value(1)   #發超聲波
    time.sleep_us(10)   #延遲ms
    trig.value(0)    #超聲波
    count=0
    timeout=False   #
    start=time.ticks_us()
    while echo.value() == 0: #用來wait for HIGH
        start=time.ticks_us()    #tick代表計時，紀錄發出後的時間
    while echo.value() : #wait for HIGH
        stop=time.ticks_us()
    duration = stop - start
    dist = ( duration *0.034) /2
    return dist  

      
def servo(degrees):
    servo_1.freq(50)
    if degrees > 180: degrees=180
    if degrees < 0: degrees=0   
    maxDuty=8000
    minDuty=1800
    newDuty=minDuty+(maxDuty-minDuty)*(degrees/180)
    servo_1.duty_u16(int(newDuty))
    
def mqtt_connect():
    client = MQTTClient(client_id, mqtt_server, port=1883, keepalive=3600)
    client.connect()
    print('Connected to %s MQTT Broker'%(mqtt_server))
    return client

def reconnect():
    print('Failed to connect to the MQTT Broker. Reconnecting...')
    time.sleep(5)
    machine.reset()

try:
    client = mqtt_connect()
except OSError as e:
    reconnect()
servoSwitch.value(0)
while True:
    distance = round(ping())
    print("%s cm" %distance)
    if distance>100:
        if flame_sensor.value() == 0:   #此時有火源
            client.publish(topic_pub,"on1")
            request2= urequests.get("https://api.thingspeak.com/update?api_key=ORAIVXS2FDL752J7&field3=2")
            request2.close()
            time.sleep(1)     #開火後經過 秒
            servoSwitch.value(1)  #電流流通
            pin_led.value(1)
            servo(180)  #順時針到高點
            pin_led.value(0)
            request1= urequests.get("https://api.thingspeak.com/update?api_key=ORAIVXS2FDL752J7&field3=1")
            request1.close()
            client.publish(topic_pub,"off1")
            time.sleep(0.1)    #過 秒再從while迴圈第一航開始
    else:
        servoSwitch.value(0)
        pin_led.value(0)
        time.sleep(0.1)