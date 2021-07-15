import numpy as np
from matplotlib.pyplot import figure, show, imshow, savefig, cm

import text_processing as tp
import lyapunov as ly

def make_2d_plot(fname, axis=("a", "b"), save_figure=False):
    """ Function that creates a two dimensional plot for a given filename. This function works 
        best with files that are generated using the 'write_data' function. The input 'axis' 
        gives the labels for the axis in the shape (y,x); so the first entry is the y direction 
        and the second is the x direction. If save_figure is set to True, then the figure is 
        saved.
        
        Input:      fname = name of the file that contains the data (string);
                    axis  = labels of the axis (tuple).
    """
    
    # Reading the data
    data_read = tp.read_data(fname)
    
    # Reading the headers
    headers = tp.analyse_headers(data_read[1], axis)
    
    # Tick marks for axes
    xticks = headers[1]
    yticks = headers[0]
    
    # Reading the data
    combined_data = tp.comb_data(data_read[0], len(xticks)-1, len(yticks)-1)
    
    # Tick locations
    L = len(combined_data)-1
    
    # x ticks
    xl = len(xticks)-1
    xtick_locs = [i*L/xl for i in range(xl+1)]
    
    # y ticks
    yl = len(yticks)-1
    ytick_locs = [i*L/yl for i in range(yl+1)]
    
    # Plotting
    fig = figure(figsize=(8,8))
    frame = fig.add_subplot(1,1,1)
    
    im = frame.imshow(min_data, cmap=cm.jet)
    fig.colorbar(im, shrink=0.8, aspect=10)
    
    # Frame labels
    frame.set_xlabel(axis[1])
    frame.set_ylabel(axis[0])
    
    # Tick locations and labels
    frame.set_xticks(xtick_locs)
    frame.set_yticks(ytick_locs)

    frame.set_xticklabels(xticks)
    frame.set_yticklabels(yticks)
    
    if save_figure:
        fig.savefig("lyapunov_2d_plot.png")
    
    show()
    
def lyapunov_grid(fname_max, fname_min, axis=("a", "b"), plot=True, save_figure=False):
    """ Function that determines the Lyapunov grid for two files which contain the maximum and 
        minimum Lyapunov exponents. 'axis' denotes the labels of the axes which should 
        correspond to what is written in both files. If 'plot' is True, then a two dimensional 
        plot is displayed; save_figure can be set to True to save this figure. It is assumed that 
        both files contain the same number of tables.
        
        Input:      fname_max = name of the file containing the maximum Lyapunov exponents (string);
                    fname_min = name of the file containing the minimum Lyapunov exponents (string);
                    axis      = name of the axes (tuple);
                    plot      = whether or not the type of attractors should be plotted (bool);
                    
        Returns:    attr      = list containing the type of attractor (list).
    """
    
    # Reading the data
    data_min = tp.read_data(fname_min)
    data_max = tp.read_data(fname_max)
    
    # Reading the headers, it is assumed that both files have the same range of values
    headers = tp.analyse_headers(data_min[1], axis)
    
    # Tick marks for axes
    xticks = headers[1]
    yticks = headers[0]
    
    # Reading the data
    combined_min = tp.comb_data(data_min[0], len(xticks)-1, len(yticks)-1, rewr_to=None)
    combined_max = tp.comb_data(data_max[0], len(xticks)-1, len(yticks)-1, rewr_to=None)
    
    # Determining the type of attractor    
    attr = [[ly.det_att(combined_max[row][entry], combined_min[row][entry], acc=0.05) 
             for entry in range(len(combined_min[row]))] for row in range(len(combined_min))]
        
    if plot:
        # Tick locations
        L = len(combined_min)-1

        # x ticks
        xl = len(xticks)-1
        xtick_locs = [i*L/xl for i in range(xl+1)]

        # y ticks
        yl = len(yticks)-1
        ytick_locs = [i*L/yl for i in range(yl+1)]
        
        # Plotting
        fig = figure(figsize=(8,8))
        frame = fig.add_subplot(1,1,1)

        im = frame.imshow(attr, cmap=cm.gist_rainbow)
        fig.colorbar(im, shrink=0.8, aspect=10)

        # Frame labels
        frame.set_xlabel(axis[1])
        frame.set_ylabel(axis[0])

        # Tick locations and labels
        frame.set_xticks(xtick_locs)
        frame.set_yticks(ytick_locs)

        frame.set_xticklabels(xticks)
        frame.set_yticklabels(yticks)

        if save_figure:
            fig.savefig("lyapunov_grid.png")
        
        show()
        
    return attr
