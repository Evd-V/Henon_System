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
