from io import BytesIO
from lxml import etree
# x = "-10"
# y = "-10"
# text - anchor = "end"
BRANDABLE_FORMATS = ['svg']

BRANDING = """
<g>
<text 
    stroke="cadetblue"
    font-family="courier">
    <a href="https://pointillism.io">pointillism.io</a>
</text>
</g>
"""


def is_brandable_format(format):
    return format in BRANDABLE_FORMATS


def brand(body):
    """
    param body:
    """
    rendering = etree.parse(BytesIO(body))
    target = rendering.find("/")
    target.insert(2, etree.XML(BRANDING))
    return etree.tostring(rendering).decode('utf8')  # todo, don't decode


