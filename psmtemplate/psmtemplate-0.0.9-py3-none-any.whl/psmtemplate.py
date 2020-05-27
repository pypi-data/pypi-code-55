try:
    import importlib.resources as pkg_resources
except ImportError:
    # Try backported to PY<37 `importlib_resources`.
    import importlib_resources as pkg_resources

from io import BytesIO, open
import os
from shutil import move
import warnings
import uuid

import PIL

# PDF Setup
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4, A3, portrait, landscape
from reportlab.lib.units import cm
from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_RIGHT
from reportlab.platypus import SimpleDocTemplate,Frame, Flowable, Paragraph, Spacer, Image
from reportlab.pdfbase.pdfmetrics import registerFont
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase.pdfmetrics import stringWidth

from pdfrw import PdfReader, PdfWriter, IndirectPdfDict
from pdfrw.buildxobj import pagexobj
from pdfrw.toreportlab import makerl


# Matplotlib Setup
import matplotlib
import matplotlib.pyplot as plt

class Padding():
    left = 0
    right = 0
    top = 0
    bottom = 0


class PDFImage(Flowable):
    """
    PDFImage wraps the first page from a PDF file as a Flowable
    which can be included into a ReportLab Platypus document.
    Based on the vectorpdf extension in rst2pdf (http://code.google.com/p/rst2pdf/)

    """
    def __init__(self,filename_or_object,width=None,height=None,kind='direct'):
        if hasattr(filename_or_object,'read'):
            filename_or_object.seek(0)
        page = PdfReader(filename_or_object,decompress=False).pages[0]
        self.xobj = pagexobj(page)
        x1,y1,x2,y2 = self.xobj.BBox

        self._w, self._h = x2-x1,y2-y1

        self.imageWidth = self._w
        self.imageHeight = self._h
        
        self.__ratio = float(self.imageWidth)/self.imageHeight
        if kind in ['direct','absolute']:
            self.drawWidth = width or self.imageWidth
            self.drawHeight = height or self.imageHeight
        elif kind in ['bound','proportional']:
            if width == None or height == None:
                factor = float(width)/self._w or factor(height)/self._h
            else:
                factor = min(float(width)/self._w,float(height)/self._h)
            self.drawWidth = self._w*factor
            self.drawHeight = self._h*factor

    def wrap(self,aW,aH):
        return self.drawWidth, self.drawHeight

    def drawOn(self,canv,x,y,_sW=0):
        if _sW > 0 and hasattr(self, 'hAlign'):
            a = self.hAlign
            if a in ('CENTER', 'CENTRE', TA_CENTER):
                x += 0.5*_sW
            elif a in ('RIGHT', TA_RIGHT):
                x += _sW
            elif a not in ('LEFT', TA_LEFT):
                raise ValueError("Bad hAlign value " + str(a))

        xobj = self.xobj
        xobj_name = makerl(canv._doc, xobj)

        xscale = self.drawWidth/self._w
        yscale = self.drawHeight/self._h

        x -= xobj.BBox[0] * xscale
        y -= xobj.BBox[1] * yscale

        canv.saveState()
        canv.translate(x, y)
        canv.scale(xscale, yscale)
        canv.doForm(xobj_name)
        canv.restoreState()

class PSMTemplateBuildError(Exception):
    """Raised when psm template cannot be built
    """
    def __init__(self,message):
        self.message = message

