import time,math
from machine import Pin
#import usonic

pin_led = Pin(2, Pin.OUT)
trig = Pin(17, Pin.OUT)
echo = Pin(16, Pin.IN,Pin.PULL_DOWN)

def ping():
    trig.value(1)
    time.sleep_us(10)
    trig.value(0)
    count=0
    timeout=False
    start=time.ticks_us()
    while not echo.value(): #wait for HIGH
        time.sleep_us(10)
        count += 1
        if count > 10000: #over 1s timeout
            timeout=True
            break
    if timeout: #timeout return 0
        duration=0
    else: #got HIGH pulse:calculate duration
        count=0
        start=time.ticks_us()
        while echo.value(): #wait for LOW
            time.sleep_us(10)
            count += 1
            if count > 2320: #over 400cm range:quit
                break
        duration=time.ticks_diff(time.ticks_us(), start)
    return duration   

while True:
    distance=round(ping()/58)
    print("%scm" % distance)
    if distance <= 15 :
        pin_led.on()
    else :
        pin_led.off()
    time.sleep(0.5)