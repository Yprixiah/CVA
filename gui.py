from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt, QThread, pyqtSignal
from PyQt5 import QtGui
import matplotlib.backends.backend_qt5agg
from matplotlib.backends.backend_template import FigureCanvas
from matplotlib.figure import Figure
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import (NavigationToolbar2QT as NavigationToolbar)
import sys
import time
import pandas as pd
from tkinter import filedialog
import tkinter as tk
from MplWidget import MplWidget
from currentVsSignal import currentVsSignal


class gui():

    def __init__(self, mainBox):
        buttonLoad = QPushButton('Load Data')
        buttonLoad.clicked.connect(self.load_data)
        buttonPlot = QPushButton('Plot Data')
        buttonPlot.clicked.connect(self.plot_rawData)
        buttonProcess = QPushButton('Process Data')
        buttonProcess.clicked.connect(self.processCvsT)
        buttonSave = QPushButton('Save processed data')
        buttonSave.clicked.connect(self.save)
        hbox1 = QHBoxLayout()
        vbox1 = QVBoxLayout()
        vbox1.addWidget(buttonLoad)
        vbox1.addWidget(buttonPlot)
        vbox1.addWidget(buttonProcess)
        vbox1.addWidget(buttonSave)
        hbox2 = QHBoxLayout()
        self.rawDataGraph = MplWidget()
        self.rawGraphToolbar = NavigationToolbar(self.rawDataGraph.canvas, self)
        vbox2 = QVBoxLayout()
        vbox2.addWidget(self.rawGraphToolbar)
        vbox2.addWidget(self.rawDataGraph)
        self.processedDataGraph1 = MplWidget()
        self.processedGraph1Toolbar = NavigationToolbar(self.processedDataGraph1.canvas, self)
        vbox3 = QVBoxLayout()
        vbox3.addWidget(self.processedGraph1Toolbar)
        vbox3.addWidget(self.processedDataGraph1)
        self.processedDataGraph2 = MplWidget()
        self.processedGraph2Toolbar = NavigationToolbar(self.processedDataGraph2.canvas, self)
        vbox4 = QVBoxLayout()
        vbox4.addWidget(self.processedGraph2Toolbar)
        vbox4.addWidget(self.processedDataGraph2)
        hbox1.addLayout(vbox1)
        hbox1.addLayout(vbox2)
        hbox2.addLayout(vbox3)
        hbox2.addLayout(vbox4)
        mainBox.addLayout(hbox1)
        mainBox.addLayout(hbox2)

    def load_data(self):
        global d
        root = tk.Tk()
        root.withdraw()
        file_path = filedialog.askopenfilename()
        d = (pd.read_csv(file_path, sep='\t', header=None))

    def plot_rawData(self):
        self.rawDataGraph.canvas.axes.clear()
        self.rawDataGraph.canvas.axes.plot(d[0], d[1])
        self.rawDataGraph.canvas.draw()

    def processCvsT(self):
        currentVsSignal(d)
        self.P = currentVsSignal.getCorrData()
        # global I
        # global P
        #
        # for i in range(1, (len(d) - 2)):
        #     h = i - 1
        #     j = i + 1
        #     if d[0][h] > d[0][j] and d[0][j] > d[0][i] or d[0][j] > d[0][h] and d[0][h] > d[0][i] or d[0][i] > d[0][
        #         j] and d[0][j] > d[0][h] or d[0][i] > d[0][h] and d[0][h] > d[0][j]:
        #         I.append(i)
        #
        # for i in range(0, (len(I) - 1)):
        #     j = i + 1
        #     p = I[j] - I[i]
        #     P.append(p)

        self.processedDataGraph1.canvas.axes.clear()
        self.processedDataGraph1.canvas.axes.plot(self.P)
        self.processedDataGraph1.canvas.draw()

    def save(self):
        print('save')