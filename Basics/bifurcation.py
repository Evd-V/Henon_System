import numpy as np
from matplotlib.pyplot import figure, show, cm

import full_henon as fh
import helper as he

def henon_bifurc(start, end, iterations, accuracy=1000, cut=950, bvalue=0.3):
    """ Function that generates data to plot the bifurcation of the Hénon map. 
        The first step is generating the values of the parameter "a", and 
        generating an equal amount of random x and y starting points. Then the 
        map is iterated a number of times, given by the input parameter 
        "accuracy". If the points do not diverge, then the last few points are 
        taken and added to a list. The number of points that are added are given 
        by accuracy - cut. Finally the number of x points is defined, which has 
        the same length as the number of y points and ranges from the minimum to 
        the maximum value of the parameter a. This can be used for plotting.
        
        Input:  start      = lower boundary for "a" parameter value (float);
                end        = upper boundary for "a" parameter value (float);
                iterations = number of distinct "a" parameter values (int);
                accuracy   = number of times the Hénon map is iterated (int);
                cut        = iterated points thrown away (int);
                bvalue     = value of the "b" parameter (float);
                
        Returns: apoints   = used "a" parameters (array);
                 xpoints   = "a" parameter values for plotting (array);
                 ypoints   = calculated x points of Hénon map (array).
    """
    
    # Generating the 'a' parameter points
    apoints = np.linspace(start, end, iterations)
    
    # Generating the random starting points of the Hénon map
    x_starting = np.random.uniform(-1, 1, size=iterations)
    y_starting = np.random.uniform(-1, 1, size=iterations)
    
    # List to put the results in
    ypoints = []
    
    # Looping over all values of the 'a' parameter
    for ind, a in enumerate(apoints):   
        # Finding the x and y values of the Hénon map
        xvals, yvals = fh.Henon(x_starting[ind], y_starting[ind], accuracy, a, 
                                bvalue, div=True)
        
        # Adding the values to the list
        if xvals != None:
            xred = xvals[cut:]      # Using accuracy-cut values
            for i in xred: 
                ypoints.append(i)
        else:
            for i in range(int(accuracy-cut)):
                ypoints.append(None)
    
    # For plotting the length of x and y data sets must be equal
    xpoints = np.linspace(start, end, len(ypoints))
    
    return apoints, xpoints, ypoints


def bifurc_grid(aSize, xSize, aLim, xLim, acc=1000, bV=0.3):
    """ Function that plots the bifurcation diagram as a 2D grid instead of all 
        separate points. This results in a higher resolution and much smaller 
        image size. For large grid sizes and number of iterations the 
        computation time can be long.
    """
    
    grid = np.zeros((xSize, aSize))                     # Creating the grid
    aPoints = np.linspace(aLim[0], aLim[1], aSize)      # a points
    xPoints = np.linspace(xLim[0], xLim[1], xSize)      # x points
    
    colW = (aPoints[1] - aPoints[0]) / 14               # Column width / 7
    redF = int(acc / 10)                                # Points thrown away
    
    for ind in range(len(aPoints)):
        print(f"Processing {ind} out of {aSize}")
        aV = aPoints[ind]                               # Improved speed
        extraA = np.linspace(aV-colW, aV+colW, 7)       # Creating extra a vals
        
        xS = np.random.uniform(-1, 1, 7)                # Random x start
        yS = np.random.uniform(-1, 1, 7)                # Random y start
        
        for aInd in range(len(extraA)):                 # Looping over a values
            xV, yV = fh.Henon(xS[aInd], yS[aInd], acc, extraA[aInd], bV, 
                              div=True, threshold=10)   # Henon map
            
            if xV:                                      # if xV != None
                xRed = xV[redF:]                        # Throwing away points
                
                for x in xRed:                          # Remaining points
                    val, xInd = he.take_closest(xPoints, x)
                    grid[xInd][ind] += 1
            
    
    return grid


def save_bifur(fname, grid, delim="|"):
    """ Save the bifurcation diagram """
    np.savetxt(fname, grid, delimiter=delim)

def load_bifur(fname, delim="|"):
    """ Load the bifurcation diagram data """
    return np.loadtxt(fname, delimiter=delim)


def process_bifurc(fname, threshold, delim="|"):
    """ Processing the bifurcation diagram data """
    
    grid = np.loadtxt(fname, delimiter=delim)   # Loading grid
    grid[grid > threshold] = threshold          # Setting maximum value
    maxVals = np.max(grid, axis=0)              # Max values for each column
    
    # Dividing each column by its maximum value if maximum value != 0
    redGrid = np.where(maxVals <= 1, grid, grid / maxVals)
    
    return redGrid[-1::-1]

def plot_bifurc(fname, threshold, xSize, ySize, xLim, yLim, saveFig=None):
    """ Plotting the bifurcation diagram for the Hénon map """
    
    grid = process_bifurc(fname, threshold)         # Retrieving the data
    
    # Setting the ticks and labels for the axes
    nTicks = 5                                      # Number of ticks on axes
    xTicks = np.round(np.linspace(xLim[0], xLim[1], nTicks), 1)  # a tick values
    yTicks = np.round(np.linspace(yLim[0], yLim[1], nTicks), 1)  # x tick values
    
    xLocs = np.linspace(0, xSize, nTicks)           # a tick locations
    yLocs = np.linspace(0, ySize, nTicks)           # x tick locations
    
    # Plotting
    fig = figure(figsize=(15,8))
    frame = fig.add_subplot(1,1,1)
    
    frame.imshow(grid, cmap=cm.binary)
    
    # Setting axes
    frame.set_xlabel("$a$", fontsize=20)
    frame.set_ylabel("$x$", fontsize=20)
    
    frame.set_xticks(xLocs)
    frame.set_yticks(yLocs)
    
    frame.set_xticklabels(xTicks)
    frame.set_yticklabels(yTicks)
    
    frame.tick_params(axis="both", labelsize=15)
    
    if saveFig: fig.savefig(saveFig)
    else: show()    
