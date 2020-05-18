# PLS with NIPALS

import numpy as np

def PLS(X, Y, nbPC):
    s0, s1 = X.shape
    s0, s2 = Y.shape
    T = np.zeros(shape=(s0, nbPC))
    U = np.zeros(shape=(s0, nbPC))
    P = np.zeros(shape=(s1, nbPC))
    W = np.zeros(shape=(s1, nbPC))
    Q = np.zeros(shape=(s2, nbPC))
    B = np.zeros(shape=(nbPC, nbPC))
    SSX = np.zeros(shape=(nbPC, 1))
    SSY = np.zeros(shape=(nbPC, 1))
    X0 = X # Save a copy
    Y0 = Y # Save a copy
    
    for i in range(0,nbPC):
        error = 1
        u_temp = np.random.randn(s0, 1)
        u = np.random.randn(s0, 1)
        
        while error > 1E-10:
            w = (X.T @ u) / np.linalg.norm(X.T @ u)
            t = X @ w    
            q = (Y.T @ t) / np.linalg.norm(Y.T @ t)
            u = Y @ q
            # Check t convergence 
            error = sum(np.power((u-u_temp),2),0) # Squared error
            u_temp = u
        
        # Deflation
        p = (X.T@t)/(t.T@t)
        b = (u.T@t)/(t.T@t) # U = fct(T)
        X = X - t@p.T
        Y = Y - b*t@q.T
               
        # Save        
        W[:,i] = np.squeeze(w)
        P[:,i] = np.squeeze(p)
        T[:,i] = np.squeeze(t)
        U[:,i] = np.squeeze(u)
        Q[:,i] = np.squeeze(q)
        B[i,i] = b

        # Sum of squares X
        Xhat = t@p.T
        ssX0 = np.sum(np.sum(X0 * X0)) # Each element squared
        ssX = np.sum(np.sum(Xhat * Xhat))
        ssX = ssX / ssX0
        SSX[i] = ssX
 
        # Sum of squares Y 
        Yhat = b*t@q.T
        ssY0 = np.sum(np.sum(Y0 * Y0)) # Each element squared
        ssY = np.sum(np.sum(Yhat * Yhat))
        ssY = ssY / ssY0
        SSY[i] = ssY
        
    Yhat = T@B@Q.T # NIPALS
        
    return T, U, P, W, Q, B, Yhat, SSX, SSY
