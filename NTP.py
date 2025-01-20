from machine import RTC
import socket
import network
import struct
import time

def gettime(addr='uk.pool.ntp.org'):
    REF_TIME_1970 = 2208988800
    client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    data = b'\x1b' + 47 * b'\0'
    client.connect(socket.getaddrinfo(addr, 123)[0][-1])
    client.send(data)
    data, address = client.recvfrom(1024)
    if data:
        t = struct.unpack('!12I', data)[10]
        t -= REF_TIME_1970
        tim = time.gmtime(t)
        rtc = RTC()
        rtc.datetime((tim[0], tim[1], tim[2], 0, tim[3]+8, tim[4], tim[5], 0))        
        client.close()
    return time.localtime()

