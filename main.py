#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Mar 16 19:23:49 2024

@author: coco
"""
import PyQt5.QtWidgets as QtWidgets
import sys
from ui import Ui_MainWindow
from PyQt5 import QtCore as qtc
from pyqtgraph.Qt import QtCore, QtGui
import sys
from ui import Ui_MainWindow
from PyQt5 import QtCore as qtc
from pyqtgraph.Qt import QtCore, QtGui
from PyQt5 import QtWidgets as qtw
from PyQt5.QtGui import QColor

#from ChamberControl import ChamberControl
import os
import pyqtgraph as pg
import math
import numpy as np
from pyqtgraph import PlotWidget, plot
import pyqtgraph as pg
import time


class Main(qtw.QMainWindow):

    def __init__(self):

        super(Main, self).__init__()
        self.port = "none"
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        
        #self.ui.graphicsView.setBackground('gray') 

        # Define colors for the different elements
        self.curve_color = QColor(255, 165, 0)  # Orange
        self.derivative_line_color = QColor(255, 255, 0)  # Yellow
        self.tangent_line_color = QColor(255, 0, 0)  # Red
        self.points_color = QColor(255, 192, 203)  # Pink
        
        self.tangentLine = None
        
        #self.ui.horizontalSlider.valueChanged.connect(self.sliderValueH)
        self.ui.horizontalSlider.valueChanged.connect(self.sliderValueH1)

        
        # Array contains x values from -10 to 10, once inputted in the linear function, it will output the y values
        self.x = [-10, -9, -8, -7, -6, -5, -4, -3, -2, -1, 0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
        
        self.ui.btn_enterEquation.clicked.connect(self.organizeValues)
        self.ui.btn_enterx0.clicked.connect(self.derivative)
        self.ui.btn_enterh.clicked.connect(self.clearTangentLine)
        self.ui.btn_enterh.clicked.connect(self.calculateSlopeOfTangent_1)
        #self.ui.btn_enterh.clicked.connect(self.calculateSlopeOfTangent_slider)
        
        self.ui.btn_enterh.clicked.connect(self.clearPoints)
        self.ui.btn_enterh.clicked.connect(self.graphIntersectionPoints)
        # self.ui.btn_enterCalcParam.clicked.connect(self.calculateSlopeOfTangent)

    def organizeValues(self):
        self.a3 = self.ui.tf_a3.text()
        self.a2 = self.ui.tf_a2.text()
        self.a1 = self.ui.tf_a1.text()
        self.a0 = self.ui.tf_a0.text()

        self.A3 = float(self.a3)
        self.A2 = float(self.a2)
        self.A1 = float(self.a1)
        self.A0 = float(self.a0)
       
        self.h = float(self.ui.tf_h.text())
        self.x0 = float(self.ui.tf_x_0.text())
        
        self.graphEquation()  
                
        
    def graphEquation(self):
        A3 = self.A3
        A2 = self.A2
        A1 = self.A1
        A0 = self.A0
        
        print(A3)
        print(A3)
        print(A3)
        print(A3)
        
        self.ui.graphicsView.clear()

        penCustomized = pg.mkPen(color='yellow', width=1.5)

        self.ui.graphicsView.showGrid(x=True, y=True)
        self.ui.graphicsView.setLabel('left', 'Y axis')
        self.ui.graphicsView.setLabel('bottom', 'X axis')

        yarray = []  # y values will be calculated and appended to this array

        # Loop goes through each x value in the array and calculates the output
        for i in range(len(self.x)):
            # y = self.A * self.A * self.x[i] * self.x[i] + self.B * self.x[i] + self.C # Calculate

            y = A3 * (self.x[i])**3 + A2 * (self.x[i])**2 + A1 * (self.x[i])**1 + A0         

            yarray.append(y)  # Appends the calculated y values to the array
            
            print("f(x) =", y ,"self.x[i]", self.x[i])

        self.cubicFunction = self.ui.graphicsView.plot(self.x, yarray, pen=penCustomized)

    def derivative(self):
        A3 = self.A3
        A2 = self.A2
        A1 = self.A1
        A0 = self.A0
        
        yarray = []
        
        print(A3)
        
        penCustomized = pg.mkPen(color='red', width=2)
        
        x0 = float(self.ui.tf_x_0.text())

        derivative = 3 * A3 * x0**2
        derivative += 2 * A2 * x0 + A1
        
        m = derivative

        print("derivative =", derivative)
        
        self.ui.tf_fprime.setText(str(derivative))
        
        fx0 = (A3 * x0**3) + (A2 * x0**2) + (A1 * x0**1) + (A0) 
        
        print("fx0=",fx0)
        
        b = fx0 - (m*x0)
        
        # Loop goes through each x value in the array and calculates the output
        for i in range(len(self.x)):
            y = m * self.x[i] + b  # Calculate
            
            print(y)

            yarray.append(y)  # Appends the calculated y values to the array
        
        self.derivative = self.ui.graphicsView.plot(self.x, yarray, pen=penCustomized)  # Store the new tangent line
        
    # Function to handle slider value change
    def sliderValueH(self, value):
        # Set the scaling factor
        self.scaling_factor = 10       
        
        h = self.h
        #h = 10
        h += 1.5 
        
        epsilon = 2  # The h value can never get to 0 (ε)
        
        # Calculate scaled minimum and maximum values
        min_h = epsilon # Example: minimum value of 1.5
        max_h = h  # Example: maximum value of 10.0
        scaled_min_h = int(min_h * self.scaling_factor)
        scaled_max_h = int(max_h * self.scaling_factor)
        
        # Adjust the minimum and maximum values of the horizontal slider
        self.ui.horizontalSlider.setMinimum(scaled_min_h)
        self.ui.horizontalSlider.setMaximum(scaled_max_h)
        
        #self.ui.horizontalSlider.setMinimum(0.001)
        #self.ui.horizontalSlider.setMaximum(scaled_max_h)
        
        slider_h = self.ui.horizontalSlider.value()
        slider_h = self.ui.horizontalSlider.maximum() - value
        slider_h = slider_h / self.scaling_factor
        print(f"Slider value changed: {slider_h}")
        
        self.calculateSlopeOfTangent_slider(slider_h)
        
        self.ui.graphicsView.removeItem(self.tangentLine)    

        self.ui.tf_h.setText(str(slider_h))
    
    # Function to handle slider value change
    def sliderValueH1(self, value):
        # Set the scaling factor
        self.scaling_factor = 100   
        
        h = self.h
        h = 10
        
        epsilon = 0.01  # The h value can never get to 0 (ε)
        
        # Calculate scaled minimum and maximum values
        min_h = epsilon # Example: minimum value of 1.5
        max_h = h  # Example: maximum value of 10.0
        
        scaled_min_h = int(min_h * self.scaling_factor)
        scaled_max_h = int(max_h * self.scaling_factor)
        
        # Adjust the minimum and maximum values of the horizontal slider
        self.ui.horizontalSlider.setMinimum(scaled_min_h)
        self.ui.horizontalSlider.setMaximum(scaled_max_h)
        
        #self.ui.horizontalSlider.setMinimum(0.001)
        #self.ui.horizontalSlider.setMaximum(scaled_max_h)
        
        slider_h = self.ui.horizontalSlider.value()
        slider_h = self.ui.horizontalSlider.maximum() - value
        
        if slider_h == 0:
            slider_h += 0.1
        
        slider_h = slider_h / self.scaling_factor
        print(f"Slider value changed: {slider_h}")
        
        self.ui.graphicsView.removeItem(self.tangentLine)    

        
        self.calculateSlopeOfTangent_slider(slider_h)
        

        self.ui.tf_h.setText(str(slider_h))    
        
    # DADS VERSION DADS VERSION DADS VERSION DADS VERSION DADS VERSION DADS VERSION DADS VERSION DADS VERSION 
    def calculateSlopeOfTangent_slider(self,h):
        
        A3 = self.A3
        A2 = self.A2
        A1 = self.A1
        A0 = self.A0
        
        print("a3,a2,a1,a0=",A3,A2,A1,A0)
        
        
        penCustomized = pg.mkPen(color='lightgreen', width=2)
        self.ui.graphicsView.showGrid(x=True, y=True)
        self.ui.graphicsView.setLabel('left', 'Y axis')
        self.ui.graphicsView.setLabel('bottom', 'X axis')

        yarray = []  # y values will be calculated and appended to this array

        #h = float(self.ui.tf_h.text())
        print("THE H VALUE FROM THE SLIDER =", h)
        x0 = float(self.ui.tf_x_0.text())
        
        print("h = ",h)
        print("x0 = ",x0)
        
        newx0 = x0+h
       
        print("newx0 = ", newx0)
        
        fx0h = (A3 * newx0**3) + (A2 * newx0**2) + (A1 * newx0**1) + A0 
        fx0 = (A3 * x0**3) + (A2 * x0**2) + (A1 * x0**1) + A0
        
        print("f(x_0+h) =", fx0h)
        print("f(x_0) =", fx0)

        m = (fx0h - fx0) / h
        b = -m*(x0)+fx0
    

        print("m =", m)
        print("b =", b)
        

        tanEquation = str(m) + "x +" + str(b)
        
        print("tangent equation =", tanEquation)
        
        self.ui.tf_tangent.setText(tanEquation)

        # Loop goes through each x value in the array and calculates the output
        for i in range(len(self.x)):
            y = m * self.x[i] + b  # Calculate
            
            #print(y)

            yarray.append(y)  # Appends the calculated y values to the array

        #self.ui.graphicsView.plot(self.x, yarray, pen = penCustomized)
        #==============================================================
        
        # for i in range (len(self.x)):
        #     derivative = (3 * A3 * (self.x[i])**3) + (2 * A2 * (self.x[i])**2 + A1)
        #     yarray.append(derivative)
        
        self.tangentLine = self.ui.graphicsView.plot(self.x, yarray, pen=penCustomized)  # Store the new tangent line    
    
    
    # DADS VERSION DADS VERSION DADS VERSION DADS VERSION DADS VERSION DADS VERSION DADS VERSION DADS VERSION 
    def calculateSlopeOfTangent_1(self,h):
        
        A3 = self.A3
        A2 = self.A2
        A1 = self.A1
        A0 = self.A0
        
        print("a3,a2,a1,a0=",A3,A2,A1,A0)
        
        
        penCustomized = pg.mkPen(color='lightgreen', width=2)
        self.ui.graphicsView.showGrid(x=True, y=True)
        self.ui.graphicsView.setLabel('left', 'Y axis')
        self.ui.graphicsView.setLabel('bottom', 'X axis')

        yarray = []  # y values will be calculated and appended to this array

        h = float(self.ui.tf_h.text())
        print("THE H VALUE FROM THE SLIDER =", h)
        x0 = float(self.ui.tf_x_0.text())
        
        print("h = ",h)
        print("x0 = ",x0)
        
        newx0 = x0+h
       
        print("newx0 = ", newx0)
        
        fx0h = (A3 * newx0**3) + (A2 * newx0**2) + (A1 * newx0**1) + A0 
        fx0 = (A3 * x0**3) + (A2 * x0**2) + (A1 * x0**1) + A0
        
        print("f(x_0+h) =", fx0h)
        print("f(x_0) =", fx0)

        m = (fx0h - fx0) / h
        b = -m*(x0)+fx0
    

        print("m =", m)
        print("b =", b)
        

        tanEquation = str(m) + "x +" + str(b)
        
        print("tangent equation =", tanEquation)
        
        self.ui.tf_tangent.setText(tanEquation)

        # Loop goes through each x value in the array and calculates the output
        for i in range(len(self.x)):
            y = m * self.x[i] + b  # Calculate
            
            #print(y)

            yarray.append(y)  # Appends the calculated y values to the array

        #self.ui.graphicsView.plot(self.x, yarray, pen = penCustomized)
        #==============================================================
        
        # for i in range (len(self.x)):
        #     derivative = (3 * A3 * (self.x[i])**3) + (2 * A2 * (self.x[i])**2 + A1)
        #     yarray.append(derivative)
        
        self.tangentLine = self.ui.graphicsView.plot(self.x, yarray, pen=penCustomized)  # Store the new tangent line    
        
        
    
    def clearTangentLine(self):
        self.ui.graphicsView.removeItem(self.tangentLine)    
    
    def graphIntersectionPoints(self):        
        penCustomized = pg.mkPen(color='green', width=5)
        
        x1 = self.x0
        fx1 = self.A3 * (x1**3) + self.A2 * (x1**2) + self.A1 * x1 + self.A0
        
        x1 = [x1]
        fx1 = [fx1]
        
        print("graph intersection points (X1):", x1)
        print("graph intersection points (Y1):", fx1)
        
        #self.derivative = self.ui.graphicsView.plot(x1, fx1, pen=penCustomized)
        # Define the X and Y coordinates of the point
        x = [0]
        y = [0]
        
        penCustomized = pg.mkPen(color='green', width=5)
        
        x2 = self.x0 + self.h
        
        fx2 = self.A3 * (x2**3) + self.A2 * (x2**2) + self.A1 * x2 + self.A0
        
        x2 = [x2]
        fx2 = [fx2]
        
        print("graph intersection points (X2):", x2)
        print("graph intersection points (Y2):", fx2)
        
        # Plot the point at (0, 0)
        self.point1 = self.ui.graphicsView.plot(x1, fx1, pen=penCustomized, symbol='x')  # Use 'o' symbol for point
        
        # Plot the point at (0, 0)
        self.point2 = self.ui.graphicsView.plot(x2, fx2, pen=penCustomized, symbol='x')  # Use 'o' symbol for point
        
    def clearPoints(self):
        # if hasattr(self, 'point1'):
        #     self.ui.graphicsView.removeItem(self.point1)
        #     del self.point1
        # if hasattr(self, 'point2'):
        #     self.ui.graphicsView.removeItem(self.point2)
        #     del self.point2
        self.ui.graphicsView.removeItem(self.point1)
        self.ui.graphicsView.removeItem(self.point2)
        
        self.point1.clear()
        self.point2.clear()

        # Plot the point at (0, 0)
        self.point1 = self.ui.graphicsView.plot(x = None, y= None)  # Use 'o' symbol for point
        
        # Plot the point at (0, 0)
        self.point2 = self.ui.graphicsView.plot(x = None, y = None)  # Use 'o' symbol for point


if __name__ == '__main__':

    app = qtw.QApplication([])

    widget = Main()
    widget.show()

    app.exec_()
