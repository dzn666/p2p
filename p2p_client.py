#!/usr/bin/python
#coding:utf-8

from PyQt4 import QtCore,QtGui,Qt
from PyQt4 import uic

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s
try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)


import socket,SocketServer
import time
import threading
import sys,os
import copy

import cv2.cv as cv
import cv2

reload(sys)
sys.setdefaultencoding('utf-8')

lock = threading.Lock()

HOST, PORT = '115.29.227.229', 9999

interval = 15 #heartbeat interval
HEARTBEAT = '0'
GETLIST = '1'
CONNECTWHO = '2'
LOGIN = '3'
LOGOUT = '4'
FAILED = '5'
OPERATESUCCESS = '6'
PICHEAD = '7'
HOLE = '8'
DISCONNECT = '9'
HOLE1 = 'E'
HOLE2 = 'F'

serveState = True
sendState = False
recvState = False
loginState = False
waitting = False

udpHost = ''
udpPort = None

sock = None
sendSock = None
recvSock = None

proc = None

capture = cv.CaptureFromCAM(0) #获取摄像头

sendHost,sendPort = '', 0
recvHost,recvPort = '', 0

class HeartBeat():
    def __init__(self):
        self.th = threading.Thread(target=self.__heatbeat, args=())
        self.th.setDaemon(True)
        self.th.start()
        print("启动心跳检测线程...")


    def __heatbeat(self):
        data = HEARTBEAT
        while True:
            try:
                if loginState == True:
                    socket.setdefaulttimeout(15)
                    sock.sendto(data,(HOST,PORT))
                time.sleep(interval)
            except socket.timeout:
                print("服务器不可到达")
                setServInvalid()
                time.sleep(5)


def setServInvalid():
    global serveState
    lock.acquire()
    serveState = False
    lock.release()

def setServValid():
    global serveState
    lock.acquire()
    serveState = True
    lock.release()

def setLogin(state):
    global loginState
    lock.acquire()
    loginState = state
    lock.release()

def setWaitting(state):
    global waitting
    lock.acquire()
    waitting = state
    lock.release()

def localTime():
    return time.strftime('%Y-%m-%d:%H:%M:%S',time.localtime(time.time()))

def login():
    '''登陆'''
    sock.sendto(LOGIN,(HOST,PORT))
    setWaitting(True)

def setSendHostPort(host,port):
    global sendHost,sendPort
    lock.acquire()
    sendHost = str(host)
    sendPort = int(port)
    lock.release()

def setRecvHostPort(host,port):
    global recvHost,recvPort
    lock.acquire()
    recvHost = str(host)
    recvPort = int(port)
    lock.release()


