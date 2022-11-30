#距離聲波產生器大於60公分，旋鈕回到12點鐘

import time,math
from machine import Pin, PWM, Timer
from time import sleep

pin_led = Pin(2, Pin.OUT)
trig = Pin(17, Pin.OUT)
echo = Pin(16, Pin.IN,Pin.PULL_DOWN)
distance=0
'''servo_1 = PWM(Pin(23))
servo_1.freq(50)
servoSwitch=Pin(22,Pin.OUT)
flame_sensor = Pin(21, Pin.IN)'''


def ping(x):
    global distance #設定全域變數
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
    distance = round(dist)
    print("%s cm" %distance)
    return distance  

      
'''def servo(degrees):
    servo_1.freq(50)
    if degrees > 180: degrees=180
    if degrees < 0: degrees=0   
    maxDuty=8000
    minDuty=1800
    newDuty=minDuty+(maxDuty-minDuty)*(degrees/180)
    servo_1.duty_u16(int(newDuty))'''


'servoSwitch.value(0)'
tim1=Timer(1)
tim1.init(period=500,mode=Timer.PERIODIC,callback=ping)

#tim1.init(period=500, mode=Timer.PERIODIC, callback=led_switch)   
while True:
    
    if distance>100:             
        pin_led.value(1)
        time.sleep(1)    #過 秒再從while迴圈第一航開始
    else:
        pin_led.value(0)
        time.sleep(1)