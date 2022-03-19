import numpy as np
from matplotlib.pyplot import figure, cm, savefig, show

import full_henon as fh
import lyapunov as ly
import create_grid as cg


def lya_dim(nIts=int(1e5), a=1.4, b=0.3, xS=0, yS=0):
    """ Compute the Lyapunov dimension of the Hénon map """
    
    x0 = y0 = 0                             # Starting values of Hénon map
    cut = 1000                              # Points thrown away
    
    xv, yv = fh.Henon(xS, yS, nIts, a, b)           # Hénon map
    exp = ly.Lyapunov(nIts-cut, xv[cut:], a, b)     # Lyapunov exponents
    
    m = 0
    for ind in range(len(exp)):
        if sum(exp[:ind+1]) >= 0: m += 1
    
    if max(exp) <= 0: dim = 0
    elif sum(exp) > 0: dim = 2
    else: dim = m + sum(exp[:m]) / abs(exp[m])
    
    return dim

def lya_henon_dim(lya):
    """ Assumes lya[0] >= lya[1]
    """
    
    if max(lya) < 0: dim = 1
#     elif max(lya) < acc and max(lya) > -acc: dim = 1
    elif sum(lya) > 0: dim = 2
    else: dim = 1 - lya[0] / lya[1]
    
    return dim


def plot_dim(var, const, a=True, its=int(5e3), xS=0, yS=0, saveFig=None):
    """ Plot the dimension when varying one of the parameters """
    
    if a: dims = [lya_dim(nIts=its, a=a, b=const, xS=xS, yS=yS) for a in var]
    else: dims = [lya_dim(nIts=its, a=const, b=b, xS=xS, yS=yS) for b in var]
    
    # Plotting
    fig = figure(figsize=(15,8))
    frame = fig.add_subplot(1,1,1)
    
    frame.scatter(var, dims, color="navy", marker='x', s=10)
    
    if a: frame.set_xlabel("a")
    else: frame.set_xlabel("b")
    frame.set_ylabel("Dimension")
    
    frame.grid()
    
    if saveFig: fig.savefig(str(saveFig))
    else: show()


def  det_lya_dim(maxData, minData, size):
    """ Assumes lya1 >= lya2 """
    
    L = range(len(maxData))
    dimen = [np.zeros((size, size)) for i in L]
    
    for frame in L:
        s = range(len(maxData[frame]))
        for indX in s:
            for indY in s:
                dimen[frame][indX][indY] = lya_henon_dim(
                                                [maxData[frame][indX][indY], 
                                                 minData[frame][indX][indY]])
    
    return dimen


def plot_dim_grid(dimGrid, xRange, yRange, cMap=cm.inferno, fname=None):
    """ 
    """
    
    # Plotting
    fig = figure()
    frame = fig.add_subplot(1,1,1)
    
    im = frame.imshow(dimGrid, cmap=cMap)
    fig.colorbar(im, pad=0.05, aspect=12, shrink=0.92)
    
    # Setting axes
    xTicks = np.linspace(0, len(dimGrid[0]), int(len(dimGrid[0])/75))
    yTicks = np.linspace(0, len(dimGrid), int(len(dimGrid)/75))
    
    xLabels = np.round(np.linspace(min(xRange), max(xRange), 
                       len(xTicks)), decimals=1)
    yLabels = np.round(np.linspace(min(yRange), max(yRange), 
                       len(yTicks)), decimals=1)
    
    frame.set_xticks(xTicks)
    frame.set_yticks(yTicks)
    
    frame.set_xticklabels(xLabels, fontsize=15)
    frame.set_yticklabels(yLabels, fontsize=15)
    
    frame.set_xlabel("$b$", fontsize=20)
    frame.set_ylabel("$a$", fontsize=20)
    
    
    if fname != None: fig.savefig(fname)
    else: show()


def create_dim_grid(fmax, fmin, frame_size, ystack, aRange, bRange):
    """ 
    """
    
    max_generated = cg.read_data(fmax, frame_size)     # Max L.E.
    min_generated = cg.read_data(fmin, frame_size)     # Min L.E.
    dim_gen = det_lya_dim(max_generated, min_generated, frame_size)   # Dim
    
    # Concatenate separate frame in right order and shape
    all_colls = [np.concatenate
                (dim_gen[row*ystack:(row+1)*ystack], axis = 0) 
                for row in range(ystack)]
    
    xCut, yCut = 250, 200               # Part to be cutted from frame
    
    tot_generated = np.hstack(tuple(all_colls))[xCut:, yCut:]
    aRange = aRange[yCut:]
    bRange = bRange[xCut:]
    
    fName = "dimensions_grid.pdf"
    plot_dim_grid(tot_generated, bRange, aRange, fname=fName)
    
    return tot_generated


def main():
    """ Function that will be executed """
    
#     lDim = lya_dim()
#     print(f"The dimension of the Hénon map is: {lDim:.8f}")
    
#     figName = "dim_var_b.pdf"
#     aVals = np.linspace(1, 1.5, 1000)
#     bVals = np.linspace(-0.05, 0.35, 1000)
#     plot_dim(bVals, 1.4, a=False, saveFig=figName)
    
    fileMax = "lya2_max_540_1.txt"
    fileMin = "lya2_min_540_1.txt"
    frameSize = 90
    yStack = 6
    aVals = np.linspace(0.5, 1.5, 6*90)
    bVals = np.linspace(-0.5, 0.5, 6*90)
    create_dim_grid(fileMax, fileMin, frameSize, yStack, aVals, bVals)


if __name__ == "__main__":
    main()
