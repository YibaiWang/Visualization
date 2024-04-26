import sys
import os
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

class PlotWindow(QWidget):
     def __init__(self):
        super().__init__()
        self.setWindowTitle("Test2")
        layout = QVBoxLayout()
        plot = QLabel(self)
        pixel = QPixmap('C:/Users/yibai/Desktop/zuofu.png')
        plot.setPixmap(pixel)
        layout.addWidget(plot)
        self.setLayout(layout)

class MainWindow(QWidget):
    global folder_path #not implanted yet
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Test")
        
        ####draw layout####
        h_layout = QVBoxLayout()
        table_in = QTableWidget()
        table_in.setColumnCount(3)
        table_in.setRowCount(15)
        table_out = QTableWidget()
        table_out.setColumnCount(2)
        table_out.setRowCount(23)
        splitter1 = QSplitter(Qt.Horizontal)
        splitter1.addWidget(table_in)
        splitter1.addWidget(table_out)
        splitter1.setSizes([300,200])
        splitter1.setStretchFactor(0,0)
        self.upload_btn = QPushButton("upload")
        self.text = QLabel("Please upload your input file")
        run_sim_btn = QPushButton("run sim")
        self.plot = QPushButton("show plot")
        splitter2 = QSplitter(Qt.Horizontal)
        splitter2.addWidget(splitter1)
        splitter2.addWidget(self.upload_btn)
        splitter2.addWidget(self.text)
        splitter2.addWidget(run_sim_btn)
        splitter2.addWidget(self.plot)
        splitter2.setStretchFactor(0.2,10)  #looks like it will force the button's height
        h_layout.addWidget(splitter1)
        h_layout.addWidget(splitter2)
        self.setLayout(h_layout)
        ####upload dialog####
        self.upload_btn.clicked.connect(self.openFileDialog)
        self.setGeometry(50,100,740,950)
        ####show plot####
        self.w = None  #to prevent recreation
        self.plot.clicked.connect(self.plotWindow)
        self.show()
    def openFileDialog(self):
        path = "c:\\"
        filename = QFileDialog.getOpenFileName(self, "OpenFile", path, "CSV Files (*.csv)")
        file_path = filename[0]
        self.text.setText(file_path)
    def plotWindow(self):
        ####to prevent recreation####
        if self.w is None:
            self.w = PlotWindow()
        self.w.show()    
        
if __name__ == "__main__":
    app = QApplication(sys.argv)
    main_window = MainWindow()
    main_window.show()
    sys.exit(app.exec())