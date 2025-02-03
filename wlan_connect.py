from machine import Pin
import network
import time

led = Pin("LED", Pin.OUT)
def connect(ssid, passwd):
    #Connect WLAN
    global led
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    
    wlan.connect(ssid, passwd)
    wlan.config(hostname="pico1")
    while not wlan.isconnected():
        print('Waiting for connection...')
        led.toggle()
        time.sleep(1)
    #print(wlan.ifconfig())
    #print(wlan.config("hostname"))
    return wlan.ifconfig()[0]

