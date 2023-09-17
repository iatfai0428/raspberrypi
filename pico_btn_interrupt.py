from machine import Pin
import time

interrupt_flag=0
debounce_time=0
led = Pin(25,Pin.OUT) 
btn = Pin(16,Pin.IN,Pin.PULL_UP)

def btn_release_callback(btn):
    global interrupt_flag, debounce_time
    if (time.ticks_ms()-debounce_time) > 250:
        interrupt_flag=1
        debounce_time=time.ticks_ms()

btn.irq(trigger=Pin.IRQ_FALLING, handler=btn_release_callback)
#GPIO.setup(BUTTON_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)
#GPIO.add_event_detect(BUTTON_PIN, GPIO.BOTH,
#                      callback=btn_release_callback,
#                      bouncetime=100)

#while True:
while True:
    if interrupt_flag is 1:
        interrupt_flag=0
        print("Interrupt Detected")
        led.toggle()
    #led.high()
    #utime.sleep(0.1)
    #led.low()
    #utime.sleep(0.1)
