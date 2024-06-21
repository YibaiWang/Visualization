import os
import sys
import pandas as pd
import numpy as np
from numpy import genfromtxt
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

tab_parameter = []
tab_par = []
output_parameter = []
output_par = []
file_path = ''
folder_path = ''
row = 0
column = 0
####Window for output values####
##to be implemented##

####To set for read-only/non-editable Qtable cells####
class ReadOnly(QStyledItemDelegate):
    def createEditor(self, parent, option, index):
        return None
    
####Window for output plots####
#Tab-like lists for output graph
class PlotWindow(QWidget):
     def resizeEvent(self, event):      # works, but the process looks lagging
        new_width = event.size().width()
        new_height = int(new_width / self.aspect_ratio)
        self.resize(new_width, new_height)
     def __init__(self, tab_par = [], output_par = []):
        super().__init__()
        self.aspect_ratio = 1
        self.plot_layout = QVBoxLayout()
        self.plot_tabs = QTabWidget()
        self.plot_layout.addWidget(self.plot_tabs)
        self.setLayout(self.plot_layout)
        for i in range(len(tab_par)-1):
            # new_tab = QTabWidget()
            label = QLabel()
            file = 'PVT_result/design_point_0/' + output_par[i+1] + '.tif'      # need resize
            pixmap = QPixmap(file)
            scaled_pixmap = pixmap.scaled(500,500, Qt.KeepAspectRatio, Qt.SmoothTransformation)
            label.setPixmap(scaled_pixmap)
            label.setScaledContents(True)
            self.plot_tabs.addTab(label, tab_par[i+1])

