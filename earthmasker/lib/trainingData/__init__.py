#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
#
# Copyright © 2022 Andrew Hoffman <hoffmaao@uw.edu>
#
# Distributed under terms of the GNU GPL-3.0 license.

"""The basic class of mask-tool
"""

import numpy as np
import rasterio as rio
from rasterio.plot import plotting_extent
from scipy import spatial
import os.path


class trainingData(object):
    """A class that holds the relevant information for a training dataset."""

    #: Attributes that every RadarData object should have.
    #: These should not be None.
    attrs_guaranteed = [
        "fn",
        "data",
        "mask",
        "profile",
        "transform",
        "xarray",
        "yarray",
        "extent",
    ]
    attrs_optional = ["width", "height", "xarray", "yarray", "extent"]

    def __init__(self, fn):
        self.fn, self.ext = os.path.splitext(fn)
        with rio.open(fn) as src:
            self.data = src.read(1)
            self.profile = src.profile
            self.transform = src.transform
            self.extent = plotting_extent(src)

        self.height = self.data.shape[0]
        self.width = self.data.shape[1]
        cols, rows = np.meshgrid(np.arange(self.width), np.arange(self.height))
        xs, ys = rio.transform.xy(self.transform, rows, cols)
        self.xarray = np.array(xs)
        self.yarray = np.array(ys)
        self.initialize_tree()
        self.mask = np.zeros((self.width, self.height))
        self.mask[:] = np.nan 

    def initialize_tree(self):
        self.tree = spatial.cKDTree(
            np.dstack([self.yarray.ravel(), self.xarray.ravel()])[0]
        )

    def do_kdtree(self,points):
        np.dstack([self.yarray.ravel(), self.xarray.ravel()])[0]
        dist, ind = self.tree.query(points)
        return np.unravel_index(ind, self.xarray.shape)

    def save(self, fn):
        if fn == None:
            self.mask[np.isnan(self.mask)]=0.0
            with rio.open(self.fn + "_mask" + self.ext, "w", **self.profile) as dst:
                dst.write((self.mask*255).astype('uint8'),1)
        else:
            self.mask[np.isnan(self.mask)]=0.0
            with rio.open(self.fn + "_mask" + self.ext, "w", **self.profile) as dst:
                dst.write((self.mask*255).astype('uint8'),1)
