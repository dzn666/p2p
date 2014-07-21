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

import sys,os


class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName(_fromUtf8("Dialog"))
        Dialog.resize(640, 480)
        self.label = QtGui.QLabel(Dialog)
        self.label.setGeometry(QtCore.QRect(0, 0, 640, 480))
        self.label.setText(_fromUtf8(""))
        self.label.setObjectName(_fromUtf8("label"))

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(_translate("Dialog", "Dialog", None))


class PicShowDlg(QtGui.QDialog):
    def __init__(self,name,path=os.getcwd(),parent=None):
        QtGui.QDialog.__init__(self,parent)
        #self.dlg = uic.loadUi('PicShow.ui',self)
        self.path = path
        self.name = name
        self.dlg = Ui_Dialog()
        self.dlg.setupUi(self)
        self.setWindowTitle(_fromUtf8(path+'/'+name))
        self.showPic()

    def showPic(self):
        im = QtGui.QImage()
        if im.load(self.path+'/'+self.name):
            self.dlg.label.setPixmap(QtGui.QPixmap.fromImage(im))

if __name__=='__main__':
    app = QtGui.QApplication(None)
    name = sys.argv[1]
    p = PicShowDlg(name)
    p.show()
    sys.exit(app.exec_())