class PSMTemplate():
    
    # All units are in cm
    page_width = None
    page_height = None
    canvas = None

    figures = []
    Story = []
    notes = []

    padding = Padding()

    title_block_font_size = 10
    note_font_size = 10
    footnote_font_size = 8


    def __init__(self,file_name:str,page_size,padding_left=0.0,padding_right=0.0,padding_top=0.0,padding_bottom=0.0):
        """Initialise PSMTemplate
        
        :param file_name: file name of the page
        :type file_name: str
        :param page_size: size of the page
        :type page_size: (width,height)
        :param padding_left: left padding, defaults to 0.0
        :type padding_left: float, optional
        :param padding_right: right padding, defaults to 0.0
        :type padding_right: float, optional
        :param padding_top: top padding, defaults to 0.0
        :type padding_top: float, optional
        :param padding_bottom: bottom padding, defaults to 0.0
        :type padding_bottom: float, optional
        """
        self.ARIAL_FONT_PATH = os.path.join(os.path.dirname(__file__), 'static', 'ARIAL.ttf')
        self.PSM_Logo_Path = os.path.join(os.path.dirname(__file__), 'static', 'PSM Logo.jpg')
        os.environ["MATPLOTLIBRC"] = os.path.join(os.path.dirname(__file__), 'static', 'matplotlibrc')

        registerFont(TTFont('Arial',self.ARIAL_FONT_PATH))

        self.doc = SimpleDocTemplate(file_name,pagesize=page_size)
        self.canvas = canvas.Canvas(file_name,page_size)
        self.page_width,self.page_height = [size/cm for size in page_size]
        self.padding.left = padding_left
        self.padding.right = padding_right
        self.padding.top = padding_top
        self.padding.bottom = padding_bottom
        self.file_name = file_name
        self.footnote = os.path.abspath(os.path.join(self.file_name))
        self.notes = []
        self.Story = []
        self.figures = []
        self.built = False

        self.title_block_width = 9
        self.title_block_height = 2.54
        self.divider_height = 0.45
        self.title_block_font_size = 10

        self.note_title = "Notes:" # First line of notes

        return


    def _draw_frame(self,canvas,doc)->bool:
        """PRIVATE Draw the outter frame of the page
        
        :param canvas: Canvas of the page
        :type canvas: Canvas
        :param doc: Document of the page
        :type doc: Document
        :return: success
        :rtype: bool
        """
        canvas.saveState()
        canvas.translate(self.padding.left*cm,self.padding.bottom*cm)
        canvas.setStrokeColorRGB(0,0,0)

        # Outer Frame
        canvas.line(0,0,(self.page_width-self.padding.right-self.padding.left)*cm,0)
        canvas.line((self.page_width-self.padding.right-self.padding.left)*cm,0,(self.page_width-self.padding.right-self.padding.left)*cm,(self.page_height-self.padding.top-self.padding.bottom)*cm)
        canvas.line((self.page_width-self.padding.right-self.padding.left)*cm,(self.page_height-self.padding.top-self.padding.left)*cm,0,(self.page_height-self.padding.top-self.padding.bottom)*cm)
        canvas.line(0,(self.page_height-self.padding.top-self.padding.bottom)*cm,0,0)

        canvas.restoreState()

    def add_titleblock(self,client:str,project:str,location:str,description_line_1:str,description_line_2:str,doc_no:str,page_no:str,title_block_width=9.0,title_block_height=2.54,divider_height=0.45,title_block_font_size=10)->bool:
        """Add titleblock to the page
        
        :param client: client string in the titleblock
        :type client: str
        :param project: project string in the titleblock
        :type project: str
        :param location: location string in the titleblock
        :type location: str
        :param description_line_1: description_line_1 in the titleblock
        :type description_line_1: str
        :param description_line_2: description_line_2 in the titleblock
        :type description_line_2: str
        :param doc_no: Document Number in the titleblock
        :type doc_no: str
        :param page_no: Page Number in the titleblock
        :type page_no: str
        :param title_block_width: Width of the titleblock in cm, defaults to 9.0
        :type title_block_width: float, optional
        :param title_block_height: Height of the titleblock in cm, defaults to 2.54
        :type title_block_height: float, optional
        :param divider_height: height of the divider, defaults to 0.45
        :type divider_height: float, optional
        :param title_block_font_size: title block font size, defaults to 10
        :type title_block_font_size: int, optional
        :return: Success
        :rtype: bool
        """
        self.client = client
        self.project = project
        self.location = location
        self.description_line_1 = description_line_1
        self.description_line_2 = description_line_2
        self.doc_no = doc_no
        self.page_no = page_no
        self.title_block_width = title_block_width
        self.title_block_height = title_block_height
        self.divider_height = divider_height
        self.title_block_font_size = title_block_font_size

        return True


        

    def _draw_title_block(self,canvas,doc)->bool:
        """PRIVATE Draw the titleblock of the page
        
        :param canvas: Canvas of the page
        :type canvas: Canvas
        :param doc: Document of the page
        :type doc: Document
        :return: success
        :rtype: bool
        """
        # Titleblock Frame
        canvas.saveState()
        canvas.translate(self.padding.left*cm,self.padding.bottom*cm)
        canvas.setStrokeColorRGB(0,0,0)

        canvas.line((self.page_width-self.padding.right-self.padding.left-self.title_block_width)*cm,0,(self.page_width-self.padding.right-self.padding.left-self.title_block_width)*cm,self.title_block_height*cm)
        canvas.line((self.page_width-self.padding.right-self.padding.left-self.title_block_width)*cm,self.title_block_height*cm,(self.page_width-self.padding.right-self.padding.left)*cm,self.title_block_height*cm)
        canvas.line((self.page_width-self.padding.right-self.padding.left-self.title_block_width)*cm,self.divider_height*cm,(self.page_width-self.padding.right-self.padding.left)*cm,self.divider_height*cm)
        canvas.line((self.page_width-self.padding.right-self.padding.left-0.5*self.title_block_width)*cm,self.divider_height*cm,(self.page_width-self.padding.right-self.padding.left-0.5*self.title_block_width)*cm,0)
        
        # Add Texts

        # Capitalise all texts
        client = self.client.upper()
        project = self.project.upper()
        location = self.location.upper()
        description_line_1 = self.description_line_1.upper()
        description_line_2 = self.description_line_2.upper()
        doc_no = self.doc_no.upper()
        page_no = self.page_no.upper()

        # Adjust font size such that minimum padding is 0.1 cm
        title_block_font_size = self.get_font_size_from_max_width([client,project,location,description_line_1,description_line_2],"Arial",self.title_block_font_size,(self.title_block_width-0.2)*cm)
        
        canvas.setFont("Arial",title_block_font_size)
        client_text_width = stringWidth(client,"Arial",title_block_font_size)
        canvas.drawString((self.page_width-self.padding.right-self.padding.left-0.5*self.title_block_width)*cm-0.5*client_text_width,(self.divider_height+(self.title_block_height-self.divider_height)/5*4+0.1)*cm,client)
        project_text_width = stringWidth(project,"Arial",title_block_font_size)
        canvas.drawString((self.page_width-self.padding.right-self.padding.left-0.5*self.title_block_width)*cm-0.5*project_text_width,(self.divider_height+(self.title_block_height-self.divider_height)/5*3+0.1)*cm,project)
        location_text_width = stringWidth(location,"Arial",title_block_font_size)
        canvas.drawString((self.page_width-self.padding.right-self.padding.left-0.5*self.title_block_width)*cm-0.5*location_text_width,(self.divider_height+(self.title_block_height-self.divider_height)/5*2+0.1)*cm,location)
        description_line_1_text_width = stringWidth(description_line_1,"Arial",title_block_font_size)
        canvas.drawString((self.page_width-self.padding.right-self.padding.left-0.5*self.title_block_width)*cm-0.5*description_line_1_text_width,(self.divider_height+(self.title_block_height-self.divider_height)/5*1+0.1)*cm,description_line_1)
        description_line_2_width = stringWidth(description_line_2,"Arial",title_block_font_size)
        canvas.drawString((self.page_width-self.padding.right-self.padding.left-0.5*self.title_block_width)*cm-0.5*description_line_2_width,self.divider_height*cm+0.1*cm,description_line_2)
        
        # Add doc number and page number
        title_block_font_size = self.get_font_size_from_max_width([doc_no,page_no],"Arial",self.title_block_font_size,(0.5*self.title_block_width-0.2)*cm)
        doc_no_text_width = stringWidth(doc_no,"Arial",title_block_font_size)
        canvas.drawString((self.page_width-self.padding.right-self.padding.left-0.75*self.title_block_width)*cm-0.5*doc_no_text_width,0.1*cm,doc_no)
        page_no_text_width = stringWidth(page_no,"Arial",title_block_font_size)
        canvas.drawString((self.page_width-self.padding.right-self.padding.left-0.25*self.title_block_width)*cm-0.5*page_no_text_width,0.1*cm,page_no)

        # Add Logo
        canvas.drawImage(self.PSM_Logo_Path ,x=(self.page_width-self.padding.right-self.padding.left-self.title_block_width-1.82)*cm,y=0.1*cm,width=1.71*cm,preserveAspectRatio=True,anchor='sw')
        canvas.restoreState()

        return True

    def _initial_page_content(self,canvas,doc):
        """PRIVATE called at the start of the build sequence for the page
        
        :param canvas: Page Canvas
        :type canvas: Canvas
        :param doc: Page Document
        :type doc: Document
        """
        canvas.setAuthor("PSM")
        canvas.setTitle(os.path.basename(self.file_name))
        canvas.setSubject(os.path.basename(self.file_name))
        self._draw_frame(canvas,doc)
        self._draw_title_block(canvas,doc)
        self._draw_notes(canvas,doc)
        self._draw_footnote(canvas,doc)

    def get_font_size_from_max_width(self,texts,font,font_size,max_width):
        """Calculate font size based on max allowable width of the text
        
        :param texts: the texts to be tested
        :type texts: str
        :param font: font name
        :type font: str
        :param font_size: initial font size
        :type font_size: float
        :param max_width: max allowable width
        :type max_width: float
        :return: font size
        :rtype: float
        """
        if isinstance(texts,str):
            text_width = stringWidth(texts,font,font_size)
            if text_width < max_width:
                return font_size
            else:
                warnings.warn(f"Reduce font size to {font_size-1} pt to accommodate {texts}")
                return self.get_font_size_from_max_width(texts,font,font_size-1,max_width)
        else:
            for t in texts:
                font_size =  min(font_size,self.get_font_size_from_max_width(t,font,font_size,max_width))

            return font_size
    
    def add_note(self,note,counter_text=None):
        """Add note to the page
        
        :param note: Note
        :type note: str
        :type counter_text: str
        """
        self.notes.append({note:note,counter_text:counter_text})
    
    def add_footnote(self,footnote):
        """Add footnote to the page
        
        :param footnote: Footnote
        :type footnote: str
        """
        self.footnote = footnote

    def _draw_notes(self,canvas,doc)->bool:
        """PRIVATE Draw the notes of the page
        
        :param canvas: Canvas of the page
        :type canvas: Canvas
        :param doc: Document of the page
        :type doc: Document
        :return: success
        :rtype: bool
        """
        if len(self.notes) == 0:
            return
        canvas.saveState()
        canvas.translate(self.padding.left*cm,self.padding.bottom*cm)
        canvas.setFont("Arial",self.note_font_size)
        note_height = max((self.title_block_height-1)*cm,self.note_font_size*(len(self.notes)+1))+1*cm
        canvas.drawString(0.5*cm,note_height,self.note_title)
        
        note_counter = 1
        for n in self.notes:
            if n.counter_text == None:
                canvas.drawString((0.5)*cm,note_height-note_counter*self.note_font_size,f"{note_counter}.")
            else:
                canvas.drawString((0.5)*cm,note_height-note_counter*self.note_font_size,f"{n.counter_text}.")
            canvas.drawString((0.5+1)*cm,note_height-note_counter*self.note_font_size,n.note)
            note_counter = note_counter + 1
        canvas.restoreState()
        return True
    
    def _draw_footnote(self,canvas,doc)->bool:
        """PRIVATE Draw the footnote of the page
        
        :param canvas: Canvas of the page
        :type canvas: Canvas
        :param doc: Document of the page
        :type doc: Document
        :return: success
        :rtype: bool
        """          
        canvas.saveState()
        canvas.translate(self.padding.left*cm,self.padding.bottom*cm)
        canvas.setFont("Arial",self.footnote_font_size)
        canvas.drawString(0,-self.footnote_font_size-1,self.footnote)
        canvas.restoreState()
        return True

    def add_figure(self,img_path,width=None,height=None,keep_aspect_ratio=True)->bool:
        """Add image to the page from image path
        
        :param img_data: path to the image
        :type img_data: str
        :param width: target width of the image, defaults to None
        :type width: float, optional
        :param height: target height of the image, defaults to None
        :type height: float, optional
        :param keep_aspect_ratio: whether to keep aspect ratio, defaults to True
        :type keep_aspect_ratio: bool, optional
        :return: Success
        :rtype: bool
        """
        return self._add_figure(img_path,width,height,keep_aspect_ratio)

    def _add_figure(self,img_data,width=None,height=None,keep_aspect_ratio=True):
        """PRIVATE add figure to the page from image path or using matplotlib figure
        
        :param img_data: Image Data
        :type img_data: str or matplotlib figure
        :param width: target width of the image, defaults to None
        :type width: float, optional
        :param height: target height of the image, defaults to None
        :type height: float, optional
        :param keep_aspect_ratio: whether to keep aspect ratio, defaults to True
        :type keep_aspect_ratio: bool, optional
        """
        max_width = self.page_width-2*self.padding.left - 2*self.padding.right

        if hasattr(self,'title_block_height'):
            # make sure image is above the titleblock if there is one
            max_height = self.page_height-2*self.padding.top-2*self.padding.bottom - self.title_block_height
        else:
            # make sure image is within the frame
            max_height = self.page_height-2*self.padding.top-2*self.padding.bottom

        if width == None:
            # make sure image is within the frame
            width = max_width
        elif width > max_width:
            Warning("input image width is larger than max allowable width, image has been rescaled")
            width = max_width
        
        if height == None:
            height = max_height
        elif height > max_height:
            Warning("input image height is larger than max allowable height, image has been rescaled")
            height = max_height
        
        if isinstance(img_data,str):
            # If img_data is a path to the image file
            with PIL.Image.open(img_data) as img:
                image_width, image_height = img.size
                if keep_aspect_ratio:
                    factor = min(width*cm/image_width,height*cm/image_height)
                    width = image_width*factor
                    height = image_height*factor

                self.Story.append(Image(img_data,width,height))
        else:
            # If img_data is binary
            self.figures.append(img_data)
            pdfImage = PDFImage(img_data,width=(width)*cm,height=(height)*cm, kind='bound')
            pdfImage.hAlign = 'CENTRE'
            self.Story.append(pdfImage)

    def add_matplotlib_figure(self,fig,width=None,height=None):
        """Add matplotlib figure to the page
        
        :param fig: matplotlib figure
        :type fig: matplotlib figure
        :param width: target width of the figure, defaults to None
        :type width: float, optional
        :param height: target height of the figure, defaults to None
        :type height: float, optional
        """
        # save matplotlib figure to a byte stream
        img_data = BytesIO()
        fig.savefig(img_data,format='PDF')
        
        self._add_figure(img_data,width=width,height=height)

    def add_table(self,table):
        """Add table to the page
        
        :param table: Table
        :type table: ReportLab table
        """
        self.Story.append(table)

    def save(self):
        """Build and save the page
        
        :raises PSMTemplateBuildError: When the page object was built before
        :return: file name
        :rtype: str
        """
        if self.built:
            raise PSMTemplateBuildError("PSMTemplate can only be built once")
        self.doc.build(self.Story,onFirstPage=self._initial_page_content,onLaterPages=self._initial_page_content)
        self.built = True
        return self.file_name
    
    def add_element(self,element):
        """Add a generic element to the story board
        
        :param element: Generic element
        :type element: ReportLab element
        """
        self.Story.append(element)



