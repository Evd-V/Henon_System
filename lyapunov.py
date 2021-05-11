import numpy as np

def norm_vect(vector):
    """ Calculate the norm of a vector. """
    values = [i*i for i in vector]
    return sum(values)[0]

def inner_vect(vect1, vect2):
    """ Calculate the inner product of two vectors. """
    values = [vect1[i] * vect2[i] for i in range(len(vect1))]
    return sum(values)[0]

def proj_vect(vect1, vect2):
    """ Calculate the projection of vector v onto vector u. """
    return (inner_vect(vect1, vect2) / norm_vect(vect1)) * vect1
    
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
    u_nk = Gram_Schmidt([v_1k[0], v_1k[1]])                 # Calculating the 'first' u_nk
    
    # Adding to 'exponents', used for the calculating of the Lyapunov exponents
    for i in range(dim): exponents[i] += np.log(norm_vect(u_nk[i]))
    
    u_nk = [u / norm_vect(u) for u in u_nk]                 # Normalizing
    
    for n in range(1, N):
        
        v_nk = [np.matmul(J, u) for u in u_nk]              # Calculating v_nk
        u_nk = Gram_Schmidt([v_nk[i] for i in range(dim)])  # Gram-Schmidt
        
        # Adding the newly obtained value to the list
        for i in range(dim): exponents[i] += np.log(norm_vect(u_nk[i]))
        
        J = np.array([[-2.8*xvalues[n], 1], [0.3, 0]])      # Updating the Jacobian matrix
        u_nk = [u / norm_vect(u) for u in u_nk]             # Normalizing
        
    # Calculating the lyapunov exponents
    lya = [exponents[i] / N for i in range(dim)]
    
    return lya
