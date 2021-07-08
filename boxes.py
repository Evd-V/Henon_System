import numpy as np
from matplotlib.pyplot import figure, show, vlines, hlines, savefig

from full_attractor import Henon

# Calculating the points of the Hénon attractor
Xvalues, Yvalues = Henon(X0, Y0, It, Av, Bv)

def cut_interval(X_Lim, Y_Lim, X_Points, Y_Points):
    """ Function that selects the points of a set of points - for example the Hénon attractor - that 
        lie inside a specific interval. The reason this is useful is that when you are 'zooming' in 
        on a specific part of the attractor and select a certain x and y limits, matplotlib still 
        'generates'/'plots' all off the points including the ones outside the frame which are not 
        visible. When saving this file it results in more, unnecessary, data. So when using this 
        function, only the points that will be visible in the ranges are plotted and hence the file 
        size of the saved figure will be smaller.
        
        Input:      X_Lim      = sorted limits of x values (tuple); 
                    Y_Lim      = sorted limits of x values (tuple); 
                    X_Points   = list of x points that will be cutted (list); 
                    Y_Points   = list of x points that will be cutted (list);
        
        Returns:    X_Interval = cutted list of x points (list); 
                    Y_Interval = cutted list of y points (list).
    """
    
    # Making the lists array to make computations faster
    X_Attractor = np.array(X_Points)
    Y_Attractor = np.array(Y_Points)
    
    # Finding the lower and upper x and y limits
    Lower_X = np.min(X_Lim)
    Upper_X = np.max(X_Lim)
    Lower_Y = np.min(Y_Lim)
    Upper_Y = np.max(Y_Lim)
    
    # Creating empty lists to put the selected points in
    X_Interval = []
    Y_Interval = []
    
    # Looping over all points and selecting the right one
    for i in range(len(X_Attractor)):
        
        # Current x point
        A = X_Attractor[i]
        
        # Checking if it is inside the given limits
        if A > Lower_X and A < Upper_X:
            
            # The current y point
            B = Y_Attractor[i]
            
            # Checking if it is inside the given limits
            if B > Lower_Y and B < Upper_Y:
                X_Interval.append(A)
                Y_Interval.append(B)
                
    return X_Interval, Y_Interval

def find_lines(vals):
    """ Function that finds the x and y limits of a dictionary which contains x and y 
        coordinates. A valid input would be: vals={'x': (1, -0.9, 0.31), 'y': (0.37, 0.93)}. 
        The output is a list containing two tuples; the first tuple has the minimum and 
        maximum x values respectively. The second tuple contains the same but for the 
        y values. In the example above this would thus be: limits=[(-0.9, 1), (0.37, 0.93)].
        
        Input:      vals   = the values of which the limits will be found (dictionary);
        Returns:    limits = the limits of the input values (list).
    """
    # Limits of the box
    x_lim = (min(vals['x']), max(vals['x']))
    y_lim = (min(vals['y']), max(vals['y']))
    
    # Combining the x and y limits
    limits = [x_lim, y_lim]
    
    return limits
    
def create_box_plot(lines, xv=Xvalues, yv=Yvalues, ax=None, cut_interval_=None, ms=1, 
                    extra_lines=("maroon", "-.", 1.5)):
    """ Function that creates the plot containing a box and a set of points (xv, yv). Generally 
        this function can be combined with the function 'create_box_grid' (see below) to create 
        a grid of subplots. The input 'lines' gives the limits of the box that will be plotted, 
        if this function is called inside the 'create_box_grid', these will automatically be 
        given. 'xv' and 'yv' give the points that will be plotted for all subplots. 'ax' gives 
        the name of the matplotlib.pyplot.axes object which is used for plotting. 'cut_interval_' 
        determines whether or not the interval of points should be cutted to prevent plotting 
        too many points that will not be shown. 'ms' gives the marker size for the plot and 
        'extra_lines' gives extra properties of the lines of the boxes; the input is the color, 
        linestyle and linewidth respectively.
        
        Input:      lines         = the limits of the box that will be plotted (list);
                    xv            = the x points that will be plotted (list or numpy array);
                    yv            = the y points that will be plotted (list or numpy array);
                    ax            = the name of the axes of the plot (matplotlib.pyplot.axes);
                    cut_interval_ = the interval that will be cutted if not None (tuple or list);
                    ms            = marker size of the points (float);
                    extra_lines   = extra information for the lines of the box (tuple);
    """
    
    # Checking if the a part has to be cutted
    if cut_interval_ != None:
        # 'Cutting' the points according to the limits
        xv, yv = cut_interval(cut_interval_[0], cut_interval_[1], xv, yv)
    
    # Plotting    
    ax.scatter(xv, yv, s=0.0004*ms, label='points', marker='.', color='navy')
    
    # Vertical lines
    ax.vlines(lines[0][0], ymin=lines[1][0], ymax=lines[1][1], color=extra_lines[0], 
              linestyle=extra_lines[1], lw=extra_lines[2])
    ax.vlines(lines[0][1], ymin=lines[1][0], ymax=lines[1][1], color=extra_lines[0], 
              linestyle=extra_lines[1], lw=extra_lines[2])
    
    # Horizontal lines
    ax.hlines(lines[1][0], xmin=lines[0][0], xmax=lines[0][1], color=extra_lines[0], 
              linestyle=extra_lines[1], lw=extra_lines[2])
    ax.hlines(lines[1][1], xmin=lines[0][0], xmax=lines[0][1], color=extra_lines[0], 
              linestyle=extra_lines[1], lw=extra_lines[2])

    
