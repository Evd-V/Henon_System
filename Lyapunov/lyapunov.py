import math
import numpy as np
from matplotlib.pyplot import figure, savefig, show

import full_henon as fh


def norm_vect(vector):
    """ Calculate the norm of a vector. """
    values = [i*i for i in vector]
    return math.sqrt(sum(values))

def inner_vect(vect1, vect2):
    """ Calculate the inner product of two vectors. """
    values = [vect1[i] * vect2[i] for i in range(len(vect1))]
    return sum(values)

def proj_vect(vect1, vect2):
    """ Calculate the projection of vector v onto vector u. """
    return (inner_vect(vect1, vect2) / inner_vect(vect1, vect1)) * vect1

def basis(dim):
    """ Creating the standard basis vectors for n dimensions. """
    
    basisVects = [np.zeros(dim) for i in range(dim)]
    for i in range(dim):
        basisVects[i][i] += 1
    
    return basisVects

def Gram_Schmidt(vectors):
    """ Function that uses the Gram-Schmidt process to orthogonalize a set of n-
        dimensional vectors. The normalization of the vectors is not included.
        
        Input: vectors = list containing the vectors; a valid input is for 
                         example:[v1, v2] where v1 = [[x1], [y1]] and v2 = 
                         [[x2], [y2]];
        
        Returns: basis = list containing the orthogonalised set of vectors in 
                         the same format as the input 'vectors'.
    """
    
    basis = [vectors[0]]
    for v in range(1, len(vectors)):
        for j in range(v):
            new_vect = vectors[v] - proj_vect(vectors[j], vectors[v])
        basis.append(new_vect)
    
    return basis


def Lyapunov(N, xvalues, A, B):
    """ Function that calculates the Lyapunov exponents for the Henon map.
    
        Input:  N       = number of loops that have to be computed (integer);
                basis   = the standard basis vectors in n dimensions. The 
                          syntax is for example: [e1, e2] where e1 = [[1], [0]] 
                          and e2 = [[0], [1]] (list);
                xvalues = list of x values of the Henon map;
                A       = value for parameter a for the Henon map;
                B       = value for parameter b for the Henon map;
        
        Returns:lya     = list containing the computed lyapunov exponents.
    """
    
    dim = 2                                 # Dimension of system
    exponents = [0 for i in range(2)]       # Array to put the results in
    u_nk = basis(dim)                       # Basis vectors
    
    for n in range(1, N):
        
        J = np.array([[-2*A*xvalues[n], 1], [B, 0]])     # Updating the Jacobian
        
        v_nk = [np.matmul(J, u) for u in u_nk]              # Calculating v_nk
        u_nk = Gram_Schmidt([v_nk[i] for i in range(dim)])  # Gram-Schmidt
        
        for i in range(dim):
            u_i = u_nk[i]
            norm_v = norm_vect(u_i)            # Norm of the vector
            exponents[i] += np.log(norm_v)     # Adding the newly obtained value
            u_nk[i] = u_i / norm_v             # Normalizing
    
    # Calculating the lyapunov exponents
    lya = [exponents[i] / N for i in range(dim)]
    
    return lya

def plot_1D(vals, const, nIts, nCut, a=True, plotMin=False, saveFig=None):
    """ Plotting the Lyapunov exponents for varying the parameter a or b """
    
    lyaMin, lyaMax = [], []
    xs, ys = 0, 0                               # Initial conditions
    
    # Initializing the plot
    fig = figure(figsize=(15,8))
    frame = fig.add_subplot(1,1,1)
    
    for ind, val in enumerate(vals):
        if a:                                           # If b is kept constant
            x, y = fh.Henon(xs, ys, nIts, val, const)
            Lexp = Lyapunov(nIts-nCut, x[nCut:], val, const)
            
            frame.set_xlabel("a", fontsize=20)
            
        else:                                           # If a is kept constant
            x, y = fh.Henon(xs, ys, nIts, const, val)
            Lexp = Lyapunov(nIts-nCut, x[nCut:], const, val)
            
            frame.set_xlabel("b", fontsize=20)
        
        # Adding the exponents to the lists
        lyaMax.append(Lexp[0])
        lyaMin.append(Lexp[1])
    
    frame.plot(vals, lyaMax, color="darkblue", lw=0.8)
    if plotMin: frame.plot(vals, lyaMin, color="crimson", lw=0.8)
    
    frame.set_ylabel("Lyapunov exponent", fontsize=20)
    frame.grid()
    
    if saveFig != None: fig.savefig(str(saveFig))
    else: show()


def plot_diff(maxIts, a=1.4, b=0.3, saveFig=None):
    """ Function to plot the values of the Lyapunov exponents for different 
        number of iterations.
    """
    
    x0 = y0 = 0                                           # Starting point
    cut = 100                                             # Removed points
    step = int(maxIts/10)                                 # Number of steps
    its = np.linspace(cut, maxIts, step)                  # Iteration steps
    
    x, y = fh.Henon(x0, y0, maxIts, a, b)                 # Henon map
    lExp = [Lyapunov(int(it), x, a, b) for it in its]     # Exponents
    
    
    # Plotting
    fig = figure(figsize=(16,8))
    ax1 = fig.add_subplot(1,1,1)
    ax2 = ax1.twinx()
    
    for ind, exp in enumerate(lExp):
        ax1.scatter(its[ind], exp[0], marker="x", s=10, color="navy")
        ax2.scatter(its[ind], exp[1], marker="o", s=10, color="maroon")
    
    ax1.grid()
    
    ax1.set_xlabel("Iterations", fontsize=20)
    ax1.set_ylabel("Max exponent", color="navy", fontsize=20)
    ax2.set_ylabel("Min exponent", color="maroon", fontsize=20)
    
    if saveFig != None: fig.savefig(str(saveFig))
    else: show()

