import os
import sys
import pandas as pd
import numpy as np
from numpy import genfromtxt
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

####Window for output plots####
#Tab-like lists for output graph
class PlotWindow(QWidget):
     def __init__(self, tab_parameters = []):
        super().__init__()
        tab_parameters = ["xx", "dd", "cc","rr"]
        self.setWindowTitle("Test2")
        # layout = QVBoxLayout()
        # plot = QLabel(self)
        # pixel = QPixmap('C:/Users/yibai/Desktop/zuofu.png')
        # plot.setPixmap(pixel)
        # layout.addWidget(plot)
        # self.setLayout(layout)
        self.plot_layout = QVBoxLayout(self)
        self.plot_tabs = QTabWidget()
        self.plot_layout.addWidget(self.plot_tabs)
        self.setLayout(self.plot_layout)
        for parameter in tab_parameters:
            new_tab = QTabWidget()
            self.plot_tabs.addTab(new_tab, parameter)
        self.plot_tabs.resize(300,300)


class MainWindow(QWidget):
    global folder_path #ok
    global file_path
    global csv_file
    global header
    global row
    global column

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Test")
        ####draw layout####
        h_layout = QVBoxLayout()
        self.table_in = QTableWidget()
        # need to set table size later
        # table_in.setItem(1,1,QTableWidgetItem("1"))
        # table_in.item(1,1).setBackground(QColor(100,100,100))
        splitter1 = QSplitter(Qt.Horizontal)
        splitter1.addWidget(self.table_in)
        splitter1.setStretchFactor(0,0)
        self.upload_btn = QPushButton("upload")
        self.text = QLabel("Please upload your input file")
        self.run_sim_btn = QPushButton("run sim")
        self.plot = QPushButton("show plot")
        splitter2 = QSplitter(Qt.Horizontal)
        splitter2.addWidget(splitter1)
        splitter2.addWidget(self.upload_btn)
        splitter2.addWidget(self.text)
        splitter2.addWidget(self.run_sim_btn)
        splitter2.addWidget(self.plot)
        splitter2.setStretchFactor(0.2,10)  #looks like it will force the button's height
        h_layout.addWidget(splitter1)
        h_layout.addWidget(splitter2)
        self.setLayout(h_layout)
        ####upload dialog####
        self.upload_btn.clicked.connect(self.openFileDialog)
        self.setGeometry(50,100,660,950)
        ####show plot####
        self.plot_window = None  #to prevent recreation

        self.plot.clicked.connect(self.plotWindow)
        self.run_sim_btn.clicked.connect(self.runSim)
        self.show()

    ####open dialog and allow read and display####
    def openFileDialog(self):
        path = "c:\\"
        filename = QFileDialog.getOpenFileName(self, "OpenFile", path, "CSV Files (*.csv)")
        file_path = filename[0]
        folder_path = os.path.abspath(os.path.join(file_path, "..")) #general way of getting parent path
        self.text.setText(folder_path)
        csv_file = genfromtxt(file_path, delimiter=',', dtype=str)
        print(csv_file)
        row = csv_file.shape[0]     #22
        column = csv_file.shape[1]      #3
        self.table_in.setColumnCount(column)
        self.table_in.setRowCount(row)
        header = csv_file[0]
        self.table_in.setHorizontalHeaderLabels(header)
        self.table_in.setColumnWidth(0, 200)
        self.table_in.setColumnWidth(1, 200)
        self.table_in.setColumnWidth(2, 200)
        for x in range(row):
            for y in range(column):
                if x+1 <= 22:
                    self.table_in.setItem(x,y, QTableWidgetItem(csv_file[x+1][y]))

    def plotWindow(self):
        ####to prevent recreation####
        if self.plot_window is None:
            self.plot_window = PlotWindow()
        self.plot_window.show()

    ####csv file is updated from QTable#### (ML should be run here)
    def runSim(self):
        to_file = np.empty(shape=(self.table_in.rowCount(), self.table_in.colorCount()), dtype=object)
        header = np.empty(shape=(self.table_in.columnCount(),), dtype=object)
        for i in range(self.table_in.columnCount()):
            print(self.table_in.horizontalHeaderItem(i).text())
            to_file[0][i] = "tttttttt"
        # print(to_file)
        # print(self.table_in.horizontalHeaderItem(0).text())
        # np.append(header, str(self.table_in.horizontalHeaderItem(0).text()))
        # print(header)
        # to_file = np.append(header)
        # print(to_file)

    
        
if __name__ == "__main__":
    app = QApplication(sys.argv)
    main_window = MainWindow()
    main_window.show()
    sys.exit(app.exec())