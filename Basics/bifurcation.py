import numpy as np
from matplotlib.pyplot import figure, show, cm
import argparse

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



def plot_bifurc_grid(aSize, xSize, aLim, xLim, acc=1000, bV=0.3, saveFig=None):
    """ OLD
        Plotting the bifurcation diagram of the Hénon map. 
    """
    
    nTicks = 5                                      # Number of ticks on axes
    aTicks = np.round(np.linspace(aLim[0], aLim[1], nTicks), 1)  # a tick values
    xTicks = np.round(np.linspace(xLim[0], xLim[1], nTicks), 1)  # x tick values
    
    aLocs = np.linspace(0, aSize, nTicks)           # a tick locations
    xLocs = np.linspace(0, xSize, nTicks)           # x tick locations
    
    grid = bifurc_grid(aSize, xSize, aLim, xLim, acc=acc, bV=bV)
    
    # Finding max and dividing each column by the max value of that column
    redGrid = grid / np.max(grid, axis=0)
    
    # Plotting
    fig = figure(figsize=(15,8))
    frame = fig.add_subplot(1,1,1)
    
    frame.imshow(redGrid[-1::-1], cmap=cm.binary)
    
    # Setting axes
    frame.set_xlabel("$a$", fontsize=20)
    frame.set_ylabel("$x$", fontsize=20)
    
    frame.set_xticks(aLocs)
    frame.set_yticks(xLocs)
    
    frame.set_xticklabels(aTicks)
    frame.set_yticklabels(xTicks)
    
    frame.tick_params(axis="both", labelsize=15)
    
    if saveFig: fig.savefig(saveFig)
    else: show()


def parseArgs():
    """ Testing some stuff """
    parser = argparse.ArgumentParser(description=" Bifurcation Henon map")
    parser.add_argument("a", help="Number of a points", type=int)
    parser.add_argument("aMin", help="Minimum value of a", type=float)
    parser.add_argument("aMax", help="Maximum value of a", type=float)
#     parser.add_argument("size", help="Marker size", type=float)
    parser.add_argument("b", help="Value of the b parameter", type=float)
#     parser.add_argument("Name", help="Name of the saved figure", type=str)
    
    return vars(parser.parse_args())


def main():
    """ Main function that will be executed """
#     aPoints,aMin, aMax, bv = parseArgs().values()
#     av, xv, yv = henon_bifurc(aMin, aMax, aPoints, bvalue=bv)
#     
#     # Plotting
#     fig = figure(figsize=(15,8))
#     frame = fig.add_subplot(1,1,1)
#     
#     frame.scatter(xv, yv, s=0.001, color="navy")
#     
#     frame.tick_params(axis="both", labelsize=15)
#     frame.set_xlabel("a", fontsize=20)
#     frame.set_ylabel("x", fontsize=20)
#     
#     fig.savefig("bifurcation_test.pdf")
    
    aRange = (1, 1.4)
    xRange = (1.4, -1.4)
    aS, xS = 4250, 2500
    figName = "bifurcation_4250_2500.pdf"
    textFile = "bifur_4250_2500_data.txt"
    
#     grid = bifurc_grid(aS, xS, aRange, xRange, acc=int(1e5))
#     np.savetxt(textFile, grid, delimiter="|", fmt="%1.4f")
    plot_bifurc(textFile, int(1.25e3), aS, xS, aRange, xRange, saveFig=figName)
    
    

if __name__ == "__main__":
    main()
    
