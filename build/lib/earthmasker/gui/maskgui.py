#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
#
# Copyright © 2022 Andrew Hoffman <hoffmaao@uw.edu>
#
# Distributed under terms of the GNU GPL3.0 license.

import numpy as np
import matplotlib.pyplot as plt
import rasterio as rio
from scipy import spatial
import numpy as np
from matplotlib import colors
from PyQt5 import QtCore, QtWidgets, QtGui
from PyQt5.QtWidgets import QFileDialog, QMessageBox, QDialog

from .ui import RawImageGUI
from ..lib import trainingData  # om ..lib import ImageData, masklib
from ..lib.plot import plot_image

SYMBOLS_FOR_CPS = ["o", "d", "s"]


class InteractiveMasker(QtWidgets.QMainWindow, RawImageGUI.Ui_MainWindow):
    """The main window."""

    def __init__(self, dat, guard_save=False):
        # Next line is required for Qt, then give us the layout
        super(InteractiveMasker, self).__init__()
        self.setupUi(self)
        self.setWindowTitle(dat.fn)
        self.FigCanvasWidget.canvas.setFocusPolicy(QtCore.Qt.ClickFocus)
        self.FigCanvasWidget.canvas.setFocus()

        # Connect the menu to actions
        # save menu
        self.actionSave_mask.triggered.connect(self._save_as)
        self.actionSave_as.triggered.connect(self._save_as)
        self.actionClose.triggered.connect(self.close)

        # Connect controls on the left
        self.ColorSelector.currentTextChanged.connect(self._color_select)

        # Easy access to normal mpl figure and axes
        #: The axes upon which things get plotted.
        self.ax = self.FigCanvasWidget.canvas.ax
        #: The figure upon which things get plotted.
        self.fig = self.FigCanvasWidget.canvas.fig
        plt.ion()

        # Two constants to keep track of how to prompt for saves
        #: The filename, updated by things like "save as"
        self.fn = dat.fn
        self._saved = True

        # TODO ask the user whether they would like to save or not.
        self._unfinished_mask = False

        # Set defaults
        #: Threshold of the mask we seek
        # self.threshold_low = 255
        self.threshold = 255
        self.brush_size = 3
        #: The mode we are in (either select or edit)
        self.mask_mode = "mask"

        #: The ImageData object being plotted
        self.dat = dat

        self.mask_tmp = self.dat.mask.copy()

        (self.im, self.im_mask, self.lims) = plot_image(
            self.dat, cmap=plt.cm.gray, fig=self.fig, ax=self.ax, return_plotinfo=True
        )

        # Store some info that we need for later

        self.minSpinner.setValue(int(self.lims[0]))
        self.maxSpinner.setValue(int(self.lims[1]))
        self.brushsizeSpinner.setValue(int(self.brush_size))
        self.thresholdSpinner.setValue(self.threshold)
        self.modeButton.clicked.connect(self._mode_update)
        self.thresholdButton.clicked.connect(self._apply_threshold)

        self.cid = self.fig.canvas.mpl_connect('button_press_event', self._on_press)
        self.rid = self.fig.canvas.mpl_connect('buttom_release_event', self._on_release)
        self.did = self.fig.canvas.mpl_connect('motion_notify_event', self._moved_and_pressed)

        # We need this so we no if we are nanpicking
        self._n_pressed = False

        #####
        # Connect some stuff after things are set up
        # Do this here so we don't unintentionally trigger things that are not initialized
        #####

        # Process menu

        self.minSpinner.valueChanged.connect(self._lim_update)
        self.maxSpinner.valueChanged.connect(self._lim_update)
        self.thresholdSpinner.valueChanged.connect(self._threshold_update)
        self.brushsizeSpinner.valueChanged.connect(self._brush_size_update)

        try:
            plt.show()
        except KeyboardInterrupt:
            plt.close("all")

    ####### Functions for algorithim ##########

    def _color_select(self, val):
        self.im.set_cmap(plt.cm.get_cmap(val))
        self.fig.canvas.draw()
        self.fig.canvas.flush_events()

    def _lim_update(self, val):
        if self.maxSpinner.value() < self.minSpinner.value():
            self.maxSpinner.setValue(self.minSpinner.value() + 1)
        return self._update_lims(self.minSpinner.value(), self.maxSpinner.value())

    def _update_lims(self, vmin, vmax):
        if vmin >= vmax:
            raise ValueError("Min must be less than max")
        self.im.set_clim(vmin=vmin, vmax=vmax)
        self.lims[0] = self.minSpinner.value()
        self.lims[1] = self.maxSpinner.value()
        self.fig.canvas.draw()
        self.fig.canvas.flush_events()

    def _threshold_update(self, val):
        # TODO add upper theshold
        self.threshold = val
        self.mask_tmp[:] = np.nan
        self.mask_tmp[self.dat.data > self.threshold] = 1.0
        self.fig.canvas.draw()
        self.fig.canvas.flush_events()
    def _brush_size_update(self, val):
        # TODO add upper theshold
        self.brush_size = val
        self.fig.canvas.draw()
        self.fig.canvas.flush_events()


    def _apply_threshold(self):
        _translate = QtCore.QCoreApplication.translate
        # TODO unsaved mask variable self.unsaved_mask
        self.dat.mask = self.mask_tmp
        self.im_mask.set_data(self.dat.mask)
        self.fig.canvas.draw()
        self.fig.canvas.flush_events()


    def _mode_update(self):
        _translate = QtCore.QCoreApplication.translate
        if self.mask_mode == "mask":
            self.modeButton.setText(_translate("MainWindow", "Mask Mode"))
            self.FigCanvasWidget.setCursor(QtGui.QCursor(QtCore.Qt.CrossCursor))
            self.mask_mode = "draw"
            self.fig.canvas.mpl_disconnect(self.cid)
            self.fig.canvas.mpl_disconnect(self.rid)
            self.fig.canvas.mpl_disconnect(self.did)
            self.did = self.fig.canvas.mpl_connect(
                "motion_notify_event", self._moved_and_pressed
            )

        else:
            self.modeButton.setText(_translate("MainWindow", "Draw Mode"))
            self.FigCanvasWidget.setCursor(QtGui.QCursor(QtCore.Qt.ArrowCursor))
            self.mask_mode = "mask"
            self.fig.canvas.mpl_disconnect(self.did)
            self.fig.canvas.mpl_disconnect(self.cid)
            self.fig.canvas.mpl_disconnect(self.rid)
            self.cid = self.fig.canvas.mpl_connect(
                "button_press_event", self._on_press,
            )
            self.rid = self.fig.canvas.mpl_connect(
                "button_release_event", self._on_release
            )

    #######
    # Handling of mouse events
    #######

    def _moved_and_pressed(self,event):
        try:
            zooming_panning = self.fig.canvas.cursor().shape() != 0
        except:
            zooming_panning = False
        if zooming_panning:
            return
        if event.inaxes == self.ax:
            if event.button == 1:
                ind = self.dat.do_kdtree(np.array([event.ydata, event.xdata]))
                self.dat.mask[max(ind[0]-self.brush_size,0):min(ind[0]+self.brush_size,self.dat.height),max(ind[1]-self.brush_size,0):min(ind[1]+self.brush_size,self.dat.width)] = 1.0
            if event.button == 3:
                ind = self.dat.do_kdtree(np.array([event.ydata, event.xdata]))
                self.dat.mask[max(ind[0]-self.brush_size,0):min(ind[0]+self.brush_size,self.dat.height),max(ind[1]-self.brush_size,0):min(ind[1]+self.brush_size,self.dat.width)] = np.nan

            #self.im_mask.set_data(self.dat.mask)

            self.fig.canvas.draw()
            self.fig.canvas.flush_events()

    def _on_press(self, event):
        try:
            zooming_panning = self.fig.canvas.cursor().shape() != 0
        except:
            zooming_panning = False
        if zooming_panning:
            return
        if event.inaxes == self.ax:
            self.ind_1 = self.dat.do_kdtree(
                np.array([event.ydata, event.xdata])
            )
    def _on_release(self, event):
        try:
            zooming_panning = self.fig.canvas.cursor().shape() != 0
        except:
            zooming_panning = False
        if zooming_panning:
            return
        if event.inaxes == self.ax:
            if event.button == 1:
                self.ind_2 = self.dat.do_kdtree(np.array([event.ydata, event.xdata]))
                # highlight cells
                self.dat.mask[
                    min(self.ind_1[0],self.ind_2[0]) : max(self.ind_1[0],self.ind_2[0]), min(self.ind_1[1],self.ind_2[1]) : max(self.ind_1[1],self.ind_2[1])
                ] = 1.0
            if event.button == 3:
                self.ind_2 = self.dat.do_kdtree(np.array([event.ydata, event.xdata]))

                # delete cells
                self.dat.mask[
                    min(self.ind_1[0],self.ind_2[0]) : max(self.ind_1[0],self.ind_2[0]), min(self.ind_1[1],self.ind_2[1]) : max(self.ind_1[1],self.ind_2[1])
                ] = np.nan
            self.im_mask.set_data(self.dat.mask)
            self.fig.canvas.draw()
            self.fig.canvas.flush_events()

    #######
    # Logistics of saving and closing
    #######
    def closeEvent(self, event):
        """Close with the option of saving if data modified, otherwise close."""
        if not self._saved:
            self._save_cancel_close(event)
        else:
            event.accept()

    # Add ability so save multiple masks
    def _save_cancel_close(self, event):
        dialog = QMessageBox()
        dialog.setStandardButtons(
            QMessageBox.Save | QMessageBox.Close | QMessageBox.Cancel
        )
        dialog.setText("Unsaved data")
        dialog.setInformativeText("Changes will be lost if closed")
        result = dialog.exec_()
        if result == QMessageBox.Cancel:
            print(result, QMessageBox.Cancel)
            event.ignore()
        elif result == QMessageBox.Close:
            event.accept()
        else:
            if self.fn is None:
                if not self._save_as(event):
                    event.ignore()
                else:
                    event.accept()
            else:
                self._save(event)
                event.accept()

    def _save(self, evt):
        """Save the file without changing name."""
        if not hasattr(self, "fn") or self.fn is None:
            raise AttributeError(
                'Filename for gui is undefined, needs to be set with "save as"...'
            )
        self._save_fn(self.fn)

    def _save_as(self, event=None):
        """Fancy file handler for gracious exit."""
        fn, _ = QFileDialog.getSaveFileName(self,
                                            "QFileDialog.getSaveFileName()",
                                            self.dat.fn+'_mask',
                                            "All Files (*);;tif Files (*.tif)")
        if fn:
            self._save_fn(fn)
        return fn

    def _save_fn(self, fn):
        self.fn = fn
        self.dat.save(fn)
        self._saved = True
        self.actionSave_mask.triggered.disconnect()
        self.actionSave_mask.triggered.connect(self._save)


def warn(message, long_message):
    """Raise a popup warning dialog.
    Parameters
    ----------
    message: str
        The short warning
    long_message: str
        The long warning
    """
    msg = QtWidgets.QMessageBox()
    msg.setIcon(QtWidgets.QMessageBox.Warning)

    msg.setText(message)
    msg.setInformativeText(long_message)
    msg.setWindowTitle(message)
    msg.setStandardButtons(QMessageBox.Ok)
    return msg.exec_()
