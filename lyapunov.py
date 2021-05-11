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

def Lyapunov(N, basis, xvalues, k):
    """ Function that calculates the Lyapunov exponents. Still work in progress.
    """
    
    dim = len(basis)
    exponents = np.zeros(dim)
    
    # List to put the rescaled factors in
    resc = []
    
    J = np.array([[-2.8*xvalues[0], 1], [0.3, 0]])
    u_1k = [b for b in basis]
    v_1k = [np.matmul(J, u) for u in u_1k]
    
    u_nk = Gram_Schmidt_rev([v_1k[0], v_1k[1]])
    resc.append(u_nk[k])
    u_nk = [u / np.linalg.norm(u) for u in u_nk]
    
    for n in range(1, N):
        
        # Calculating v_nk
        v_nk = [np.matmul(J, u) for u in u_nk]
        
        # Gram-Schmidt
        u_nk = Gram_Schmidt_rev([v_nk[0], v_nk[1]])
        
        # Adding the newly obtained vector to the list
        #for i in range(dim):
        #    exponents[i] += u_nk[i]
        
        resc.append(u_nk[k])
        
        # Updating the Jacobian matrix
        J = np.array([[-2.8*xvalues[n], 1], [0.3, 0]])
        
        # Normalizing
        u_nk = [u / norm_vect(u) for u in u_nk]
        
    #lyas = []
    #for i in range(dim):
    #    lyas.append([sum(np.log(norm_vect(u))) for u in exponents[i]])
    
    log_ = [np.log(norm_vect(u)) for u in resc]
    
    lya_k = sum(log_) / N
    
    return lya_k#, lyas
