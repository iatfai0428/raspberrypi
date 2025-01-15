from machine import Pin, I2C
from machine import RTC
#import utime
import adxl345 
import network
import socket
import time
import struct
import sys
import rp2

led = Pin("LED", Pin.OUT)

def connect():
    #Connect WLAN
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    #wlan.connect("Wifi-Choice-Public", "065057289")
    wlan.connect("Wifi-Choice", "Ch-5057289")
    global led
    while wlan.isconnected() == False:
        led.toggle()
        print('Waiting for connection...')
        time.sleep(1)
    return wlan.ifconfig()[0]
    
def reqTime(addr='uk.pool.ntp.org'):
    REF_TIME_1970 = 2208988800
    client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    data = b'\x1b' + 47 * b'\0'
    address = socket.getaddrinfo(addr, 123)[0][-1]
    
    client.connect(address)
    client.send(data)
    data, address = client.recvfrom(1024)
    if data:
        t = struct.unpack('!12I', data)[10]
        t -= REF_TIME_1970
    return time.gmtime(t)

time.sleep(1)
rtc=RTC()
#rtc.datetime((1970,1,1,0, 12,0,0,0))
rtc.datetime((2025,1,14,0, 16,0,0,0))
ip = connect()
tim = reqTime()
#rtc = RTC()
rtc.datetime((tim[0], tim[1], tim[2], 0, tim[3]+8, tim[4], tim[5], 0))

i2c = I2C(0, scl=Pin(9), sda=Pin(8), freq=100000)
addr = i2c.scan()[0]
print(ip, hex(addr))

adxl = adxl345.ADXL345(i2c, addr)

time.sleep_ms(100)
now = time.localtime()
print(now)
filename=f"/test/adxl{now[7]}-{now[3]}-{now[4]}-{now[5]}.txt";
print(filename)
f = open(filename, 'w')

led.on()
adxl.data_rate = adxl345.DataRate.RATE_200_HZ
adxl.range = adxl345.Range.RANGE_2_G
start = time.ticks_ms()
t2 = time.ticks_ms()
while (time.ticks_diff(t2, start)<5000):
    x, y, z = adxl.acceleration
    t2 = time.ticks_ms()
    f.write(f"{time.ticks_diff(t2, start)}  {x}, {y}, {z}\n")
    time.sleep_ms(5)
    led.toggle()
f.close()
led.off()
