#向量处理
def vectRange(vect, selector=[1, 3]):
	res = []
	for i in range(len(selector)):
		res.append(vect[selector[i]])
	return(res)