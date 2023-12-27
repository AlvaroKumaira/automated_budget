# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'design.ui'
#
# Created by: PyQt5 UI code generator 5.15.9
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1413, 600)
        MainWindow.setMinimumSize(QtCore.QSize(1000, 0))
        MainWindow.setMaximumSize(QtCore.QSize(16777215, 16777215))
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/dependencies/icon.ico"), QtGui.QIcon.Normal, QtGui.QIcon.On)
        MainWindow.setWindowIcon(icon)
        MainWindow.setStyleSheet("")
        MainWindow.setIconSize(QtCore.QSize(24, 24))
        MainWindow.setToolButtonStyle(QtCore.Qt.ToolButtonTextBesideIcon)
        MainWindow.setTabShape(QtWidgets.QTabWidget.Rounded)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.centralwidget)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setSpacing(0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.top_bar = QtWidgets.QFrame(self.centralwidget)
        self.top_bar.setMinimumSize(QtCore.QSize(0, 35))
        self.top_bar.setMaximumSize(QtCore.QSize(16777215, 30))
        self.top_bar.setStyleSheet("background-color: rgb(78, 125, 255);")
        self.top_bar.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.top_bar.setFrameShadow(QtWidgets.QFrame.Raised)
        self.top_bar.setObjectName("top_bar")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.top_bar)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout.setSpacing(0)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.logo = QtWidgets.QLabel(self.top_bar)
        self.logo.setMinimumSize(QtCore.QSize(60, 0))
        self.logo.setStyleSheet("image: url(:/dependencies/logo.png);")
        self.logo.setText("")
        self.logo.setObjectName("logo")
        self.horizontalLayout.addWidget(self.logo)
        spacerItem = QtWidgets.QSpacerItem(402, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.title = QtWidgets.QLabel(self.top_bar)
        self.title.setMinimumSize(QtCore.QSize(0, 30))
        font = QtGui.QFont()
        font.setFamily("Segoe UI")
        font.setPointSize(14)
        font.setBold(True)
        font.setWeight(75)
        self.title.setFont(font)
        self.title.setStyleSheet("color: rgb(238, 238, 238);")
        self.title.setObjectName("title")
        self.horizontalLayout.addWidget(self.title)
        spacerItem1 = QtWidgets.QSpacerItem(401, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem1)
        self.verticalLayout.addWidget(self.top_bar)
        self.view = QtWidgets.QFrame(self.centralwidget)
        self.view.setMinimumSize(QtCore.QSize(0, 500))
        self.view.setStyleSheet("background-color: rgb(238, 238, 238);")
        self.view.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.view.setFrameShadow(QtWidgets.QFrame.Raised)
        self.view.setObjectName("view")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.view)
        self.verticalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_2.setSpacing(0)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.client_frame = QtWidgets.QFrame(self.view)
        self.client_frame.setMinimumSize(QtCore.QSize(0, 30))
        self.client_frame.setMaximumSize(QtCore.QSize(16777215, 35))
        self.client_frame.setStyleSheet("background-color: rgb(142, 142, 142);")
        self.client_frame.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.client_frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.client_frame.setLineWidth(0)
        self.client_frame.setObjectName("client_frame")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout(self.client_frame)
        self.horizontalLayout_2.setContentsMargins(3, 0, 0, 0)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.client_label = QtWidgets.QLabel(self.client_frame)
        self.client_label.setMaximumSize(QtCore.QSize(45, 16777215))
        font = QtGui.QFont()
        font.setFamily("Segoe UI")
        font.setPointSize(9)
        font.setBold(True)
        font.setWeight(75)
        self.client_label.setFont(font)
        self.client_label.setStyleSheet("color: rgb(238, 238, 238);")
        self.client_label.setObjectName("client_label")
        self.horizontalLayout_2.addWidget(self.client_label)
        self.client_search = QtWidgets.QLineEdit(self.client_frame)
        self.client_search.setMaximumSize(QtCore.QSize(150, 16777215))
        font = QtGui.QFont()
        font.setFamily("Segoe UI")
        self.client_search.setFont(font)
        self.client_search.setStyleSheet("background-color: rgb(238, 238, 238);")
        self.client_search.setObjectName("client_search")
        self.horizontalLayout_2.addWidget(self.client_search)
        self.search_button = QtWidgets.QPushButton(self.client_frame)
        self.search_button.setMinimumSize(QtCore.QSize(50, 25))
        self.search_button.setMaximumSize(QtCore.QSize(75, 16777215))
        font = QtGui.QFont()
        font.setFamily("Segoe UI")
        self.search_button.setFont(font)
        self.search_button.setStyleSheet("QPushButton {\n"
"    background-color: qlineargradient(x1:0, y1:0, x2:0, y2:1,\n"
"                      stop:0 rgb(90, 133, 250), stop:1 rgb(70, 113, 230));\n"
"    color: rgb(255, 255, 255);\n"
"    border-top: 1px solid rgb(140, 180, 250);\n"
"    border-left: 1px solid rgb(140, 180, 250);\n"
"    border-bottom: 1px solid rgb(30, 53, 190);\n"
"    border-right: 1px solid rgb(30, 53, 190);\n"
"    border-radius: 4px;\n"
"    box-shadow: 5px 5px 10px rgba(0, 0, 0, 0.3);\n"
"    padding: 5px 15px; /* Adjust padding if needed */\n"
"    text-align: center;\n"
"}\n"
"\n"
"QPushButton:pressed {\n"
"    background-color: qlineargradient(x1:0, y1:0, x2:0, y2:1,\n"
"                      stop:0 rgb(60, 93, 210), stop:1 rgb(50, 83, 200));\n"
"    box-shadow: 2px 2px 5px rgba(0, 0, 0, 0.2); /* Smaller shadow for pressed state */\n"
"    border-top: 1px solid rgb(120, 160, 230);\n"
"    border-bottom: 1px solid rgb(20, 43, 180);\n"
"}\n"
"")
        self.search_button.setObjectName("search_button")
        self.horizontalLayout_2.addWidget(self.search_button)
        self.info_label = QtWidgets.QLabel(self.client_frame)
        self.info_label.setMinimumSize(QtCore.QSize(300, 0))
        font = QtGui.QFont()
        font.setFamily("Segoe UI")
        font.setPointSize(9)
        font.setBold(True)
        font.setWeight(75)
        self.info_label.setFont(font)
        self.info_label.setStyleSheet("color: rgb(238, 238, 238);")
        self.info_label.setText("")
        self.info_label.setTextInteractionFlags(QtCore.Qt.LinksAccessibleByMouse|QtCore.Qt.TextSelectableByKeyboard|QtCore.Qt.TextSelectableByMouse)
        self.info_label.setObjectName("info_label")
        self.horizontalLayout_2.addWidget(self.info_label)
        self.verticalLayout_2.addWidget(self.client_frame)
        self.table_frame = QtWidgets.QFrame(self.view)
        self.table_frame.setStyleSheet("background-color: rgb(238, 238, 238);")
        self.table_frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.table_frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.table_frame.setObjectName("table_frame")
        self.gridLayout = QtWidgets.QGridLayout(self.table_frame)
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.gridLayout.setHorizontalSpacing(0)
        self.gridLayout.setVerticalSpacing(3)
        self.gridLayout.setObjectName("gridLayout")
        self.budget_table = QtWidgets.QTableWidget(self.table_frame)
        self.budget_table.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.budget_table.setStyleSheet("QTableWidget {\n"
"    gridline-color: #c0c0c0; /* Light grey grid lines */\n"
"}\n"
"\n"
"QTableWidget::item {\n"
"    padding: 2px; /* Adjust padding for cell content */\n"
"    border-color: #d0d0d0; /* Slightly darker border for cells */\n"
"}\n"
"\n"
"QTableHeader::section {\n"
"    background-color: qlineargradient(x1:0, y1:0, x2:0, y2:1,\n"
"                      stop:0 rgb(90, 133, 250), stop:1 rgb(70, 113, 230));\n"
"    color: rgb(255, 255, 255); /* White text in header */\n"
"    padding: 5px;\n"
"    border: 1px solid #505050; /* Darker border for header */\n"
"    text-align: center;\n"
"}\n"
"\n"
"QTableWidget::item:selected {\n"
"    background-color: rgb(120, 160, 230); /* Lighter blue for selected items */\n"
"    color: rgb(255, 255, 255); /* White text for selected items */\n"
"}\n"
"\n"
"/* Alternating row colors for better readability */\n"
"QTableWidget QTableWidget::item:alternate {\n"
"    background-color: rgb(240, 240, 240); /* Slightly off-white for alternate rows */\n"
"}")
        self.budget_table.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.budget_table.setSizeAdjustPolicy(QtWidgets.QAbstractScrollArea.AdjustToContents)
        self.budget_table.setEditTriggers(QtWidgets.QAbstractItemView.AnyKeyPressed|QtWidgets.QAbstractItemView.DoubleClicked|QtWidgets.QAbstractItemView.EditKeyPressed)
        self.budget_table.setAlternatingRowColors(True)
        self.budget_table.setSelectionMode(QtWidgets.QAbstractItemView.MultiSelection)
        self.budget_table.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectItems)
        self.budget_table.setTextElideMode(QtCore.Qt.ElideMiddle)
        self.budget_table.setShowGrid(True)
        self.budget_table.setGridStyle(QtCore.Qt.SolidLine)
        self.budget_table.setWordWrap(True)
        self.budget_table.setCornerButtonEnabled(True)
        self.budget_table.setRowCount(0)
        self.budget_table.setColumnCount(14)
        self.budget_table.setObjectName("budget_table")
        item = QtWidgets.QTableWidgetItem()
        font = QtGui.QFont()
        font.setFamily("Segoe UI")
        item.setFont(font)
        self.budget_table.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.budget_table.setHorizontalHeaderItem(1, item)
        item = QtWidgets.QTableWidgetItem()
        self.budget_table.setHorizontalHeaderItem(2, item)
        item = QtWidgets.QTableWidgetItem()
        item.setTextAlignment(QtCore.Qt.AlignCenter)
        font = QtGui.QFont()
        font.setFamily("Segoe UI")
        item.setFont(font)
        self.budget_table.setHorizontalHeaderItem(3, item)
        item = QtWidgets.QTableWidgetItem()
        self.budget_table.setHorizontalHeaderItem(4, item)
        item = QtWidgets.QTableWidgetItem()
        item.setTextAlignment(QtCore.Qt.AlignCenter)
        font = QtGui.QFont()
        font.setFamily("Segoe UI")
        item.setFont(font)
        self.budget_table.setHorizontalHeaderItem(5, item)
        item = QtWidgets.QTableWidgetItem()
        font = QtGui.QFont()
        font.setFamily("Segoe UI")
        item.setFont(font)
        self.budget_table.setHorizontalHeaderItem(6, item)
        item = QtWidgets.QTableWidgetItem()
        font = QtGui.QFont()
        font.setFamily("Segoe UI")
        item.setFont(font)
        self.budget_table.setHorizontalHeaderItem(7, item)
        item = QtWidgets.QTableWidgetItem()
        font = QtGui.QFont()
        font.setFamily("Segoe UI")
        item.setFont(font)
        self.budget_table.setHorizontalHeaderItem(8, item)
        item = QtWidgets.QTableWidgetItem()
        font = QtGui.QFont()
        font.setFamily("Segoe UI")
        item.setFont(font)
        self.budget_table.setHorizontalHeaderItem(9, item)
        item = QtWidgets.QTableWidgetItem()
        self.budget_table.setHorizontalHeaderItem(10, item)
        item = QtWidgets.QTableWidgetItem()
        font = QtGui.QFont()
        font.setFamily("Segoe UI")
        item.setFont(font)
        self.budget_table.setHorizontalHeaderItem(11, item)
        item = QtWidgets.QTableWidgetItem()
        self.budget_table.setHorizontalHeaderItem(12, item)
        item = QtWidgets.QTableWidgetItem()
        self.budget_table.setHorizontalHeaderItem(13, item)
        self.budget_table.horizontalHeader().setCascadingSectionResizes(True)
        self.budget_table.horizontalHeader().setDefaultSectionSize(130)
        self.budget_table.horizontalHeader().setMinimumSectionSize(130)
        self.budget_table.verticalHeader().setCascadingSectionResizes(True)
        self.gridLayout.addWidget(self.budget_table, 1, 1, 1, 1)
        self.frame_2 = QtWidgets.QFrame(self.table_frame)
        self.frame_2.setMinimumSize(QtCore.QSize(0, 35))
        self.frame_2.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_2.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_2.setObjectName("frame_2")
        self.horizontalLayout_5 = QtWidgets.QHBoxLayout(self.frame_2)
        self.horizontalLayout_5.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_5.setSpacing(0)
        self.horizontalLayout_5.setObjectName("horizontalLayout_5")
        spacerItem2 = QtWidgets.QSpacerItem(721, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_5.addItem(spacerItem2)
        self.save_progressbar = QtWidgets.QProgressBar(self.frame_2)
        self.save_progressbar.setMaximumSize(QtCore.QSize(150, 20))
        self.save_progressbar.setStyleSheet("QProgressBar {\n"
"    border: 1px solid rgb(140, 180, 250);\n"
"    border-radius: 4px;\n"
"    text-align: center;\n"
"    background-color: rgb(255, 255, 255);\n"
"}\n"
"\n"
"QProgressBar::chunk {\n"
"    background-color: qlineargradient(x1:0, y1:0, x2:0, y2:1,\n"
"                      stop:0 rgb(90, 133, 250), stop:1 rgb(70, 113, 230));\n"
"    border-radius: 3px; /* Slightly less than the progress bar for a nice effect */\n"
"}\n"
"\n"
"QProgressBar::chunk:indeterminate {\n"
"    background-color: qlineargradient(x1:0, y1:0, x2:1, y2:0,\n"
"                      stop:0 rgb(90, 133, 250), stop:1 rgb(70, 113, 230));\n"
"}")
        self.save_progressbar.setMaximum(0)
        self.save_progressbar.setProperty("value", 0)
        self.save_progressbar.setTextVisible(False)
        self.save_progressbar.setObjectName("save_progressbar")
        self.horizontalLayout_5.addWidget(self.save_progressbar)
        spacerItem3 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_5.addItem(spacerItem3)
        self.save_table_button = QtWidgets.QPushButton(self.frame_2)
        self.save_table_button.setMinimumSize(QtCore.QSize(50, 30))
        self.save_table_button.setStyleSheet("QPushButton {\n"
"    background-color: qlineargradient(x1:0, y1:0, x2:0, y2:1,\n"
"                      stop:0 rgb(90, 133, 250), stop:1 rgb(70, 113, 230));\n"
"    color: rgb(255, 255, 255);\n"
"    border-top: 1px solid rgb(140, 180, 250);\n"
"    border-left: 1px solid rgb(140, 180, 250);\n"
"    border-bottom: 1px solid rgb(30, 53, 190);\n"
"    border-right: 1px solid rgb(30, 53, 190);\n"
"    border-radius: 4px;\n"
"    box-shadow: 5px 5px 10px rgba(0, 0, 0, 0.3);\n"
"    padding: 5px 15px; /* Adjust padding if needed */\n"
"    text-align: center;\n"
"}\n"
"\n"
"QPushButton:pressed {\n"
"    background-color: qlineargradient(x1:0, y1:0, x2:0, y2:1,\n"
"                      stop:0 rgb(60, 93, 210), stop:1 rgb(50, 83, 200));\n"
"    box-shadow: 2px 2px 5px rgba(0, 0, 0, 0.2); /* Smaller shadow for pressed state */\n"
"    border-top: 1px solid rgb(120, 160, 230);\n"
"    border-bottom: 1px solid rgb(20, 43, 180);\n"
"}\n"
"")
        self.save_table_button.setObjectName("save_table_button")
        self.horizontalLayout_5.addWidget(self.save_table_button)
        self.gridLayout.addWidget(self.frame_2, 2, 1, 1, 1)
        self.frame = QtWidgets.QFrame(self.table_frame)
        self.frame.setMinimumSize(QtCore.QSize(0, 50))
        self.frame.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.frame.setFrameShadow(QtWidgets.QFrame.Plain)
        self.frame.setObjectName("frame")
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout(self.frame)
        self.horizontalLayout_3.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_3.setSpacing(0)
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.label = QtWidgets.QLabel(self.frame)
        font = QtGui.QFont()
        font.setFamily("Segoe UI")
        font.setPointSize(9)
        font.setBold(False)
        font.setWeight(50)
        self.label.setFont(font)
        self.label.setObjectName("label")
        self.horizontalLayout_3.addWidget(self.label)
        self.filial_select = QtWidgets.QComboBox(self.frame)
        self.filial_select.setStyleSheet("QComboBox {\n"
"    background-color: qlineargradient(x1:0, y1:0, x2:0, y2:1,\n"
"                      stop:0 rgb(90, 133, 250), stop:1 rgb(70, 113, 230));\n"
"    color: rgb(255, 255, 255);\n"
"    border: 1px solid rgb(140, 180, 250);\n"
"    border-radius: 4px;\n"
"    padding: 5px 15px;\n"
"}\n"
"\n"
"QComboBox:hover {\n"
"    border: 1px solid rgb(160, 200, 255);\n"
"}\n"
"\n"
"QComboBox::drop-down {\n"
"    subcontrol-origin: padding;\n"
"    subcontrol-position: top right;\n"
"    width: 15px;\n"
"    border-left: 1px solid rgb(140, 180, 250);\n"
"}\n"
"\n"
"QComboBox::down-arrow {\n"
"    image: url(:/dependencies/seta.png);\n"
"    width: 20px;\n"
"    height: 20px;\n"
"}\n"
"\n"
"QComboBox QAbstractItemView {\n"
"    border: 2px solid rgb(90, 133, 250);\n"
"    selection-background-color: rgb(70, 113, 230); /* Blue background */\n"
"    color: rgb(0, 0, 0); /* White text */\n"
"}\n"
"")
        self.filial_select.setSizeAdjustPolicy(QtWidgets.QComboBox.AdjustToContentsOnFirstShow)
        self.filial_select.setObjectName("filial_select")
        self.filial_select.addItem("")
        self.filial_select.setItemText(0, "")
        self.filial_select.addItem("")
        self.filial_select.addItem("")
        self.filial_select.addItem("")
        self.filial_select.addItem("")
        self.horizontalLayout_3.addWidget(self.filial_select)
        spacerItem4 = QtWidgets.QSpacerItem(825, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_3.addItem(spacerItem4)
        self.buttons_frame = QtWidgets.QFrame(self.frame)
        self.buttons_frame.setMinimumSize(QtCore.QSize(150, 0))
        self.buttons_frame.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.buttons_frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.buttons_frame.setObjectName("buttons_frame")
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout(self.buttons_frame)
        self.horizontalLayout_4.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_4.setSpacing(0)
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.add_line_button = QtWidgets.QPushButton(self.buttons_frame)
        self.add_line_button.setMinimumSize(QtCore.QSize(0, 0))
        self.add_line_button.setMaximumSize(QtCore.QSize(30, 16777215))
        self.add_line_button.setStyleSheet("image: url(:/dependencies/mais.png);")
        self.add_line_button.setText("")
        self.add_line_button.setFlat(True)
        self.add_line_button.setObjectName("add_line_button")
        self.horizontalLayout_4.addWidget(self.add_line_button)
        self.remove_line_button = QtWidgets.QPushButton(self.buttons_frame)
        self.remove_line_button.setMaximumSize(QtCore.QSize(30, 16777215))
        self.remove_line_button.setStyleSheet("image: url(:/dependencies/menos.png);")
        self.remove_line_button.setText("")
        self.remove_line_button.setFlat(True)
        self.remove_line_button.setObjectName("remove_line_button")
        self.horizontalLayout_4.addWidget(self.remove_line_button)
        self.horizontalLayout_3.addWidget(self.buttons_frame)
        self.gridLayout.addWidget(self.frame, 0, 1, 1, 1)
        spacerItem5 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem5, 1, 0, 1, 1)
        spacerItem6 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem6, 1, 2, 1, 1)
        self.verticalLayout_2.addWidget(self.table_frame)
        self.verticalLayout.addWidget(self.view)
        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Orçamentos"))
        self.title.setText(_translate("MainWindow", "ORÇAMENTOS"))
        self.client_label.setText(_translate("MainWindow", "Cliente:"))
        self.search_button.setText(_translate("MainWindow", "Buscar"))
        self.budget_table.setSortingEnabled(True)
        item = self.budget_table.horizontalHeaderItem(0)
        item.setText(_translate("MainWindow", "Código"))
        item = self.budget_table.horizontalHeaderItem(1)
        item.setText(_translate("MainWindow", "Agrupamento"))
        item = self.budget_table.horizontalHeaderItem(2)
        item.setText(_translate("MainWindow", "Descrição"))
        item = self.budget_table.horizontalHeaderItem(3)
        item.setText(_translate("MainWindow", "Quantidade"))
        item = self.budget_table.horizontalHeaderItem(4)
        item.setText(_translate("MainWindow", "Quantidade disponível"))
        item = self.budget_table.horizontalHeaderItem(5)
        item.setText(_translate("MainWindow", "Custo"))
        item = self.budget_table.horizontalHeaderItem(6)
        item.setText(_translate("MainWindow", "Preço calculado"))
        item = self.budget_table.horizontalHeaderItem(7)
        item.setText(_translate("MainWindow", "U.V. Geral"))
        item = self.budget_table.horizontalHeaderItem(8)
        item.setText(_translate("MainWindow", "U.V. Cliente"))
        item = self.budget_table.horizontalHeaderItem(9)
        item.setText(_translate("MainWindow", "Desconto(%)"))
        item = self.budget_table.horizontalHeaderItem(10)
        item.setText(_translate("MainWindow", "Over(%)"))
        item = self.budget_table.horizontalHeaderItem(11)
        item.setText(_translate("MainWindow", "Margem(%)"))
        item = self.budget_table.horizontalHeaderItem(12)
        item.setText(_translate("MainWindow", "Preço unitário"))
        item = self.budget_table.horizontalHeaderItem(13)
        item.setText(_translate("MainWindow", "Preço final"))
        self.save_table_button.setText(_translate("MainWindow", "Salvar"))
        self.label.setText(_translate("MainWindow", "Filial:  "))
        self.filial_select.setItemText(1, _translate("MainWindow", "Matriz - MG"))
        self.filial_select.setItemText(2, _translate("MainWindow", "Poconé - MT"))
        self.filial_select.setItemText(3, _translate("MainWindow", "Cariacica - ES"))
        self.filial_select.setItemText(4, _translate("MainWindow", "Parauapebas - PA"))
from . import resources_rc
