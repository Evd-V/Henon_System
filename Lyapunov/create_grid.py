from matplotlib.pyplot import figure, cm, savefig, show
import numpy as np

import full_henon as fh
import lyapunov as ly
import helper as he


def save_grid(size, amin, amax, bmin, bmax, fmax, fmin):
    """ Saving Lyapunov exponents of the Hénon map for a range of values for the 
        parameters a and b to a text file.
    """
    
    grid_size = (size, size)                # Grid is square
    lya_grid_max = np.zeros(grid_size)      # Maximum L.E.
    lya_grid_min = np.zeros(grid_size)      # Minimum L.E.
    
    a_vals = np.linspace(amin, amax, size)  # a values over which will be looped
    b_vals = np.linspace(bmin, bmax, size)  # b values over which will be looped
    
    Ntot = 1000                             # Times Hénon map will be iterated
    Ncut = 100                              # Points that will be thrown away
    xStart = yStart = 0                     # Initial conditions
    
    for aind, a in enumerate(a_vals):       # The a values and index
        for bind, b in enumerate(b_vals):   # The b values and index
            x,y = fh.Henon(xStart, yStart, Ntot, a, b)      # Iterating the map
            Lexp = ly.Lyapunov(Ntot-Ncut, x[Ncut:], a, b)   # L.E.
            lya_grid_max[aind][bind] = Lexp[0]              # Max L.E.
            lya_grid_min[aind][bind] = Lexp[1]              # Min L.E.
    
    label = f"{amin} < a < {amax}, {bmin} < b < {bmax}"     # Header for table
    
    # Saving the data
    with open(fmax, "ab") as f:
        np.savetxt(f, lya_grid_max, fmt="%.3e", delimiter="|", header=label)
    with open(fmin, "ab") as f:
        np.savetxt(f, lya_grid_min, fmt="%.3e", delimiter="|", header=label)


def read_data(fname, size, comment="#", delimiter="|"):
    """ Function that reads data from a given file. This function works best 
        combined with the files that are written using the 'save_grid' function 
        defined above. The input parameter 'comment' gives the character which 
        determines the commented lines that can be ignored. The 'delimiter' 
        paramter gives the character which separates two different values in a 
        table.
        
        Input:      fname     = name of the file that will be read (string);
                    comment   = character that comments lines (string);
                    delimiter = character that separate values (string);
                    
        Returns:    all_data  = the obtained data (list);       
    """
    
    with open(fname, "r") as f:                 # Reading the file
        
        lines = f.readlines()                   # Reading the lines
        all_data = []                           # List for all data
                
        grid_values = np.zeros((size, size))    # Grid where values will be stored
        table_number = 0                        # Number of tables
        
        for row_ind, line in enumerate(lines):  # Looping over all lines
            
            if row_ind == 0: continue           # First Table
            
            elif comment in line:               # New table
                table_number += 1
                
                all_data.append(grid_values)    # Add current grid to all data
                grid_values = np.zeros((size, size))    # Reset grid
                continue
                
            else:
                data = line.split(delimiter)             # Splitting the entries
                
                for column_ind, val in enumerate(data):  # Looping over entries
                    #  Setting value of entry to grid
                    grid_values[row_ind-1-table_number*(size+1)][column_ind] = val
                    
                if row_ind == len(lines)-1:        # EOF
                    all_data.append(grid_values)   # Add grid values to all data
                    break
                
        return all_data

def create_grid(fmax, fmin, frame_size, ystack):
    """ Assumes frame is square. """
    
    max_generated = read_data(fmax, frame_size)     # Max L.E.
    min_generated = read_data(fmin, frame_size)     # Min L.E.
    type_gen = he.array_att(max_generated, min_generated, frame_size)   # Types
    
        # Concatenate separate frames in right order and shape
    all_colls = [np.concatenate
                (type_gen[row*ystack:(row+1)*ystack], axis = 0) 
                for row in range(ystack)]
    
    max_gen = [np.concatenate
              (max_generated[row*ystack:(row+1)*ystack], axis = 0)
              for row in range(ystack)]
    
    min_gen = [np.concatenate
              (min_generated[row*ystack:(row+1)*ystack], axis = 0)
              for row in range(ystack)]
    
    tot_generated = np.hstack(tuple(all_colls))
    tot_max = np.hstack(tuple(max_gen))
    tot_min = np.hstack(tuple(min_gen))
    
    return tot_max, tot_min, tot_generated


