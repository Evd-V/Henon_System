import numpy as np
from matplotlib.pyplot import figure, cm, show

import full_henon as fh
import helper as he


def basin_attr(xVals, yVals, xSize, ySize, its=100, a=1.4, b=0.3):
    """ Function that creates the basin of attraction """
    
    # Creating x and y starting values
    xRange = np.linspace(xVals[0], xVals[1], xSize)
    yRange = np.linspace(yVals[1], yVals[0], ySize)
    
    grid = np.zeros((ySize, xSize))     # Grid
    
    # Looping over all staring values
    for xInd, x0 in enumerate(xRange):
        for yInd, y0 in enumerate(yRange):
            xv, yv = fh.Henon(x0, y0, its, a, b, div=True, threshold=1e2)
            
            if xv != None: grid[yInd][xInd] += 1
    
    return grid


def plot_basin(saveFig=None):
    """ Function that plots the basin of attraction. """
    
    
    # Values for creating the grid and plot
    xVals = (-2, 2)         # Range of x values
    yVals = (-3, 5)         # Range of y values
    xSize = 2048            # Number of x pixels
    ySize = 1080            # Number of y pixels
    numb = 5                # Number of x and y ticks for the plot
    
    # Axes labels and ticks
    xLabels = np.linspace(xVals[0], xVals[1], numb).astype(int)
    yLabels = np.linspace(yVals[0], yVals[1], numb).astype(int)
    xLocs = np.linspace(0, xSize, numb)
    yLocs = np.linspace(ySize, 0, numb)
    
    # Finding the trapping region
    trappingRegion = basin_attr(xVals, yVals, xSize, ySize, its=25)
    
    # Plotting
    fig = figure(figsize=(15,8))
    frame = fig.add_subplot(1,1,1)
    
    frame.imshow(trappingRegion, cmap=cm.binary)
    
    # Axes labeling and ticks
    frame.set_xlabel(r"$x_0$", fontsize=20)
    frame.set_ylabel(r"$y_0$", fontsize=20)
    
    frame.set_xticks(xLocs)
    frame.set_yticks(yLocs)
    
    frame.set_xticklabels(xLabels, fontsize=15)
    frame.set_yticklabels(yLabels, fontsize=15)
    
    if saveFig != None: fig.savefig(saveFig)
    else: show()

def trapp_region(saveFig=None, output=False):
    """ Function that plots the trapping region of the Hénon map """
    
    # Vertices (see Peitgens et al.)
    P1 = (-1.33, 0.42)
    P2 = (1.32, 0.133)
    P3 = (1.245, -0.14)
    P4 = (-1.06, -0.5)
    
    # Creating the lines
    Vert1 = he.Create_Line(P1, P2)
    Vert2 = he.Create_Line(P2, P3)
    Vert3 = he.Create_Line(P3, P4)
    Vert4 = he.Create_Line(P4, P1)
    
    # Combining the points and vertices in lists
    ps = [P1, P2, P3, P4]
    vs = [Vert1, Vert2, Vert3, Vert4]
    
    if output: return ps, vs
    
    # Generating points of the Hénon map
    xv, yv = fh.Henon(0, 0, int(1e4), 1.4, 0.3)
    
    # Plotting
    fig = figure(figsize=(10,8))
    frame = fig.add_subplot(1,1,1)
    
    frame.scatter(xv, yv, s=0.01, label='points', color='darkblue', marker='.')
    
    for i in range(len(ps)):
        frame.scatter(ps[i][0], ps[i][1], color='crimson', marker='o', s=50)
        frame.plot(vs[i][0], vs[i][1], color='seagreen', linestyle='--', lw=1.8)
    
    frame.set_xlabel("x", fontsize=20)
    frame.set_ylabel("y", fontsize=20)
    
    frame.grid()
    
    if saveFig != None: fig.savefig(saveFig)
    else: show()

def plot_n_img(n_start=0, n_end=8, output=False, plot=True, saveFig=None,
               color=['indigo'], lw=[1], av1=1.4, bv1=0.3):
    """ Function that creates the image of a geometrical shape using the Hénon 
        map. The initial vertices of the geometric shape are given by the input 
        parameter 'init_vert'. This function is able to generate multiple images 
        based on the initial input. This implies that the Hénon map will be 
        applied multiple times to the initial conditions based on the input.
        'n_start' gives the lowest order image. So n_start=0 is the image 
        obtained after the map has acted on it once; 'n_end' gives the highest 
        order image. It is possible to select which output is desirable, either 
        a list containing all images or a plot showing the images or both.
        
        Input:      n_start   = lowest order image (integer);
                    n_end     = highest order image (integer);
                    output    = whether or not the boundaries in a list are the 
                                output (Boolean);
                    plot      = whether or not a plot has to be made (Boolean);
                    saveFig   = if the figure has to be saved (None or string);
                    color     = color of the images (list);
                    lw        = line widths of the different images (list);
                    av1       = a parameter of the Hénon map (float);
                    bv1       = b parameter of the Hénon map (float);

        Returns:    optional: all_bounds = list containing the images (list).
    """

    # Starting values
    j = 0
    points, vert = trapp_region(output=True)
    
    count = 0
    
    # Empty list to put the boundaries in
    if output: all_bounds = []
    
    # Initializing the plot
    fig = figure(figsize=(15,8))
    frame = fig.add_subplot(1,1,1)
    
    for ind, v in enumerate(vert):
        frame.scatter(points[ind][0], points[ind][1], color='crimson', 
                      marker='o', s=65, zorder=3)
        frame.plot(v[0], v[1], color='seagreen', linestyle='--', lw=2)
    
    # Looping
    while j <= n_end:
        bounds = he.image_func(vert, av1, bv1)
        
        # Checking if the values need to be added to the boundaries
        if j >= n_start and j <= n_end:
            if output: all_bounds.append(bounds)
        
            for ind, b in enumerate(bounds):
                if ind == 0:
                    frame.plot(b[0], b[1], label=f"Image {j+1}", zorder=3-j/10, 
                               color=color[count], lw=lw[count])
                else:
                    frame.plot(b[0], b[1], color=color[count], lw=lw[count])
            count += 1
        
        # New conditions for the next loop
        vert = bounds
        j += 1
    
    # Finishing the plot
    frame.set_xlabel(r"$x$", fontsize=20)
    frame.set_ylabel(r"$y$", fontsize=20)
    frame.tick_params(axis="both", labelsize=15)
    
    frame.legend(fontsize=20)
    frame.grid()
    
    if saveFig != None: fig.savefig(str(saveFig))
    elif plot: show()
    elif output: return all_bounds
