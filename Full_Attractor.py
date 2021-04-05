import numpy as np

def Henon(Xstart, Ystart, Iterations, a, b, div=False, threshold=1e3):
    ''' Function that calculates the location of points according to the Hénon map.

        Input:

            Xstart: initial x condition (float);

            Ystart: initial y condition (float);

            Iterations: number of iterations (integer);

            a: value for parameter a (float);

            b: value for parameter b (float);

            div: parameter that can be used if we expect the values for
                 x and y to diverge. If false (default) then the expectation
                 is that there is convergence; if true then divergence
                 is expected (boolean);

            threshold: the maximum value an x or y coordinate can have.
                       If this value is exceeded than divergence is
                       assumed and the previously generated values are
                       returned (float);

        Returns:

            Xvals: all generated x values (list);

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

def step_1(x_ax, y_ax, a):
    ''' Function that calculates the x and y values of the first step of the Hénon map.
        The initial shape on which the first step of the Hénon map acts is taken to be
        an ellipse just like Hénon did in his initial paper.

        Input:

            x_ax: value of the size of the x axis of the ellipse (float);
            y_ax: value of the size of the y axis of the ellipse (float);
            a: value for parameter a (float);

        Returns:

            Xstep1: x values after the first step of the Hénon map (numpy array);
            Ystep1: y values after the first step of the Hénon map (numpy array);

    '''

    # Creating the values for the angle
    radians = np.linspace(0, 2*np.pi, 400)

    # Creating the x and y values for the ellipse
    Xvals = x_ax * np.cos(radians)
    Yvals = y_ax * np.sin(radians)

    # Creating the x and y values for the first step of the transformation
    Xstep1 = Xvals
    Ystep1 = Yvals + 1 - a * Xvals * Xvals

    return Xstep1, Ystep1

def step_2(X, Y, b):
    ''' Function that calculates the x and y values of the second step of the Hénon map.
        The x and y values on which this second step will act have to be given. These
        can be the generated x and y values of the first step or other x and y values.

        Input:

            X: x values on which the second step of the Hénon map will act (numpy array);
            Y: y values on which the second step of the Hénon map will act (numpy array);
            b: value for parameter b (float);


        Returns:

            Xstep2: x values after the second step of the Hénon map has acted (numpy array);
            Ystep2: y values after the second step of the Hénon map has acted (numpy array);
    '''

    # Creating the x and y values for the second step of the transformation
    Xstep2 = b * X
    Ystep2 = Y

    return Xstep2, Ystep2

def step_3(X, Y):
    ''' Function that calculates the x and y values of the third step of the Hénon map.
        The x and y values on which this third step will act have to be given. These
        can be the generated x and y values of the second or first step or other x and
        y values.

        Input:

            X: x values on which the second step of the Hénon map will act (numpy array);
            Y: y values on which the second step of the Hénon map will act (numpy array);


        Returns:

            Xstep3: x values after the third step of the Hénon map has acted (numpy array);
            Ystep3: y values after the third step of the Hénon map has acted (numpy array);
    '''

    # Creating the x and y values for the third step of the transformation
    Xstep3 = Y
    Ystep3 = X

    return Xstep3, Ystep3
