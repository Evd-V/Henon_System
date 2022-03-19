import numpy as np
from math import log2
import scipy.optimize as optimization
from matplotlib.pyplot import figure, show, cm

import full_henon as fh
import helper as he


def closest(lst, val):
    """ Finding closest value in list """
    
    lst = np.asarray(lst)
    ind = (np.abs(lst - val)).argmin()
    
    return lst[ind], ind


def return_plot(xS, yS, its, a, b, saveFig=None):
    """ Plot the return plot of the Hénon map """
    
    dif = 1e-5
    
    xv, yv = fh.Henon(xS, yS, its, a, b)            # Iterating Henon map
    x2, y2 = fh.Henon(xS+dif, yS+dif, its, a, b)    # Different starting point
    
    # Plotting
    fig = figure(figsize=(15,6))
    frame = fig.add_subplot(1,1,1)
    
    frame.scatter(xv, x2, color="navy", marker="o", s=0.01)
    
    frame.set_xlabel("$x_n$", fontsize=20)
    frame.set_ylabel("$x_{n+1}$", fontsize=20)
    
    frame.grid(zorder=2)
    
    if saveFig: fig.savefig(str(saveFig))
    else: show()


def hist_plot(xv, nBins, saveFig=None):
    """ Plot a histogram of a set of x points """
    
    # Plotting
    fig = figure(figsize=(15,8))
    frame = fig.add_subplot(1,1,1)
    
    frame.hist(xv, nBins, label="$x$", color="teal", rwidth=0.9)
    
    frame.set_xlabel("$x$", fontsize=20)
    frame.set_ylabel("Frequency", fontsize=20)
    frame.tick_params(axis="both", labelsize=15)
    
    if saveFig: fig.savefig(saveFig)
    else: show()


def box_henon(xv, yv, nBoxes, xSpace=0.05, ySpace=0.05, saveFig=None):
    """ Plot the Hénon map divided into boxes """
    
    xMin, xMax = min(xv)-xSpace, max(xv)+xSpace     # x limit of plot
    yMin, yMax = min(yv)-ySpace, max(yv)+ySpace     # y limit of plot
    
    xBoxes = np.linspace(xMin, xMax, nBoxes+1)      # x coordinates of box lines
    yBoxes = np.linspace(yMin, yMax, nBoxes+1)      # y coordinates of box lines
    
    totBoxes = nBoxes * nBoxes                              # Number of boxes
    text = np.linspace(1, totBoxes, totBoxes, dtype=int)    # Labels
    
    # Determining height of labels in plot
    if nBoxes >= 4:
        ySize = 4 * (max(yBoxes) - min(yBoxes)) / (nBoxes * len(yBoxes))
    else: ySize = (max(yBoxes) - min(yBoxes)) / len(yBoxes)
    
    pad = 0.08 / nBoxes                             # x padding for text
    
    # Finding the locations of the text labels
    xLocations = [xBoxes[yInd] + pad for xInd in range(len(xBoxes)-1) 
                                     for yInd in range(len(yBoxes)-1)]
    
    yLocations = [yBoxes[xInd] + ySize for xInd in range(len(xBoxes)-1) 
                                       for yInd in range(len(yBoxes)-1)]
    
    # Plotting
    fig = figure(figsize=(15,8))
    frame = fig.add_subplot(1,1,1)
    
    frame.scatter(xv, yv, s=0.5, color="navy")            # The Hénon map
    
    for xLim in xBoxes:
        frame.axvline(xLim, color="k", lw=1.3, zorder=3)  # Vertical box lines
    for yLim in yBoxes:
        frame.axhline(yLim, color="k", lw=1.3, zorder=3)  # Horizontal box lines
    
    # Adding text
    for i in range(len(xLocations)):
        frame.text(xLocations[i], yLocations[i], text[i], fontsize=15, zorder=3)
    
    # Setting axes
    frame.set_xlabel("$x$", fontsize=20)
    frame.set_ylabel("$y$", fontsize=20)
    frame.tick_params(axis="both", labelsize=15)
    
    # Setting plot limits
    frame.set_xlim(xMin, xMax)
    frame.set_ylim(yMin, yMax)
    
    if saveFig: fig.savefig(saveFig)
    else: show()


