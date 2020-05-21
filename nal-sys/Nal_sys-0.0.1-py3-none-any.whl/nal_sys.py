def Peaks(Sample):
    """ This functions takes the y-value and returns all peaks for an oscilating measurment """
    if not isinstance(Sample, (list,tuple)):
        raise TypeError("The Input in maximums is of the wrong type, requires a list or tuple")

    peaks=[]
    index=[]
    for i in range(1,len(Sample)):
        if i == len(Sample):
            break
        else:
            if Sample[i]>Sample[i+1] and Sample[i]>Sample[i-1]:
                peaks.append(Sample[i])
                index.append(i)
    return peaks, index 