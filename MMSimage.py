from PIL import Image, ImageDraw, ImageFont
import msg
import textwrap
import os


def img(customer_id):
    message, icon = msg.msg(customer_id)
    font_folder = os.environ['FONT_FOLDER']
    icon = 'clear-day'

    font = ImageFont.truetype(r'{}'.format(font_folder), 50)

    image = Image.open('Weather-Photos/templates/{}.jpg'.format(icon))
    # todo make the image smaller so it fits on the preview on phones
    draw = ImageDraw.Draw(image)
    draw.text(xy=(80, 80), text="\n".join(textwrap.wrap(message, width=35)), fill=(0, 0, 0), font=font)
    image.save('Weather-Photos/user{}.jpg'.format(customer_id))

    return 'http://192.241.149.241:8000/Weather-Photos/updates/user{}.jpg'.format(customer_id)


if __name__ == "__main__":
    img(20)
