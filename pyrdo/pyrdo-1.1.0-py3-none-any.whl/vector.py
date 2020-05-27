#向量处理
def vectRange(vect, selector=[1, 3]):
	res = []
	for i in range(len(selector)):
		res.append(vect[selector[i]])
	return(res)
def testPrint():
	print('hello world')


if __name__ == "__main__":
	mydata = [1,2,3,4,5]
	print(vectRange(mydata,[1,2]))
	myarr = [['A1'],['B1']]
	text = "|".join(['a',"b","c"])
	print(text)
	a = ["我是胡立磊"]
	b = "我是e"
	mydata2 =[['1','tom'],['2','jack']]