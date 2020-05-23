import argparse
import os
from PIL import Image, ImageEnhance, ImageFilter


def main():

    #ALL  FUNCTIONS
    def pixel(src):
        """
        This Function pixelates the image given by resizing it bilinearly to it's nearest pixel density.
        """
        
        img = Image.open('%s'%(src))

        small_IMG = img.resize((64,64),Image.BILINEAR)
        result = small_IMG.resize(img.size,Image.NEAREST)

        result_path = os.path.dirname(src)
        str(result_path)
        result_path = (result_path+'\\')
        result.save(result_path+'pixelated.png')
        print('Image saved at : '+result_path+'pixelated.png')

    def black_white(src):
        """
        This function converts the inmage into black and white by the convert function in the pillow library.
        """
        img = Image.open('%s'%(src))
        img = img.convert('1')
        result_path = os.path.dirname(src)
        str(result_path)
        result_path = (result_path+'\\')
        img.save(result_path+'black_white.png')
        print('Image saved at : '+result_path+'black_white.png')

    def blur(src):
        """
        This function blurs the image by reducing the pixel intensity and smoothens the edges of the pixels
        """
        intensity = 4
        img = Image.open('%s'%(src))
        result = img.filter(ImageFilter.MinFilter(intensity))

        result_path = os.path.dirname(src)
        str(result_path)
        result_path = (result_path+'\\')
        result.save(result_path+'blur.png')
        print('Image saved at : '+result_path+'blur.png')

    def blur_edge(src):
        """
        This function blurs the edges of the image, by reducing the pixel intensity and smoothens the edges of the pixels
        """
        radius, diameter = 20, 30
        
        img = Image.open('%s'%(src))
        
        background_size = (img.size[0] + diameter, img.size[1] + diameter)
        background = Image.new('RGB', background_size, (255, 255, 255))
        background.paste(img, (radius, radius))
        
        mask_size = (img.size[0] + diameter, img.size[1] + diameter)
        mask = Image.new('L', mask_size, 255)
        black_size = (img.size[0] - diameter, img.size[1] - diameter)
        black = Image.new('L', black_size, 0)

        mask.paste(black, (diameter, diameter))
        
        blur = background.filter(ImageFilter.GaussianBlur(radius / 2))
        background.paste(blur, mask=mask)

        result_path = os.path.dirname(src)
        str(result_path)
        result_path = (result_path+'\\')
        background.save(result_path+'bluredge.png')
        print('Image saved at : '+result_path+'bluredge.png')

    def gen_thumbnail(src):
        """
        This function is used to create a thumbnail out of the image by reducing the overall size entirely
        """
        width, height = 200,200
        img = Image.open('%s'%(src))
        
        size = (width, height)
        
        img.thumbnail(size)

        result_path = os.path.dirname(src)
        str(result_path)
        result_path = (result_path+'\\')
        img.save(result_path+'thumbnail.png')
        print('Image saved at : '+result_path+'thumbnail.png')

    def makepdf(src):
        img = Image.open('%s'%(src))
        img = img.convert('RGB')

        result_path = os.path.dirname(src)
        str(result_path)
        result_path = (result_path+'\\')

        img.save(result_path+'makepdf.pdf')
        print('PDF saved at : '+result_path+'makepdf.pdf')

    # Arguments to be passed:
    parser = argparse.ArgumentParser(description= 'PFX can help with Imaging Effects')

    parser.add_argument('-pixelate','-p' ,dest= 'pixel', help= 'Pixelates the image!')

    parser.add_argument('-black_white','-bg', dest= 'blackwhite' , help= 'Decolourises the image!')

    parser.add_argument('-blur','-b', dest= 'blur' , help= 'Blurs the image!')

    parser.add_argument('-bluredge','-be', dest= 'bluredge' , help= 'Blurs the edges of the image!')

    parser.add_argument('-thumbnail','-tn', dest= 'thumbnail' , help= 'Creates a Thumbnail of the image!')

    parser.add_argument('-makepdf','-pdf',dest= 'makepdf' , help= 'Creates a pdf of the image!')

    args = parser.parse_args()

    #Arguments to be checked:
    if args.blackwhite:
        black_white(args.blackwhite)
    if  args.pixel:
        pixel(args.pixel)
    if args.blur:
        blur(args.blur)
    if args.bluredge:
        blur_edge(args.bluredge)
    if args.thumbnail:
        gen_thumbnail(args.thumbnail)
    if args.makepdf:
        makepdf(args.makepdf)


if __name__ == "__main__":
    """
    The godly 2-liner to sum up everything!
    """
    main()