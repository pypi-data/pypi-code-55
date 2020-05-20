from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont
import datetime

def generateDateImage():
    """
    Haha. This project sucks. resize stuff if text overflows.
    Args:
        None
    Returns:
        None
    """
    
    todaystr = datetime.date.today().strftime("%B %d, %Y")
    
    fontloc = 'generatedateimage/res/BalsamiqSans-Bold.ttf'

    font = ImageFont.truetype(fontloc, size=100)
    img = Image.new('RGB', (500, 500))
    d = ImageDraw.Draw(img)
    d.text((100, 100), 'IS IT', fill=(255, 255, 255),font=font)
    font2 = ImageFont.truetype(fontloc,size=70)
    d.text((0, 207), todaystr+'?', fill=(200,200,200), font=font2)
    
    img.save("image.png")
