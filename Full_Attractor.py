import numpy as np
from matplotlib.pyplot import figure, show

def Henon(Xstart, Ystart, Iterations, a, b):
    '''
        Function that calculates the location of points according to the Hénon map.
        Input: Xstart = floating point number; Ystart = floating point number; Iterations = integer;
               a = floating point number; b = floating point number.
        Returns: Xvals = list, Yvals = list
    '''
    # The initial values
    Xvals = [Xstart]
    Yvals = [Ystart]
    
    # Finding all other values
    for i in range(Iterations):
        X_arr = Xvals[i]         # Slight improvement in computing speed
        Xvals.append(Yvals[i] + 1 - a * X_arr * X_arr)
        Yvals.append(b * X_arr)
            
    return Xvals, Yvals

# Creating the starting values
X0 = 0
Y0 = 0
It = int(1e5)
Av = 1.4
Bv = 0.3

# Calculating the points of the Hénon attractor
Xvalues, Yvalues = Henon(X0, Y0, It, Av, Bv)

# ------------------ #
Markersize = 0.0004

# Plotting
fig = figure(figsize=(10,8))
frame = fig.add_subplot(1,1,1)

frame.scatter(Xvalues, Yvalues, s=Markersize, label='points', color='darkblue', marker='.')

frame.set_title(f'Hénon attractor with {It} points')
frame.set_xlabel('x')
frame.set_ylabel('y')

frame.grid()

# Uncomment to save the figure
#fig.savefig('Hénon_map_1e6.pdf')

show()
