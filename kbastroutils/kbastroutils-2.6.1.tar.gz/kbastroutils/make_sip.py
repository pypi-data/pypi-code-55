def make_SIP(coef,x,y,startx=True):
    import numpy as np
    if startx:
        xref,yref = x,y
    else:
        xref,yref = y,x
    n = len(coef)
    d = []
    px,py = 0,0
    a = [(px,py)]
    b = [(xref,yref)]
    p = 0
    q = True
    while(q):
        if px==0:
            p+=1
            px=p
            py=0
        else:
            px-=1
            py+=1
        a.append((px,py))
        b.append((xref,yref))
        if len(a)>=len(coef):
            q = False
    a,b = np.array(a),np.array(b)
    c = b**a
    c = np.sum(c[:,0]*c[:,1]*coef)
    d.append(c)
    d = np.array(d)
    return d  