class PSMA4(PSMTemplate):
    def __init__(self,file_name:str,direction='portrait'):
        """Initialise PSMA4 object
        
        :param file_name: file name
        :type file_name: str
        :param direction: direction, defaults to 'portrait'
        :type direction: str, optional
        :raises ValueError: invalid input
        """
        if direction == 'portrait':
            super().__init__(file_name,portrait(A4),padding_left=1.38,padding_right=1.38,padding_top=1.38,padding_bottom=1.38)
        elif direction == 'landscape':
            super().__init__(file_name,landscape(A4),padding_left=1.38,padding_right=1.38,padding_top=1.38,padding_bottom=1.38)
        else:
            raise ValueError("invalid direction input, direction should be 'portrait' or 'landscape'")
        
        self.direction = direction

        return

    def add_titleblock(self,client:str,project:str,location:str,description_line_1:str,description_line_2:str,doc_no:str="",page_no:str="")->bool:
        """Add titleblock to the page
        
        :param client: client string in the titleblock
        :type client: str
        :param project: project string in the titleblock
        :type project: str
        :param location: location string in the titleblock
        :type location: str
        :param description_line_1: description_line_1 in the titleblock
        :type description_line_1: str
        :param description_line_2: description_line_2 in the titleblock
        :type description_line_2: str
        :param doc_no: Document Number in the titleblock
        :type doc_no: str
        :param page_no: Page Number in the titleblock
        :type page_no: str
        :param title_block_width: Width of the titleblock in cm, defaults to 9.0
        :type title_block_width: float, optional
        :param title_block_height: Height of the titleblock in cm, defaults to 2.54
        :type title_block_height: float, optional
        :param divider_height: height of the divider, defaults to 0.45
        :type divider_height: float, optional
        :param title_block_font_size: title block font size, defaults to 10
        :type title_block_font_size: int, optional
        :return: Success
        :rtype: bool
        """
        return super().add_titleblock(client,project,location,description_line_1,description_line_2,doc_no,page_no)
    
    def add_matplotlib_figure(self,fig)->bool:
        """Add matplotlib figure to the page
        
        :param fig: matplotlib figure
        :type fig: matplotlib figure
        :return: Success
        :rtype: bool
        """
        return super().add_matplotlib_figure(fig,self.page_width-2*self.padding.left - 2*self.padding.right)

    def add_figure(self,img_path):
        """Add image to the page
        
        :param img_path: image path
        :type img_path: str
        :return: Success
        :rtype: bool
        """
        return super().add_figure(img_path,self.page_width-2*self.padding.left - 2*self.padding.right)

