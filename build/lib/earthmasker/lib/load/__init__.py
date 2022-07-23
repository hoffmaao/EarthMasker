# -*- coding: utf-8 -*-
# vim:fenc=utf-8
#
# Copyright © 2019 Andrew Hoffman <hoffmaao@sleipnir.ess.washington.edu>
#
# Distributed under terms of the GNU GPL3 license.


import os.path
import glob
from ..trainingData import trainingData

def load(filename):
    """Load a list of files of a certain type
    Parameters
    ----------
    filename: str
        The type of file to load.
    fns: list
        List of files to load
    channel: Receiver channel that the data were recorded on
        This is primarily for the St. Olaf HF data
    Returns
    -------
    imageData: list of ~mask-tool.ImageData (or its subclasses)
        Objects with relevant image information
    """

    dat = trainingData(filename)
    return dat