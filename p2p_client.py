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


import socket
import time
import threading
import sys,os
import copy

import cv2.cv as cv
import cv2

from PIL import Image

reload(sys)
sys.setdefaultencoding('utf-8')

lock = threading.Lock()

HOST, PORT = '115.29.227.229', 9999
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

interval = 15  #heartbeat interval
HEARTBEAT   = '0'
GETLIST     = '1'
CONNECTWHO  = '2'
LOGIN       = '3'
LOGOUT      = '4'
FAILED      = '5'
OPERATESUCCESS = '6'
PICHEAD     = '7'
HOLE = '8'
DISCONNECT = '9'
TRANSMIT = '-'

serveState = True
transState = False
loginState = False
waitting = False

udpHost = ''
udpPort = None


def Compress(content):
    import StringIO,gzip
    buf = StringIO.StringIO()
    zfile = gzip.GzipFile(mode='wb', compresslevel=9, fileobj=buf)
    zfile.write(content)
    zfile.close()
    return buf.getvalue()

def Decompress(content):
    import StringIO,gzip
    inbuf = StringIO.StringIO(content)
    f = gzip.GzipFile(mode='rb', fileobj=inbuf)
    dat = f.read()
    f.close()
    return dat


class HeartBeat():
    def __init__(self):
        self.th = threading.Thread(target=self.__heatbeat, args=())
        self.th.setDaemon(True)
        self.th.setName('heatbeat')
        self.th.start()
        print("启动心跳检测线程...")


    def __heatbeat(self):
        data = HEARTBEAT
        while True:
            try:
                if loginState == True:
                    '''here heatbeat 67'''
                    socket.setdefaulttimeout(15)
                    sock.sendto(data,(HOST,PORT))
                time.sleep(interval)
            except KeyboardInterrupt:
                pass
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

def stopTrans():
    global transState
    lock.acquire()
    transState = False
    lock.release()

def startTrans():
    global transState
    lock.acquire()
    transState = True
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

def setUdpHostPort(host,port):
    global udpPort,udpHost
    lock.acquire()
    udpHost = str(host)
    udpPort = int(port)
    lock.release()

def setTransmitPort():
    global udpHost,udpPort
    lock.acquire()
    udpHost = '115.29.227.229'
    udpPort = int(9988)
    lock.release()

