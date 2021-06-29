import numpy as np

def check_limit(point, xp, yp, acc=1e-5):
    """ Function that checks whether or not a point is within a certain range of an
        x and y coordinate. The input parameter 'point' gives the point that has to 
        be checked. 'xp' and 'yp' give the coordinates to which the point will be 
        compared to. 'acc' gives the accuracy for how close the point should be to 
        the x and y coordinates.
        
        Input:      point = point that will be compared (tuple);
                    xp    = x coordinate to which the point will be compared (float);
                    yp    = y coordinate to which the point will be compared (float);
                    acc   = accuracy of how close the point should be (float);
                    
        Returns:    boolean whether or not the point is inside the given range.
    """
    
    # Checking x coordinate
    if point[0] >= xp-acc and point[0] <= xp+acc:
        # Checking y coordinate
        if point[1] >= yp-acc and point[1] <= yp+acc:
            # Point is inside range
            return True
        
    # Point is outside range
    else: return False

def determine_point(xv, yv, acc=1e-10):
    """ Function that determines whether or not the a set of points converge to a point; 
        e.g. whether or not an attractor is a point attractor. 'xv' and 'yv' give the 
        list of x and y coordinates respectively. 'acc' determines how close points have 
        to be to be considered a point attractor.
        
        Input:      xv  = list or array of x coordinates of the points (list or numpy array);
                    yv  = list or array of y coordinates of the points (list or numpy array);
                    acc = accuracy for how close the points should be (float);
                    
        Returns:    the coordinates of the point for a point attractor, None otherwise.
    """
    
    # Constants
    L = len(xv)             # Number of points in the lists
    step = int(L/10)        # Step size that will be used
    count = 0               # Number of times the point has been found in the list
    
    # The last point of the list
    point = (xv[-1], yv[-1])
    
    for i in range(step, L, step):
        # Checking if the current point is equal to the last point of the list
        if check_limit((xv[i], yv[i]), point[0], point[1], acc=acc):
            
            # Point found
            count += 1
            
            # Check to see if it was not just coincidentally
            if count > 2:
                return point            # Point attractor
                    
    return None

def line_height(value, lower_Val, diff):
    """ Function that calculates the hight, on a scale from 0 to 1, for a vertical or horizontal 
        line. The input 'value' gives the absolute hight of where the vertical line should be. 
        'lower_Val' gives the lower bound of the plot; 'diff' gives the difference in the upper 
        bound and the lower bound of the plot. The output 'height' returns the height of the 
        vertical line.
        
        Input:      value     = absolute hight of the vertical line (float); 
                    lower_Val = the lower bound of the plot (float); 
                    Diff      = the difference in upper and lower bound of the plot (float);
                    
        Returns:    height    = the height of the vertical line (float).
    """
    
    # Checking if the value of Yvalue < 0
    if value < 0:
        height = abs((value + lower_Val) / diff)
    
    # For all other cases
    else:
        height = abs((value - lower_Val) / diff)
        
    return height

def create_box(box_lim, Xbound, Ybound):
    """ Function that creates the relative limits for the horizontal and vertical lines 
        for a box. These relative limits can be used for matplotlib.pyplot.axvline and 
        axhline functions; however in reality often the matplotlib.pyplot.vlines and 
        hlines are easier to use as they make use of the absolute limits. 'box_lim' 
        gives the limits of the boxes in dictionary form containing an 'x' and 'y' 
        component. 'Xbound' gives the x boundary of the plot, so it contains the upper 
        and lower limit. 'Ybound' is the exact same as 'Xbound' but now for the y 
        boundaries. The output is a dictionary containing the relative heights of the 
        box limits relative to the plot; the syntax is the same as the input 'box_lim'.
        
        Input:      box_lim  = the limits of the box (dictionary); 
                    Xbound   = x boundaries of the plot (tuple); 
                    Ybound   = y boundaries of the plot (tuple);
                    
        Returns:    all_vals = the limits of the box relative to the plot (dictionary).
    """
    
    # Finding the start and end values of the box
    Xstart, Xend = min(box_lim['x']), max(box_lim['x'])
    Ystart, Yend = min(box_lim['y']), max(box_lim['y'])
    
    # Calculating the minimum value of the bounds
    X_Min = np.min(Xbound)
    Y_Min = np.min(Ybound)
    
    # Finding the difference between maximum and minimum bounds
    X_Difference = np.max(Xbound) - X_Min
    Y_Difference = np.max(Ybound) - Y_Min
    
    # Finding the lowest x and y values for the box
    X_Low = line_height(Xstart, X_Min, X_Difference)
    Y_Low = line_height(Ystart, Y_Min, Y_Difference)
    
    # Finding the highest x and y values for the box
    x_height = line_height(Xend, X_Min, X_Difference)
    y_height = line_height(Yend, Y_Min, Y_Difference)
    
    # Combining the found values
    all_vals = {'x': (X_Low, x_height), 'y': (Y_Low, y_height)}
    return all_vals