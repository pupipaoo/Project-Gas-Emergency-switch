#距離聲波產生器大於60公分，旋鈕回到12點鐘

import time,math
from machine import Pin, PWM
from time import sleep

pin_led = Pin(2, Pin.OUT)
trig = Pin(17, Pin.OUT)
echo = Pin(16, Pin.IN,Pin.PULL_DOWN)
servo_1 = PWM(Pin(23))
servo_1.freq(50)
servoSwitch=Pin(22,Pin.OUT)

def ping():
    trig.value(1)   #發超聲波
    time.sleep_us(10)   #延遲ms
    trig.value(0)    #超聲波
    count=0
    timeout=False   #延遲
    start=time.ticks_us()
    while echo.value() == 0: #wait for HIGH
        start=time.ticks_us()
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
    
while True:
    distance = round(ping())
    print("%s cm" %distance)
    if distance>100:
        servoSwitch.value(1)  #電流流通
        pin_led.value(1)
        servo(180)  #順時針到12點
        time.sleep(0.1)    #過5秒再從while迴圈第一航開始
    else:
        servoSwitch.value(0)
        pin_led.value(0)
        time.sleep(0.1)