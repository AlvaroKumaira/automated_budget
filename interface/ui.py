import os
from PyQt5.QtWidgets import QMainWindow, QDesktopWidget, QWidget, QFileDialog, QTableWidget
from PyQt5.QtCore import QPropertyAnimation, Qt, QPoint
from .design import Ui_MainWindow
from .logic import MainLogic, TableLogic


class MainWindow(QMainWindow, Ui_MainWindow):

    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.logic = MainLogic(self)
        self.table_logic = TableLogic(self)
        self.save_progressbar.hide()
        self.budget_table.setSelectionBehavior(QTableWidget.SelectItems)
        self.budget_table.setSelectionMode(QTableWidget.MultiSelection)
        self.budget_table.horizontalHeader().setSectionsClickable(False)

        self.showMaximized()

