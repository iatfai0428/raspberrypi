from machine import Pin, RTC, Timer
import utime
import network
import socket
import time
import struct
import sys
import rp2
import _thread
import asyncio

def connect(ssid, passwd):
    #Connect WLAN
    global led
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    #wlan.connect("Wifi-Choice-Public", "065057289")
    wlan.connect(ssid, passwd)
    while wlan.isconnected() == False:
        print('Waiting for connection...')
        led.toggle()
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

def sendmsg_task(addr, port):
    #import time
    #import socket
    global message, thread_exit, lock

    print("thread_exit", thread_exit)
    while not thread_exit:
        print("send waiting...")
        wait_counter = 0
        while not lock.acquire(1, 0.001):
            if thread_exit:
                break
            wait_counter += 1
        lock.release()
        if thread_exit:
            print("break send loop")
            break
        if message == "":
            print("empty loop again")
            continue
        
        print(f"send wait{wait_counter} ended", message)
        msg = message
        message = ""
        client2 = socket.socket()
        client2.connect(socket.getaddrinfo(addr, port)[0][-1])
        
        #client2.settimeout(0.75)   
        #pending = False
        
        client2.send(msg)
        data, address = client2.recvfrom(1024)
        if data:
            print(data, address)
        client2.close()
    print("thread exits")
    return 1

def sendmsg(addr, port, msg):
    client = socket.socket()
    client.connect(socket.getaddrinfo(addr, port)[0][-1])   
        
    print("send ", msg)
    client.send(msg)
    if msg == "end":
        return 0
    data, address = client.recvfrom(1024)
    if data:
        print(data, address)
    client.close()
    return 1

def gettime():
    tim = reqTime()
    rtc = RTC()
    rtc.datetime((tim[0], tim[1], tim[2], 0, tim[3]+8, tim[4], tim[5], 0))

def tick(timer):
    global led
    led.toggle()
    
led = Pin("LED", Pin.OUT)
lock = _thread.allocate_lock()
thread_exit = False
message = ""

def main(ssid, passwd, addr):
    global led, lock, message, thread_exit
    #pending = False
    
    time.sleep(0.5)
    led.on()
    #utime.sleep_ms(500)
    print(connect(ssid, passwd))
    gettime()

    utime.sleep_ms(100)
    now = utime.localtime()
    print(now)
    filename=f"adxl{now[7]}-{now[3]}-{now[4]}-{now[5]}.txt";

    
   

    #message = "time"
    #pending = True
    #sendmsg_task('192.168.1.66', 5021)
    start = time.ticks_ms()
    
    lock.acquire()
    msg_thread = _thread.start_new_thread(sendmsg_task, (addr, 5021))
    time.sleep(1.5)
    tim = Timer()
    tim.init(freq=3, mode=Timer.PERIODIC, callback=tick) 

    #message = "end"
    #pending = True
    #sendmsg_task(addr, 5021)
    

    message = "time"
    lock.release()
    time.sleep(0.5)
    print("main [", message, "]")
    print(lock.acquire(1,1), "wait result")
    #pending = True
    
    #sendmsg(addr, 5021, message)
    time.sleep(5)

    print("date")
    message = "date"
    lock.release()
    #pending = True
    time.sleep(0.5)
    lock.acquire()
    #sendmsg(addr, 5021, message)
    time.sleep(5)

    print("time")
    message = "time"
    lock.release()
    time.sleep(0.5)
    lock.acquire()
    #pending = True
    #sendmsg(addr, 5021, message)
    time.sleep(5)

    print("end")
    message = ""
    #pending = True
    time.sleep(10)
    #pending = True

    thread_exit = True
    lock.release()

    print("main exits")
    tim.deinit()
    led.off()