class PSMA3(PSMTemplate):
    def __init__(self,file_name:str,direction='portrait'):
        if direction == 'portrait':
            super().__init__(file_name,portrait(A3),padding_left=1.38,padding_right=1.38,padding_top=1.38,padding_bottom=1.38)
        elif direction == 'landscape':
            super().__init__(file_name,landscape(A3),padding_left=1.38,padding_right=1.38,padding_top=1.38,padding_bottom=1.38)
        else:
            raise ValueError("invalid direction input, direction should be 'portrait' or 'landscape'")

        self.direction = direction

        return
        
    def add_titleblock(self,client:str,project:str,location:str,description_line_1:str,description_line_2:str,doc_no:str="",page_no:str="")->bool:
        """Add titleblock to the page
        
        :param client: client string in the titleblock
        :type client: str
        :param project: project string in the titleblock
        :type project: str
        :param location: location string in the titleblock
        :type location: str
        :param description_line_1: description_line_1 in the titleblock
        :type description_line_1: str
        :param description_line_2: description_line_2 in the titleblock
        :type description_line_2: str
        :param doc_no: Document Number in the titleblock
        :type doc_no: str
        :param page_no: Page Number in the titleblock
        :type page_no: str
        :param title_block_width: Width of the titleblock in cm, defaults to 9.0
        :type title_block_width: float, optional
        :param title_block_height: Height of the titleblock in cm, defaults to 2.54
        :type title_block_height: float, optional
        :param divider_height: height of the divider, defaults to 0.45
        :type divider_height: float, optional
        :param title_block_font_size: title block font size, defaults to 10
        :type title_block_font_size: int, optional
        :return: Success
        :rtype: bool
        """
        return super().add_titleblock(client,project,location,description_line_1,description_line_2,doc_no,page_no)


