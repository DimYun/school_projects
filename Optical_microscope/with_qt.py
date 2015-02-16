#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
This example shows how to display a SimpleCV image in a QT window
the code was taken from the forum post here:
http://help.simplecv.org/question/1866/any-simple-pyqt-sample-regarding-ui-or-display/

Author: Rodrigo gomes 
'''

import os
import sys
#import signal
from PyQt4 import QtGui, QtCore
from SimpleCV import *


class Microscope_main(QtGui.QMainWindow):
    webcam = 0
    number_cam = 0

    def __init__(self, parent=None):
        QtGui.QMainWindow.__init__(self, parent)
        desktop = QtGui.QApplication.desktop()
        x = desktop.width()
        y = desktop.height()
        #print x, y
        self.move(x / 2.0, y / 2.0)
        self.setWindowTitle('Optical microscope')
        self.vl_main = QtGui.QVBoxLayout(self)
        self.cb_camera = QtGui.QComboBox()
        self.cb_camera.addItems(['1', '2', '3'])
        self.vl_main.addWidget(self.cb_camera)
        self.label = QtGui.QLabel()
        self.vl_main.addWidget(self.label)
        #self.label.setGeometry(QtCore.QRect(80, 30, 491, 391))
        self.hl_button = QtGui.QHBoxLayout()
        self.button_start = QtGui.QPushButton('Start video')
        self.button_start.setCheckable(True)
        self.button_save = QtGui.QPushButton('Save picture')
        self.hl_button.addWidget(self.button_start)
        self.hl_button.addWidget(self.button_save)
        self.vl_main.addLayout(self.hl_button)

        if self.button_start.isEnabled():
            self.start_video
        QtCore.QObject.connect(self.button_start, QtCore.SIGNAL('toggled(bool)'), self.start_video)
        QtCore.QObject.connect(self.button_save, QtCore.SIGNAL('click()'), self.save_pict)

    def save_pict(self):
        filename = QtGui.QFileDialog.getSaveFileName(self, u'Сохранить изображение', '.png')
        filename = str(filename.toLocal8Bit())
        if self.webcam == 0:
            self.number_cam = self.cb_camera.currentIndex()
            self.webcam = Camera(self.number_cam, {"width": 640, "height": 480})
        else:
            pass
        image = self.webcam.getImage()
        image.save(filename)

    def start_video(self):
        if self.number_cam == 0:
            self.number_cam = self.cb_camera.currentIndex()
            self.webcam = Camera(self.number_cam, {"width": 640, "height": 480})
            self.timer = QtCore.QTimer()
            QtCore.QObject.connect(self.timer, QtCore.SIGNAL('timeout()'), self.show_frame)
            self.timer.start(1)

    def show_frame(self):
        ipl_image = self.webcam.getImage()
        ipl_image = ipl_image.crop(x=0, y=0, w=100, h=100)
        ipl_image.dl().circle((150, 75), 50, Color.RED, filled = True)
        data = ipl_image.getBitmap().tostring()
        image = QtGui.QImage(data, ipl_image.width, ipl_image.height, 3 * ipl_image.width, QtGui.QImage.Format_RGB888)
        pixmap = QtGui.QPixmap()
        pixmap.convertFromImage(image.rgbSwapped())
        self.MainWindow.label.setPixmap(pixmap)

if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    microscope = Microscope_main()
    microscope.show()
    app.exec_()
