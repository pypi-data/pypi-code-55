import pickle

def get_centuryfromyear(year:str):
    """# 1 because 2017 is 21st century, and 1989 = 20th century"""
    return (year) // 100 + 1

def get_datetimestr_fromCCYYMMDD(ccyymmdd:str):
    day = ccyymmdd[-2:]
    month = ccyymmdd[4:-2]
    year = ccyymmdd[2:4]
    
    return '%s-%s-%s' % (day, month, year)

def save_object(obj, filepath):
    with open(filepath, 'wb') as handle:
        pickle.dump(obj, handle, protocol=pickle.HIGHEST_PROTOCOL)