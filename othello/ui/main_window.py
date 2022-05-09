from typing import Optional

# Fiona need to be imported before geopandas to avoid a current bug
# https://github.com/Toblerity/Fiona/issues/944
import fiona

from PySide2 import QtCore, QtWidgets
from PySide2.QtWidgets import QWidget

from othello.macbeth.parser import MacbethParser
from othello.ui.aggregate import AggregateTab
from othello.ui.criteria import CriteriaTab


class MainWindow(QWidget):

    def __init__(self):
        super(MainWindow, self).__init__()

        self.macbeth_parser: Optional[MacbethParser] = None

        self.setObjectName('App')
        self.resize(800, 600)

        self.tabs = QtWidgets.QTabWidget(self)
        self.tabs.setGeometry(QtCore.QRect(10, 10, 781, 581))
        self.tabs.setObjectName('tabs')

        self.tab_criteria_macbeth = CriteriaTab(self)
        self.tab_aggregate = AggregateTab(self)

        self.tabs.addTab(self.tab_criteria_macbeth, '')
        self.tabs.addTab(self.tab_aggregate, '')

        self.set_labels(self)
        self.tabs.setCurrentIndex(0)

        QtCore.QMetaObject.connectSlotsByName(self)

    def set_labels(self, app):
        app.setWindowTitle('Othello')

        self.tabs.setTabText(self.tabs.indexOf(self.tab_criteria_macbeth), 'MacBeth')
        self.tabs.setTabText(self.tabs.indexOf(self.tab_aggregate), 'Aggregate')
