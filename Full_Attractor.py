import numpy as np

def Henon(Xstart, Ystart, Iterations, a, b, div=False, threshold=1e3):
    ''' Function that calculates the location of points according to the Hénon map.

        Input:      Xstart: initial x condition (float);
                    
                    Ystart: initial y condition (float);
                    
                    Iterations: number of iterations (integer);
                    
                    a: value for parameter a (float);
                    
                    b: value for parameter b (float);

                    div: parameter that can be used if we expect the values for
                         x and y to diverge. If false (default) then the expectation
                         ist that there is convergence; if true then divergence
                         is expected (boolean);

                    threshold: the maximum value an x or y coordinate can have.
                               If this value is exceeded than divergence is
                               assumed and the previously generated values are
                               returned (float);
                               

        Returns:    Xvals: all generated x values (list);
                    
                    Yvals: all generated y values (list);
    '''

    # The initial values
    Xvals = [Xstart]
    Yvals = [Ystart]

    # Improvement in computing speed
    Xadd = Xvals.append
    Yadd = Yvals.append

    # Finding all other values
    for i in range(Iterations):

        # Slight improvement in computing speed
        X_arr = Xvals[i]
        Y_arr = Yvals[i]

        # Calculating the new x and y values
        Xadd(Y_arr + 1 - a * X_arr * X_arr)
        Yadd(b * X_arr)

        # Checking if we expect divergence
        if div:
            # Checking if it diverges
            if abs(X_arr) > threshold or abs(Yvals[i]) > threshold:
                return Xvals, Yvals

    return Xvals, Yvals
