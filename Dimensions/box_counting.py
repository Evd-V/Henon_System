import numpy as np
from scipy.optimize import curve_fit
from matplotlib.pyplot import figure, show, cm, xticks, yticks

import full_henon as fh
import helper as he


def closest(array, val):
    """ Finding closest value in list """
    
#     lst = np.asarray(lst)
    ind = (np.abs(array - val)).argmin()
    
    return array[ind], ind


def box_counting(xv, yv, sF, xS=4, yS=4):
    """ Improved version of the function box_counting """
    
    finxS = int(xS / sF)                        # Final x box size
    finyS = int(yS / sF)                        # Final y box size
    
    # Region in which Hénon map is defined
    xMin, xMax = -1.33, 1.32
    yMin, yMax = -0.5, 0.42
    
    grid = np.zeros((finxS, finyS))             # Creating the grid
    xRange = np.linspace(xMin, xMax, finxS)     # x range of grid
    yRange = np.linspace(yMin, yMax, finyS)     # y range of grid
    
    for ind in range(len(xv)):
        xPos, xInd = he.take_closest(xRange, xv[ind])   # x index in grid
        yPos, yInd = he.take_closest(yRange, yv[ind])   # y index in grid
        grid[yInd][xInd] += 1                           # Closest pixel in grid
    
    gridN = np.count_nonzero(grid)              # Counting non zero values
    
    return gridN


def naive_box_dim(xv, yv, sRange, saveFig=None):
    """ Naive implementation of the box-counting dimension """
    
    grids = np.asarray([box_counting(xv, yv, s) for s in sRange]) # Counting boxes
    print(grids)
    
    # Taking logarithms
    grids = np.log2(grids)
    sRange = -np.log2(sRange)                           # log(1/s) = -log(s)
    
    # Linear fit
    def fit_linear(x, a, b):
        return a * x + b
    
    para, error = curve_fit(fit_linear, sRange, grids)  # Best fit parameters
    
    # Label
    lab = f"$\log_2 (N(s))$ = {para[0]:.2f} $* \log_2 (1/s)$ + {para[1]:.2f}"
    
    xRange = np.linspace(min(sRange), max(sRange), int(1e3))    # x values
    yRange = fit_linear(xRange, *para)                          # y values
    
    # Plotting
    fig = figure(figsize=(12,8))
    frame = fig.add_subplot(1,1,1)
    
    frame.scatter(sRange, grids, s=175, marker="X", color="navy", zorder=3)
    frame.plot(xRange, yRange, lw=2, label=lab, color="crimson")
    
    frame.set_xlabel("$\log_2 (1/s)$", fontsize=20)
    frame.set_ylabel("$\log_2 (N(s))$", fontsize=20)
    
    frame.tick_params(axis='both', labelsize=15)
    
    frame.legend(fontsize=20)
    frame.grid(zorder=2)
    
    if saveFig: fig.savefig(saveFig)
    else: show()


def red_box_dim(sF, nIts, xv, yv, xv2, yv2):
    """ Calculate the reduced box counting dimension """
    
    gridN = np.asarray(box_counting(xv, yv, sF))        # N(s, n)
    grid2N = np.asarray(box_counting(xv2, yv2, sF))     # N(s, 2n)
    grid2S = np.asarray(box_counting(xv, yv, 2*sF))     # N(2s, n)
    
    print(f"N(s, n) = {gridN}")
    print(f"N(2s, n) = {grid2S}")
    
    # From Grassberger
    alpha, beta = 2.42, 0.89                            # Values of constants
    mult1 = (sF**(-alpha)) * (nIts**(-beta))            # Recurring factor
    mult2 = ((2*sF)**(-alpha)) * (nIts**(-beta))
    
    # See Peitgens, Jurgens, Saupe
    denom = (1 - 2**(-beta)) * mult1                    # Denominator
    gamma1 = (grid2N - gridN) / denom                   # Constant gamma_1
    
    nS = gridN + gamma1 * mult1                         # Finding N(s)
    n2S = grid2S + gamma1 * mult2                       # Finding N(2s)
    
    boxDim = (np.log(nS) - np.log(n2S)) / np.log(2)     # The dimension
    
    return boxDim


def main():
    """ Main function that will be executed """
    
    # Parameters for the Hénon map
    x0, y0 = 0, 0
    a, b = 1.4, 0.3
    nIts = int(1e5) - 1
    
    # Iterating the Hénon map
    xv, yv = fh.Henon(x0, y0, nIts, a, b)               # Hénon map
#     xv2, yv2 = fh.Henon(x0, y0, 2*nIts, a, b)           # 2x iterations
    
    # Parameters for finding the box counting dimension
    steps = np.linspace(0, -14, 15)
    stepSize = 2**steps
    
    figName = "naive_box_dim_2.pdf"
    naive_box_dim(xv,yv, stepSize, saveFig=figName)
    
#     for stp in stepSize:
#         print(f"Now processing s = {stp}")
#         testDim = red_box_dim(stp, nIts, xv, yv, xv2, yv2)
#         print(f"The dimension = {testDim}")
#         print()
    
#     finalS = 2**(-7)
#     
#     boxDim = red_box_dim(finalS, nIts, xv, yv, xv2, yv2)
#     print(f"The box dimension is: {boxDim}.")


if __name__ == "__main__":
    main()