class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName(_fromUtf8("Form"))
        Form.resize(960, 540)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(Form.sizePolicy().hasHeightForWidth())
        Form.setSizePolicy(sizePolicy)
        self.widget = QtGui.QWidget(Form)
        self.widget.setGeometry(QtCore.QRect(20, 430, 681, 101))
        self.widget.setObjectName(_fromUtf8("widget"))
        self.horizontalLayoutWidget_3 = QtGui.QWidget(self.widget)
        self.horizontalLayoutWidget_3.setGeometry(QtCore.QRect(30, 30, 631, 61))
        self.horizontalLayoutWidget_3.setObjectName(_fromUtf8("horizontalLayoutWidget_3"))
        self.horiButton = QtGui.QHBoxLayout(self.horizontalLayoutWidget_3)
        self.horiButton.setMargin(0)
        self.horiButton.setObjectName(_fromUtf8("horiButton"))
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.shutBtn = QtGui.QPushButton(self.horizontalLayoutWidget_3)
        self.shutBtn.setObjectName(_fromUtf8("shutBtn"))
        self.horizontalLayout.addWidget(self.shutBtn)
        self.viewShutBtn = QtGui.QPushButton(self.horizontalLayoutWidget_3)
        self.viewShutBtn.setObjectName(_fromUtf8("viewShutBtn"))
        self.horizontalLayout.addWidget(self.viewShutBtn)
        self.closeVideoBtn = QtGui.QPushButton(self.horizontalLayoutWidget_3)
        self.closeVideoBtn.setObjectName(_fromUtf8("closeVideoBtn"))
        self.horizontalLayout.addWidget(self.closeVideoBtn)
        self.horiButton.addLayout(self.horizontalLayout)
        self.horizontalLayout_2 = QtGui.QHBoxLayout()
        self.horizontalLayout_2.setObjectName(_fromUtf8("horizontalLayout_2"))
        self.FriendListBtn = QtGui.QPushButton(self.horizontalLayoutWidget_3)
        self.FriendListBtn.setObjectName(_fromUtf8("FriendListBtn"))
        self.horizontalLayout_2.addWidget(self.FriendListBtn)
        self.switchVideoBtn = QtGui.QPushButton(self.horizontalLayoutWidget_3)
        self.switchVideoBtn.setObjectName(_fromUtf8("switchVideoBtn"))
        self.horizontalLayout_2.addWidget(self.switchVideoBtn)
        self.qualitylabel = QtGui.QLabel(self.horizontalLayoutWidget_3)
        self.qualitylabel.setObjectName(_fromUtf8("qualitylabel"))
        self.horizontalLayout_2.addWidget(self.qualitylabel)
        self.qualityBar = QtGui.QSlider(self.horizontalLayoutWidget_3)
        self.qualityBar.setOrientation(QtCore.Qt.Horizontal)
        self.qualityBar.setObjectName(_fromUtf8("qualityBar"))
        self.horizontalLayout_2.addWidget(self.qualityBar)
        self.horiButton.addLayout(self.horizontalLayout_2)
        self.piclabl = QtGui.QLabel(Form)
        self.piclabl.setGeometry(QtCore.QRect(0, 0, 720, 540))
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.piclabl.sizePolicy().hasHeightForWidth())
        self.piclabl.setSizePolicy(sizePolicy)
        self.piclabl.setText(_fromUtf8(""))
        self.piclabl.setObjectName(_fromUtf8("piclabl"))
        self.frdlist = QtGui.QListWidget(Form)
        self.frdlist.setGeometry(QtCore.QRect(740, 20, 211, 441))
        self.frdlist.setAutoFillBackground(True)
        self.frdlist.setObjectName(_fromUtf8("frdlist"))
        self.horizontalLayoutWidget = QtGui.QWidget(Form)
        self.horizontalLayoutWidget.setGeometry(QtCore.QRect(750, 470, 191, 31))
        self.horizontalLayoutWidget.setObjectName(_fromUtf8("horizontalLayoutWidget"))
        self.horizontalLayout_3 = QtGui.QHBoxLayout(self.horizontalLayoutWidget)
        self.horizontalLayout_3.setMargin(0)
        self.horizontalLayout_3.setObjectName(_fromUtf8("horizontalLayout_3"))
        self.refreshBtn = QtGui.QPushButton(self.horizontalLayoutWidget)
        self.refreshBtn.setObjectName(_fromUtf8("refreshBtn"))
        self.horizontalLayout_3.addWidget(self.refreshBtn)
        self.logoutBtn = QtGui.QPushButton(self.horizontalLayoutWidget)
        self.logoutBtn.setObjectName(_fromUtf8("logoutBtn"))
        self.horizontalLayout_3.addWidget(self.logoutBtn)
        self.reconnectBtn = QtGui.QPushButton(self.horizontalLayoutWidget)
        self.reconnectBtn.setObjectName(_fromUtf8("reconnectBtn"))
        self.horizontalLayout_3.addWidget(self.reconnectBtn)
        self.melabel = QtGui.QLabel(Form)
        self.melabel.setGeometry(QtCore.QRect(500, 360, 200, 160))
        self.melabel.setText(_fromUtf8(""))
        self.melabel.setObjectName(_fromUtf8("melabel"))

        self.retranslateUi(Form)
        QtCore.QObject.connect(self.shutBtn, QtCore.SIGNAL(_fromUtf8("clicked()")), Form.show)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        Form.setWindowTitle(_translate("Form", "视频", None))
        self.shutBtn.setText(_translate("Form", "截图", None))
        self.viewShutBtn.setText(_translate("Form", "查看截图", None))
        self.closeVideoBtn.setText(_translate("Form", "关闭视频", None))
        self.FriendListBtn.setText(_translate("Form", "好友列表", None))
        self.switchVideoBtn.setText(_translate("Form", "切换", None))
        self.qualitylabel.setText(_translate("Form", "视频画质", None))
        self.refreshBtn.setText(_translate("Form", "刷新列表", None))
        self.logoutBtn.setText(_translate("Form", "注销", None))
        self.reconnectBtn.setText(_translate("Form", "重新连接", None))