def create_box_grid(boxes, base_xsize=7, xpoints=Xvalues, ypoints=Yvalues, basic=True, extra=("maroon", "-.", 2)):
    """ Function that can create a grid of plots which all contain the same set of points; however, 
        it is possible to add boxes which result in a zooming effect on a specific part of the set 
        of points. 'boxes' give the limits of these boxes in dictionary form containing both the x 
        and y coordinates, a valid input is: boxes = [{'x': (0, 0.5), 'y': (0.15, 0.28)}]. Multiple 
        boxes can be added by putting adding them to the list; e.g. boxes=[box1, box2] where box1 
        and box2 both contain the coordinates of two separate boxes. 'base_xsize' gives the 
        approximate size of each subplot in the grid in the x direction. 'xpoints' and 'ypoints' 
        give the set of points that will be plotted. 'basic' determines whether or not basic 
        information, like axis labels, plot titles and a grid should be added. 'extra' gives extra 
        information for the lines of the boxes; the input is the color, linestyle and linewidth 
        respectively.
        
        Input:      boxes      = the boxes that will be plotted as a 'zoom' factor (list);
                    base_xsize = approximate size of each subplot in the x direction (float);
                    xpoints    = x points that will be plotted (list or numpy array);
                    ypoints    = y points that will be plotted (list or numpy array);
                    basic      = whether basic information should be plotted (boolean);
                    extra      = extra information for the lines of the boxes (tuple);
    """
    
    # The number of subplots that will be created
    L = len(boxes) + 1
    
    # Subplots
    grid = ceil(L * 0.5)
    
    # size (x,y) = (15, 2*base_size+1)
    size = (15, 2 * base_xsize + 1)
    
    # Plotting
    fig = figure(figsize=size)
    
    # Plotting each subplot
    for i in range(L):
        frame = fig.add_subplot(grid, grid, i+1)
        
        # The first subplot
        if i == 0:
            # Creating the lines of the box
            box_lines = find_lines(boxes[i])
            
            # Creating the subplot
            create_box_plot(box_lines, xv=xpoints, yv=ypoints, ax=frame, extra_lines=extra)
            
        # The last subplot
        elif i == (L-1):
            # The lines of the boxes
            prev_lines = box_lines
            
            # Determining the interval that can be cutted
            cut_int_x = (prev_lines[0][0], prev_lines[0][1])
            cut_int_y = (prev_lines[1][0], prev_lines[1][1])
            
            # Cutting the interval
            cutted = cut_interval(cut_int_x, cut_int_y, xpoints, ypoints)
            
            # Plotting the points
            frame.scatter(xpoints, ypoints, s=0.0004*100*i*i, color='navy', marker='.')
            
            # Setting axes limits
            frame.set_xlim(prev_lines[0][0], prev_lines[0][1])
            frame.set_ylim(prev_lines[1][0], prev_lines[1][1])
            
        # All other subplots
        else:
            # Renaming the lines of the previous box, will be used for the limits later on
            prev_lines = box_lines
            
            # Finding the new lines of the box
            box_lines = find_lines(boxes[i])
            
            # Determining the interval that can be cutted
            cut_int_x = (prev_lines[0][0], prev_lines[0][1])
            cut_int_y = (prev_lines[1][0], prev_lines[1][1])
            
            # Creating the subplot
            create_box_plot(box_lines, xv=xpoints, yv=ypoints, ax=frame, ms=100*i*i, 
                            cut_interval_=(cut_int_x, cut_int_y), extra_lines=extra)
            
            # Setting axes limits
            frame.set_xlim(prev_lines[0][0], prev_lines[0][1])
            frame.set_ylim(prev_lines[1][0], prev_lines[1][1])
        
        # Checking if basic information has to be provided
        if basic:
            
            # Setting the labels of the plot and axes
            frame.set_title(f'Zoom {i} of the Hénon attractor')
            frame.set_xlabel('x')
            frame.set_ylabel('y')

            frame.grid()
        
    show()
