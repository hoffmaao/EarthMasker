#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
#
# Copyright © 2019 Andrew Hoffman <hoffmaao@uw.edu>
#
# Distributed under terms of the GNU GPL3.0 license.

"""Plotting functions for radar data."""
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import is_color_like



def plot_image(dat, cmap=plt.cm.gray, fig=None, ax=None,
                   return_plotinfo=False, clims=None):
    
    """Plot an image for segmentation.
    This function is a little weird since I want to be able to plot on top of
    existing figures/axes or on new figures an axes. There is therefore an
    argument `return_plotinfo` that funnels between these options and changes
    the return types.
    Parameters
    ----------
    dat: rasterio.dataset
        The image and mask dataset
    cmap: matplotlib.pyplot.cm, optional
        The colormap to use
    fig: matplotlib.pyplot.Figure
        Figure canvas that should be plotted upon
    ax: matplotlib.pyplot.Axes
        Axes that should be plotted upon
    Returns
    -------
    If not return_plotinfo
        fig: matplotlib.pyplot.Figure
            Figure canvas that was plotted upon
        ax: matplotlib.pyplot.Axes
            Axes that were plotted upon
    else
        im: pyplot.imshow
            The image object plotted
        xd: np.ndarray
            The x values of the plot
        yd: np.ndarray
            The y values of the plot
        x_range: 2-tuple
            The limits of the x range,
            after modification to remove negative indices
        clims: 2-tuple
            The limits of the colorbar
    """


    if clims is None:
        clims = np.percentile(dat.data[~np.isnan(dat.data)], (5, 99.5))

    if fig is not None:
        if ax is None:
            ax = plt.gca()
    else:
        fig, ax = plt.subplots(figsize=(12, 8))



    img = ax.imshow(dat.data,
    	            extent=dat.extent,
                    cmap=cmap,
                    vmin=clims[0],
                    vmax=clims[1]
                    )

    img_mask = ax.imshow(dat.mask,
    	            extent=dat.extent,
                    cmap='Reds',
                    alpha = .5,
                    vmin=0,
                    vmax=1
                    )
    #contour = ax.contour(dat.xarray, dat.yarray, dat.mask, (1,), colors='r', linewidths=2)

    return img, img_mask, clims