class PSMAppendix():
    def __init__(self,appendix_name,doc_no,path="",size=A4,direction="portrait",client="",project="",location="",save_temp_file=False):
        """PSMAppendix is a class that combines multiple PSMTemplate pages into a single document
        
        :param appendix_name: Name of the appendix e.g. Appendix A
        :type appendix_name: str
        :param doc_no: Document number e.g. PSM0000-001M
        :type doc_no: str
        :param path: folder to save the appendix in, defaults to ""
        :type path: str, optional
        :param size: default page size of the appendix, defaults to A4
        :type size: (width,height), optional
        :param direction: default page direction of the appendix, defaults to "portrait"
        :type direction: str, optional
        :param client: client string in the titleblock, defaults to ""
        :type client: str, optional
        :param project: project string in the titleblock, defaults to ""
        :type project: str, optional
        :param location: location string in the titleblock, defaults to ""
        :type location: str, optional
        :param save_temp_file: whether the temporary files (individual pages) are saved, defaults to False
        :type save_temp_file: bool, optional
        """
        self.appendix_name = appendix_name
        self.doc_no = doc_no
        self.page_counter = 0
        self.file_names = []
        self.pages = []
        self.size = size
        self.direction = direction
        self.path = path
        self.client = client
        self.project = project
        self.location = location
        self.save_temp_file = save_temp_file
    def add_page(self,page:PSMTemplate):
        """Add a PSMTemplate page to the appendix
        
        :param page: the page to add to the appendix
        :type page: PSMTemplate
        """
        self.pages.append(page)
    def new_page(self,description_line_1:str,description_line_2:str,size=None,direction=None):
        """Create a new page for the appendix. Note: this page needs to be added back to the appendix after external modifications

        :param description_line_1: description_line_1 in the titleblock
        :type description_line_1: str
        :param description_line_2: description_line_2 in the titleblock
        :type description_line_2: str
        :param size: size of the page, defaults to the default page size when the appendix was initialised
        :type size: (width,height), optional
        :param direction: direction of the page, defaults to the default page direction when the appendix was initialised
        :type direction: str, optional
        :raises ValueError: when the page size is not valid
        :return: PSMTemplate page
        :rtype: PSMTemplate
        """
        if size == None:
            size = self.size
        
        if direction == None:
            direction = self.direction

        if self.client == "":
            Warning("Client has not been set")
        if self.project == "":
            Warning("Project has not been set")
        if self.location == "":
            Warning("Location has not been set")
        if(size == A4):
            p = PSMA4(os.path.abspath(os.path.join(self.path,f"{uuid.uuid4()}.pdf")),direction)
        elif(size == A3):
            p = PSMA3(os.path.abspath(os.path.join(self.path,f"{uuid.uuid4()}.pdf")),direction)
        else:
            raise ValueError("Invalid page size")

        p.client = self.client
        p.project = self.project
        p.location = self.location
        p.description_line_1 = description_line_1
        p.description_line_2 = description_line_2
        return p
        
        
    def build(self):
        """Build the appendix and save the document
        """
        for p in self.pages:
            self.page_counter = self.page_counter + 1
            p.doc_no = self.doc_no
            p.page_no = f"{self.appendix_name}{self.page_counter}"
            p.footnote = os.path.abspath(os.path.join(self.path,f"{self.appendix_name}.pdf"))
            self.file_names.append(p.save())
        writer = PdfWriter(os.path.join(self.path,f"{self.appendix_name}.pdf"))

        for fn in self.file_names:
            reader = PdfReader(fn)
            writer.addpages(reader.pages)

        writer.trailer.Info = IndirectPdfDict(
                Title=self.appendix_name,
                Author="PSM",
                Subject=self.appendix_name,
                Creator="psmtemplate"
            )
        writer.write()


        temp_page_counter = 1
        for fn in self.file_names:
            if self.save_temp_file:
                move(fn,os.path.abspath(os.path.join(self.path,f"{self.appendix_name}{temp_page_counter}.pdf")))
            else:
                os.remove(fn)
            
            temp_page_counter = temp_page_counter + 1


        

        
