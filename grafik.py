from PIL import Image, ImageDraw
import db
#(0,0) = (547,495) gorizont 1 = 45 vertikal 1 = 45
def create_pic(id):
    startx = 547
    starty = 495
    pos = db.get_current_position(id).split()
    x= int(pos[0])
    y = int(pos[1])
    im = Image.open('midq.jpg')
    draw = ImageDraw.Draw(im)
    draw.rounded_rectangle([(startx+x*45-10,starty-y*45-10), (startx+x*45+10, starty-y*45+10)],radius=10, fill=(0,255,0))
    im.save(f'{id}.jpg')