class P2P_Client(QtGui.QWidget):
    def __init__(self,parent=None):
        QtGui.QWidget.__init__(self,parent)
        # self.ui = uic.loadUi('Video.ui',self)
        self.ui = Ui_Form()
        self.ui.setupUi(self)

        QtCore.QObject.connect(self.ui.FriendListBtn, QtCore.SIGNAL(_fromUtf8("clicked()")), self.friendList)
        QtCore.QObject.connect(self.ui.switchVideoBtn,QtCore.SIGNAL(_fromUtf8("clicked()")), self.switchVideo)
        QtCore.QObject.connect(self,QtCore.SIGNAL(_fromUtf8("ShowFramClient()")), self.ShowFramClient)
        QtCore.QObject.connect(self.ui.shutBtn,QtCore.SIGNAL(_fromUtf8("clicked()")), self.shot)
        QtCore.QObject.connect(self.ui.viewShutBtn,QtCore.SIGNAL(_fromUtf8("clicked()")), self.viewShot)
        QtCore.QObject.connect(self.ui.closeVideoBtn,QtCore.SIGNAL(_fromUtf8("clicked()")), self.CloseVideo)
        QtCore.QObject.connect(self.ui.qualityBar,QtCore.SIGNAL(_fromUtf8("clicked()")), self.switchVideo)
        QtCore.QObject.connect(self,QtCore.SIGNAL(_fromUtf8("PicIn()")),self.ShowRecvPic)
        QtCore.QObject.connect(self,QtCore.SIGNAL(_fromUtf8("ParseCmd(QString)")),self.ParseCmd)

        QtCore.QObject.connect(self.ui.refreshBtn, QtCore.SIGNAL(_fromUtf8("clicked()")), self.refresh)
        QtCore.QObject.connect(self,QtCore.SIGNAL(_fromUtf8("refresh(QString)")),self.refresh)
        QtCore.QObject.connect(self.ui.logoutBtn, QtCore.SIGNAL(_fromUtf8("clicked()")), self.logout)
        QtCore.QObject.connect(self.ui.reconnectBtn, QtCore.SIGNAL(_fromUtf8("clicked()")), self.reconnect)

        QtCore.QObject.connect(self.ui.qualityBar,QtCore.SIGNAL(_fromUtf8("valueChanged(int)")),self.ChangeQuality)
        QtCore.QObject.connect(self.ui.frdlist,QtCore.SIGNAL(_fromUtf8("itemDoubleClicked(QListWidgetItem*)")),self.ListWigetDoubleClickedFun)

        self.setWindowFlags(self.windowFlags() & ~QtCore.Qt.WindowMaximizeButtonHint) #隐藏最大化窗口按钮
        #调整控件显示层
        self.ui.piclabl.stackUnder(self.ui.widget)
        self.ui.melabel.stackUnder(self.ui.widget)
        self.ui.piclabl.stackUnder(self.ui.melabel)

        self.resize(960,540)
        self.setMaximumHeight(540)
        self.setMinimumHeight(540)
        self.setMinimumWidth(720)
        self.setMaximumWidth(960)
        self.ui.qualityBar.setRange(1,99)
        self.ui.qualityBar.setValue(10)

        self.cap = capture
        if cv.QueryFrame(self.cap) == None:
            print("无法识别你的摄像头，程序结束")
            sys.exit(0)

        self.FriendShow = True # 窗口主要显示朋友视频状态
        self.lastShotName = None # 最后截图保存的名字
        self.capture_is_avaliable = True # 摄像头是否可用
        self.freq = 5 # 默认视频采集帧数
        self.ItemList = [] # 可视频信息列表
        self.quality = 20
        self.picdata = ''
        self.hb = None
        self.rftime = time.time()

        self.startShowVideo() #开始播放视频线程
        self.image = cv.CreateImage((128,96), 8, 3)


    def outer_init(self):
        login()
        print("登陆中...")
        self.hb = HeartBeat()
        self.refresh()

    def ParseCmd(self,data):
        '''数据包解析'''
        global loginState,recvState,sendState
        global sendSock,recvSock
        data = str(data)
        if len(data) > 1:
            op = data[0]
            if op==PICHEAD:
                self.picdata = data[1:]
                print("recv: %d bit" % len(data)-1)
                recvState = True
                self.emit(QtCore.SIGNAL(_fromUtf8("PicIn()")))
            elif op == GETLIST:
                self.refresh(data.strip()[1:])
            elif op == CONNECTWHO:
                act = str(data[1])
                ip, port = data[2:].split(":")
                print("%s:%s 请求打洞 "%(ip,port))
                self.UDPHole(ip,port)
                setRecvHostPort(ip,port)
                recvState = True
                if act == HOLE1:
                    dat = CONNECTWHO + HOLE2 + str(ip) + ':' + str(port)
                    recvSock,sendSock = sock, recvSock
                else:
                    dat = OPERATESUCCESS + sendHost + ':' + str(sendPort)
                    sendState = True
                if dat:
                    sock.sendto(dat,(HOST,PORT))
            elif op == OPERATESUCCESS:
                ip, port = data[1:].split(":")
                print("打洞成功! %s:%s" % (ip,port))
                setSendHostPort(ip,port)
                sendState = True
                sendSock = recvSock
            else:
                print('==== ', ' ====')
        else:
            if data == HEARTBEAT:
                if not loginState:
                    setLogin(True)
                if not serveState:
                    setServValid()
            elif data == LOGIN:
                if waitting == True:
                    setWaitting(False)
                    print('登陆成功')
                setLogin(True)
            elif data == LOGOUT:
                setLogin(False)
                sendState = False
            elif data == GETLIST: #服务器返回空列表
                self.clearList()
            elif data == HOLE:
                print('收到打洞数据包,打洞成功')
            elif data == DISCONNECT:
                stopTrans()
            else:
                print("unknown exception!:"+data)
                pass

    def UDPHole(self,host,port):
        '''UDP打洞发包'''
        port = int(port)
        try:
            sendsock.sendto(HOLE,(host,port))
            sendsock.sendto(HOLE,(host,port))
            sendsock.sendto(HOLE,(host,port))
            print("向%s:%d发送打洞包数据！"%(host,port))
        except Exception as e:
            print(e)
            print("UDP hole err")
            pass

    def ShowRecvPic(self):
        '''播放椄收到的帧'''
        data = self.picdata
        width,height,channel = 96,128,3

        while len(data)<width*height*channel:
            data += chr(0)
        for i in range(0,width):
	        for j in range(0,height):
		        self.image[i,j] = ord(data[channel*(height*i+j)+0]),ord(data[channel*(height*i+j)+1]),ord(data[channel*(height*i+j)+2])

        if self.FriendShow == True:
            new_img = cv.CreateImage((self.ui.piclabl.width(),self.ui.piclabl.height()),8,3) # 创建一张空图片
            cv.Resize(self.image,new_img,0) # 将img重新设置尺寸
            img = new_img
            # 将opencv的图像转换为QImage
            pic = QtGui.QImage(img.tostring(),img.width,img.height,QtGui.QImage.Format_RGB888).rgbSwapped()
            self.ui.piclabl.setPixmap(QtGui.QPixmap.fromImage(pic)) # 设置图片显示
        else:
            new_img = cv.CreateImage((self.ui.melabel.width(),self.ui.melabel.height()),8,3)
            cv.Resize(self.image,new_img,0)
            img = new_img
            pic = QtGui.QImage(img.tostring(),img.width,img.height,QtGui.QImage.Format_RGB888).rgbSwapped()
            self.ui.melabel.setPixmap(QtGui.QPixmap.fromImage(pic))

    def ListWigetDoubleClickedFun(self,item):
        global sendSock,sock
        text = str(item.text())
        host,port = text.split(':')
        port = int(port)
        dat = CONNECTWHO + HOLE1 + text
        sock.sendto(dat,(HOST,PORT))
        print(text)
        setSendHostPort(host,port)
        sendSock = sock

    def closeEvent(self, QCloseEvent):
        '''重定义点击关闭按钮事件'''
        self.logout(False)
        if sendPort:
            sock.sendto(DISCONNECT,(sendHost,int(sendPort)))
            sock.sendto(DISCONNECT,(sendHost,int(sendPort)))

    def startShowVideo(self):
        '''开始后台控制图片采集时间线程'''
        th = threading.Thread(target=self.ShowVideo,args=())
        th.setDaemon(True)
        th.start()
        print("启动后台采集图像线程...")
        return True

    def ShowVideo(self):
        global loginState
        '''后台Video掌控线程，用于在规定频率内发射一个信号，由相应函数执行显示图片帧和刷新好友列表'''
        while True:
            if time.time()-self.rftime > 3:
                self.rftime = time.time()
                if loginState == True:
                    self.emit(QtCore.SIGNAL(_fromUtf8("refresh(QString)")),_fromUtf8("refresh"))

            if self.capture_is_avaliable == True:
                self.emit(QtCore.SIGNAL(_fromUtf8("ShowFramClient()")))
                time.sleep(1./20)
            else:
                time.sleep(10)

    def ShowFramClient(self):
        '''从本地采集并显示一帧图片,并将图片临时保存至self.img,用于向其他客户端发送,图片数据只在下一帧采集之前有效'''
        img = cv.QueryFrame(self.cap)
        if img == None:
            if self.capture_is_avaliable == True:
                self.capture_is_avaliable = not self.capture_is_avaliable
            print("无法识别你的摄像头设备或不存在,请检查后再操作")
            return
        lock.acquire()
        self.img = img
        lock.release()
        if self.FriendShow == True:
            new_img = cv.CreateImage((self.ui.melabel.width(),self.ui.melabel.height()),8,3)
            cv.Resize(img,new_img,0)
            img = new_img
            pic = QtGui.QImage(img.tostring(),img.width,img.height,QtGui.QImage.Format_RGB888).rgbSwapped()
            self.ui.melabel.setPixmap(QtGui.QPixmap.fromImage(pic))
        else:
            new_img = cv.CreateImage((self.ui.piclabl.width(),self.ui.piclabl.height()),8,3)
            cv.Resize(img,new_img,0)
            img = new_img
            pic = QtGui.QImage(img.tostring(),img.width,img.height,QtGui.QImage.Format_RGB888).rgbSwapped()
            self.ui.piclabl.setPixmap(QtGui.QPixmap.fromImage(pic))

    def CloseVideo(self):
        '''关闭和朋友的视频连接,但本地视频依然进行采集'''
        global transState
        stopTrans()
        lock.acquire()
        self.FriendShow = False
        transState = False
        lock.release()
        print("已断开视频连接")
        if udpPort:
            sendsock.sendto(DISCONNECT,(udpHost,udpPort))
            sendsock.sendto(DISCONNECT,(udpHost,udpPort))
        self.ui.melabel.clear()
        self.ui.piclabl.clear()

    def switchVideo(self):
        '''切换视频显示'''
        self.ui.piclabl.clear()
        self.ui.melabel.clear()
        lock.acquire()
        self.FriendShow = not self.FriendShow
        lock.release()

    def shot(self):
        '''截图'''
        name = './VideoShot-'+localTime()+'.jpg'
        if self.FriendShow == False or transState == False:
        #自我拍照模式
            frame = cv.QueryFrame(self.cap)
            cv.SaveImage(name,frame)
            self.lastShotName = name
            self.viewShot()
        else:
        # 给视频的人拍照模式
            cv.SaveImage(name,self.image)
            self.viewShot()

    def viewShot(self):
        '''查看截图'''
        if self.lastShotName != None:
            im = cv.LoadImageM(self.lastShotName, True)
            cv.ShowImage("截图", im)
            cv.WaitKey()
            cv.DestroyAllWindows()
        else:
            reply = QtGui.QMessageBox.question(self,_fromUtf8('提示'),\
                                           _fromUtf8('你还没有截图哦!'),\
                                           QtGui.QMessageBox.Ok)

    def ChangeQuality(self,value):
        '''改变传输给朋友的视频质量'''
        if value < 10:
            self.ui.qualityBar.setValue(10) # 设置最小值为10
            return
        if value % 10 > 5:
            value = value / 10 + 10
        self.quality = value

    def refresh(self,data='refresh'):
        '''刷新朋友列表'''
        if str(data) == 'refresh':
            sock.sendto(GETLIST,(HOST,PORT))
            return
        else:
            self.clearList()
            if data:
                lst = data.split('#')
                for addr in lst:
                    self.addListItem(str(addr))

    def logout(self, isreply = True):
        '''断开和服务器的连接'''
        global loginState,sendState
        if loginState == True:
            sock.sendto(LOGOUT,(HOST,PORT))
            sendState = False
            setLogin(False)

    def reconnect(self):
        '''重新连接服务器'''
        if loginState == True:
            self.logout()
            login()
            self.clearList()
            self.refresh()
        else:
            login()

    def friendList(self):
        '''显示和关闭朋友列表'''
        if self.width() > 720:
            self.resize(720,540) #720:视频尺寸 960:为视频+列表尺寸
        else:
            self.resize(960,540)

    def addListItem(self,data):
        '''添加一条朋友信息进入列表'''
        item = QtGui.QListWidgetItem(str(data))
        self.ui.frdlist.insertItem(self.ui.frdlist.count(),item)

    def clearList(self):
        '''清除列表信息'''
        i = 0
        while i < self.ui.frdlist.count():
            item = self.ui.frdlist.item(i)
            self.ui.frdlist.takeItem(i)


