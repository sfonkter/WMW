from PIL import Image, ImageDraw, ImageFont
import msg
import textwrap
import os


def img(customer_id):
    message, icon = msg.msg(customer_id)
    font_folder = os.environ['FONT_FOLDER']
    # set default icon
    default_icon = 'clear-day'

    font = ImageFont.truetype(r'{}'.format(font_folder), 50)
    print(icon)
    try:
        image = Image.open('Weather-Photos/templates/{}.jpg'.format(icon))
    except Exception as e:
        print(e)
        image = Image.open('Weather-Photos/templates/{}.jpg'.format(default_icon))

    draw = ImageDraw.Draw(image)
    draw.text(xy=(70, 270), text="\n".join(textwrap.wrap(message, width=35)), fill=(0, 0, 0), font=font)
    image.save('Weather-Photos/user{}.jpg'.format(customer_id))

    return 'http://weathermywardrobe.com:8000/user{}.jpg'.format(customer_id)