def comb_multiple(max_fnames, min_fnames, xsize, frame_size, av, bv, numb):
    """ Combining multiple different grids of Lyapunov exponents into one big 
        grid 
    """
    
    cR = [[create_grid(max_fnames[ind], min_fnames[ind], frame_size, numb)[-1]] 
           for ind in range(len(max_fnames))]
    
    # Creating the three different "y grids", so yColumn consists of 3 arrays,
    # each containing a third of the grid. The first array the left most side, 
    # the second array the middle part, and the last array the right side
    yColumn = [np.concatenate(
              (np.vstack((cR[:xsize]))[x], np.vstack((cR[xsize:]))[x]), axis=0) 
              for x in range(xsize)]
    
    # Combining the three different parts
    fullConc = np.concatenate(([col for col in yColumn]), axis=1)
    
    # Ticks, a on y-axis, b on x-axis
    xLen, xNum = len(fullConc[0]), 11
    yLen, yNum = len(fullConc), 5
    
    # Labels of the ticks
    xL = np.round(np.linspace(bv[0], bv[1], xNum), 2)
    yL = np.round(np.linspace(av[0], av[1], yNum), 2)
    
    # Locations of the ticks
    xTL = np.linspace(0, xLen, xNum)
    yTL = np.linspace(0, yLen, yNum)
    
    # Name of the figure that will be saved
    full_name = "full_lyapunov2_grid_540.png"
    
    plot_grid(fullConc, xL, yL, xTL, yTL, full_name)


def save_vals(fmax, fmin):
    """ Saving the Lyapunov exponents of the Hénon map """
    
    # Input values from user
    totSize = eval(input("size: "))
    minA = eval(input("minA: "))
    maxA = eval(input("maxA: "))
    minB = eval(input("minB: "))
    maxB = eval(input("maxB: "))
    number = eval(input("Number: "))
    
    aVals = np.linspace(minA, maxA, number+1)
    bVals = np.linspace(minB, maxB, number+1)
    
    leng = number               # Number of values for a and b
    L = range(leng)             # Range used in loops
    
    for bInd in L:              # Looping over all b values
        print(f"Currently processing: {bVals[bInd]} <= b <= {bVals[bInd+1]}")
        for aInd in L:          # Looping over all a values
            print(f"Currently processing: {aVals[aInd]} <= a <= {aVals[aInd+1]}")
            save_grid(totSize, aVals[aInd], aVals[aInd+1], bVals[bInd], 
                      bVals[bInd+1], fmax, fmin)
    
    tic_locs = [round(ind*totSize, 2) for ind in L]  # Firs leng-1 tic locations
        # Last tic location not at end due to layout issues
    tic_locs.append(round(leng * totSize - .5, 2))
    
    redaVals = [round(val, 2) for val in aVals]
    redbVals = [round(val, 2) for val in bVals]
    
    return redaVals, redbVals, tic_locs


def plot_grid(data, xlabels=None, ylabels=None, xticks=None, yticks=None, 
              fname=None):
    """ Plotting 2D data and the corresponding labels """
    
    # Plotting
    fig = figure()
    frame = fig.add_subplot(1,1,1)
    
    frame.imshow(data, cmap=cm.inferno)
    
    if xticks: frame.set_xticks(xticks)
    if yticks: frame.set_yticks(yticks)
    
    if xlabels: frame.set_xticklabels(xlabels, fontsize=15)
    if ylabels: frame.set_yticklabels(ylabels, fontsize=15)
    
    frame.set_xlabel("b", fontsize=20)
    frame.set_ylabel("a", fontsize=20)
    
    if fname != None: fig.savefig(fname)
    else: show

