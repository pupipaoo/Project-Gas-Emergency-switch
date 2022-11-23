from machine import Pin,PWM
from time import sleep

led=Pin(2,Pin.OUT)

while True:
    print("hekko")
    led.value(1)
    sleep(1)
    led.value(0)
    sleep(1)