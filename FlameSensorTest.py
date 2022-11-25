from machine import Pin
import utime

flame_sensor = Pin(10, Pin.IN)
utime.sleep(2)

while True:
   if flame_sensor.value() == 1:
       print("No Flame")
       utime.sleep(1)
   else:
       print("Flame Detected")
       utime.sleep(10)
