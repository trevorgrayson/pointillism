# https://www.blog.pythonlibrary.org/2017/10/17/how-to-watermark-your-photos-with-python/
from PIL import Image
import io


WATERMARK_POSITION = (0, 0)

def load_stream(pipe):
    buffer = io.BytesIO()
    buffer.write(pipe)
    buffer.seek(0)

    return Image.frombytes('RGB', buffer)


def load_image(path):
    return Image.open(path)

DEFAULT_WATERMARK = load_image('public/images/watermark.png')

def watermark(image, watermark=None):
    """
    Arguments:
    image - base image
    watermark - image to overlay
    Returns: PIL.Image
    """
    if watermark is None:
        watermark = DEFAULT_WATERMARK

    width, height = image.size
    union = Image.new('RGBA', (width, height), (0,0,0,0))
    union.paste(image, (0,0))
    union.paste(watermark, WATERMARK_POSITION, watermark)
    # union.show()
    # union.save('newpath')
    return union