if __name__ == "__main__":

    try:
        os.listdir('test')
    except FileNotFoundError:
        os.makedirs('test')
        
    # Template Test for Matplotlib figures
    a4_portrait_temp = PSMA4("test/matplotlib/A4-portrait.pdf")
    a4_portrait_temp.add_titleblock("Test Client","Test Project","Test Location","Description Line 1","Description Line 2","PSMTEST","FIGURE")
    

    fig = plt.figure(figsize=(4, 3))
    plt.plot([1,2,3,4])
    plt.ylabel('some numbers')

    a4_portrait_temp.add_matplotlib_figure(fig)
    a4_portrait_temp.save()

    a4_landscape_temp = PSMA4("test/matplotlib/A4-landscape.pdf",direction='landscape')
    a4_landscape_temp.add_titleblock("Test Client","Test Project","Test Location","Description Line 1","Description Line 2","PSMTEST","FIGURE")
    

    fig = plt.figure(figsize=(4, 3))
    plt.plot([1,2,3,4])
    plt.ylabel('some numbers')

    a4_landscape_temp.add_matplotlib_figure(fig)
    a4_landscape_temp.save()

    a3_portrait_temp = PSMA3("test/matplotlib/A3-portrait.pdf")
    a3_portrait_temp.add_titleblock("Test Client","Test Project","Test Location","Description Line 1","Description Line 2","PSMTEST","FIGURE")
    

    fig = plt.figure(figsize=(4, 3))
    plt.plot([1,2,3,4])
    plt.ylabel('some numbers')

    a3_portrait_temp.add_matplotlib_figure(fig)
    a3_portrait_temp.save()

    a3_landscape_temp = PSMA3("test/matplotlib/A3-landscape.pdf",direction='landscape')
    a3_landscape_temp.add_titleblock("Test Client","Test Project","Test Location","Description Line 1","Description Line 2","PSMTEST","FIGURE")
    

    fig = plt.figure(figsize=(4, 3))
    plt.plot([1,2,3,4])
    plt.ylabel('some numbers')

    a3_landscape_temp.add_matplotlib_figure(fig)
    a3_landscape_temp.save()

    # Template test for images

    a4_portrait_temp = PSMA4("test/image/A4-portrait.pdf")
    a4_portrait_temp.add_titleblock("Test Client","Test Project","Test Location","Description Line 1","Description Line 2","PSMTEST","FIGURE")

    a4_portrait_temp.add_figure("test/image/test.png")
    a4_portrait_temp.save()

    a4_landscape_temp = PSMA4("test/image/A4-landscape.pdf",direction='landscape')
    a4_landscape_temp.add_titleblock("Test Client","Test Project","Test Location","Description Line 1","Description Line 2","PSMTEST","FIGURE")

    a4_landscape_temp.add_figure("test/image/test.png")
    a4_landscape_temp.save()

    a3_portrait_temp = PSMA3("test/image/A3-portrait.pdf")
    a3_portrait_temp.add_titleblock("Test Client","Test Project","Test Location","Description Line 1","Description Line 2","PSMTEST","FIGURE")

    a3_portrait_temp.add_figure("test/image/test.png")
    a3_portrait_temp.save()

    a3_landscape_temp = PSMA3("test/image/A3-landscape.pdf",direction='landscape')
    a3_landscape_temp.add_titleblock("Test Client","Test Project","Test Location","Description Line 1","Description Line 2","PSMTEST","FIGURE")

    a3_landscape_temp.add_figure("test/image/test.png")
    a3_landscape_temp.save()

    # Appendix Test

    appA = PSMAppendix("Appendix A","PSMTEST","test/appendix/",client="Test Client",project="Test Project",location="Test Location")

    a4_portrait_temp = appA.new_page("Description Line 1","Description Line 2")
    
    for i in range(0,5):
        a4_portrait_temp.add_note(f"Note {i}")

    fig = plt.figure(figsize=(4, 3))
    plt.plot([1,2,3,4])
    plt.ylabel('some numbers')

    a4_portrait_temp.add_matplotlib_figure(fig)

    a4_landscape_temp = appA.new_page("Description Line 1","Description Line 2",size=A4,direction="landscape")

    fig = plt.figure(figsize=(4, 3))
    plt.plot([1,2,3,4])
    plt.ylabel('some numbers')

    a4_landscape_temp.add_matplotlib_figure(fig)

    for i in range(0,5):
        a4_landscape_temp.add_note(f"Note {i}")


    a3_portrait_temp = appA.new_page("Description Line 1","Description Line 2",size=A3,direction="portrait")

    a3_portrait_temp.add_figure("test/image/test.png")
    for i in range(0,5):
        a3_portrait_temp.add_note(f"Note {i}")

    
    a3_landscape_temp = appA.new_page("Description Line 1","Description Line 2",size=A3,direction="landscape")
    a3_landscape_temp.add_figure("test/image/test.png")
    for i in range(0,5):
        a3_landscape_temp.add_note(f"Note {i}")
    
    appA.save_temp_file = True

    appA.add_page(a4_portrait_temp)
    appA.add_page(a4_landscape_temp)
    appA.add_page(a3_portrait_temp)
    appA.add_page(a3_landscape_temp)
    appA.build()