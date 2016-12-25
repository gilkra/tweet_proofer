import urllib, cStringIO
from PIL import Image

def check_image_size(url):
    file = cStringIO.StringIO(urllib.urlopen(url).read())
    im=Image.open(file)
    # width, height = im.size

    print im.size 

check_image_size('http://www.designjuices.co.uk/wp-content/uploads/2011/09/luca-molnar4-1024x512.jpg')