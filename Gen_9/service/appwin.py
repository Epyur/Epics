import sys
from openpyxl import load_workbook
import pandas as pd
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QMessageBox, QMainWindow, QApplication
from PyQt6 import QtCore, QtGui, QtWidgets
from pyasn1_modules.rfc5280 import id_qt

from Gen_9.service.body import filtered_work_data
from Gen_9.service.passw.passw import mail_login, mail_pass, tracker_adress
from Gen_9.service.rout_map import ns, closedtasks, alltasks
from Gen_9.service.sender import NotificationSender


class Ui_LPIApp(object):
    def setupUi(self, LPIApp):
        LPIApp.setObjectName("LPIApp")
        LPIApp.resize(1123, 950)
        palette = QtGui.QPalette()
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.BrushStyle.SolidPattern)
        palette.setBrush(QtGui.QPalette.ColorGroup.Active, QtGui.QPalette.ColorRole.Base, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.BrushStyle.SolidPattern)
        palette.setBrush(QtGui.QPalette.ColorGroup.Active, QtGui.QPalette.ColorRole.Window, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.BrushStyle.SolidPattern)
        palette.setBrush(QtGui.QPalette.ColorGroup.Inactive, QtGui.QPalette.ColorRole.Base, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.BrushStyle.SolidPattern)
        palette.setBrush(QtGui.QPalette.ColorGroup.Inactive, QtGui.QPalette.ColorRole.Window, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.BrushStyle.SolidPattern)
        palette.setBrush(QtGui.QPalette.ColorGroup.Disabled, QtGui.QPalette.ColorRole.Base, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.BrushStyle.SolidPattern)
        palette.setBrush(QtGui.QPalette.ColorGroup.Disabled, QtGui.QPalette.ColorRole.Window, brush)
        LPIApp.setPalette(palette)
        self.listWidget = QtWidgets.QListWidget(parent=LPIApp)
        self.listWidget.setGeometry(QtCore.QRect(0, 160, 290, 750))
        self.listWidget.setMinimumSize(QtCore.QSize(290, 750))
        self.listWidget.setObjectName("listWidget")
        self.label = QtWidgets.QLabel(parent=LPIApp)
        self.label.setGeometry(QtCore.QRect(460, 20, 631, 71))
        palette = QtGui.QPalette()
        brush = QtGui.QBrush(QtGui.QColor(255, 0, 0))
        brush.setStyle(QtCore.Qt.BrushStyle.SolidPattern)
        palette.setBrush(QtGui.QPalette.ColorGroup.Active, QtGui.QPalette.ColorRole.WindowText, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 0, 0))
        brush.setStyle(QtCore.Qt.BrushStyle.SolidPattern)
        palette.setBrush(QtGui.QPalette.ColorGroup.Inactive, QtGui.QPalette.ColorRole.WindowText, brush)
        brush = QtGui.QBrush(QtGui.QColor(120, 120, 120))
        brush.setStyle(QtCore.Qt.BrushStyle.SolidPattern)
        palette.setBrush(QtGui.QPalette.ColorGroup.Disabled, QtGui.QPalette.ColorRole.WindowText, brush)
        self.label.setPalette(palette)
        font = QtGui.QFont()
        font.setPointSize(17)
        font.setBold(True)
        font.setItalic(True)
        font.setWeight(75)
        self.label.setFont(font)
        self.label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.label.setObjectName("label")
        self.line = QtWidgets.QFrame(parent=LPIApp)
        self.line.setGeometry(QtCore.QRect(290, 113, 821, 16))
        self.line.setFrameShape(QtWidgets.QFrame.Shape.HLine)
        self.line.setFrameShadow(QtWidgets.QFrame.Shadow.Sunken)
        self.line.setObjectName("line")
        self.label_2 = QtWidgets.QLabel(parent=LPIApp)
        self.label_2.setGeometry(QtCore.QRect(430, 120, 541, 21))
        font = QtGui.QFont()
        font.setFamily("Times New Roman")
        font.setPointSize(14)
        font.setBold(True)
        font.setWeight(75)
        self.label_2.setFont(font)
        self.label_2.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.label_2.setObjectName("label_2")
        self.layoutWidget = QtWidgets.QWidget(parent=LPIApp)
        self.layoutWidget.setGeometry(QtCore.QRect(310, 290, 371, 31))
        self.layoutWidget.setObjectName("layoutWidget")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout(self.layoutWidget)
        self.horizontalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.label_4 = QtWidgets.QLabel(parent=self.layoutWidget)
        self.label_4.setMaximumSize(QtCore.QSize(106, 29))
        font = QtGui.QFont()
        font.setFamily("Times New Roman")
        font.setPointSize(11)
        self.label_4.setFont(font)
        self.label_4.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.label_4.setObjectName("label_4")
        self.horizontalLayout_2.addWidget(self.label_4)
        self.CustMailWidget = QtWidgets.QPlainTextEdit(parent=self.layoutWidget)
        self.CustMailWidget.setMaximumSize(QtCore.QSize(257, 29))
        font = QtGui.QFont()
        font.setFamily("Times New Roman")
        font.setPointSize(11)
        self.CustMailWidget.setFont(font)
        self.CustMailWidget.setAcceptDrops(False)
        self.CustMailWidget.setReadOnly(True)
        self.CustMailWidget.setObjectName("CustMailWidget")
        self.horizontalLayout_2.addWidget(self.CustMailWidget)
        self.layoutWidget_2 = QtWidgets.QWidget(parent=LPIApp)
        self.layoutWidget_2.setGeometry(QtCore.QRect(510, 170, 331, 31))
        self.layoutWidget_2.setObjectName("layoutWidget_2")
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout(self.layoutWidget_2)
        self.horizontalLayout_3.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.label_6 = QtWidgets.QLabel(parent=self.layoutWidget_2)
        self.label_6.setMaximumSize(QtCore.QSize(160, 29))
        font = QtGui.QFont()
        font.setFamily("Times New Roman")
        font.setPointSize(11)
        self.label_6.setFont(font)
        self.label_6.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.label_6.setObjectName("label_6")
        self.horizontalLayout_3.addWidget(self.label_6)
        self.DateINWidget = QtWidgets.QPlainTextEdit(parent=self.layoutWidget_2)
        self.DateINWidget.setMaximumSize(QtCore.QSize(163, 29))
        font = QtGui.QFont()
        font.setFamily("Times New Roman")
        font.setPointSize(11)
        self.DateINWidget.setFont(font)
        self.DateINWidget.setAcceptDrops(False)
        self.DateINWidget.setReadOnly(True)
        self.DateINWidget.setObjectName("DateINWidget")
        self.horizontalLayout_3.addWidget(self.DateINWidget)
        self.layoutWidget_3 = QtWidgets.QWidget(parent=LPIApp)
        self.layoutWidget_3.setGeometry(QtCore.QRect(700, 290, 371, 31))
        self.layoutWidget_3.setObjectName("layoutWidget_3")
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout(self.layoutWidget_3)
        self.horizontalLayout_4.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.label_7 = QtWidgets.QLabel(parent=self.layoutWidget_3)
        self.label_7.setMaximumSize(QtCore.QSize(118, 29))
        font = QtGui.QFont()
        font.setFamily("Times New Roman")
        font.setPointSize(11)
        self.label_7.setFont(font)
        self.label_7.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.label_7.setObjectName("label_7")
        self.horizontalLayout_4.addWidget(self.label_7)
        self.CustTelWidget = QtWidgets.QPlainTextEdit(parent=self.layoutWidget_3)
        self.CustTelWidget.setMaximumSize(QtCore.QSize(245, 29))
        font = QtGui.QFont()
        font.setFamily("Times New Roman")
        font.setPointSize(11)
        self.CustTelWidget.setFont(font)
        self.CustTelWidget.setAcceptDrops(False)
        self.CustTelWidget.setReadOnly(True)
        self.CustTelWidget.setObjectName("CustTelWidget")
        self.horizontalLayout_4.addWidget(self.CustTelWidget)
        self.layoutWidget_4 = QtWidgets.QWidget(parent=LPIApp)
        self.layoutWidget_4.setGeometry(QtCore.QRect(310, 250, 611, 31))
        self.layoutWidget_4.setObjectName("layoutWidget_4")
        self.horizontalLayout_5 = QtWidgets.QHBoxLayout(self.layoutWidget_4)
        self.horizontalLayout_5.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_5.setObjectName("horizontalLayout_5")
        self.label_8 = QtWidgets.QLabel(parent=self.layoutWidget_4)
        self.label_8.setMinimumSize(QtCore.QSize(106, 0))
        self.label_8.setMaximumSize(QtCore.QSize(106, 29))
        font = QtGui.QFont()
        font.setFamily("Times New Roman")
        font.setPointSize(11)
        self.label_8.setFont(font)
        self.label_8.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.label_8.setObjectName("label_8")
        self.horizontalLayout_5.addWidget(self.label_8)
        self.CustNameWidget = QtWidgets.QPlainTextEdit(parent=self.layoutWidget_4)
        self.CustNameWidget.setMaximumSize(QtCore.QSize(500, 29))
        font = QtGui.QFont()
        font.setFamily("Times New Roman")
        font.setPointSize(11)
        self.CustNameWidget.setFont(font)
        self.CustNameWidget.setAcceptDrops(False)
        self.CustNameWidget.setReadOnly(True)
        self.CustNameWidget.setObjectName("CustNameWidget")
        self.horizontalLayout_5.addWidget(self.CustNameWidget)
        self.layoutWidget_5 = QtWidgets.QWidget(parent=LPIApp)
        self.layoutWidget_5.setGeometry(QtCore.QRect(420, 340, 561, 32))
        self.layoutWidget_5.setObjectName("layoutWidget_5")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.layoutWidget_5)
        self.verticalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.label_9 = QtWidgets.QLabel(parent=self.layoutWidget_5)
        self.label_9.setMaximumSize(QtCore.QSize(560, 21))
        font = QtGui.QFont()
        font.setFamily("Times New Roman")
        font.setPointSize(14)
        font.setBold(False)
        font.setItalic(True)
        font.setWeight(50)
        self.label_9.setFont(font)
        self.label_9.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.label_9.setObjectName("label_9")
        self.verticalLayout_2.addWidget(self.label_9)
        self.line_3 = QtWidgets.QFrame(parent=self.layoutWidget_5)
        self.line_3.setFrameShape(QtWidgets.QFrame.Shape.HLine)
        self.line_3.setFrameShadow(QtWidgets.QFrame.Shadow.Sunken)
        self.line_3.setObjectName("line_3")
        self.verticalLayout_2.addWidget(self.line_3)
        self.layoutWidget_6 = QtWidgets.QWidget(parent=LPIApp)
        self.layoutWidget_6.setGeometry(QtCore.QRect(310, 380, 201, 41))
        self.layoutWidget_6.setObjectName("layoutWidget_6")
        self.horizontalLayout_6 = QtWidgets.QHBoxLayout(self.layoutWidget_6)
        self.horizontalLayout_6.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_6.setObjectName("horizontalLayout_6")
        self.label_10 = QtWidgets.QLabel(parent=self.layoutWidget_6)
        font = QtGui.QFont()
        font.setFamily("Times New Roman")
        font.setPointSize(11)
        self.label_10.setFont(font)
        self.label_10.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.label_10.setObjectName("label_10")
        self.horizontalLayout_6.addWidget(self.label_10)
        self.EknNumWidget = QtWidgets.QPlainTextEdit(parent=self.layoutWidget_6)
        self.EknNumWidget.setMaximumSize(QtCore.QSize(160, 29))
        font = QtGui.QFont()
        font.setFamily("Times New Roman")
        font.setPointSize(11)
        self.EknNumWidget.setFont(font)
        self.EknNumWidget.setAcceptDrops(False)
        self.EknNumWidget.setReadOnly(True)
        self.EknNumWidget.setObjectName("EknNumWidget")
        self.horizontalLayout_6.addWidget(self.EknNumWidget)
        self.layoutWidget_7 = QtWidgets.QWidget(parent=LPIApp)
        self.layoutWidget_7.setGeometry(QtCore.QRect(520, 380, 591, 41))
        self.layoutWidget_7.setObjectName("layoutWidget_7")
        self.horizontalLayout_7 = QtWidgets.QHBoxLayout(self.layoutWidget_7)
        self.horizontalLayout_7.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_7.setObjectName("horizontalLayout_7")
        self.label_11 = QtWidgets.QLabel(parent=self.layoutWidget_7)
        font = QtGui.QFont()
        font.setFamily("Times New Roman")
        font.setPointSize(11)
        self.label_11.setFont(font)
        self.label_11.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.label_11.setObjectName("label_11")
        self.horizontalLayout_7.addWidget(self.label_11)
        self.IdentNumWidget = QtWidgets.QPlainTextEdit(parent=self.layoutWidget_7)
        self.IdentNumWidget.setMaximumSize(QtCore.QSize(400, 29))
        font = QtGui.QFont()
        font.setFamily("Times New Roman")
        font.setPointSize(11)
        self.IdentNumWidget.setFont(font)
        self.IdentNumWidget.setAcceptDrops(False)
        self.IdentNumWidget.setReadOnly(True)
        self.IdentNumWidget.setObjectName("IdentNumWidget")
        self.horizontalLayout_7.addWidget(self.IdentNumWidget)
        self.layoutWidget_8 = QtWidgets.QWidget(parent=LPIApp)
        self.layoutWidget_8.setGeometry(QtCore.QRect(420, 480, 561, 32))
        self.layoutWidget_8.setObjectName("layoutWidget_8")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout(self.layoutWidget_8)
        self.verticalLayout_3.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.label_12 = QtWidgets.QLabel(parent=self.layoutWidget_8)
        self.label_12.setMaximumSize(QtCore.QSize(560, 21))
        font = QtGui.QFont()
        font.setFamily("Times New Roman")
        font.setPointSize(14)
        font.setBold(False)
        font.setItalic(True)
        font.setWeight(50)
        self.label_12.setFont(font)
        self.label_12.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.label_12.setObjectName("label_12")
        self.verticalLayout_3.addWidget(self.label_12)
        self.line_4 = QtWidgets.QFrame(parent=self.layoutWidget_8)
        self.line_4.setFrameShape(QtWidgets.QFrame.Shape.HLine)
        self.line_4.setFrameShadow(QtWidgets.QFrame.Shadow.Sunken)
        self.line_4.setObjectName("line_4")
        self.verticalLayout_3.addWidget(self.line_4)
        self.layoutWidget_9 = QtWidgets.QWidget(parent=LPIApp)
        self.layoutWidget_9.setGeometry(QtCore.QRect(310, 420, 801, 31))
        self.layoutWidget_9.setObjectName("layoutWidget_9")
        self.horizontalLayout_8 = QtWidgets.QHBoxLayout(self.layoutWidget_9)
        self.horizontalLayout_8.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_8.setObjectName("horizontalLayout_8")
        self.label_13 = QtWidgets.QLabel(parent=self.layoutWidget_9)
        self.label_13.setMaximumSize(QtCore.QSize(132, 29))
        font = QtGui.QFont()
        font.setFamily("Times New Roman")
        font.setPointSize(11)
        self.label_13.setFont(font)
        self.label_13.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.label_13.setObjectName("label_13")
        self.horizontalLayout_8.addWidget(self.label_13)
        self.EknNum_2 = QtWidgets.QPlainTextEdit(parent=self.layoutWidget_9)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.EknNum_2.sizePolicy().hasHeightForWidth())
        self.EknNum_2.setSizePolicy(sizePolicy)
        self.EknNum_2.setMaximumSize(QtCore.QSize(661, 29))
        font = QtGui.QFont()
        font.setFamily("Times New Roman")
        font.setPointSize(11)
        self.EknNum_2.setFont(font)
        self.EknNum_2.setAcceptDrops(False)
        self.EknNum_2.setReadOnly(True)
        self.EknNum_2.setObjectName("EknNum_2")
        self.horizontalLayout_8.addWidget(self.EknNum_2)
        self.layoutWidget1 = QtWidgets.QWidget(parent=LPIApp)
        self.layoutWidget1.setGeometry(QtCore.QRect(310, 170, 185, 31))
        self.layoutWidget1.setObjectName("layoutWidget1")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.layoutWidget1)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.label_3 = QtWidgets.QLabel(parent=self.layoutWidget1)
        self.label_3.setMinimumSize(QtCore.QSize(106, 29))
        self.label_3.setMaximumSize(QtCore.QSize(106, 29))
        font = QtGui.QFont()
        font.setFamily("Times New Roman")
        font.setPointSize(11)
        self.label_3.setFont(font)
        self.label_3.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.label_3.setObjectName("label_3")
        self.horizontalLayout.addWidget(self.label_3)
        self.IncIDWidjget = QtWidgets.QPlainTextEdit(parent=self.layoutWidget1)
        self.IncIDWidjget.setMaximumSize(QtCore.QSize(71, 29))
        font = QtGui.QFont()
        font.setFamily("Times New Roman")
        font.setPointSize(11)
        self.IncIDWidjget.setFont(font)
        self.IncIDWidjget.setAcceptDrops(False)
        self.IncIDWidjget.setReadOnly(True)
        self.IncIDWidjget.setObjectName("IncIDWidjget")
        self.horizontalLayout.addWidget(self.IncIDWidjget)
        self.layoutWidget2 = QtWidgets.QWidget(parent=LPIApp)
        self.layoutWidget2.setGeometry(QtCore.QRect(420, 220, 561, 32))
        self.layoutWidget2.setObjectName("layoutWidget2")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.layoutWidget2)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.label_5 = QtWidgets.QLabel(parent=self.layoutWidget2)
        self.label_5.setMaximumSize(QtCore.QSize(560, 21))
        font = QtGui.QFont()
        font.setFamily("Times New Roman")
        font.setPointSize(14)
        font.setBold(False)
        font.setItalic(True)
        font.setWeight(50)
        self.label_5.setFont(font)
        self.label_5.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.label_5.setObjectName("label_5")
        self.verticalLayout.addWidget(self.label_5)
        self.line_2 = QtWidgets.QFrame(parent=self.layoutWidget2)
        self.line_2.setFrameShape(QtWidgets.QFrame.Shape.HLine)
        self.line_2.setFrameShadow(QtWidgets.QFrame.Shadow.Sunken)
        self.line_2.setObjectName("line_2")
        self.verticalLayout.addWidget(self.line_2)
        self.AdditionalnfoWidget = QtWidgets.QPlainTextEdit(parent=LPIApp)
        self.AdditionalnfoWidget.setGeometry(QtCore.QRect(320, 670, 780, 240))
        self.AdditionalnfoWidget.setMaximumSize(QtCore.QSize(780, 270))
        self.AdditionalnfoWidget.setReadOnly(True)
        self.AdditionalnfoWidget.setObjectName("AdditionalnfoWidget")
        self.layoutWidget_10 = QtWidgets.QWidget(parent=LPIApp)
        self.layoutWidget_10.setGeometry(QtCore.QRect(420, 620, 561, 32))
        self.layoutWidget_10.setObjectName("layoutWidget_10")
        self.verticalLayout_4 = QtWidgets.QVBoxLayout(self.layoutWidget_10)
        self.verticalLayout_4.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        self.label_14 = QtWidgets.QLabel(parent=self.layoutWidget_10)
        self.label_14.setMaximumSize(QtCore.QSize(560, 21))
        font = QtGui.QFont()
        font.setFamily("Times New Roman")
        font.setPointSize(14)
        font.setBold(False)
        font.setItalic(True)
        font.setWeight(50)
        self.label_14.setFont(font)
        self.label_14.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.label_14.setObjectName("label_14")
        self.verticalLayout_4.addWidget(self.label_14)
        self.line_5 = QtWidgets.QFrame(parent=self.layoutWidget_10)
        self.line_5.setFrameShape(QtWidgets.QFrame.Shape.HLine)
        self.line_5.setFrameShadow(QtWidgets.QFrame.Shadow.Sunken)
        self.line_5.setObjectName("line_5")
        self.verticalLayout_4.addWidget(self.line_5)
        self.label_15 = QtWidgets.QLabel(parent=LPIApp)
        self.label_15.setGeometry(QtCore.QRect(0, 110, 290, 50))
        self.label_15.setMinimumSize(QtCore.QSize(290, 50))
        self.label_15.setMaximumSize(QtCore.QSize(290, 50))
        font = QtGui.QFont()
        font.setPointSize(13)
        font.setBold(True)
        font.setWeight(75)
        font.setStrikeOut(False)
        self.label_15.setFont(font)
        self.label_15.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.label_15.setObjectName("label_15")
        self.layoutWidget3 = QtWidgets.QWidget(parent=LPIApp)
        self.layoutWidget3.setGeometry(QtCore.QRect(320, 530, 674, 23))
        self.layoutWidget3.setObjectName("layoutWidget3")
        self.horizontalLayout_9 = QtWidgets.QHBoxLayout(self.layoutWidget3)
        self.horizontalLayout_9.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_9.setObjectName("horizontalLayout_9")
        self.CombGOSTButton = QtWidgets.QRadioButton(parent=self.layoutWidget3)
        self.CombGOSTButton.setMinimumSize(QtCore.QSize(220, 0))
        self.CombGOSTButton.setMaximumSize(QtCore.QSize(220, 21))
        font = QtGui.QFont()
        font.setPointSize(11)
        font.setUnderline(True)
        self.CombGOSTButton.setFont(font)
        self.CombGOSTButton.setCheckable(False)
        self.CombGOSTButton.setObjectName("CombGOSTButton")
        self.horizontalLayout_9.addWidget(self.CombGOSTButton)
        self.CombLookButton = QtWidgets.QPushButton(parent=self.layoutWidget3)
        self.CombLookButton.setMinimumSize(QtCore.QSize(220, 0))
        self.CombLookButton.setMaximumSize(QtCore.QSize(220, 21))
        self.CombLookButton.setObjectName("CombLookButton")
        self.horizontalLayout_9.addWidget(self.CombLookButton)
        self.CombAddButton = QtWidgets.QPushButton(parent=self.layoutWidget3)
        self.CombAddButton.setMinimumSize(QtCore.QSize(220, 0))
        self.CombAddButton.setMaximumSize(QtCore.QSize(220, 21))
        self.CombAddButton.setObjectName("CombAddButton")
        self.horizontalLayout_9.addWidget(self.CombAddButton)
        self.layoutWidget4 = QtWidgets.QWidget(parent=LPIApp)
        self.layoutWidget4.setGeometry(QtCore.QRect(320, 560, 674, 23))
        self.layoutWidget4.setObjectName("layoutWidget4")
        self.horizontalLayout_10 = QtWidgets.QHBoxLayout(self.layoutWidget4)
        self.horizontalLayout_10.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_10.setObjectName("horizontalLayout_10")
        self.FlamGOSTButton = QtWidgets.QRadioButton(parent=self.layoutWidget4)
        self.FlamGOSTButton.setMinimumSize(QtCore.QSize(220, 0))
        self.FlamGOSTButton.setMaximumSize(QtCore.QSize(220, 21))
        font = QtGui.QFont()
        font.setPointSize(11)
        font.setUnderline(True)
        self.FlamGOSTButton.setFont(font)
        self.FlamGOSTButton.setObjectName("FlamGOSTButton")
        self.horizontalLayout_10.addWidget(self.FlamGOSTButton)
        self.FlamLookButton = QtWidgets.QPushButton(parent=self.layoutWidget4)
        self.FlamLookButton.setMinimumSize(QtCore.QSize(220, 0))
        self.FlamLookButton.setMaximumSize(QtCore.QSize(220, 21))
        self.FlamLookButton.setObjectName("FlamLookButton")
        self.horizontalLayout_10.addWidget(self.FlamLookButton)
        self.FlamAddButton = QtWidgets.QPushButton(parent=self.layoutWidget4)
        self.FlamAddButton.setMinimumSize(QtCore.QSize(220, 0))
        self.FlamAddButton.setMaximumSize(QtCore.QSize(220, 21))
        self.FlamAddButton.setObjectName("FlamAddButton")
        self.horizontalLayout_10.addWidget(self.FlamAddButton)

        self.retranslateUi(LPIApp)
        QtCore.QMetaObject.connectSlotsByName(LPIApp)

    def retranslateUi(self, LPIApp):
        _translate = QtCore.QCoreApplication.translate
        LPIApp.setWindowTitle(_translate("LPIApp", "LPI TN"))
        self.label.setText(_translate("LPIApp", "Лаборатория пожарных испытаний СБЕ ПМиПИР"))
        self.label_2.setText(_translate("LPIApp", "Общая информация о заявке"))
        self.label_4.setText(_translate("LPIApp", "Почта заказчика"))
        self.label_6.setText(_translate("LPIApp", "Дата поступления заявки:"))
        self.label_7.setText(_translate("LPIApp", "Телефон заказчика"))
        self.label_8.setText(_translate("LPIApp", "ФИО заказчика:"))
        self.label_9.setText(_translate("LPIApp", "Информация об объекте исследования"))
        self.label_10.setText(_translate("LPIApp", "ЕКН:"))
        self.label_11.setText(_translate("LPIApp", "Идентификатор (№ партии):"))
        self.label_12.setText(_translate("LPIApp", "Информация о предмете исследования"))
        self.label_13.setText(_translate("LPIApp", "Название материала:"))
        self.label_3.setText(_translate("LPIApp", "№ заявки"))
        self.label_5.setText(_translate("LPIApp", "Информация о заказчике"))
        self.label_14.setText(_translate("LPIApp", "Дополнительная информация от заказчика"))
        self.label_15.setText(_translate("LPIApp", "Перечень заявок"))
        self.CombGOSTButton.setText(_translate("LPIApp", "Метод 2 ГОСТ 30244"))
        self.CombLookButton.setText(_translate("LPIApp", "Смотреть/редактировать результаты"))
        self.CombAddButton.setText(_translate("LPIApp", "Внести результаты"))
        self.FlamGOSTButton.setText(_translate("LPIApp", "ГОСТ 30402"))
        self.FlamLookButton.setText(_translate("LPIApp", "Смотреть/редактировать результаты"))
        self.FlamAddButton.setText(_translate("LPIApp", "Внести результаты"))





