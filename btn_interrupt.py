import RPi.GPIO as GPIO
import time
BUTTON_PIN = 16
GPIO.setmode(GPIO.BCM)

def btn_release_callback(channel):
    if GPIO.input(BUTTON_PIN) == GPIO.HIGH:
        print("General Kenobi")
    else:
        print("...")
        

GPIO.setup(BUTTON_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)

#GPIO.wait_for_edge(BUTTON_PIN, GPIO.RISING)
GPIO.add_event_detect(BUTTON_PIN, GPIO.BOTH,
                      callback=btn_release_callback,
                      bouncetime=100)

try: 
    while True:
        time.sleep(0.50)
        print("Hello there")
except KeyboardInterrupt:
    GPIO.cleanup()
    