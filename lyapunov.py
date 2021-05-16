import numpy as np
from Full_Attractor import Henon

def norm_vect(vector):
    """ Calculate the norm of a vector. """
    values = [i*i for i in vector]
    return sum(values)

def inner_vect(vect1, vect2):
    """ Calculate the inner product of two vectors. """
    values = [vect1[i] * vect2[i] for i in range(len(vect1))]
    return sum(values)

def proj_vect(vect1, vect2):
    """ Calculate the projection of vector v onto vector u. """
    return (inner_vect(vect1, vect2) / norm_vect(vect1)) * vect1

def basis(dim):
    """ Creating the standard basis vectors for n dimensions. """
    
    basisVects = [np.zeros(dim) for i in range(dim)]    
    for i in range(dim):
        basisVects[i][i] += 1
    
    return basisVects
    
def Gram_Schmidt_rev(vectors):
    """ Function that uses the Gram-Schmidt process to orthogonalize a set of n-dimensional 
        vectors. The normalization of the vectors is not included.
        
        Input: vectors = list containing the vectors; a valid input is for example:
                         [v1, v2] where v1 = [[x1], [y1]] and v2 = [[x2], [y2]];
                         
        Returns: basis = list containing the orthogonalised set of vectors in the same format 
                         as the input 'vectors'.
    """
    basis = [vectors[0]]
    for v in range(1, len(vectors)):
        for j in range(v):
            new_vect = vectors[v] - proj_vect(vectors[j], vectors[v])
        basis.append(new_vect)
            
    return basis

def Lyapunov(N, basis, xvalues):
    """ Function that calculates the Lyapunov exponents for the Henon map.
        For now this function only works for the Hénon map, still working on making it more general.
    
    
        Input:      N       = number of loops that have to be computed (integer);
                    basis   = the standard basis vectors in n dimensions. The syntax is for example: 
                              [e1, e2] where e1 = [[1], [0]] and e2 = [[0], [1]] (list);
                    xvalues = list of x values of the Hénon map;
                    
        Returns:    lya     = list containing the computed lyapunov exponents.
    """
    
    dim = len(basis)                # Dimension
    exponents = np.zeros(dim)       # Array to put the intermediate results in
    
    # First step
    J = np.array([[-2.8*xvalues[0], 1], [0.3, 0]])          # The 'first' Jacobian
    v_1k = [np.matmul(J, b) for b in basis]                 # Calculating the 'first' v_nk
    u_nk = Gram_Schmidt([v_1k[i] for i in range(dim)])      # Calculating the 'first' u_nk
    
    # Adding to 'exponents', used for the calculating of the Lyapunov exponents
    for i in range(dim): exponents[i] += np.log(norm_vect(u_nk[i]))
    
    u_nk = [u / norm_vect(u) for u in u_nk]                 # Normalizing
    
    for n in range(1, N):
        
        v_nk = [np.matmul(J, u) for u in u_nk]              # Calculating v_nk
        u_nk = Gram_Schmidt([v_nk[i] for i in range(dim)])  # Gram-Schmidt
        
        # Adding the newly obtained value to the array 'exponents'
        for i in range(dim): exponents[i] += np.log(norm_vect(u_nk[i]))
        
        J = np.array([[-2.8*xvalues[n], 1], [0.3, 0]])      # Updating the Jacobian matrix
        u_nk = [u / norm_vect(u) for u in u_nk]             # Normalizing
        
    # Calculating the lyapunov exponents
    lya = [exponents[i] / N for i in range(dim)]
    
    return lya

def calc_lya_henon(Ninit, cutoff, start, A, B, div=True, thres=1e5):
    """ Calculation of the Lyapunov exponents specifically for the Hénon map.
    
        Input:      Ninit   = number of iterations for the Hénon map (integer);
                    Cutoff  = number of points that get thrown away (integer);
                    start   = intial starting point for the Hénon map (tuple);
                    A       = value of the 'a' parameter in the iterative equations (float);
                    B       = value of the 'b' parameter in the iterative equations (float);
                
        Returns:    lya     = the Lyapunov exponents for the Hénon map (list).
    """
    
    if type(A) == float and type(B) == float:
        Xvalues, Yvalues = Henon(start[0], start[1], Ninit, A, B)       # Generating the points of the Hénon map    
        basisVects = basis(len(start))                                  # Basis vectors

        if abs(Xvalues[cutoff]) == np.inf or abs(Xvalues[cutoff]) > thres: return None

        # Calculating the Lyapunov exponents
        lya = Lyapunov(Ninit-cutoff, np.array(basisVects), Xvalues[cutoff:])
        
        return lya
        
    else:
        all_exp1, all_exp2 = [], []
        for a in A:
            a_exp1 = []
            a_exp2 = []
            for b in B:
                Xvalues, Yvalues = Henon(start[0], start[1], Ninit, a, b, div=div)       # Generating the points of the Hénon map    
                basisVects = basis(len(start))                                  # Basis vectors
                
                try:
                    if abs(Xvalues[cutoff]) == np.inf or abs(Xvalues[cutoff]) > thres:
                        a_exp1.append(0)
                        a_exp2.append(0)
                        continue
                        
                except:
                    a_exp1.append(0)
                    a_exp2.append(0)
                    continue
                        
                # Calculating the Lyapunov exponents
                lya = Lyapunov(Ninit-cutoff, np.array(basisVects), Xvalues[cutoff:])
                
                sort = np.sort(lya)
                a_exp1.append(sort[0])
                a_exp2.append(sort[1])
                
            all_exp1.append(a_exp1)
            all_exp2.append(a_exp2)
    
        return all_exp1, all_exp2
    
def create_lya_grid(a_vals, b_vals, start=(0,0), N=int(1e4), cutoff=int(1e3), div=True):
    """ Function that calculates the grid for a given arrays of a and b values. """
    vals = np.array(calc_lya_henon(N, cutoff, start, a_vals, b_vals, div=div))
    return vals[0], vals[1]
