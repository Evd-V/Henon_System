import numpy as np

def Henon(Xstart, Ystart, Iterations, a, b, div=False, threshold=1e3):
    """ Function that calculates the location of points for the Henon map.

        Input:      Xstart     = initial x condition (float);
                    Ystart     = initial y condition (float);
                    Iterations = number of iterations (integer);
                    a          = value for parameter a (float);
                    b          = value for parameter b (float);
                    div        = parameter that can be used if we expect the 
                                 values for x and y to diverge. If false then 
                                 convergence is expected;if true then divergence
                                 is expected (boolean);
                    threshold  = the maximum value an x or y coordinate can have.
                                 If this value is exceeded than divergence is
                                 assumed and None is returned (float);

        Returns:    Xvals      = all generated x values (list);
                    Yvals      = all generated y values (list);
    """

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
                return None, None

    return Xvals, Yvals

    
def step_0(x_ax, y_ax):
    """ 
    """
    # Creating the values for the angle
    radians = np.linspace(0, 2*np.pi, 400)

    # Creating the x and y values for the ellipse
    Xvals = x_ax * np.cos(radians)
    Yvals = y_ax * np.sin(radians)
    
    return Xvals, Yvals


def step_1(X, Y, a):
    """ Function that calculates the x and y values of the first step of the 
        Hénon map. The initial shape on which the first step of the Hénon map 
        acts is taken to be an ellipse just like Hénon did in his initial paper.
        
        Input:
            X: initial x values (numpy array);
            Y: initial y values (numpy array);
            a: value for parameter a (float);
        
        Returns:
            Xstep1: generated x values (numpy array);
            Ystep1: generated y values (numpy array).
    
    """
    
    # Creating the x and y values for the first step of the transformation
    Xstep1 = X
    Ystep1 = Y + 1 - a * X * X
    
    return Xstep1, Ystep1

def step_2(X, Y, b):
    """ Function that calculates the x and y values of the second step of the 
        Hénon map. The x and y values on which this second step will act have to 
        be given. These can be the generated x and y values of the first step or 
        other x and y values.
        
        Input:
            X: initial x values (numpy array);
            Y: initial y values (numpy array);
            b: value for parameter b (float);
        
        Returns:
            Xstep2: generated x values (numpy array);
            Ystep2: generated y values (numpy array);
    """
    
    # Creating the x and y values for the second step of the transformation
    Xstep2 = b * X
    Ystep2 = Y
    
    return Xstep2, Ystep2

def step_3(X, Y):
    """ Function that calculates the x and y values of the third step of the 
        Hénon map. The x and y values on which this third step will act have to 
        be given. These can be the generated x and y values of the second or 
        first step or other x and y values.
        
        Input:
            X: initial x values (numpy array);
            Y: initial y values (numpy array);
        
        Returns:
            Xstep3: generated x values (numpy array);
            Ystep3: generated y values (numpy array);
    """
    
    # Creating the x and y values for the third step of the transformation
    Xstep3 = Y
    Ystep3 = X
    
    return Xstep3, Ystep3


def plotSteps(x_ax, y_ax, steps, a=1.4, b=0.3, saveFig=None):
    """ Plot one or more steps of the Hénon map """
    
    # Generating the three different steps
    S0 = step_0(x_ax, y_ax)
    S1 = step_1(S0[0], S0[1], a)
    S2 = step_2(S1[0], S1[1], b)
    S3 = step_3(S2[0], S2[1])
    
    genSteps = [S0, S1, S2, S3]     # All the different steps
    n = len(steps)                  # Number of steps that have to be plotted
    
    xLim = (-1.6, 1.6)              # x limits for plots
    yLim = (-2.3, 2)                # y limits for plots
    
    # Plotting
    fig = figure(figsize=(15,8))
    
    for f in range(n):
        frame = fig.add_subplot(1,n,f+1)
        frame.plot(genSteps[steps[f]][0], genSteps[steps[f]][1], lw=2.4)
        
        frame.tick_params(axis="both", labelsize=15)
        frame.set_xlabel("$x$", fontsize=20)
        frame.set_ylabel("$y$", fontsize=20)
        frame.grid()
        
        if steps[f] != 3:
            frame.set_xlim(xLim[0], xLim[1])
            frame.set_ylim(yLim[0], yLim[1])
        
        else:                                   # Invert the axes
            frame.set_xlim(yLim[0], yLim[1])
            frame.set_ylim(xLim[0], xLim[1])
    
    fig.tight_layout()
    
    if saveFig: fig.savefig(str(saveFig))
    else: show()
