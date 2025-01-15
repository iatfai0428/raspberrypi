from machine import Pin, Timer, PWM
import time
#led = Pin(25, Pin.OUT)
pwm = PWM(Pin(25))

pwm.freq(1000)
#tim = Timer()
def tick(timer):
    global led
    led.toggle()
    
#tim.init(freq=3, mode=Timer.PERIODIC, callback=tick)
duty = 0
direction = 1
for _ in range(8 * 256):
    duty += direction
    if duty > 255:
        duty = 255
        direction = -1
    elif duty < 0:
        duty = 0
        direction = 1
    pwm.duty_u16(duty * duty)
    time.sleep(0.001)