def mean_fig(nSize, nRuns):
    """ Plot ratio geometric mean over arithmic mean, always < 1. """
    
    nSize = int(nSize)
    ratios = []
    
    for run in range(nRuns):
        randNumbs = np.random.uniform(low=1e-2, high=5, size=nSize)     # Random
        
        geomMean = np.prod(randNumbs)**(1/nSize)        # Geometric mean
        arithMean = sum(randNumbs) / nSize              # Arithmetic mean
        
        ratios.append(geomMean / arithMean)    
    
    # Plotting
    fig = figure(figsize=(15,8))
    frame = fig.add_subplot(1,1,1)
    frame2 = frame.twinx()
    
    frame.scatter(np.asarray(range(nRuns))/nRuns, 1-np.sort(ratios), 
                  color="teal", marker="o", s=5)
    frame2.hist(1-np.asarray(ratios), bins=int(nRuns/50), density=True, 
                histtype="step", color="forestgreen", lw=1.5)
    
    frame.set_xlabel("Run")
    frame.set_ylabel("Ratio")
    
    frame.grid()
    
    show()


def weight_boxes(x, y, start, power, plot=False, text=False):
    """ 
    """
    
    nBox = start**power                 # Number of boxes
    boxes = np.zeros((nBox, nBox))      # Creating the boxes
    
    xCoords = np.linspace(min(x)-.1, max(x)+.1, nBox+1)     # x limits of boxes
    yCoords = np.linspace(min(y)-.05, max(y)+.05, nBox+1)   # y limits of boxes
    
    for ind, x in enumerate(x):
        xV, xPos = closest(xCoords, x)
        yV, yPos = closest(yCoords, y[ind])
        
        if x <= xV: xPos -= 1
        if y[ind] <= yV: yPos -= 1
        if yPos == -1: yPos = 0
        
        boxes[abs(nBox-1-yPos)][xPos] += 1
    
    # Normalizing boxes
    redBox = boxes / np.sum(boxes)
    
    if plot:
        # Plotting
        fig = figure(figsize=(14,8))
        frame = fig.add_subplot(1,1,1)
        
        if text:
            for xInd in range(len(xCoords)-1):
                for yInd in range(len(yCoords)-1):
                    label = f"{redBox[yInd][xInd]:.3f}"
                    frame.text(xCoords[xInd], yCoords[yInd], label, 
                               va='center', ha='center')
        
        im = frame.imshow(boxes, cmap=cm.inferno)
        fig.colorbar(im)
        
        show()
    
    return redBox


def inform_dim(x, y, start, power):
    """ Calculate the information dimension of the Hénon map """
    
    boxes = weight_boxes(x, y, start, power)    # Values of the boxes
    
    I = 0                                       # Bits of information
    
    for b in boxes:
        for box in b:
            if box != 0: I -= box * log2(box)   # -log(x) = log(1/x)
    
    return I


def change_dim(base, pRange, xv, yv, saveFig=None):
    """ 
    """
    
    inf = [inform_dim(xv, yv, base, p) for p in pRange]         # Information
    
    # Linear fit
    def lin_fit(x, i0, di):
        return i0 + di * x
    
    para, cov = optimization.curve_fit(lin_fit, pRange, inf)    # Fitting
    perr = np.sqrt(np.diag(cov))                                # Errors
    
    # Printing the results
    print(f"The constant = {para[0]:.3f}")
    print(f"The information dimension = {para[1]}")
    print(f"The error = {perr}")
    
    # Making line for plotting
    xVals = np.linspace(min(pRange), max(pRange), 100)
    yVals = lin_fit(xVals, para[0], para[1])
    lab = f"$I(k)$ = {para[1]:.3f}$* k$ + {para[0]:.2f}"
    
    # Plotting
    fig = figure(figsize=(15,8))
    frame = fig.add_subplot(1,1,1)
    
    frame.scatter(pRange, inf, color="navy", marker="X", s=150, zorder=3)
    frame.plot(xVals, yVals, color="darkred", label=lab, lw=2)
    
    frame.tick_params(axis="both", labelsize=15)
    
    frame.set_xlabel("k", fontsize=20)
    frame.set_ylabel("Information (bits)", fontsize=20)
    
    frame.legend(fontsize=20)
    frame.grid(zorder=2)
    
    if saveFig: fig.savefig(str(saveFig))
    else: show()


def main():
    """ Function that will be executed """
    
    # Setting constants
    x0, y0 = 0, 0
    its = int(1e3)
    av, bv = 1.4, 0.3
    
    xv, yv = fh.Henon(x0, y0, its, av, bv)
    figName = "info_dim.pdf"
    
#     hist_plot(xv, 96, saveFig=figName)
#     return_plot(x0, y0, its, av, bv)
#     box_henon(xv, yv, 4, saveFig=False)
    
    xv, yv = fh.Henon(x0, y0, its, av, bv)
    start = 2
    power = 11
#     
#     boxVals = weight_boxes(xv, yv, start, power)
#     information = inform_dim(xv, yv, start, power)
    
#     powers = range(start, power)
#     change_dim(start, powers, xv, yv, saveFig=False)

    mean_fig(10, 10000)

if __name__ == "__main__":
    main()
