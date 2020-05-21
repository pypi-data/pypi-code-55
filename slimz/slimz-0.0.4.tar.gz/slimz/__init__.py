import datetime

today_str = datetime.datetime.now().strftime('%m/%d/%Y')

# check file or folder if exists 
# pth: the path of the file/folder
def isExist(pth):
	return Path(pth).exists()

# uppercase the first letter of the str
# eg: "I lOve yoU & and the family" =>"I Love You & And The Family"
def firstLetterToUpper(str):
	str = str.lower().strip()
	
	if " " in str:
		str = str.split(' ')
		new_str = ""
		
		for x in str:
			item =""
			n = 0
			for y in x:
				n += 1
				if n==1:
	 				if ord(x[0]) >=97 and ord(x[0]) <= 122:
	 					y = chr(ord(x[0])-32)
				item += y
		return new_str	
	else:
		return str.capitalize()
