# https://www.blog.pythonlibrary.org/2017/10/17/how-to-watermark-your-photos-with-python/
from PIL import Image

WATERMARK_POSITION = (0, 0)

def load_image(path):
    return Image.open(path)


def watermark(image, watermark):
    """
    Arguments:
    image - base image
    watermark - image to overlay
    Returns: PIL.Image
    """
    width, height = image.size
    union = Image.new('RGBA', (width, height), (0,0,0,0))
    union.paste(image, (0,0))
    union.paste(watermark, WATERMARK_POSITION, watermark)
    # union.show()
    # union.save('newpath')
    return union
