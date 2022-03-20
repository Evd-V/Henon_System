import numpy as np
from bisect import bisect_left

def det_att(lya1, lya2, acc=0.05):
    """ Function that finds the type of attractor for two given Lyapunov 
        exponents; it is assumed that lya1 >= lya2. For some type of attractor 
        it is required to see if either one of the two exponents are zero or 
        that the exponents are equal to each other. Since the accuracy of the 
        exponents is limited there has to be some threshold at which it is 
        determined that an exponent is zero or that both are equal to each other. 
        The input parameter acc represents this accuracy; the default value is 
        0.1 which is relatively high. The function returns an integer between 0 
        and 5 which represent which type of attractor it is.
        
        Input:      lya1 = first Lyapunov exponent (float);
                    lya2 = second Lyapunov exponent (float);
                    acc  = accuracy (float);
                    
        Returns:    type of attractor (integer).
    """
    
    if lya1 is None: return 5                     # No attractor
    
    # 6 possibilities, see Garst, S., & Sterk, A. E. (2018)
    elif lya1 < 0-acc:
        if lya1 > lya2+acc: return 0              # 0 > lya1 > lya2, Point
        else: return 1                            # 0 > lya1 = lya2, Point
        
    elif lya1 > -acc and lya1 < acc: return 2     # 0 = lya1 > lya2, Periodic
    elif lya1 > 0:
        if lya2 < acc: return 3                   # lya1 > 0 >= lya2, Chaotic
        else: return 4                            # lya1 >= lya2 > 0, Chaotic
        
    else: return 5                                # No attractor
    
def array_att(max_data, min_data, size):
    """ Determine the type of attractor for an array of Lyapunov exponents """
    
    L = range(len(max_data))
    types = [np.zeros((size, size)) for i in L]
    
    for frame in L:
        s = range(len(max_data[frame]))
        for indX in s:
            for indY in s:
                types[frame][indX][indY] = det_att(max_data[frame][indX][indY], 
                                            min_data[frame][indX][indY])
    
    return types

def take_closest(myList, myNumber):
    """
        Taken from: 
        https://stackoverflow.com/questions/12141150/from-list-of-integers-get-
        number-closest-to-a-given-value
        and altered slightly.
    
        Assumes myList is sorted. Returns closest value to myNumber. If two numbers 
        are equally close, return the smallest number. Makes use of bisection method, 
        generally very fast.
    
        Input:    myList = list or numpy array; 
                  myNumber = floating point number;
                  
        Returns:  closest value(float);
                  corresponding index (int_.
    """
    
    # Finding the position
    Position = bisect_left(myList, myNumber)
    
    # Checking to see if the position is the first entry
    if Position == 0:
        return myList[0], 0
    
    # Checking to see if the position is the last entry
    if Position == len(myList):
        return myList[-1], -1
    
    # Value before and after the 'position'
    before = myList[Position - 1]
    after = myList[Position]
    
    # Checking to see whether the two numbers are really close
    if after - myNumber < myNumber - before:
        return after, Position
    
    else:
        return before, Position-1

def Create_Line(point1, point2, size=1000):
    """ Function that returns the x and y coordinates of the straight line 
        between point 1 and point 2. The input for both is assumed to be (x, y); 
        their order does not matter. The parameter 'size' gives the number of 
        points used to make the line, in general does not have to be big as we 
        are dealing with straight lines. However, if certain operations will be 
        done that result in a stretching and bending the line, this parameter 
        does become important. In that case a high value for 'size' is desirable.
        
        Input:      point1 = the coordinates of the first point (tuple);
                    point2 = the coordinates of the second point (tuple); 
                    size   = number of points used to create the line (integer);
                    
        Returns:    xvals  = the x points of the created line (numpy array); 
                    Yvals  = the y points of the created line (numpy array).
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
    
        Input:      Xvalues   = x values that will be transformed (numpy array); 
                    Ystart    = y values that will be transformed (numpy array)
                    a         = a parameter of the Hénon map (float); 
                    b         = b parameter of the Hénon map (float);
                    
        Returns:    New_Xvals = numpy array; 
                    New_Yvals = numpy array.
    """
    
    new_xvals = Yvalues + 1 - a * Xvalues * Xvalues
    new_yvals = b * Xvalues
            
    return new_xvals, new_yvals

def image_func(vertices, av, bv):
    """ Function that finds the image for given vertices. The input is a list 
        containing both the x and y values of all the input vertices. So an 
        example of a correct input is: [[x1, y1], [x2, y2]] where the numbers 1 
        and 2 represent two different set of points that represent the vertices. 
        The output bounds has the same structure.
        
        Input:      vertices = list containing the different vertices (list);
                    av       = a parameter of the Hénon map (float);
                    bv       = b parameter of the Hénon map (float);
        
        Returns:    bounds   = list containing the image of the vertices (list).
    """
    
    bounds = [Transformation(v[0], v[1], av, bv) for v in vertices]
    
    return bounds
