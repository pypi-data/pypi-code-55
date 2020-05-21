import xlrd
import xlwt
import datetime
from xlutils.copy import copy

borders = xlwt.Borders()
borders.top = xlwt.Borders.THIN
borders.bottom = xlwt.Borders.THIN
borders.left = xlwt.Borders.THIN
borders.right = xlwt.Borders.THIN

alignment_center = xlwt.Alignment()
alignment_center.horz = xlwt.Alignment.HORZ_CENTER
alignment_center.vert = xlwt.Alignment.VERT_CENTER

alignment_left = xlwt.Alignment()
alignment_left.horz = xlwt.Alignment.HORZ_LEFT
alignment_left.vert = xlwt.Alignment.VERT_CENTER

alignment_right = xlwt.Alignment()
alignment_right.horz = xlwt.Alignment.HORZ_RIGHT
alignment_right.vert = xlwt.Alignment.VERT_CENTER

def font(name,height,isBold=False):
	font = xlwt.Font()
	font.name = name
	font.height = 20*height
	font.bold = isBold
	return font

def style(font("Arial",10),borders,alignment):
	style = xlwt.XFStyle()
	
	style.font = font
	style.borders = borders
	style.alignment = alignment

	return style

style1 = style(font1,borders,alignment_center)	

# parse the cell data, such as 1/1/2020 to 01/01/2020, if it's str, do nothing, just return str
def parseFloatTimeToString(row,col,sheet):
	res = ''
	if type(sheet.cell_value(row,col))==float:	
		res = xlrd.xldate.xldate_as_datetime(sheet.cell(row,col).value, 0).strftime( '%m/%d/%Y' )
	else:
		res = sheet.cell_value(row,col)	
	return res

# Book1 just for reading
class Book1(object):
	def __init__(self, filename):
		self.book = xlrd.open_workbook(filename)

	def sheet(self,index):	
		self.sheet = self.book.sheet_by_index(index)
		return self.sheet
	def cell_value(self,row,col):
		return self.sheet.cell_value(row,col)

# Book2 used for writing data with existing sheet template
class Book2(object):
	"""docstring for Book2"""
	def __init__(self, old_excle, new_excel):
		self.old_excle = old_excle
		self.new_excel = new_excel
		self.formatting_info = True

	def copy(self,old_sheet_index,new_sheet_index):
		old_workbook = xlrd.open_workbook(self.old_excle,self.formatting_info)
		# sheet
		target_sheet = old_workbook.sheet_by_index(old_sheet_index)

		new_excel = copy(old_workbook)
		new_sheet = new_excel.get_sheet(new_sheet_index)

		# 去掉页眉和页脚
		new_sheet.show_headers = False
		new_sheet.header_str = b''
		new_sheet.footer_str = b''
		self.book = new_excel
		self.sheet = new_sheet
		return self.sheet
		
	def write(self,row,col,value,style=style1):
		self.sheet.write(row, col, value,style)

	def save(self):
		self.book.save(self.new_excel)					

