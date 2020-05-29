import numpy as np
import matplotlib.pylab  as plt
def Kendall_change_point_detection(inputdata):
    inputdata1 = np.array(inputdata)
    n=inputdata1.shape[0]
    Sk             = [0]
    UFk            = [0]
    s              =  0
    Exp_value      = [0]
    Var_value      = [0]
    for i in range(1,n):
        for j in range(i):
            if inputdata1[i] > inputdata1[j]:
                s = s+1
            else:
                s = s+0
        Sk.append(s)
        Exp_value.append((i+1)*(i+2)/4 )                     # Sk[i] mean
        Var_value.append((i+1)*i*(2*(i+1)+5)/72 )            # Sk[i] std
        UFk.append((Sk[i]-Exp_value[i])/np.sqrt(Var_value[i]))
    #Inverse sequence computing generation
    Sk2             = [0]
    # Define the reverse order statistics UBk, the length is consistent with inputdata, initial value = 0
    UBk             = [0]
    UBk2            = [0]
    # s=0
    s2              =  0
    Exp_value2      = [0]
    Var_value2      = [0]
    # 
    inputdataT = list(reversed(inputdata1))
    for i in range(1,n):
        for j in range(i):
            if inputdataT[i] > inputdataT[j]:
                s2 = s2+1
            else:
                s2 = s2+0
        Sk2.append(s2)
        Exp_value2.append((i+1)*(i+2)/4 )                     # Sk[i] mean
        Var_value2.append((i+1)*i*(2*(i+1)+5)/72 )            # Sk[i] std
        UBk.append((Sk2[i]-Exp_value2[i])/np.sqrt(Var_value2[i]))
        UBk2.append(-UBk[i])
    UBkT = list(reversed(UBk2))
    diff = np.array(UFk) - np.array(UBkT)
    K    = list()
    # Find the intersection
    for k in range(1,n):
        if diff[k-1]*diff[k]<0:
            K.append(k)
   
 #   plt.figure(figsize=(10,5))
 #   plt.plot(range(1,n+1) ,UFk  ,label='UFk') # UFk
 #   plt.plot(range(1,n+1) ,UBkT ,label='UBk') # UBk
#    plt.ylabel('UFk-UBk')
 #   x_lim = plt.xlim()
#    plt.plot(x_lim,[-1.96,-1.96],'m--',color='r')
#    plt.plot(x_lim,[  0  ,  0  ],'m--')
#    plt.plot(x_lim,[+1.96,+1.96],'m--',color='r')
#    plt.legend(loc=2) # 图例
#     plt.savefig("./Dectection/{}_Mann-Kendall.png".format(name))
#    plt.show()
#   b=[]
#    for i in K:
#        tmp=inputdata.index[i]
#        b.append(tmp.strftime("%Y-%m-%d"))
    return K
