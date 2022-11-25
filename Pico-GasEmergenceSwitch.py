#距離聲波產生器大於60公分，旋鈕回到12點鐘

import time,math
from machine import Pin, PWM
from time import sleep

pin_led = Pin(25, Pin.OUT)
trig = Pin(10, Pin.OUT)
echo = Pin(4, Pin.IN,Pin.PULL_DOWN)
servo_1 = PWM(Pin(16))
servo_1.freq(50)
servoSwitch=Pin(17,Pin.OUT)
flame_sensor = Pin(26, Pin.IN)

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

servoSwitch.value(0)
while True:
    distance = round(ping())
    print("%s cm" %distance)
    if distance>100:
        if flame_sensor.value() == 0:   #此時有火源
            time.sleep(1)     #開火後經過 秒
            servoSwitch.value(1)  #電流流通
            pin_led.value(1)
            servo(180)  #順時針到高點
            time.sleep(0.1)    #過 秒再從while迴圈第一航開始
    else:
        servoSwitch.value(0)
        pin_led.value(0)
        time.sleep(0.1)