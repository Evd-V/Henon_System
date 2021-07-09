import numpy as np

def Create_Line(point1, point2, size=1000):
    """ Function that returns the x and y coordinates of the straight line between point 1 
        and point 2. The input for both is assumed to be (x, y); their order does not matter. 
        The parameter 'size' gives the number of points used to make the line, in general 
        does not have to be big as we are dealing with straight lines. However, if certain 
        operations will be done that result in a stretching and flexing the line, this 
        parameter does become important. In that case a high value for 'size' is desirable.
        
        Input:      point1 = the coordinates of the first point (tuple);
                    point2 = the coordinates of the second point (tuple); 
                    size   = number of points used to create the line (integer);
                    
        Returns:    xvals  = the x points of the newly created line (numpy array); 
                    Yvals  = the y points of the newly created line (numpy array).
    """
    
    # Unpacking the points
    X1 = point1[0]; Y1 = point1[1]
    X2 = point2[0]; Y2 = point2[1]
    
    # Finding the coefficient
    coeff = (Y2 - Y1) / (X2 - X1)
    b = Y1 - coeff * X1
    
    # Finding the x and y values
    xvals = np.linspace(min(X1, X2), max(X1, X2), size)
    yvals = coeff * xvals + b
    
    return xvals, yvals

def Transformation(Xvalues, Yvalues, a, b):
    """ Function that applies the Hénon map to a list of points.
    
        Input:      Xvalues   = x values that have to be transformed (numpy array); 
                    Ystart    = y values that have to be transformed (numpy array)
                    a         = a parameter of the Hénon map (float); 
                    b         = b parameter of the Hénon map (float);
                    
        Returns:    New_Xvals = numpy array; 
                    New_Yvals = numpy array.
    """
    
    new_xvals = Yvalues + 1 - a * Xvalues * Xvalues
    new_yvals = b * Xvalues
            
    return new_xvals, new_yvals

def image_func(vertices, av, bv):
    """ Function that finds the image for given vertices. The input is a list containing
        both the x and y values of all the input vertices. So an example of a correct
        input is: [[x1, y1], [x2, y2]] where the numbers 1 and 2 represent two different
        set of points that represent the vertices. The output bounds has the same
        structure.

        Input:      vertices = list containing the different vertices (list);
                    av       = a parameter of the Hénon map (float);
                    bv       = b parameter of the Hénon map (float);

        Returns:    bounds   = list containing the image of the vertices (list).
    """

    bounds = [Transformation(v[0], v[1], av, bv) for v in vertices]

    return bounds

def plot_n_img(init_vert, n_start=0, n_end=8, output=False, plot=True, ax=None, color=['indigo'],
               lw=[1], av1=1.4, bv1=0.3):
    """ Function that creates the image of a geometrical shape using the Hénon map. The initial
        vertices of the geometric shape are given by the input parameter 'init_vert'. This function
        is able to generate multiple images based on the initial input. This implies that the
        Hénon map will be applied multiple times to the initial conditions based on the input.
        'n_start' gives the lowest order image. So n_start=0 is the image obtained after the map
        has acted on it once; 'n_end' gives the highest order image. It is possible to select which
        output is desirable, either a list containing all images or a plot showing the images or
        both. 'ax' gives the name of the axis of the plot, depends on the plot. If the plot output
        is selected then it is of course required that the rest of the plot is set up correctly.

        Input:      init_vert = initial vertices of the geometrical shapes (list);
                    n_start   = lowest order image (integer);
                    n_end     = highest order image (integer);
                    output    = whether or not the boundaries in a list are the output (Boolean);
                    plot      = whether or not a plot has to be made (Boolean);
                    ax        = axis name of the plot (matplotlib.axes._subplots.AxesSubplot);
                    color     = color of the image;
                    av1       = a parameter of the Hénon map (float);
                    bv1       = b parameter of the Hénon map (float);

        Returns:    optional: all_bounds = list containing the images (list).
    """

    # Starting values
    j = 0
    vert = init_vert
    count = 0

    # Empty list to put the boundaries in
    if output: all_bounds = []

    # Looping
    while j <= n_end:
        bounds = image_func(vert, av1, bv1)

        # Checking if the values need to be added to the boundaries
        if j >= n_start and j <= n_end:
            if output: all_bounds.append(bounds)

            # Checking if the bounds have to be plotted
            if plot:
                for ind, b in enumerate(bounds):
                    if ind == 0:
                        ax.plot(b[0], b[1], label=f'Boundary {j}', color=color[count], lw=lw[count])
                    else:
                        ax.plot(b[0], b[1], color=color[count], lw=lw[count])
            count += 1

        # New conditions for the next loop
        vert = bounds
        j += 1

    if output:
        return all_bounds
