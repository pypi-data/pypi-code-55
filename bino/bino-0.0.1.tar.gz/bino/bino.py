def bino(y):
    y=int(y)
    l=[]
    while y>=1:
        n=y%2
        l.append(int(n))
        y=y/2
    l.reverse()
    return l



