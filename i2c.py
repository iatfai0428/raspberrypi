from machine import Pin, I2C
from machine import RTC
import utime
import adxl345 
import network
import socket
import time
import struct
import sys
import rp2

def connect():
    #Connect WLAN
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    #wlan.connect("Wifi-Choice-Public", "065057289")
    wlan.connect("Wifi-Choice", "Ch-5057289")
    while wlan.isconnected() == False:
        print('Waiting for connection...')
        time.sleep(1)
    #print(wlan.ifconfig())
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




#utime.sleep_ms(500)
print(connect())
tim = reqTime()
rtc = RTC()
rtc.datetime((tim[0], tim[1], tim[2], 0, tim[3]+8, tim[4], tim[5], 0))


i2c = I2C(0, scl=Pin(9), sda=Pin(8), freq=100000)
addr = i2c.scan()[0]
print(hex(addr))

adxl = adxl345.ADXL345(i2c, addr)



utime.sleep_ms(100)
#print(i2c.readfrom(addr, 2))
now = utime.localtime()
print(now)
filename=f"adxl{now[7]}-{now[3]}-{now[4]}-{now[5]}.txt";
print(filename)
f = open(filename, 'w')
i = 0
led = Pin("LED", Pin.OUT)
led.on()
adxl.data_rate = 0b1011
adxl.range = 0b01
start = time.ticks_ms()
while (i<300):
    #f.write(f"hello {i}\n")
    x, y, z = adxl.acceleration
    f.write(f"{time.ticks_diff(time.ticks_ms(), start)}  {x}, {y}, {z}\n")
    i = i+1;
    utime.sleep_ms(10)
f.close()
led.off()