class Ui_LPIApp(Ui_LPIApp):
    def setupUi(self, LPIApp):
        super().setupUi(LPIApp)
        self.LPIApp = LPIApp
        # Инициализируем переменные для DataFrame
        self.original_df1 = None
        self.original_df2 = None
        self.df = None
        self.current_row_index = None

        # Делаем поля редактируемыми
        self.IdentNumWidget.setReadOnly(False)
        self.EknNum_2.setReadOnly(False)

        # Подключаем сигналы изменения текста
        self.IdentNumWidget.textChanged.connect(lambda: self.save_text_changes(ns[13]))
        self.EknNum_2.textChanged.connect(lambda: self.save_text_changes(ns[15]))

        # Дополнительные настройки интерфейса
        self.listWidget.itemClicked.connect(self.load_request_data)
        self.CombGOSTButton.setCheckable(False)
        self.FlamGOSTButton.setCheckable(False)

        # Добавляем обработчик двойного клика
        self.listWidget.itemDoubleClicked.connect(self.on_double_click)

        # Размещаем кнопки под списком
        self.saveButton = QtWidgets.QPushButton("Сохранить изменения", parent=LPIApp)
        self.saveButton.setGeometry(QtCore.QRect(10, 910, 130, 30))
        self.saveButton.clicked.connect(self.save_all_changes)

        self.refreshButton = QtWidgets.QPushButton("Обновить список", parent=LPIApp)
        self.refreshButton.setGeometry(QtCore.QRect(150, 910, 130, 30))
        self.refreshButton.clicked.connect(self.refresh_list)
        self.refreshButton.setStyleSheet("""
            QPushButton {
                background-color: #4CAF50;
                color: white;
                border: none;
                padding: 5px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #45a049;
            }
        """)
        # В методе setupUi класса Ui_LPIApp оставляем кнопку без изменений:
        self.closeRequestButton = QtWidgets.QPushButton(parent=LPIApp)
        self.closeRequestButton.setGeometry(QtCore.QRect(320, 910, 780, 30))
        self.closeRequestButton.setStyleSheet("""
            QPushButton {
                background-color: #ff4444;
                color: white;
                border: none;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #cc0000;
            }
            QPushButton:disabled {
                background-color: #aaaaaa;
            }
        """)
        self.closeRequestButton.setText("Закрыть заявку")
        self.closeRequestButton.setEnabled(False)
        self.closeRequestButton.clicked.connect(self.close_request)

        # Добавьте в конец setupUi:
        self.update_close_button_state()  # Инициализируем состояние кнопки

    def update_close_button_state(self):
        """Обновляет состояние кнопки закрытия заявки"""
        try:
            # Кнопка активна, если есть выбранная заявка и она загружена
            is_enabled = hasattr(self, 'current_row_index') and self.current_row_index is not None
            self.closeRequestButton.setEnabled(is_enabled)
        except Exception as e:
            print(f"Ошибка обновления состояния кнопки: {e}")
            self.closeRequestButton.setEnabled(False)

    def safe_int(self, value):
        """Безопасное преобразование в целое число (строку) с обработкой ошибок"""
        try:
            return str(int(float(value))) if pd.notna(value) and str(value).strip() else ""
        except (ValueError, TypeError):
            return str(value).strip() if pd.notna(value) else ""

    def load_request_data(self, item):
        """Загружает данные выбранной заявки в поля формы"""
        if not hasattr(self, 'df') or self.df.empty:
            return

        self.current_row_index = self.listWidget.row(item)
        if self.current_row_index < 0 or self.current_row_index >= len(self.df):
            return

        row = self.df.iloc[self.current_row_index]

        try:
            self.IdentNumWidget.blockSignals(True)
            self.EknNum_2.blockSignals(True)

            # Используем self.safe_int() вместо локальной функции
            self.IncIDWidjget.setPlainText(self.safe_int(row.get(ns[8], '')))
            self.CustNameWidget.setPlainText(str(row.get(ns[11], '')).strip())
            self.CustMailWidget.setPlainText(str(row.get(ns[10], '')).strip())
            self.CustTelWidget.setPlainText(str(row.get(ns[95], '')).strip())
            self.DateINWidget.setPlainText(str(row.get(ns[3], '')).strip())
            self.EknNumWidget.setPlainText(self.safe_int(row.get(ns[14], '')))
            self.IdentNumWidget.setPlainText(str(row.get(ns[13], '')).strip())
            self.EknNum_2.setPlainText(str(row.get(ns[15], '')).strip())
            self.AdditionalnfoWidget.setPlainText(str(row.get(ns[20], '')).strip())

            self.update_method_indicators(row)

        except Exception as e:
            QMessageBox.warning(self.LPIApp, "Ошибка", f"Не удалось загрузить данные: {str(e)}")
        finally:
            self.IdentNumWidget.blockSignals(False)
            self.EknNum_2.blockSignals(False)

        # Добавьте эту строку для обновления состояния кнопки
        self.update_close_button_state()

    def refresh_list(self):
        """Перезагружает данные из сохранённых DataFrame"""
        try:
            # Полностью перезагружаем данные из файлов
            self.original_df1 = pd.read_excel(alltasks)
            self.original_df2 = pd.read_excel(closedtasks)

            # Пересоздаем объединенный DataFrame
            self.df = pd.concat([self.original_df1, self.original_df2]).drop_duplicates().reset_index(drop=True)

            # Сортируем по ID
            try:
                self.df[ns[8]] = pd.to_numeric(self.df[ns[8]], errors='coerce')
                self.df = self.df.sort_values(by=ns[8], ascending=False)
            except Exception as e:
                print(f"Ошибка сортировки: {e}")
                self.df = self.df.sort_values(by=ns[8], ascending=False, key=lambda x: x.astype(str))

            # Обновляем список
            self.listWidget.clear()
            for idx in range(len(self.df)):
                row = self.df.iloc[idx]
                item_text = f"{self.safe_int(row.get(ns[8], ''))} | {str(row.get(ns[13], '')).strip()}, {str(row.get(ns[15], '')).strip()}"
                item = QtWidgets.QListWidgetItem(item_text)

                if row[ns[8]] in set(self.original_df1[ns[8]]).intersection(set(self.original_df2[ns[8]])):
                    item.setForeground(QtGui.QColor('red'))
                    item.setToolTip("Дубликат: запись есть в обоих файлах")
                self.listWidget.addItem(item)

            QMessageBox.information(self.LPIApp, "Обновлено", "Данные успешно обновлены")
        except Exception as e:
            QMessageBox.critical(self.LPIApp, "Ошибка", f"Ошибка обновления: {str(e)}")

    def save_all_changes(self):
        """Сохранение изменений только в alltasks.xlsx"""
        try:
            current_id = self.df.at[self.current_row_index, ns[8]]
            mask = self.original_df1[ns[8]].astype(str) == str(current_id)

            if not mask.any():
                QMessageBox.warning(self.LPIApp, "Ошибка",
                                    f"Запись с ID {current_id} не найдена в alltasks.xlsx!")
                return

            # Обновляем только указанные поля
            self.original_df1.loc[mask, ns[13]] = self.IdentNumWidget.toPlainText().strip()
            self.original_df1.loc[mask, ns[15]] = self.EknNum_2.toPlainText().strip()

            # Сохраняем и перезагружаем
            self.original_df1.to_excel(alltasks, index=False)
            self.load_data_from_dataframes(pd.read_excel(alltasks), self.original_df2)

            QMessageBox.information(self.LPIApp, "Сохранено",
                                    f"Изменения для ID {current_id} сохранены в alltasks.xlsx")

        except Exception as e:
            QMessageBox.critical(self.LPIApp, "Ошибка",
                                 f"Не удалось сохранить изменения: {str(e)}")

    def save_text_changes(self, column_name):
        """Автосохранение изменений в реальном времени"""
        if not hasattr(self, 'df') or not hasattr(self, 'current_row_index'):
            return

        try:
            new_value = self.IdentNumWidget.toPlainText() if column_name == ns[13] else self.EknNum_2.toPlainText()
            self.df.at[self.current_row_index, column_name] = new_value.strip()

            # Синхронизируем с original_df1 если строка существует
            if hasattr(self, 'original_df1'):
                current_id = self.df.at[self.current_row_index, ns[8]]
                mask = self.original_df1[ns[8]] == current_id
                if mask.any():
                    self.original_df1.loc[mask, column_name] = new_value.strip()
        except Exception as e:
            print(f"Ошибка автосохранения: {e}")


    def on_double_click(self, item):
        """Улучшенная версия с форматированием вывода"""
        if not hasattr(self, 'df') or self.df.empty:
            QMessageBox.warning(self.LPIApp, "Ошибка", "Нет данных для отображения")
            return

        row_idx = self.listWidget.row(item)
        if 0 <= row_idx < len(self.df):
            row = self.df.iloc[row_idx]

            # Форматируем вывод для лучшей читаемости
            info = "\n".join([f"{col}: {val}" for col, val in row.items()])

            msg = QMessageBox(self.LPIApp)
            msg.setWindowTitle("Полная информация")
            msg.setText(info)
            msg.setStandardButtons(QMessageBox.StandardButton.Ok)
            msg.exec()

    def load_data_from_dataframes(self, df1: pd.DataFrame, df2: pd.DataFrame):
        """Загрузка данных с приоритетом alltasks.xlsx"""
        # Проверка на дубликаты внутри каждого файла
        if df1[ns[8]].duplicated().any() or df2[ns[8]].duplicated().any():
            QMessageBox.warning(self.LPIApp, "Предупреждение",
                                "Обнаружены дубликаты ID в исходных файлах!")

        # Сохраняем оригинальные данные
        self.original_df1 = df1.copy()
        self.original_df2 = df2.copy()

        # Объединяем с приоритетом df1 (alltasks)
        combined = pd.concat([df1, df2])

        # Создаем новый DataFrame вместо работы с представлением
        self.df = combined.drop_duplicates(subset=[ns[8]], keep='first').copy()  # Явное создание копии

        # Преобразуем ID в числовой формат безопасным способом
        try:
            self.df.loc[:, ns[8]] = pd.to_numeric(self.df[ns[8]])  # Используем .loc для явного указания
            self.df = self.df.sort_values(by=ns[8], ascending=False)
        except Exception as e:
            print(f"Ошибка преобразования ID: {e}")
            self.df = self.df.sort_values(by=ns[8], ascending=False, key=lambda x: x.astype(str))

        # Заполняем список
        self.listWidget.clear()
        for _, row in self.df.iterrows():
            item_text = f"{row[ns[8]]} | {row.get(ns[13], '')}, {row.get(ns[15], '')}"
            item = QtWidgets.QListWidgetItem(item_text)

            if row[ns[8]] in df2[ns[8]].values:
                item.setForeground(QtGui.QColor('orange'))
                item.setToolTip("Запись присутствует в обоих файлах (приоритет у alltasks)")

            self.listWidget.addItem(item)


    def update_method_indicators(self, row):
        """Обновляет индикаторы методов испытаний с более сложной логикой проверки"""
        try:
            aim_value = str(row.get(ns[1], '')).strip().lower()

            # Проверяем разные варианты написания ключевых слов
            comb_keywords = ['горючест', 'combust', 'ггру', 'гост 30244']
            flam_keywords = ['воспламеняемост', 'flammab', 'вспл', 'гост 30402']

            # Проверяем наличие любого из ключевых слов
            comb_active = any(keyword in aim_value for keyword in comb_keywords)
            flam_active = any(keyword in aim_value for keyword in flam_keywords)

            # Устанавливаем стиль
            self.set_indicator_style(self.CombGOSTButton, comb_active)
            self.set_indicator_style(self.FlamGOSTButton, flam_active)

        except Exception as e:
            print(f"Ошибка при обновлении индикаторов: {str(e)}")
            # Устанавливаем индикаторы в неактивное состояние при ошибке
            self.set_indicator_style(self.CombGOSTButton, False)
            self.set_indicator_style(self.FlamGOSTButton, False)

    def set_indicator_style(self, indicator, is_active):
        """Устанавливает стиль индикатора"""
        if is_active:
            indicator.setStyleSheet("""
                QRadioButton {
                    color: green;
                    font-weight: bold;
                    text-decoration: underline;
                }
                QRadioButton::indicator {
                    background-color: green;
                    border: 1px solid darkgreen;
                }
            """)
        else:
            indicator.setStyleSheet("""
                QRadioButton {
                    color: red;
                    font-weight: bold;
                    text-decoration: underline;
                }
                QRadioButton::indicator {
                    background-color: red;
                    border: 1px solid darkred;
                }
            """)

    def close_request(self):
        """Отправляет email-уведомление о закрытии заявки без изменения файлов"""
        if not hasattr(self, 'current_row_index') or self.current_row_index is None:
            QMessageBox.warning(self.LPIApp, "Ошибка", "Не выбрана заявка для закрытия")
            return

        try:
            row = self.df.iloc[self.current_row_index]
            current_id = row[ns[8]]

            # Подтверждение действия
            reply = QMessageBox.question(
                self.LPIApp,
                "Подтверждение",
                "Вы уверены, что хотите отправить уведомление о закрытии этой заявки?",
                QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
            )

            if reply != QMessageBox.StandardButton.Yes:
                return

            # Отправляем email
            self.send_close_email(row)

            QMessageBox.information(self.LPIApp, "Успех", "Email-уведомление о закрытии заявки отправлено")

        except Exception as e:
            QMessageBox.critical(self.LPIApp, "Ошибка", f"Не удалось отправить уведомление: {str(e)}")

    # В методе send_close_email() исправлено:
    def send_close_email(self, row):
        """Отправляет email о закрытии заявки с использованием NotificationSender"""
        try:
            # Получаем данные из строки
            request_id = str(row.get(ns[8], ''))
            customer_email = tracker_adress  # Используем импортированную константу

            # Проверяем наличие email
            if not customer_email or '@' not in customer_email:
                QMessageBox.warning(self.LPIApp, "Предупреждение",
                                    "Не указан или некорректен email для уведомлений")
                return

            # Создаем сообщение
            subject = f"Заявка LPIZAYAVKINAPRO-{request_id} закрыта"
            body = "end point"

            # Создаем экземпляр NotificationSender
            sender = NotificationSender(
                subject=subject,
                text=body,
                email=mail_login,
                password=mail_pass
            )

            # Отправляем email
            success = sender.send_email(
                subject=subject,
                text=body,
                recipient=customer_email
            )

            if not success:
                QMessageBox.warning(self.LPIApp, "Ошибка",
                                    "Не удалось отправить email уведомление")

        except Exception as e:
            QMessageBox.critical(self.LPIApp, "Ошибка отправки",
                                 f"Не удалось отправить email: {str(e)}")

app = QApplication(sys.argv)
window = QMainWindow()
ui = Ui_LPIApp()
ui.setupUi(window)
ia = pd.read_excel(alltasks)
iq = pd.read_excel(closedtasks)
ui.load_data_from_dataframes(ia, iq)


