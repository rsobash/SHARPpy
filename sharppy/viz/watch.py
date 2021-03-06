import numpy as np
from PySide import QtGui, QtCore
import sharppy.sharptab as tab
from scipy.misc import bytescale
from sharppy.sharptab.constants import *

## Written by Kelton Halbert - OU School of Meteorology
## and Greg Blumberg - CIMMS


__all__ = ['backgroundWatch', 'plotWatch']

class backgroundWatch(QtGui.QFrame):
    '''
    Draw the background frame and lines for the watch plot frame
    '''
    def __init__(self):
        super(backgroundWatch, self).__init__()
        self.initUI()


    def initUI(self):
        ## window configuration settings,
        ## sich as padding, width, height, and
        ## min/max plot axes
        self.lpad = 0; self.rpad = 0
        self.tpad = 0; self.bpad = 20
        self.wid = self.size().width() - self.rpad
        self.hgt = self.size().height() - self.bpad
        self.tlx = self.rpad; self.tly = self.tpad
        self.brx = self.wid; self.bry = self.hgt
        if self.physicalDpiX() > 75:
            fsize = 10
        else:
            fsize = 12
        self.title_font = QtGui.QFont('Helvetica', fsize)
        self.plot_font = QtGui.QFont('Helvetica', fsize)
        self.title_metrics = QtGui.QFontMetrics( self.title_font )
        self.plot_metrics = QtGui.QFontMetrics( self.plot_font )
        self.title_height = self.title_metrics.height()
        self.plot_height = self.plot_metrics.height()
        self.plotBitMap = QtGui.QPixmap(self.width(), self.height())
        self.plotBitMap.fill(QtCore.Qt.black)
        self.plotBackground()  

    def resizeEvent(self, e):
        '''
        Handles the event the window is resized
        '''
        self.initUI()

    def draw_frame(self, qp):
        '''
        Draw the background frame.
        qp: QtGui.QPainter object
        '''
        ## set a new pen to draw with
        pen = QtGui.QPen(QtCore.Qt.white, 2, QtCore.Qt.SolidLine)
        qp.setPen(pen)
        qp.setFont(self.title_font)
        
        ## draw the borders in white
        qp.drawLine(self.tlx, self.tly, self.brx, self.tly)
        qp.drawLine(self.brx, self.tly, self.brx, self.bry)
        qp.drawLine(self.brx, self.bry, self.tlx, self.bry)
        qp.drawLine(self.tlx, self.bry, self.tlx, self.tly)

        y1 = self.bry / 13.
        pad = self.bry / 100.
        rect0 = QtCore.QRect(0, pad*4, self.brx, self.title_height)
        qp.drawText(rect0, QtCore.Qt.TextDontClip | QtCore.Qt.AlignCenter, 'Psbl Haz. Type')
        pen = QtGui.QPen(QtCore.Qt.white, 1, QtCore.Qt.SolidLine)
        qp.setPen(pen)
        qp.drawLine(0, pad*4 + (self.title_height + 3), self.brx, pad*4 + (self.title_height + 3))
    
    def plotBackground(self):
        qp = QtGui.QPainter()
        qp.begin(self.plotBitMap)
        #qp.setRenderHint(qp.Antialiasing)
        #qp.setRenderHint(qp.TextAntialiasing)
        ## draw the frame
        self.draw_frame(qp)
        qp.end()

class plotWatch(backgroundWatch):
    '''
    Plot the data on the frame. Inherits the background class that
    plots the frame.
    '''
    def __init__(self, prof):
        self.prof = prof
        super(plotWatch, self).__init__()
        self.watch_type = self.prof.watch_type
        self.watch_type_color = self.prof.watch_type_color

    def resizeEvent(self, e):
        '''
        Handles when the window is resized
        '''
        super(plotWatch, self).resizeEvent(e)
        self.plotData()
    
    def paintEvent(self, e):
        '''
        Handles painting on the frame
        '''
        ## this function handles painting the plot
        super(plotWatch, self).paintEvent(e)
        ## create a new painter obkect
        qp = QtGui.QPainter()
        qp.begin(self)
        ## end the painter
        qp.drawPixmap(0,0,self.plotBitMap)
        qp.end()

    def plotData(self):
        qp = QtGui.QPainter()
        qp.begin(self.plotBitMap)
        qp.setRenderHint(qp.Antialiasing)
        qp.setRenderHint(qp.TextAntialiasing)
        pen = QtGui.QPen(QtGui.QColor(self.watch_type_color), 1, QtCore.Qt.SolidLine)
        qp.setPen(pen)        
        qp.setFont(self.plot_font)
        centery = self.bry / 2.
        rect0 = QtCore.QRect(0, centery, self.brx, self.title_height)
        qp.drawText(rect0, QtCore.Qt.TextDontClip | QtCore.Qt.AlignCenter, self.watch_type)
        qp.end()