class ThreadedUDPSendRequestHandler(SocketServer.BaseRequestHandler):
    def handle(self):
        global proc
        data = self.request[0].strip()  # 去除收到数据的末尾空白
        if data:
            proc.ParseCmd(data) # 调用ui界面的函数

ThreadedUDPRecvRequestHandler = ThreadedUDPSendRequestHandler

def startThrdUDPSendServer():
    global sock,proc
    SocketServer.ThreadingUDPServer.allow_reuse_address = True   #地址重用
    server = SocketServer.ThreadingUDPServer((HOST, PORT), ThreadedUDPSendRequestHandler,False)  #创建对象实例,False表示不绑定本地端口
    server.request_queue_size = 20      # 等待队列
    server.max_packet_size = 8192*200   # 缓冲区大小
    sock = server.socket                # 把sock保存为全局变量，供其他线程使用
    server.daemon_threads = True        # 设置服务当程序退出时，线程一起退出
    proc.outer_init()                   # 调用proc里面的out_init()函数，登陆服务器
    server_thread = threading.Thread(target=server.serve_forever)  # run
    # Exit the server thread when the main thread terminates
    server_thread.daemon = True
    server_thread.start()

def startThrdUDPRecvServer():
    global proc,recvSock,recvState
    SocketServer.ThreadingUDPServer.allow_reuse_address = True   #地址重用
    server = SocketServer.ThreadingUDPServer((HOST, PORT), ThreadedUDPRecvRequestHandler,False)  #创建对象实例,False表示不绑定本地端口
    server.request_queue_size = 20      # 等待队列
    server.max_packet_size = 8192*200   # 缓冲区大小
    recvSock = server.socket                # 把recvSock保存为全局变量，供其他线程使用
    server.daemon_threads = True        # 设置服务当程序退出时，线程一起退出
    server_thread = threading.Thread(target=server.serve_forever)  # run
    server_thread.daemon = True
    server_thread.start()
    recvState = True

def startSendFrameThrd():
    t = threading.Thread(target=SendFrame,args=())
    t.setDaemon(True)
    t.start()
    print("启动后台视频发送线程...")

def SendFrame():
    # width = int(6.40 * self.quality)
    # height = int(4.80 * self.quality)
    global sendPort,sendHost,capture
    width, height = 128, 96
    while True:
        if sendState == True and loginState == True:
            if not sendPort and not sendHost:
                continue
            new_img = cv.CreateImage((width,height),8,3)
            img = cv.QueryFrame(capture)
            cv.Resize(img,new_img,0)
            pic = PICHEAD + new_img.tostring()
            sendsock.sendto(pic,(sendHost,sendPort))
            print('send %d bit' % len(pic)-1)
            time.sleep(1./8)
        else:
            time.sleep(1)


def main():
    global proc
    app = QtGui.QApplication(sys.argv)
    proc = P2P_Client()
    proc.show()     # 显示ui界面
    startThrdUDPSendServer()
    startSendFrameThrd()
    startThrdUDPRecvServer()
    sys.exit(app.exec_())   # 进入界面循环

if __name__=='__main__':
    main()
