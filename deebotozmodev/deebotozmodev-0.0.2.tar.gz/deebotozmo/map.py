from io import BytesIO
import base64
import lzma
import numpy as np
import logging
from PIL import Image, ImageDraw, ImageOps

_LOGGER = logging.getLogger(__name__)

class Map:
    def __init__(self):
        self.buffer = np.zeros((64, 100, 100))
        self.mapPieces = np.empty((64), np.dtype('U100'))
        self.isMapUpdated = False
        self.base64Image = None
        self.rooms = []
        self.charger_position = None
        self.robot_position = None

        self.colors = {"floor": "#badaff", "wall": "#4e96e2", "carpet": "#1a81ed"}

        self.draw_charger = False
        self.draw_robot = False

        self.room_colors = [(238,225,235,255),(239,236,221,255),(228,239,223,255),(225,234,239,255),(238,223,216,255),(240,228,216,255),(233,139,157,255),(239,200,201,255),(201,2019,239,255)]
        self.robot_png = "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"
        self.charger_png = "iVBORw0KGgoAAAANSUhEUgAAAD8AAABuCAYAAACQjcuNAAAACXBIWXMAAAsTAAALEwEAmpwYAAAE82lUWHRYTUw6Y29tLmFkb2JlLnhtcAAAAAAAPD94cGFja2V0IGJlZ2luPSLvu78iIGlkPSJXNU0wTXBDZWhpSHpyZVN6TlRjemtjOWQiPz4gPHg6eG1wbWV0YSB4bWxuczp4PSJhZG9iZTpuczptZXRhLyIgeDp4bXB0az0iQWRvYmUgWE1QIENvcmUgNS42LWMxNDUgNzkuMTYzNDk5LCAyMDE4LzA4LzEzLTE2OjQwOjIyICAgICAgICAiPiA8cmRmOlJERiB4bWxuczpyZGY9Imh0dHA6Ly93d3cudzMub3JnLzE5OTkvMDIvMjItcmRmLXN5bnRheC1ucyMiPiA8cmRmOkRlc2NyaXB0aW9uIHJkZjphYm91dD0iIiB4bWxuczp4bXA9Imh0dHA6Ly9ucy5hZG9iZS5jb20veGFwLzEuMC8iIHhtbG5zOmRjPSJodHRwOi8vcHVybC5vcmcvZGMvZWxlbWVudHMvMS4xLyIgeG1sbnM6cGhvdG9zaG9wPSJodHRwOi8vbnMuYWRvYmUuY29tL3Bob3Rvc2hvcC8xLjAvIiB4bWxuczp4bXBNTT0iaHR0cDovL25zLmFkb2JlLmNvbS94YXAvMS4wL21tLyIgeG1sbnM6c3RFdnQ9Imh0dHA6Ly9ucy5hZG9iZS5jb20veGFwLzEuMC9zVHlwZS9SZXNvdXJjZUV2ZW50IyIgeG1wOkNyZWF0b3JUb29sPSJBZG9iZSBQaG90b3Nob3AgQ0MgMjAxOSAoV2luZG93cykiIHhtcDpDcmVhdGVEYXRlPSIyMDIwLTA1LTIyVDE0OjEwOjQ0KzAyOjAwIiB4bXA6TW9kaWZ5RGF0ZT0iMjAyMC0wNS0yMlQxNzoxODo1NCswMjowMCIgeG1wOk1ldGFkYXRhRGF0ZT0iMjAyMC0wNS0yMlQxNzoxODo1NCswMjowMCIgZGM6Zm9ybWF0PSJpbWFnZS9wbmciIHBob3Rvc2hvcDpDb2xvck1vZGU9IjMiIHhtcE1NOkluc3RhbmNlSUQ9InhtcC5paWQ6MmQ0MmM1MDQtYjhmZC0xMDRjLTg5ZGItYzQ1YTIxYmViNGE3IiB4bXBNTTpEb2N1bWVudElE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"

    def isUpdatePiece(self, index, mapPiece):
        _LOGGER.debug("isUpdatePiece " + str(index) + ' ' + str(mapPiece))

        value = str(index) + '-' + str(mapPiece)
        
        if self.mapPieces[index] != value:
            self.mapPieces[index] = value

            self.isMapUpdated = False

            if str(mapPiece) != '1295764014':
                return True
            else:
                return False

        _LOGGER.debug("AddMapPiece not to update")

    def AddMapPiece(self, mapPiece, b64):
        _LOGGER.debug("AddMapPiece " + str(mapPiece) + ' ' + str(b64))

        decoded = self.decompress7zBase64Data(b64)

        decoded = list(decoded)
        MATRIX_PIECE = np.reshape(decoded,(100,100))

        self.buffer[mapPiece] = MATRIX_PIECE
        _LOGGER.debug("AddMapPiece done")

    def decompress7zBase64Data(self, data):
        _LOGGER.debug("decompress7zBase64Data begin")
        finalArray = bytearray()
        
        # Decode Base64
        data = base64.b64decode(data)

        i = 0
        for idx in data:
            if (i == 8):
                finalArray += b'\x00\x00\x00\x00'
            finalArray.append(idx)
            i +=1

        dec = lzma.LZMADecompressor(lzma.FORMAT_AUTO, None, None)

        decompressed_data = dec.decompress(finalArray)

        _LOGGER.debug("decompress7zBase64Data done")
        return decompressed_data
    
    def updateRobotPosition(self, cordx, cordy):
        if(self.robot_position != None):
            _LOGGER.debug("New robot position: " + str(cordx) + ',' + str(cordy))
            if (self.robot_position['x'] != cordx) or (self.robot_position['y'] != cordy):
                self.robot_position = {'x':cordx ,'y': cordy}
                self.isMapUpdated = False
        else:
            _LOGGER.debug("robot position set: " + str(cordx) + ',' + str(cordy))
            self.robot_position = {'x':cordx ,'y': cordy}
            self.isMapUpdated = False
            self.draw_robot = True

    def updateChargerPosition(self, cordx, cordy):
        if(self.charger_position != None):
            _LOGGER.debug("New charger position: " + str(cordx) + ',' + str(cordy))
            if (self.charger_position['x'] != cordx) or (self.charger_position['y'] != cordy):
                self.charger_position = {'x':cordx ,'y': cordy}
                self.isMapUpdated = False
        else:
            _LOGGER.debug("charger position set: " + str(cordx) + ',' + str(cordy))
            self.charger_position = {'x':cordx ,'y': cordy}
            self.isMapUpdated = False
            self.draw_charger = True
        
    def GetBase64Map(self):
        if self.isMapUpdated == False:
            _LOGGER.debug("GetBase64Map begin")

            resizeFactor = 1
            pixelWidth = 50
            offset = 400

            im = Image.new("RGBA", (1000, 1000))
            draw = ImageDraw.Draw(im)
            roomnr = 0

            _LOGGER.debug("GetBase64Map draw_rooms")
            #Draw Rooms
            for room in self.rooms:
                coordsXY = room['values'].split(';')
                listcord = []
                _sumx = 0
                _sumy = 0
                _points = 0

                for cord in coordsXY:
                    cord = cord.split(',')

                    x = (int(cord[0])/pixelWidth)+offset
                    y = (int(cord[1])/pixelWidth)+offset

                    listcord.append(x)
                    listcord.append(y)

                    # Sum for center point
                    _sumx = _sumx + x
                    _sumy = _sumy + y


                draw.line(listcord,fill=(255,0,0),width=1)
                
                centerX = _sumx / len(coordsXY)
                centerY = _sumy / len(coordsXY)

                ImageDraw.floodfill(im,xy=(centerX,centerY),value=self.room_colors[roomnr % len(self.room_colors)])

                draw.line(listcord,fill=(0,0,0,0),width=1)
                roomnr = roomnr +1

            _LOGGER.debug("GetBase64Map draw_map")
            #Draw MAP
            imageX = 0
            imageY = 0

            for i in range(64):
                if i > 0:
                    if i % 8 != 0:
                            imageY += 100
                    else:
                        imageX += 100
                        imageY = 0

                for y in range(100):
                    for x in range(100):
                        if self.buffer[i][x][y] == 0x01: #floor
                            if im.getpixel((imageX+x,imageY+y)) == (0,0,0,0):
                                draw.point((imageX+x,imageY+y), fill=self.colors['floor'])
                        if self.buffer[i][x][y] == 0x02: #wall
                            draw.point((imageX+x,imageY+y), fill=self.colors['wall'])
                        if self.buffer[i][x][y] == 0x03: #carpet
                            if im.getpixel((imageX+x,imageY+y)) == (0,0,0,0):
                                draw.point((imageX+x,imageY+y), fill=self.colors['carpet'])

            del draw

            _LOGGER.debug("GetBase64Map resize")
            # Resize * resizeFactor
            ##im = im.resize((im.size[0]*resizeFactor, im.size[1]*resizeFactor), Image.NEAREST)

            if self.draw_charger:
                _LOGGER.debug("GetBase64Map draw robot")
                #Draw Current Deebot Position
                robot_icon = Image.open(BytesIO(base64.b64decode(self.robot_png)))
                im.paste(robot_icon, (int(((self.robot_position['x']/pixelWidth)+offset)*resizeFactor), int(((self.robot_position['y']/pixelWidth)+offset)*resizeFactor)), robot_icon.convert('RGBA'))

            if self.draw_robot:
                _LOGGER.debug("GetBase64Map draw charger")
                #Draw charger
                charger_icon = Image.open(BytesIO(base64.b64decode(self.charger_png)))
                
                im.paste(charger_icon, (int(((self.charger_position['x']/pixelWidth)+offset)*resizeFactor), int(((self.charger_position['y']/pixelWidth)+offset)*resizeFactor)), charger_icon.convert('RGBA'))

            _LOGGER.debug("GetBase64Map flip")
            #Flip
            im = ImageOps.flip(im)

            _LOGGER.debug("GetBase64Map crop")
            #Crop
            imageBox = im.getbbox()
            cropped=im.crop(imageBox)

            _LOGGER.debug("GetBase64Map save")
            #save
            buffered = BytesIO()

            cropped.save(buffered, format="PNG")

            self.isMapUpdated = True

            self.base64Image = base64.b64encode(buffered.getvalue())
            _LOGGER.debug("GetBase64Map done")

        return self.base64Image