trHost = ''
trPort = 0
def savedst(host,port):
    global trHost,trPort
    lock.acquire()
    trHost = str(host)
    trPort = int(port)
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

        # self.center()  #窗口居中显
        login()    #登陆

        self.cap = cv.CaptureFromCAM(0)   #获取摄像头
        if cv.QueryFrame(self.cap) == None:
            print("无法识别你的摄像头，程序结束")
            sys.exit(0)

        self.FriendShow = True    #窗口主要显示朋友视频状态
        self.lastShotName = None    #最后截图保存的名字
        self.capture_is_avaliable = True  #摄像头是否可用
        self.freq = 10    #默认视频采集帧数
        self.pos = 0
        self.ItemList = []  #可视频信息列表
        self.quality = 10
        self.picdata = ''

        self.rftime = time.time()

        if self.startShowVideo():   #开始播放视频线程
            if self.startMonitorThrd():  #开始从服务器接收数据线程
                login()
                print("登陆中...")
            self.hb = HeartBeat()   #心跳包，用于检测是否和服务器保持连接
            if self.capture_is_avaliable:
                self.startSendFrameThrd()  #开始视频帧的发送线程
            self.refresh()  #刷新列表

        self.recv_pic = ''
        self.picflag = [False,False,False]
        self.pic = ['','','']


    def startMonitorThrd(self):
        t = threading.Thread(target=self.MonitorRecv,args=())
        t.setDaemon(True)
        t.setName("MonitorRecv")
        t.start()
        print("启动后台接收数据线程...")
        return True

    def MonitorRecv(self):
        '''后台线程，用于收取数据'''
        while True:
            data = sock.recv(1024*1024*8)
            data = data.strip()
            if data[0] == PICHEAD:
                # data = PICHEAD + Decompress(data[1:])
                pass
            if data:
                self.emit(QtCore.SIGNAL(_fromUtf8("ParseCmd(QString)")),_fromUtf8(data))

    def startSendFrameThrd(self):
        t = threading.Thread(target=self.SendFrame,args=())
        t.setDaemon(True)
        t.setName("SendFrame")
        t.start()
        print("启动后台视频发送线程...")

    def SendFrame(self):
        self.freq = 0.5   #频率调为2s一帧
        self.quality = 20  #####
        times = 0
        while True:
            try:
                if transState == True and loginState == True:
                    if udpPort and udpHost:
                        pass
                    else:
                        print('line 357 ')
                        continue
                    lock.acquire()
                    width = int(6.40 * self.quality)
                    height = int(4.80 * self.quality)
                    new_img = cv.CreateImage((width,height),8,3)
                    cv.Resize(self.img,new_img,0)
                    lock.release()
                    data = copy.copy(new_img.tostring())  # length = 36864
                    # data = Compress(data)
                    # pic = PICHEAD + data
                    # sock.sendto(pic,(udpHost,udpPort))
                    # '''
                    length = len(data)
                    pices_len = length/3
                    # pic1 = PICHEAD + '0' + data[:pices_len]
                    # pic2 = PICHEAD + '1' + data[pices_len:pices_len*2]
                    # pic3 = PICHEAD + '2' + data[pices_len*2:]
                    pic1 = str(udpHost) + ':' + str(udpPort) + '#' + PICHEAD + '0' + data[:pices_len]
                    pic2 = str(udpHost) + ':' + str(udpPort) + '#' +  PICHEAD + '1' + data[pices_len:pices_len*2]
                    pic3 = str(udpHost) + ':' + str(udpPort) + '#' +  PICHEAD + '2' + data[pices_len*2:]

                    sock.sendto(pic1,(udpHost,udpPort))
                    sock.sendto(pic2,(udpHost,udpPort))
                    sock.sendto(pic3,(udpHost,udpPort))
                    # '''
                    print('send %d bit' % len(data))
                    time.sleep(1./self.freq)
                else:
                    time.sleep(3)
            except Exception as e:
                print(e)

    def ParseCmd(self,data):
        '''数据包解析'''
        global loginState
        data = str(data)
        if len(data) == 1:
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
                stopTrans()
            elif data == GETLIST: #服务器返回空列表
                self.clearList()
            elif data == HOLE:
                print('收到打洞数据包')
            elif data == DISCONNECT:
                stopTrans()
            else:
                print("unknown exception!:"+data)
                pass
        else:
            op = data[0]
            if op==PICHEAD:
                print("recv: %d bit" %len(data))
                self.picdata = data[1:]
                if not transState:
                    startTrans()
                self.emit(QtCore.SIGNAL(_fromUtf8("PicIn()")))
            elif op == GETLIST:
                self.refresh(data.strip()[1:])
            elif op == CONNECTWHO:
                ip, port = data[1:].split(":")
                print("%s:%s 请求打洞  "%(ip,port))
                self.UDPHole(ip,int(port))
            elif op == OPERATESUCCESS:
                ip, port = data[1:].split(":")
                print("打洞成功! %s:%s" % (ip,port))
                # setUdpHostPort(ip,port)
                savedst(ip,port)
                setTransmitPort()   # ///////////////////////
                startTrans()
            else:
                print('==== ', ' ====')

    def UDPHole(self,host,port):
        '''UDP打洞发包'''
        try:
            sock.sendto(HOLE,(host,port))
            sock.sendto(HOLE,(host,port))
            sock.sendto(HOLE,(host,port))
            sock.sendto(HOLE,(host,port))
            print("向%s:%d发送打洞包数据！"%(host,port))
            dat = OPERATESUCCESS + str(host) + ':' + str(port)
            sock.sendto(dat,(HOST,PORT))
            # setUdpHostPort(host,port)
            savedst(host,port)
            setTransmitPort()   # ///////////////////////
        except Exception as e:
            print(e)
            print("UDP hole err")
            pass

    def getPicSize(self,data):
        '''算出最接近但不大于真实接收到图片的长度'''
        length = len(data) / 3
        if length == 0: return (0,0)
        h = 48
        while h < 481:
            if h*h*4/3 - length > 0:
                return ((h-1)*4/3,h-1)
            h += 1
        return (0,0)

    def ShowRecvPic(self):
        '''播放椄收到的帧'''
        idx = int(self.picdata[0])
        data = str(self.picdata[1:])
        self.pic[idx] = data
        self.picflag[idx] = True

        if self.picflag[0] and self.picflag[1] and self.picflag[2]:
            self.picflag[0] = self.picflag[1] = self.picflag[2] = False
            data = self.pic[0] + self.pic[1] + self.pic[2]
            self.pic = ['','','']
            pass
        else:
            return
        if len(data) != 36864:
            return
        #利用收到的图片数据创建一张img
        image = cv.CreateMatHeader(1, len(data), cv.CV_8UC1)
        cv.SetData(image, data, len(data))
        img = cv.DecodeImageM(image, cv.CV_LOAD_IMAGE_COLOR)

        if self.FriendShow == True:
            new_img = cv.CreateImage((self.ui.piclabl.width(),self.ui.piclabl.height()),8,3)  # 创建一张空图片
            cv.Resize(img,new_img,0)  # 将img重新设置尺寸
            img = new_img
            # 将opencv的图像转换为QImage
            pic = QtGui.QImage(img.tostring(),img.width,img.height,QtGui.QImage.Format_RGB888).rgbSwapped()
            self.ui.piclabl.setPixmap(QtGui.QPixmap.fromImage(pic))  # 设置图片显示
        else:
            new_img = cv.CreateImage((self.ui.melabel.width(),self.ui.melabel.height()),8,3)
            cv.Resize(img,new_img,0)
            img = new_img
            pic = QtGui.QImage(img.tostring(),img.width,img.height,QtGui.QImage.Format_RGB888).rgbSwapped()
            self.ui.melabel.setPixmap(QtGui.QPixmap.fromImage(pic))


    def center(self):
        screen = QtGui.QDesktopWidget().screenGeometry()
        size = self.geometry()
        self.move((screen.width()-size.width())/2, (screen.height()-size.height())/2)


    def ListWigetDoubleClickedFun(self,item):
        global loginState,transState
        if loginState == False:
            QtGui.QMessageBox.question(self,_fromUtf8('提示'),\
                                           _fromUtf8('你还没有登陆!'),\
                                           QtGui.QMessageBox.Ok)
            return
        data = str(item.text())
        host,port = data.split(':')
        port = int(port)
        stopTrans()
        dat = CONNECTWHO + host + ':' + str(port)
        # sock.sendto(dat,(HOST,PORT))

    def closeEvent(self, QCloseEvent):
        '''重定义点击关闭按钮事件'''
        # reply = QtGui.QMessageBox.question(self,_fromUtf8('提示'),\
        #                                    _fromUtf8('你真的要退出?'),\
        #                                    QtGui.QMessageBox.Yes,QtGui.QMessageBox.No)
        # if reply == QtGui.QMessageBox.Yes:
        if True:
            self.logout(False)
            QCloseEvent.accept()
            sock.sendto(DISCONNECT,(udpHost,int(udpPort)))
            sock.sendto(DISCONNECT,(udpHost,int(udpPort)))
        else:
            QCloseEvent.ignore()

    def startShowVideo(self):
        '''开始后台控制图片采集时间线程'''
        th = threading.Thread(target=self.ShowVideo,args=())
        th.setName('ShowVideo')
        th.setDaemon(True)
        th.start()
        print("启动后台采集图像线程...")
        return True

    def ShowVideo(self):
        global loginState
        '''后台Video掌控线程，用于在规定频率内发射一个信号，由相应函数执行显示图片帧和刷新好友列表'''
        while True:
            if time.time()-self.rftime > 10:
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
        if transState == False:
            return
        reply = QtGui.QMessageBox.question(self,_fromUtf8('提示'),\
                                           _fromUtf8('你真的要关闭视频对话?'),\
                                           QtGui.QMessageBox.Yes,QtGui.QMessageBox.No)
        if reply == QtGui.QMessageBox.Yes:
            pass
        else:
            return
        stopTrans()
        lock.acquire()
        self.FriendShow = False
        transState = False
        lock.release()
        print("已断开视频连接")
        sock.sendto(DISCONNECT,(udpHost,udpPort))
        sock.sendto(DISCONNECT,(udpHost,udpPort))
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
        if self.FriendShow == False:
        #自我拍照模式
            frame = cv.QueryFrame(self.cap)
            cv.SaveImage(name,frame)
            self.lastShotName = name
        else:
        # 给视频的人拍照模式
            if transState == False:
                reply = QtGui.QMessageBox.question(self,_fromUtf8('提示'),\
                                           _fromUtf8('截图区域没有图像哦!请点击“切换”再截图!'),\
                                           QtGui.QMessageBox.Ok)
                return
            else:
                pass
        reply = QtGui.QMessageBox.question(self,_fromUtf8('提示'),\
                                           _fromUtf8('截图成功,是否立即查看?'),\
                                           QtGui.QMessageBox.Yes,QtGui.QMessageBox.No)
        if reply == QtGui.QMessageBox.Yes:
            self.viewShot()
        else:
            return

    def viewShot(self):
        '''查看截图'''
        if self.lastShotName != None:
            im = cv.LoadImageM(self.lastShotName, True)
            cv.ShowImage("camera", im)
            cv.WaitKey()
            cv.DestroyAllWindows()
            # os.popen4('python PicDlg.py '+self.lastShotName[2:])
        else:
            reply = QtGui.QMessageBox.question(self,_fromUtf8('提示'),\
                                           _fromUtf8('你还没有截图哦!'),\
                                           QtGui.QMessageBox.Ok)
            return

    def ChangeQuality(self,value):
        '''改变传输给朋友的视频质量'''
        if value < 10:
            self.ui.qualityBar.setValue(10)  # 设置最小值为10
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
        global loginState
        if loginState == True:
            if isreply:
                reply = QtGui.QMessageBox.question(self,_fromUtf8('提示'),\
                                               _fromUtf8('你真的要注销吗?'),\
                                               QtGui.QMessageBox.Yes,QtGui.QMessageBox.No)
                if reply == QtGui.QMessageBox.Yes:
                    pass
                else:
                    return
            sock.sendto(LOGOUT,(HOST,PORT))
            stopTrans()
            setLogin(False)
        else:
            if not isreply:
                QtGui.QMessageBox.question(self,_fromUtf8("提示"),\
                                       _fromUtf8("你还没有登陆"),\
                                       QtGui.QMessageBox.Ok)

    def reconnect(self):
        '''重新连接服务器'''
        if loginState == True:
            reply = QtGui.QMessageBox.question(self,_fromUtf8('提示'),\
                                               _fromUtf8('你已登陆,真的要重新连接吗?'),\
                                               QtGui.QMessageBox.Yes,QtGui.QMessageBox.No)
            if reply == QtGui.QMessageBox.Yes:
                pass
            else:
                return
            self.logout()
            login()
            self.clearList()
            self.refresh()
        else:
            login()

    def friendList(self):
        '''显示和关闭朋友列表'''
        if self.width() > 720:
            self.resize(720,540)  #720:视频尺寸 960:为视频+列表尺寸
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


def main():
    app = QtGui.QApplication(sys.argv)
    p = P2P_Client()
    p.show()
    sys.exit(app.exec_())

if __name__=='__main__':
    main()
