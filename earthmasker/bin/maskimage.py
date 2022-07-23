#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
#
# Copyright © 2022 Andrew Hoffman <hoffmaao@uw.edu>
#
# Distributed under terms of the GNU GPL3.0 license.

"""An executable to start the masker."""

import sys
import argparse
from PyQt5 import QtWidgets

from matplotlib import rc
import rasterio as rio

from earthmasker.gui import maskgui
from earthmasker.lib import load

rc("text", usetex=False)


def mask(trainingData):
    """Fire up the masker."""

    app = QtWidgets.QApplication(sys.argv)
    ip = maskgui.InteractiveMasker(trainingData)
    ip.show()
    sys.exit(app.exec_())


def main():
    """Get arguments, start masking."""
    parser = _get_args()
    args = parser.parse_args(sys.argv[1:])
    trainingData = load.load(args.fn)
    mask(trainingData)


def _get_args():
    """Get the parser for arguments."""
    parser = argparse.ArgumentParser()
    parser.add_argument("fn", type=str, help="The file to pick. One file at a time.")
    return parser


if __name__ == "__main__":
    main()
