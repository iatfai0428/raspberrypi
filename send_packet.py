from machine import Pin, RTC, Timer
import utime
import network
import socket
import usocket
import time
import struct
import sys
import rp2
import _thread
import asyncio
import wlan_connect

def sendmsg_task(addr, port):
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
        client2.connect(usocket.getaddrinfo(addr, port)[0][-1])
        
        client2.send(msg)
        data, address = client2.recvfrom(1024)
        if data:
            print(data, address)
        client2.close()
    print("thread exits")
    return 1

def tick(timer):
    global led
    led.toggle()
    
led = Pin("LED", Pin.OUT)
lock = _thread.allocate_lock()
thread_exit = False
message = ""

def main(addr):
    global led, lock, message, thread_exit
    #pending = False
    
    time.sleep(0.5)
    led.on()
    
    now = utime.localtime()
    filename = f"adxl{now[7]}-{now[3]}-{now[4]}-{now[5]}.txt";

    start = time.ticks_ms()
    
    lock.acquire()
    msg_thread = _thread.start_new_thread(sendmsg_task, (addr, 5021))
    time.sleep(1.5)
    tim = Timer()
    tim.init(freq=3, mode=Timer.PERIODIC, callback=tick) 

    message = "time"
    lock.release()
    time.sleep(0.5)
    print("main [", message, "]")
    print(lock.acquire(1,1), "wait result")
   
    time.sleep(5)

    print("date")
    message = "date"
    lock.release()
    time.sleep(0.5)
    lock.acquire()
    time.sleep(5)

    print("time")
    message = "time"
    lock.release()
    time.sleep(0.5)
    lock.acquire()
    time.sleep(5)

    print("end")
    message = ""
    time.sleep(10)

    thread_exit = True
    lock.release()

    print("main exits")
    tim.deinit()
    led.off()
    
ip = wlan_connect.connect('Wifi-Choice', 'Ch-5057289')
main('isaac-ally')


