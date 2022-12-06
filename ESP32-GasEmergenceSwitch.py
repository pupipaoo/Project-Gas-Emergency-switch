#距離聲波產生器大於60公分，旋鈕回到12點鐘
import urequests
import network
import time,math
from machine import Pin, PWM, Timer
from time import sleep
from mqttlib import MQTTClient

pin_led = Pin(2, Pin.OUT)
trig = Pin(17, Pin.OUT)
echo = Pin(16, Pin.IN,Pin.PULL_DOWN)
servo_1 = PWM(Pin(23))
servo_1.freq(50)
servoSwitch=Pin(22,Pin.OUT)
flame_sensor = Pin(21, Pin.IN)
distance=0

wlan = network.WLAN(network.STA_IF)
wlan.active(True)
wlan.connect("My ASUS","jade1234")
time.sleep(10)
print('wifi:',wlan.isconnected())
print(wlan.ifconfig())

mqtt_server = 'test.mosquitto.org'
client_id = 'pico_mqtt_iot' #裝置上(pico)的ID，自己隨便取，假設有多個裝置下，可以用來做區別
topic_pub = b'sensor/fire'
topic_sub=b'sensor/switch'


def ping(x):
    global distance #設定全域變數
    trig.value(1)   #發超聲波
    time.sleep_us(10)   #延遲ms
    trig.value(0)    #超聲波
    while echo.value() == 0: #用來wait for HIGH
        start=time.ticks_us()    #tick代表計時，紀錄發出後的時間
    while echo.value() : #wait for HIGH
        stop=time.ticks_us()
    duration = stop - start
    dist = ( duration *0.034) /2
    distance = round(dist)
    print("%s cm" %distance)  

def servo(degrees):
    servo_1.freq(50)
    if degrees >180: degrees=180
    if degrees < 0: degrees=0   
    maxDuty=8200
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

def subscribe(topic_sub):
    client.subscribe(topic_sub)

def check_socket(X): 
    client.check_msg()

def on_message(topic, msg):   #接收訊息，記得要把MQTT平台的發布功能中，將保留訊息關掉，否則每次重新執行程式，都會讀取到保留的訊息
    print(topic,msg)
    if topic==topic_sub:
        on=msg.decode('utf-8')
        print(msg)
        if on=='1':
            servoSwitch.value(1)
            time.sleep(30)
            servo(180)
            #servoSwitch.on
            time.sleep(30)
            pin_led.value(1)                        
            client.publish(topic_pub,"off1")
            request1= urequests.get("https://api.thingspeak.com/update?api_key=ORAIVXS2FDL752J7&field3=1")		#從on後送出資料表2，需經過可能3分鐘才能再送一筆資料過去
            request1.close()
            servoSwitch.value(0)
            pin_led.value(0)
            

try:
    client = mqtt_connect()
    client.set_callback(on_message)
    client.subscribe(topic_sub)
except OSError as e:
    reconnect()


servoSwitch.value(0)
tim1=Timer(1) #函式裡面第一個參數是秒數，第二個是呼叫的函示
tim1.init(period=5000,mode=Timer.PERIODIC,callback=ping) 	#每5000ms做一次
tim2=Timer(2)
tim2.init(period=10000,mode=Timer.PERIODIC,callback=check_socket) #若要有兩個中斷腳，period數字要設不一樣
while True:
    if distance>100:
        if flame_sensor.value() == 0:   #此時有火源
            client.publish(topic_pub,"on")
            request2= urequests.get("https://api.thingspeak.com/update?api_key=ORAIVXS2FDL752J7&field3=2")
            request2.close()
            time.sleep(600)     #開火後經過 秒
            #servoSwitch.value(1)  #電流流通
            if distance>100 and flame_sensor.value() == 0:
                servoSwitch.value(1)
                time.sleep(30)		#打開馬達電路後，需要給他時間讓店流劉通
                servo(180)
                #servoSwitch.on
                time.sleep(30)
                pin_led.value(1)                        
                client.publish(topic_pub,"off1")
                request1= urequests.get("https://api.thingspeak.com/update?api_key=ORAIVXS2FDL752J7&field3=1")
                request1.close()
                servoSwitch.value(0)
                pin_led.value(0)
                time.sleep(60)
    else:
        servoSwitch.value(0)
        pin_led.value(0)
        time.sleep(60)