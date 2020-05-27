def list_as_tuple(list:dict(type=list,help="list data to be convert to tuple")):
    return tuple(list)

if __name__ == "__main__":
    mydata = ['a','b','c']
    mydata2 = list_as_tuple(mydata)
    for i in range(len(mydata)):
        print(mydata[i])