# -*- coding: utf-8 -*-
import PyQt4, PyQt4.QtGui,  sys
from PyQt4 import QtCore,  QtGui
#from PyQt4.QtCore import pyqtSignature
from PyQt4.QtGui import QMainWindow, QApplication, QCursor

from Ui_main import Ui_MainWindow


from PyQt4.Qt import *

import xml.dom.minidom
import urllib


class MainWindow(QMainWindow, Ui_MainWindow):
    """
    Class documentation goes here.
    """
    flag = 0
    def __init__(self, parent=None):
        """
        Constructor
        
        @param parent reference to the parent widget (QWidget)
        """
        QMainWindow.__init__(self, parent)
        self.setupUi(self)
        
        self.URL = ""
        self.Msg = ""
        self.ImageUrl = ""
        self.readUrlInfo()
        
        # Set TImer environment
        self.timer = QtCore.QTimer(self)
        self.timer.timeout.connect(self.RecieveDataFromRS)
        self.timer.start(1000)

        self.Url_Edit.hide()
        
     #   sizeGrip=QtGui.QSizeGrip(self)
        self.setWindowFlags(Qt.FramelessWindowHint|Qt.WindowStaysOnTopHint)
        self.setWindowState(QtCore.Qt.WindowMaximized)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        self.setMouseTracking(True);

    def mousePressEvent(self, event):
        super(MainWindow, self).mousePressEvent(event)
        if event.button() == QtCore.Qt.LeftButton:
    #        self.Url_Edit.show()
            self.rdragx = event.x()
            self.rdragy = event.y() 
            self.currentx = self.width()
            self.currenty = self.height()
            self.leftClick = True
            self.dragPos=event.globalPos()-self.frameGeometry().topLeft()
            event.accept()
    
    def mouseMoveEvent(self, event):
        super(MainWindow, self).mouseMoveEvent(event)
        self.diff = self.frameGeometry().bottomRight() - event.globalPos()
        if self.diff.x() < 30:
            QApplication.setOverrideCursor(QCursor(Qt.SizeHorCursor))
        elif self.diff.y() < 30:
            QApplication.setOverrideCursor(QCursor(Qt.SizeVerCursor))
        
        if (self.diff.x() < 30 ) and ( self.diff.y() < 30):
            QApplication.setOverrideCursor(QCursor(Qt.SizeFDiagCursor)) 
        
        if self.leftClick == True:
            if (self.diff.x() < 30 )|( self.diff.y() < 30):
                
                x = max(self.minimumWidth(), 
                    self.currentx + event.x() - self.rdragx)
                y = max(self.minimumHeight(), 
                    self.currenty + event.y() - self.rdragy)
                self.resize(x, y)
            else:
                self.move(event.globalPos()-self.dragPos)
                event.accept()
 
    def mouseReleaseEvent(self, event):
        super(MainWindow, self).mouseReleaseEvent(event)
        QApplication.setOverrideCursor(QCursor(Qt.ArrowCursor))
        if event.button() == QtCore.Qt.LeftButton:
             self.leftClick = False

    def keyPressEvent(self, event):
        if event.key() == QtCore.Qt.Key_Return or event.key() == QtCore.Qt.Key_Enter:
            self.Url_Edit.hide()
        elif event.key() == QtCore.Qt.Key_Home:
            self.Url_Edit.show()	        
           
    # Get the Url address from config.ini file
    
    def readUrlInfo(self):
        import ConfigParser
        p = ConfigParser.ConfigParser()
        p.readfp (open('config.ini'))
        self.URL = p.items('app_config')[0][1]
   
    def downloadData(self):
        downloadedData = urllib.urlopen(self.URL)
        XMLData = xml.dom.minidom.parse(downloadedData)
        copy = XMLData.getElementsByTagName("copy") 
        for item in copy:
            self.Msg =  item.childNodes[0].data
            break
        imageURL = XMLData.getElementsByTagName("imageURL")
        for item in imageURL:
           self.ImageUrl = item.childNodes[0].data
           break
        
    def on_req_done(self, error):
        if not error:
            print "Success"
            print self.http.readAll()
        else:
            print "Error"
    
    
    def RecieveDataFromRS(self):
        if self.timer:
            self.timer.stop()
        if(self.URL != ""):
            self.downloadData()   
            self.DisplyPhoto(self.ImageUrl) 
            self.Message_Text.setText(self.Msg)
        self.timer.start(1000) 

    def DisplyPhoto(self, ImageUrl):
        # url = 'http://www.google.com/images/srpr/logo1w.png'
        if(ImageUrl != "") :      
            data = urllib.urlopen(ImageUrl).read()
            image = QtGui.QImage()
            image.loadFromData(data)
            self.Image_View.setPixmap(QtGui.QPixmap(image))
            
if __name__ == "__main__":

    app = PyQt4.QtGui.QApplication(sys.argv)
    dlg = MainWindow()
    dlg.show()
    sys.exit(app.exec_())
        
    
