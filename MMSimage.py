from PIL import Image, ImageDraw, ImageFont
import msg
import textwrap


def img(customer_id):
    message, icon = msg.msg(customer_id)
    icon = 'clear-day'

    #font = ImageFont.truetype('CALIBRI.TTF', 60)

    image = Image.open('Weather-Photos/templates/{}.jpg'.format(icon))

    draw = ImageDraw.Draw(image)
    draw.text(xy=(80, 80), text="\n".join(textwrap.wrap(message, width=35)), fill=(0, 0, 0))
    image.save('Weather-Photos/updates/user{}.jpg'.format(customer_id))

    return 'http://192.241.149.241:8000/updates/user{}.jpg'.format(customer_id)


if __name__ == "__main__":
    img(8)
