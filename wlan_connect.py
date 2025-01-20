from machine import Pin
import network
import time

led = Pin("LED", Pin.OUT)
def connect(ssid, passwd):
    #Connect WLAN
    global led
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    #wlan.connect("Wifi-Choice-Public", "065057289")
    wlan.connect(ssid, passwd)
    while not wlan.isconnected():
        print('Waiting for connection...')
        led.toggle()
        time.sleep(1)
    #print(wlan.ifconfig())
    return wlan.ifconfig()[0]

