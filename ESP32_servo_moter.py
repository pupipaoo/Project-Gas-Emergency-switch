from machine import Pin,PWM
from time import sleep
servo_1=PWM(Pin(23))
servo_1.freq(50)

'''def servo(degrees):
    if degrees>180:degrees=180
    if degrees<0:degrees=0
    maxDuty=9000
    minDuty=1000
    newDuty=minDuty+(maxDuty-minDuty)*(degrees/180)
    servoPin.duty_u16(int(newDuty))'''     #servoPin.duty_u16=0~65525
while True:
    for degree in range(3000,5000,50):
        servo_1.duty_u16(degree)
        sleep(0.1)
        
    
