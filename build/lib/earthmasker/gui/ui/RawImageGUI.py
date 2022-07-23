# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'RawImageGUI.ui'
#
# Created by: PyQt5 UI code generator 5.15.4
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(999, 715)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.centralwidget)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout()
        self.verticalLayout_3.setSizeConstraint(QtWidgets.QLayout.SetMaximumSize)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.modeButton = QtWidgets.QPushButton(self.centralwidget)
        self.modeButton.setMaximumSize(QtCore.QSize(161, 32))
        self.modeButton.setObjectName("modeButton")
        self.verticalLayout_3.addWidget(self.modeButton)
        self.thresholdButton = QtWidgets.QPushButton(self.centralwidget)
        self.thresholdButton.setMaximumSize(QtCore.QSize(161, 32))
        self.thresholdButton.setObjectName("thresholdButton")
        self.verticalLayout_3.addWidget(self.thresholdButton)
        self.groupBox_6 = QtWidgets.QGroupBox(self.centralwidget)
        self.groupBox_6.setMaximumSize(QtCore.QSize(161, 300))
        self.groupBox_6.setObjectName("groupBox_6")
        self.verticalLayout_9 = QtWidgets.QVBoxLayout(self.groupBox_6)
        self.verticalLayout_9.setObjectName("verticalLayout_9")
        self.groupBox_7 = QtWidgets.QGroupBox(self.groupBox_6)
        self.groupBox_7.setMinimumSize(QtCore.QSize(0, 80))
        self.groupBox_7.setMaximumSize(QtCore.QSize(16777215, 80))
        self.groupBox_7.setObjectName("groupBox_7")
        self.verticalLayout_10 = QtWidgets.QVBoxLayout(self.groupBox_7)
        self.verticalLayout_10.setObjectName("verticalLayout_10")
        self.thresholdSpinner_3 = QtWidgets.QSpinBox(self.groupBox_7)
        self.thresholdSpinner_3.setObjectName("thresholdSpinner_3")
        self.verticalLayout_10.addWidget(self.thresholdSpinner_3)
        self.verticalLayout_9.addWidget(self.groupBox_7)
        self.verticalLayout_3.addWidget(self.groupBox_6)
        self.groupBox_2 = QtWidgets.QGroupBox(self.centralwidget)
        self.groupBox_2.setMaximumSize(QtCore.QSize(161, 300))
        self.groupBox_2.setObjectName("groupBox_2")
        self.verticalLayout_5 = QtWidgets.QVBoxLayout(self.groupBox_2)
        self.verticalLayout_5.setObjectName("verticalLayout_5")
        self.groupBox_3 = QtWidgets.QGroupBox(self.groupBox_2)
        self.groupBox_3.setMinimumSize(QtCore.QSize(0, 80))
        self.groupBox_3.setMaximumSize(QtCore.QSize(16777215, 80))
        self.groupBox_3.setObjectName("groupBox_3")
        self.verticalLayout_6 = QtWidgets.QVBoxLayout(self.groupBox_3)
        self.verticalLayout_6.setObjectName("verticalLayout_6")
        self.thresholdSpinner = QtWidgets.QSpinBox(self.groupBox_3)
        self.thresholdSpinner.setObjectName("thresholdSpinner")
        self.verticalLayout_6.addWidget(self.thresholdSpinner)
        self.verticalLayout_5.addWidget(self.groupBox_3)
        self.verticalLayout_3.addWidget(self.groupBox_2)
        self.groupBox = QtWidgets.QGroupBox(self.centralwidget)
        self.groupBox.setMaximumSize(QtCore.QSize(161, 200))
        self.groupBox.setObjectName("groupBox")
        self.verticalLayout_4 = QtWidgets.QVBoxLayout(self.groupBox)
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        self.groupBox_4 = QtWidgets.QGroupBox(self.groupBox)
        self.groupBox_4.setObjectName("groupBox_4")
        self.verticalLayout_7 = QtWidgets.QVBoxLayout(self.groupBox_4)
        self.verticalLayout_7.setObjectName("verticalLayout_7")
        self.minSpinner = QtWidgets.QSpinBox(self.groupBox_4)
        self.minSpinner.setMinimum(-999999)
        self.minSpinner.setMaximum(999999)
        self.minSpinner.setObjectName("minSpinner")
        self.verticalLayout_7.addWidget(self.minSpinner)
        self.maxSpinner = QtWidgets.QSpinBox(self.groupBox_4)
        self.maxSpinner.setMinimum(-999999)
        self.maxSpinner.setMaximum(999999)
        self.maxSpinner.setObjectName("maxSpinner")
        self.verticalLayout_7.addWidget(self.maxSpinner)
        self.verticalLayout_4.addWidget(self.groupBox_4)
        self.ColorSelector = QtWidgets.QComboBox(self.groupBox)
        self.ColorSelector.setObjectName("ColorSelector")
        self.ColorSelector.addItem("")
        self.ColorSelector.addItem("")
        self.ColorSelector.addItem("")
        self.ColorSelector.addItem("")
        self.verticalLayout_4.addWidget(self.ColorSelector)
        self.verticalLayout_3.addWidget(self.groupBox)
        spacerItem = QtWidgets.QSpacerItem(148, 158, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout_3.addItem(spacerItem)
        self.progressLabel = QtWidgets.QLabel(self.centralwidget)
        self.progressLabel.setMaximumSize(QtCore.QSize(161, 16777215))
        self.progressLabel.setText("")
        self.progressLabel.setObjectName("progressLabel")
        self.verticalLayout_3.addWidget(self.progressLabel)
        self.progressBar = QtWidgets.QProgressBar(self.centralwidget)
        self.progressBar.setMaximumSize(QtCore.QSize(161, 16777215))
        self.progressBar.setProperty("value", 0)
        self.progressBar.setObjectName("progressBar")
        self.verticalLayout_3.addWidget(self.progressBar)
        self.horizontalLayout.addLayout(self.verticalLayout_3)
        self.verticalLayout_2 = QtWidgets.QVBoxLayout()
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.FigCanvasWidget = MplFigCanvasWidget(self.centralwidget)
        self.FigCanvasWidget.setMinimumSize(QtCore.QSize(800, 0))
        self.FigCanvasWidget.setObjectName("FigCanvasWidget")
        self.verticalLayout_2.addWidget(self.FigCanvasWidget)
        self.horizontalLayout.addLayout(self.verticalLayout_2)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 999, 22))
        self.menubar.setObjectName("menubar")
        self.menuFile = QtWidgets.QMenu(self.menubar)
        self.menuFile.setObjectName("menuFile")
        self.menuSave_tif = QtWidgets.QMenu(self.menuFile)
        self.menuSave_tif.setObjectName("menuSave_tif")
        self.menuSave_figure = QtWidgets.QMenu(self.menuFile)
        self.menuSave_figure.setObjectName("menuSave_figure")
        self.menuView = QtWidgets.QMenu(self.menubar)
        self.menuView.setObjectName("menuView")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.actionClose = QtWidgets.QAction(MainWindow)
        self.actionClose.setObjectName("actionClose")
        self.actionSave_in_place = QtWidgets.QAction(MainWindow)
        self.actionSave_in_place.setObjectName("actionSave_in_place")
        self.actionSave_pick = QtWidgets.QAction(MainWindow)
        self.actionSave_pick.setObjectName("actionSave_pick")
        self.actionSave_as = QtWidgets.QAction(MainWindow)
        self.actionSave_as.setObjectName("actionSave_as")
        self.actionSave_as_png = QtWidgets.QAction(MainWindow)
        self.actionSave_as_png.setObjectName("actionSave_as_png")
        self.actionColor_limits = QtWidgets.QAction(MainWindow)
        self.actionColor_limits.setObjectName("actionColor_limits")
        self.actionColor_map = QtWidgets.QAction(MainWindow)
        self.actionColor_map.setObjectName("actionColor_map")
        self.actionNext = QtWidgets.QAction(MainWindow)
        self.actionNext.setObjectName("actionNext")
        self.actionPrevious = QtWidgets.QAction(MainWindow)
        self.actionPrevious.setObjectName("actionPrevious")
        self.actionVertical_band_pass = QtWidgets.QAction(MainWindow)
        self.actionVertical_band_pass.setObjectName("actionVertical_band_pass")
        self.actionAdaptive_Horizontal_filter = QtWidgets.QAction(MainWindow)
        self.actionAdaptive_Horizontal_filter.setObjectName("actionAdaptive_Horizontal_filter")
        self.actionCrop = QtWidgets.QAction(MainWindow)
        self.actionCrop.setObjectName("actionCrop")
        self.actionReverse = QtWidgets.QAction(MainWindow)
        self.actionReverse.setObjectName("actionReverse")
        self.actionLoad_crossprofile = QtWidgets.QAction(MainWindow)
        self.actionLoad_crossprofile.setObjectName("actionLoad_crossprofile")
        self.actionshp = QtWidgets.QAction(MainWindow)
        self.actionshp.setObjectName("actionshp")
        self.actioncsv = QtWidgets.QAction(MainWindow)
        self.actioncsv.setObjectName("actioncsv")
        self.actionFlatten_layer = QtWidgets.QAction(MainWindow)
        self.actionFlatten_layer.setObjectName("actionFlatten_layer")
        self.actionSwitch_data_matrix = QtWidgets.QAction(MainWindow)
        self.actionSwitch_data_matrix.setObjectName("actionSwitch_data_matrix")
        self.menuSave_tif.addAction(self.actionSave_pick)
        self.menuSave_tif.addAction(self.actionSave_as)
        self.menuSave_figure.addAction(self.actionSave_as_png)
        self.menuFile.addAction(self.menuSave_tif.menuAction())
        self.menuFile.addAction(self.menuSave_figure.menuAction())
        self.menuFile.addSeparator()
        self.menuFile.addAction(self.actionClose)
        self.menuView.addAction(self.actionFlatten_layer)
        self.menuView.addAction(self.actionSwitch_data_matrix)
        self.menubar.addAction(self.menuFile.menuAction())
        self.menubar.addAction(self.menuView.menuAction())

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "PickGUI"))
        self.modeButton.setText(_translate("MainWindow", "Mask Mode"))
        self.thresholdButton.setText(_translate("MainWindow", "Update Mask"))
        self.groupBox_6.setTitle(_translate("MainWindow", "Draw Options"))
        self.groupBox_7.setTitle(_translate("MainWindow", "Brush Size"))
        self.groupBox_2.setTitle(_translate("MainWindow", "Mask Options"))
        self.groupBox_3.setTitle(_translate("MainWindow", "Threshold"))
        self.groupBox.setTitle(_translate("MainWindow", "View Options"))
        self.groupBox_4.setTitle(_translate("MainWindow", "Color limits"))
        self.ColorSelector.setCurrentText(_translate("MainWindow", "gray"))
        self.ColorSelector.setItemText(0, _translate("MainWindow", "gray"))
        self.ColorSelector.setItemText(1, _translate("MainWindow", "viridis"))
        self.ColorSelector.setItemText(2, _translate("MainWindow", "bwr"))
        self.ColorSelector.setItemText(3, _translate("MainWindow", "magma"))
        self.menuFile.setTitle(_translate("MainWindow", "File"))
        self.menuSave_tif.setTitle(_translate("MainWindow", "Save .tif"))
        self.menuSave_figure.setTitle(_translate("MainWindow", "Save figure"))
        self.menuView.setTitle(_translate("MainWindow", "View"))
        self.actionClose.setText(_translate("MainWindow", "Close"))
        self.actionClose.setShortcut(_translate("MainWindow", "Ctrl+W"))
        self.actionSave_in_place.setText(_translate("MainWindow", "Save in place"))
        self.actionSave_pick.setText(_translate("MainWindow", "Save"))
        self.actionSave_pick.setShortcut(_translate("MainWindow", "Ctrl+S"))
        self.actionSave_as.setText(_translate("MainWindow", "Save as"))
        self.actionSave_as.setShortcut(_translate("MainWindow", "Ctrl+Shift+S"))
        self.actionSave_as_png.setText(_translate("MainWindow", "Save png"))
        self.actionColor_limits.setText(_translate("MainWindow", "Color limits"))
        self.actionColor_map.setText(_translate("MainWindow", "Color map"))
        self.actionNext.setText(_translate("MainWindow", "Next"))
        self.actionPrevious.setText(_translate("MainWindow", "Previous"))
        self.actionVertical_band_pass.setText(_translate("MainWindow", "Vertical band pass..."))
        self.actionAdaptive_Horizontal_filter.setText(_translate("MainWindow", "Adaptive Horizontal filter..."))
        self.actionCrop.setText(_translate("MainWindow", "Crop..."))
        self.actionReverse.setText(_translate("MainWindow", "Reverse"))
        self.actionLoad_crossprofile.setText(_translate("MainWindow", "Load crossprofile"))
        self.actionshp.setText(_translate("MainWindow", "shp..."))
        self.actioncsv.setText(_translate("MainWindow", "csv..."))
        self.actionFlatten_layer.setText(_translate("MainWindow", "Switch channel"))
        self.actionSwitch_data_matrix.setText(_translate("MainWindow", "Combine rbg"))
from .mplfigcanvaswidget import MplFigCanvasWidget


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
