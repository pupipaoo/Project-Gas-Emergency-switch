import urequests
import network
import time
from machine import Pin
from mqttlib import MQTTClient
led=Pin(2,Pin.OUT)

#Run過一次後，須至少隔60秒才能再跑程式，這是板子內部的Wifi Internal設定
wlan = network.WLAN(network.STA_IF)
wlan.active(True)
wlan.connect("My ASUS","jade1234")
time.sleep(5)
print('wifi OK:',wlan.isconnected())

while True:
    '''led.value(0)     #不知道為啥，led不能動
    time.sleep(1)
    led.value(1)
    print(led.value())    #印出led目前狀態
    if led.value(0):
        sw=str(0)
    else :
        sw=str(1)
    print(sw)'''
      
    #把1這個數值丟給Thingspeak的表3資料庫
    request= urequests.get("https://api.thingspeak.com/update?api_key=ORAIVXS2FDL752J7&field3=1")
    request.close()  #urequests這個模組，若要丟東西給https，必須送一次，中斷一次
    time.sleep(10)
'''while True:  #get方案2
    time.sleep(10)
    response= urequests.get("https://api.thingspeak.com/update?api_key=ORAIVXS2FDL752J7&field3=sw")
    response.close()'''
'''while True:  #get方案2
    response= urequests.get("https://api.thingspeak.com/update?api_key=ORAIVXS2FDL752J7&field3="+sw+"\r\n")
    time.sleep(10)'''