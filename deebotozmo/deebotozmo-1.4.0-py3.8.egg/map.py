from io import BytesIO
import base64
import lzma
import numpy as np
from PIL import Image, ImageDraw, ImageOps

class Map:
    def __init__(self):
        self.buffer = np.zeros((64, 100, 100))
        self.mapPieces = np.empty((64), str)
        self.isMapUpdated = False
        self.base64Image = None

    def isUpdatePiece(self, index, mapPiece):
        value = str(index) + '-' + str(mapPiece)
        
        if self.mapPieces[index] != value:
            self.mapPieces[index] = value

            self.isMapUpdated = False

            if str(mapPiece) != '1295764014':
                return True
            else:
                return False

    def AddMapPiece(self, mapPiece, b64):
        decoded = self.decompress7zBase64Data(b64)

        decoded = list(decoded)
        MATRIX_PIECE = np.reshape(decoded,(100,100))

        self.buffer[mapPiece] = MATRIX_PIECE

    def decompress7zBase64Data(self, data):
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

        return dec.decompress(finalArray)
    
    def GetBase64Map(self):
        if self.isMapUpdated == False:
            im = Image.new("RGBA", (6400, 6400))
            draw = ImageDraw.Draw(im)

            imageX = 0
            imageY = 0

            for i in range(64):
                if i > 0:
                    if i % 8 != 0:
                            imageY += 100
                    else:
                        imageX += 100
                        imageY = 0

                for x in range(100):
                    for y in range(100):
                        if self.buffer[i][x][y] == 0x01: #floor
                            draw.point((imageX+x,imageY+y), fill=(186,218,255))
                        if self.buffer[i][x][y] == 0x02: #wall
                            draw.point((imageX+x,imageY+y), fill=(78,150,226))

            del draw

            #Flip
            im = ImageOps.flip(im)

            #Crop
            image_data = np.asarray(im)
            image_data_bw = image_data.max(axis=2)
            non_empty_columns = np.where(image_data_bw.max(axis=0)>0)[0]
            non_empty_rows = np.where(image_data_bw.max(axis=1)>0)[0]
            cropBox = (min(non_empty_rows), max(non_empty_rows), min(non_empty_columns), max(non_empty_columns))

            image_data_new = image_data[cropBox[0]:cropBox[1]+1, cropBox[2]:cropBox[3]+1 , :]

            new_image = Image.fromarray(image_data_new)

            buffered = BytesIO()
            new_image.save(buffered, format="PNG")

            self.isMapUpdated = True

            base64Image = base64.b64encode(buffered.getvalue())

        return base64Image