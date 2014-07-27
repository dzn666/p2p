#!/usr/bin/python
#coding:utf-8

import SocketServer
import socket
import fcntl
import struct
import time
import threading

def get_ip_addr(ifname='eth0'):
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    return socket.inet_ntoa(fcntl.ioctl( s.fileno(),0x8915,struct.pack('256s', ifname))[20:24])

interval = 7
HEARTBEAT   = '0'
GETLIST     = '1'
CONNECTWHO  = '2'
LOGIN       = '3'
LOGOUT      = '4'
FAILED      = '5'
OPERATESUCCESS = '6'
PICHEAD = '7'
TRANSMIT = '-'

LIST = [] # items' format: ((ip,port),socket,last_time))
lock = threading.Lock()

class ThreadedUDPRequestHandler(SocketServer.BaseRequestHandler):
    def handle(self):
        data = self.request[0].strip()
        sock = self.request[1]
        ip, port = self.client_address
	if len(data)<40:
            print ip,':',port,'->  ',data,'  <-'

        if data[0] == TRANSMIT:
            data = data[1:]
            if len(data)<40:
                return
            for i in range(40):
                if data[i] == '#':
                    addr,dat  = data[:i],data[i+1:]
		    print('recv transmit packet from %s:%s -> length: %d'%(ip,str(port),len(dat)))
                    dsthost,dstport = addr.split(':')
		    dsthost = str(dsthost)
		    dstport = int(dstport)
		    dat = PICHEAD + str(ip) + ':' + str(port) + '#' + dat
		    sock.sendto(dat,(dsthost,dstport))
                    break
        elif data[0] == HEARTBEAT:
            HeartBeat(((ip,port),sock))
        elif data[0] == GETLIST:
            lst = GetList(ip,port)
            lst = GETLIST + str(lst)
            sock.sendto(lst,(ip,port))
        elif data[0] == CONNECTWHO:
            host,port1 = str(data[1:]).split(':')
            port1 = int(port1)
            dat = CONNECTWHO + str(ip) + ':' + str(port)
            print('connect to ')
            sock.sendto(dat,(host,port1))
        elif data[0] == LOGIN:
            if Login(((ip,port),sock)):
                sock.sendto(LOGIN,(ip,port))
            else:
                sock.sendto(FAILED,(ip,port))
        elif data[0] == LOGOUT:
            Logout(ip,port)
            sock.sendto(LOGOUT,(ip,port))
        elif data[0] == OPERATESUCCESS:
            dstip, dstport = data[1:].strip().split(':')
            OperateSuccessTo((ip,port),(dstip,int(dstport)))
        else:
            pass


class ThreadedUDPServer(SocketServer.ThreadingMixIn, SocketServer.UDPServer):
    pass


def Login(((ip,port),sock)):
    for (_ip,_port),_socket,_last_time in LIST:
        if ip==_ip:
            if port==_port:
                return True
            else:
                pass
    tm = time.time()
    lock.acquire()
    LIST.append(((ip,port),sock,tm))
    lock.release()
    return True

def Logout(ip,port):
    Remove(ip,port)

def OperateSuccessTo((ip,port),(dstip,dstport)):
    for (_ip,_port),_socket,_last_time in LIST:
        if dstip == _ip and dstport == _port:
            dat = OPERATESUCCESS + str(ip) + ':' + str(port)
            _socket.sendto(dat,(dstip,int(dstport)))

def Remove(ip,port):
    lock.acquire()
    for (_ip,_port),_socket,_last_time in LIST:
        if ip==_ip and port == _port:
            print 'Remove: ',_ip,':',_port
            LIST.remove(((_ip,_port),_socket,_last_time))
            break
    lock.release()

def UpdateTime((ip,port), socket):
    lock.acquire()
    tm = time.time()
    for (_ip,_port),_socket,_last_time in LIST:
        if ip==_ip and port==_port:
            if socket==_socket:
                LIST.remove(((_ip,_port),_socket,_last_time))
                LIST.append(((_ip,_port), _socket, tm))
                break
            else:
                LIST.remove(((_ip,_port),_socket,_last_time))
                LIST.append(((_ip,_port), socket, tm))
                break
    lock.release()

def GetList(ip,port):
    lst = ''
    for (_ip,_port),_socket,_last_time in LIST:
        if _ip == ip and _port == port:
            continue
        lst += str(_ip)+':'+str(_port)+'#'
    if len(lst) > 0:
        lst = lst[:-1]
    return lst

def ConnectTo((ip,port),(dst_ip,dst_port)):
    for (_ip,_port),_socket,_last_time in LIST:
        if dst_ip==_ip and dst_port==int(_port):
            print('connectto')
            data = CONNECTWHO + str(ip) + ':' + str(port)
            _socket.sendto(data, (dst_ip,int(dst_port)))
            return True
        else:
            return False

def HeartBeat(((ip,port),socket)):
    UpdateTime((ip,port),socket)
    SendHeartBeat(((ip,port),socket))

def SendHeartBeat(((ip,port),sock)):
    if ip==None or port==None or sock==None:
        UpdateTime((ip,port),sock)
        return
    try:
        sock.sendto(HEARTBEAT,(ip,port))
    except:
        Remove(ip,port)


def ListCheck():
    try:
        while True:
            for (_ip,_port),_socket,_last_time in LIST:
                if time.time() - _last_time > 15:
                    SendHeartBeat(((_ip,_port),_socket))
                if time.time() - _last_time > 28:
                    Remove(_ip,_port)
            time.sleep(interval)
    except KeyboardInterrupt:
        pass

def StartListCheckThrd():
    th = threading.Thread(target=ListCheck(),args=())
    th.setName('ListCheckDaemon')
    th.setDaemon(True)
    th.start()

def StartUDPServerThrd():
    HOST, PORT = get_ip_addr('eth1'), 9999
    ThreadedUDPServer.allow_reuse_address = True
    server = ThreadedUDPServer((HOST, PORT), ThreadedUDPRequestHandler)
    server.request_queue_size = 20   # max request queue number
    server.max_packet_size = 8192 * 20
    try:
        server_thread = threading.Thread(target=server.serve_forever)
        # Exit the server thread when the main thread terminates
        server_thread.daemon = True
        server_thread.start()
    except KeyboardInterrupt:
        print(" UDPServer has stopped!  Bye!")
        exit(0)

def main():
    StartUDPServerThrd()  # must start the UDPServerThread first!
    StartListCheckThrd()


if __name__ == "__main__":
    main()
