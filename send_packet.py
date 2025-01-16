from machine import Pin
from machine import RTC
import utime
import network
import socket
import time
import struct
import sys
import rp2
import _thread
import asyncio

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
    client.connect(socket.getaddrinfo(addr, 123)[0][-1])
    client.send(data)
    data, address = client.recvfrom(1024)
    if data:
        t = struct.unpack('!12I', data)[10]
        t -= REF_TIME_1970
    client.close()
    return time.gmtime(t)

async def sendmsg_task(addr, port):
    import time
    import socket
    global message 
    global pending
    global thread_exit
    
    #while pending == False:
        #print("waiting for netstart")
        #time.sleep(0.5)
    #pending = False
    #client2 = socket.socket()
    #client2.connect(socket.getaddrinfo(addr, port)[0][-1])
    #client2.settimeout(0.75)
    print(thread_exit)
    while not thread_exit:
        if pending == False:
            print("core1 sleep")
            time.sleep(0.25)
            continue
        client2 = socket.socket()
        client2.connect(socket.getaddrinfo(addr, port)[0][-1])
        #client2.settimeout(0.75)   
        pending = False
        print("send ", message)
        client2.send(message)
        if message == "end":
            break
        print("#62")
        data, address = client2.recvfrom(1024)
        #data = client2,recv(10)
        print("#64")
        if data:
            print(data, address)
        client2.close()
    print("thread exits")
    return 1

def sendmsg(addr, port, msg):
    #while pending == False:
        #print("waiting for netstart")
        #time.sleep(0.5)
    #pending = False
    #client2 = socket.socket()
    #client2.connect(socket.getaddrinfo(addr, port)[0][-1])
    #client2.settimeout(0.75)
    #print(thread_exit)
    #while not thread_exit:
    #if pending == False:
    #print("core1 sleep")
    #time.sleep(0.25)
    #continue
    client2 = socket.socket()
    client2.connect(socket.getaddrinfo(addr, port)[0][-1])
        #client2.settimeout(0.75)   
        
    print("send ", msg)
    client2.send(msg)
    if msg == "end":
        return 0
    print("#62")
    data, address = client2.recvfrom(1024)
    #data = client2,recv(10)
    print("#64")
    if data:
        print(data, address)
    client2.close()
    print("thread exits")
    return 1

def gettime():
    tim = reqTime()
    rtc = RTC()
    rtc.datetime((tim[0], tim[1], tim[2], 0, tim[3]+8, tim[4], tim[5], 0))

def main():
    thread_exit = False
    message = ""
    pending = False
    #utime.sleep_ms(500)
    print(connect())
    gettime()


    utime.sleep_ms(100)
    now = utime.localtime()
    print(now)
    filename=f"adxl{now[7]}-{now[3]}-{now[4]}-{now[5]}.txt";

    led = Pin("LED", Pin.OUT)
    led.on()

    #message = "time"
    #pending = True
    #sendmsg_task('192.168.1.66', 5021)
    start = time.ticks_ms()

    #msg_thread = _thread.start_new_thread(sendmsg_task, ('192.168.1.86', 5021))
    time.sleep(1.5)
    led.off()

    #message = "end"
    #pending = True
    #sendmsg_task('192.168.1.66', 5021)
    print("time")
    message = "time"
    pending = True
    sendmsg('192.168.1.86', 5021, message)
    time.sleep(5)

    print("date")
    message = "date"
    pending = True
    sendmsg('192.168.1.86', 5021, message)
    time.sleep(5)

    print("time")
    message = "time"
    pending = True
    sendmsg('192.168.1.86', 5021, message)
    time.sleep(5)

    print("end")
    message = "end"
    pending = True
    time.sleep(10)
    pending = True


    print("main exits")

