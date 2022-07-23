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
        self.fn = None
        self._saved = True

        # TODO ask the user whether they would like to save or not.
        self._unfinished_mask = False

        # Set defaults
        #: Threshold of the mask we seek
        # self.threshold_low = 255
        self.threshold = 255
        #: The mode we are in (either select or edit)
        self.mask_mode = "mask"

        #: The ImageData object being plotted
        self.dat = dat

        self.tmp_mask = self.dat.mask.copy()

        (self.img, self.lims) = plot_image(
            self.dat, cmap=plt.cm.gray, fig=self.fig, ax=self.ax, return_plotinfo=True
        )

        # Store some info that we need for later

        self.minSpinner.setValue(int(self.lims[0]))
        self.maxSpinner.setValue(int(self.lims[1]))
        self.thresholdSpiner.setValue(self.threshold)

        # We need this so we no if we are nanpicking
        self._n_pressed = False

        #####
        # Connect some stuff after things are set up
        # Do this here so we don't unintentionally trigger things that are not initialized
        #####

        # Process menu

        self.minSpinner.valueChanged.connect(self._lim_update)
        self.maxSpinner.valueChanged.connect(self._lim_update)
        self.thresholdSpin.valueChanged.connect(self._threshold_update)
        self.checkBox_2.stateChanged.connect(self._update_color_reversal)

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
        self.mask_tmp[self.dat > self.threshold] = 1.0
        self.fig.canvas.draw()
        self.fig.canvas.flush_events()

        try:
            plt.show()
        except KeyboardInterrupt:
            plt.close("all")

    def _mode_update(self):
        _translate = QtCore.QCoreApplication.translate
        if self.mask_mode == "mask":
            self.modeButton.setText(_translate("MainWindow", "draw Mode"))
            self.FigCanvasWidget.setCursor(QtGui.QCursor(QtCore.Qt.CrossCursor))
            self.mask_mode = "draw"
            self.fig.canvas.mpl_disconnect(self.bpid)
            self.bpid = self.fig.canvas.mpl_connect(
                "button_press_event", self._moved_and_pressed
            )

        else:
            self.modeButton.setText(_translate("MainWindow", "Mask Mode"))
            self.FigCanvasWidget.setCursor(QtGui.QCursor(QtCore.Qt.ArrowCursor))
            self.mask_mode = "mask"
            self.fig.canvas.mpl_disconnect(self.bpid)
            self.bpid = self.fig.canvas.mpl_connect(
                "button_press_event", self._on_press, self.on_release
            )

    #######
    # Handling of mouse events
    #######

    def _moved_and_pressed(event):
        try:
            zooming_panning = fig.canvas.cursor().shape() != 0
        except:
            zooming_panning = False
        if zooming_panning:
            print("Zooming or panning")
            return
        if event.inaxes == ax:
            if event.button == 1:
                dist, indexes = self._do_kdtree(np.array([event.ydata, event.xdata]))
                ind = np.unravel_index(indexes, xarray.shape)
                mask[ind] = 1.0
            if event.button == 3:
                dist, indexes = do_kdtree(np.array([event.ydata, event.xdata]))
                ind = np.unravel_index(indexes, xarray.shape)
                mask[ind] = np.nan

            img_mask.set_data(mask)
            fig.canvas.draw()

    def _on_press(self, event):
        try:
            zooming_panning = self.fig.canvas.cursor().shape() != 0
        except:
            zooming_panning = False
        if zooming_panning:
            print("Zooming or panning")
            return
        if event.inaxes == self.ax:
            print("press")
            self.dist, self.indexes = self._do_kdtree(
                np.array([event.ydata, event.xdata])
            )
            self.ind_1 = np.unravel_index(indexes, xarray.shape)

    def _on_release(self, event):
        try:
            zooming_panning = self.fig.canvas.cursor().shape() != 0
        except:
            zooming_panning = False
        if zooming_panning:
            print("Zooming or panning")
            return
        if event.inaxes == self.ax:
            if event.button == 1:
                print("release")
                self.dist, self.indexes = self._do_kdtree(
                    np.array([event.ydata, event.xdata])
                )
                self.ind_2 = np.unravel_index(indexes, xarray.shape)
                # highlight cells
                self.mask_tmp[
                    self.ind_1[0] : self.ind_2[0], self.ind_2[1] : self.ind_2[1]
                ] = 1.0
            if event.button == 3:
                print("release")
                self.dist, self.indexes = self._do_kdtree(
                    np.array([event.ydata, event.xdata])
                )
                self.ind_2 = np.unravel_index(indexes, xarray.shape)
                # delete cells
                self.mask_tmp[
                    self.ind_1[0] : self.ind_2[0], self.ind_2[1] : self.ind_2[1]
                ] = 0.0

            self.ax.figure.canvas.draw()

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

    def _save_fn(self, fn):
        self.fn = fn
        self.dat.save(fn[:-4] + "_mask.tif")
        self._saved = True
        self.actionSave_pick.triggered.disconnect()
        self.actionSave_pick.triggered.connect(self._save)


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


# We want to add this fancy colormap
COLORB = [
    (1.0000, 1.0000, 1.000),
    (0.9984, 1.0000, 0.2000),
    (1.0000, 0.6792, 0.6500),
    (0.5407, 0.9000, 0.5400),
    (0.7831, 0.8950, 0.8950),
    (1.0000, 1.0000, 1.0000),
    (0.3507, 0.3500, 0.7000),
    (0.1740, 0.5800, 0.5800),
    (0.0581, 0.5800, 0.0580),
    (0.4792, 0.4800, 0.0600),
    (0.8000, 0.0, 0.0),
    (0.0, 0.0, 0.0),
]

PERCENTS = np.array([0, 63, 95, 114, 123, 127, 130, 134, 143, 162, 194, 256]) / 256.0

plt.cm.register_cmap(
    name="CEGSIC",
    cmap=colors.LinearSegmentedColormap.from_list(
        "CEGSIC", list(zip(PERCENTS, COLORB))
    ),
)
plt.cm.register_cmap(
    name="CEGSIC_r",
    cmap=colors.LinearSegmentedColormap.from_list(
        "CEGSIC_r", list(zip(PERCENTS, COLORB))
    ),
)
