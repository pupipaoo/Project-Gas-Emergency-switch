from machine import Pin,PWM
from time import sleep
servo_Pin=PWM(Pin(23))
servo_Pin.freq(50)

def servo(degrees):
    if degrees>=180:degrees=180
    if degrees<0:degrees=0
    maxDuty=9000
    minDuty=1000
    newDuty=minDuty+(maxDuty-minDuty)*(degrees/180)
    servo_Pin.duty_u16(int(newDuty))     #servoPin.duty_u16=0~65525
'''while True:
    for degree in range(9000,3000,-100):	#9000是馬達能夠轉到180度的站空直;3000是轉到快要0度的站空直
        servo_1.duty_u16(degree)
        sleep(0.1)'''
while True:
    for degree in range(180,0,-10):
        servo(degree)
        sleep(0.1)