class MainWindow(QWidget):
    global csv_file
    global header

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Test")
        ####draw layout####
        h_layout = QVBoxLayout()
        self.table_in = QTableWidget()
        self.table_in2 = QTableWidget()
        splitter1 = QSplitter(Qt.Horizontal)
        splitter1.addWidget(self.table_in)
        splitter1.addWidget(self.table_in2)
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
        self.setGeometry(50,100,1000,1000)
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
        if file_path != '':     # to avoid empty file crash
            folder_path = os.path.abspath(os.path.join(file_path, "..")) #general way of getting parent path
            self.text.setText(file_path)
            print(folder_path)
            csv_file = genfromtxt(file_path, encoding='utf-8-sig', delimiter=',', dtype=str)        # to avoid special character 
            row = csv_file.shape[0]     #22
            column = 5    #3
            self.table_in.setColumnCount(column)
            self.table_in.setRowCount(row)
            header = np.full(column, '', dtype=object)
            header[0] = csv_file[0][0]
            header[1] = csv_file[0][1]
            header[2] = csv_file[0][2]
            header[3] = "Sim Value"
            header[4] = "Trend"
            row2 = row
            column2 = 3
            self.table_in2.setColumnCount(column2)
            self.table_in2.setRowCount(row2)
            header2 = np.full(column, '', dtype=object)
            header2[0] = csv_file[0][3]
            header2[1] = "Parameter Value"
            header2[2] = "Trend"
            self.table_in.setHorizontalHeaderLabels(header)
            self.table_in.setColumnWidth(0, 200)
            self.table_in.setColumnWidth(1, 200)
            self.table_in.setColumnWidth(2, 200)
            self.table_in.setColumnWidth(3, 200)
            self.table_in.setColumnWidth(4, 200)
            self.table_in2.setHorizontalHeaderLabels(header2)
            self.table_in2.setColumnWidth(0, 200)
            self.table_in2.setColumnWidth(1, 200)
            self.table_in2.setColumnWidth(2, 200)
            ####write to QTable####
            csv_file_mod = np.full((row, column), '', dtype=object)
            csv_file_mod2 = np.full((row2, column2), '', dtype=object)
            csv_file_mod[:, 0] = csv_file[:, 0]
            csv_file_mod[:, 1] = csv_file[:, 1]
            csv_file_mod[:, 2] = csv_file[:, 2]
            csv_file_mod2[:, 0] = csv_file[:, 3]
            for x in range(row):
                for y in range(column):
                    if x+1 < row:
                        self.table_in.setItem(x,y, QTableWidgetItem(csv_file_mod[x+1][y]))           
            for x in range(row2):
                for y in range (column2):
                    if x+1 < row2:
                        self.table_in2.setItem(x,y, QTableWidgetItem(csv_file_mod2[x+1][y]))
            ####set for tab parameters####
            for x in range(row):
                    if x+1 < row:
                        tab_parameter.append(csv_file[x][0])
                        output_parameter.append(csv_file[x][1])
            for i in range(len(tab_parameter)):
                if tab_parameter[i] != '':
                    tab_par.append(tab_parameter[i])
                    output_par.append(output_parameter[i])
            self.table_in.setItemDelegateForColumn(0, ReadOnly(self))
            self.table_in.setItemDelegateForColumn(1, ReadOnly(self))
            self.table_in.setItemDelegateForColumn(2, ReadOnly(self))
            self.table_in2.setItemDelegateForColumn(0, ReadOnly(self))
            
    def plotWindow(self):
        ####to prevent recreation####
        if self.plot_window is None:
            self.plot_window = PlotWindow(tab_par, output_par)
        self.plot_window.show()

    ####csv file is updated from QTable#### (ML should be run here)
    def runSim(self):
        r = self.table_in.rowCount()
        c = self.table_in.columnCount()
        to_file = np.full((r+1, c), '', dtype=object)
        for i in range(r):
            for j in range (c):
                if self.table_in.item(i,j) is not None:
                    to_file[i+1][j] = self.table_in.item(i,j).text()
                else:
                    to_file[i+1][j] = ''
        to_file2 = np.full((r+1, 3), '', dtype=object)
        for i in range(r):
            for j in range(3):
                if self.table_in2.item(i,j) is not None:
                    to_file2[i+1][j] = self.table_in2.item(i,j).text()
                else:
                    to_file2[i+1][j] = ''
        actual_to_file = np.full((r+1, 5), '', dtype=object)
        actual_to_file[:, 0] = to_file[:, 0]
        actual_to_file[:, 1] = to_file[:, 1]
        actual_to_file[:, 2] = to_file[:, 2]
        actual_to_file[:, 3] = to_file2[:, 0]
        actual_to_file[:, 4] = to_file2[:, 1]
        actual_to_file[0][0] = self.table_in.horizontalHeaderItem(0).text()
        actual_to_file[0][1] = self.table_in.horizontalHeaderItem(1).text()
        actual_to_file[0][2] = self.table_in.horizontalHeaderItem(2).text()
        actual_to_file[0][3] = self.table_in2.horizontalHeaderItem(0).text()
        actual_to_file[0][4] = self.table_in2.horizontalHeaderItem(1).text()
        p = self.text.text()
        df=pd.DataFrame(actual_to_file)
        df.to_csv(p, header=False, index=False)
        # os.system("python analyze_pvt.py")      # Better idea?
        spec_trend = 'PVT_result/output_trends.csv'
        par_trend = 'PVT_result/trends.csv'
        if os.path.exists(spec_trend) and os.path.exists(par_trend):
            spec = genfromtxt(spec_trend, encoding='utf-8-sig', delimiter=',', dtype=str)
            par = genfromtxt(par_trend, encoding='utf-8-sig', delimiter=',', dtype=str)
            for i in range(spec.shape[0]):
                if i+1 < spec.shape[0]:
                    self.table_in.setItem(i,4,QTableWidgetItem(spec[i+1][2]))
            for i in range(par.shape[0]):
                if i+1 < par.shape[0]:
                    self.table_in2.setItem(i,2,QTableWidgetItem(par[i+1][2]))
        
if __name__ == "__main__":
    app = QApplication(sys.argv)
    main_window = MainWindow()
    main_window.show()
    sys.exit(app.exec())