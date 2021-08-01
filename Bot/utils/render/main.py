from copy import deepcopy
import re
import secrets
import os

from PIL import Image, ImageFont, ImageDraw, ImageFilter

from ..executional import get_random_analog
from .graph import gen_point, linear_gradient, gradient_color


package_directory = os.path.dirname(os.path.abspath(__file__))


def render_qiwibalance(balance, date):
    image = Image.open(
        os.path.join(
            package_directory,
            'editable',
            'qiwibalance.png'
        )
    )
    image_w, image_h = image.size

    text_amount = f"{balance} ₽"

    font_medium = ImageFont.truetype(
        os.path.join(
            package_directory,
            'fonts',
            'SFUIDisplay-Medium.ttf',
        ),
        32
    )

    font_semi = ImageFont.truetype(
        os.path.join(
            package_directory,
            'fonts',
            'SFUIText-Semibold.ttf',
        ),
        74
    )

    image_editable = ImageDraw.Draw(image)

    amount_w, amount_h = font_semi.getsize(text_amount)

    # letter spacing -3% (97%)
    width = (image_w - amount_w * 0.97) / 2
    for letter in text_amount:
        image_editable.text(
            (width, 298),
            letter,
            (256, 256, 256),  # white color
            font=font_semi
        )

        w, h = font_semi.getsize(letter)

        width += w * 0.965

    image_editable.text(
        (64, 31),
        date,
        (0, 0, 0),
        font=font_medium
    )

    img_path = f"rendered/{secrets.token_hex(6)}.png"
    image.save(img_path)
    return img_path


def render_qiwitransfer(number, amount, date):
    image = Image.open(
        os.path.join(
            package_directory,
            'editable',
            'qiwitransfer.jpg'
        )
    )
    image_w, image_h = image.size

    text_transfer = f"- {amount} ₽"
    text_amount = f"{amount} ₽"

    font_bold = ImageFont.truetype(
        os.path.join(
            package_directory,
            'fonts',
            'SFUIText-Bold.ttf',
        ),
        36
    )

    font_regular = ImageFont.truetype(
        os.path.join(
            package_directory,
            'fonts',
            'SBSansDisplay-Regular.otf',
        ),
        24
    )

    image_editable = ImageDraw.Draw(image)

    transfer_w, transfer_h = image_editable.textsize(
        text_transfer, font=font_bold
    )
    number_w, number_h = image_editable.textsize(
        number, font=font_regular
    )

    width = (image_w - transfer_w) / 2
    image_editable.text(
        (width, 376),
        text_transfer,
        (0, 0, 0),
        font=font_bold
    )

    width = (image_w - number_w) / 2
    image_editable.text(
        (width, 342),
        number,
        (173, 173, 173),
        font=font_regular
    )

    image_editable.text(
        (31, 1068),
        date,
        (0, 0, 0),
        font=font_regular
    )

    image_editable.text(
        (31, 1167),
        text_amount,
        (0, 0, 0),
        font=font_regular
    )

    img_path = f"rendered/{secrets.token_hex(6)}.jpg"
    image.save(img_path)
    return img_path


def render_sbertransfer(amount, recipient, date):
    image = Image.open(
        os.path.join(
            package_directory,
            'editable',
            'sbertransfer.png'
        )
    )
    image_w, image_h = image.size

    text_amount = f"{amount} ₽"

    for i in re.findall(r"\d+", text_amount):
        text_amount = text_amount.replace(
            i, "{:,}".format(int(i)).replace(",", " "))

    font_bold = ImageFont.truetype(
        os.path.join(
            package_directory,
            'fonts',
            'SFUIText-Bold.ttf',
        ),
        60
    )

    font_medium = ImageFont.truetype(
        os.path.join(
            package_directory,
            'fonts',
            'SFUIDisplay-Medium.ttf',
        ),
        34
    )

    font_display = ImageFont.truetype(
        os.path.join(
            package_directory,
            'fonts',
            'SBSansDisplay-Regular.otf',
        ),
        26
    )

    image_editable = ImageDraw.Draw(image)

    recipient_w, recipient_h = font_display.getsize(recipient.upper())
    amount_w, amount_h = font_bold.getsize(text_amount)

    # letter spacing -3.5% (96.5%)
    width = (image_w - amount_w * 0.965) / 2
    for letter in text_amount:
        image_editable.text(
            (width, 441),
            letter,
            (255, 255, 255),  # white color
            font=font_bold
        )

        w, h = font_bold.getsize(letter)

        width += w * 0.965

    width = (image_w - recipient_w) / 2

    image_editable.text(
        (width, 538),
        recipient.upper(),
        (255, 255, 255),
        font=font_display
    )

    image_editable.text(
        (44, 28),
        date,
        (255, 255, 255),
        font=font_medium
    )

    img_path = f"rendered/{secrets.token_hex(6)}.png"
    image.save(img_path)
    return img_path


def render_graph(profits, worker):
    image = Image.open(
        os.path.join(
            package_directory,
            'editable',
            'graph.png'
        )
    )
    image.convert("RGBA")
    draw = ImageDraw.Draw(image)

    margin_x = 331

    max_x = 2045
    max_y = 1026

    points = [(margin_x, max_y)]
    for i, profit in enumerate(profits.values()):
        try:
            profit_amounts = profits.values()
            profitn = 4 * (profit - min(profit_amounts)) / \
                (max(profit_amounts) - min(profit_amounts))
        except ZeroDivisionError:
            profitn = 0
        points.append(gen_point(i, profitn))
    points.append((max_x, max_y))

    color_palette = [(54, 241, 50, 200), (54, 241, 50, 0)]

    linear_gradient(image, points, gradient_color, color_palette)

    draw.line(points[1:-1], fill=(54, 241, 50), width=7)  # draw green line
    for point in points[1:-1]:  # draw green ellipses on line
        draw.ellipse(
            (point[0]-10, point[1]-10, point[0]+10, point[1]+10),
            fill=(54, 241, 50)
        )

    font_medium = ImageFont.truetype(
        os.path.join(
            package_directory,
            'fonts',
            'SFUIDisplay-Medium.ttf',
        ),
        36
    )

    for i in range(5):  # draw money side
        val = min(profits.values()) + \
            (max(profits.values()) - min(profits.values())) / 4 * i
        w, h = font_medium.getsize(f"{val:.0f} ₽")
        draw.text((310 - w, 1005 - i * 200), f"{val:.0f} ₽",
                  (255, 255, 255), font=font_medium)

    for i, date in enumerate(profits.keys()):  # draw date side
        w, h = font_medium.getsize(date)
        draw.text((335 + 284 * i - w / 2, 1100), date,
                  (255, 255, 255), font=font_medium)

    # draw worker username
    username = f"Воркер: @{worker}"
    w, h = font_medium.getsize(username)
    draw.text(((image.size[0] - w) / 2, 127), username,
              (255, 255, 255), font=font_medium)

    all_amount = f"Всего за неделю: {sum(profits.values()):.0f} ₽"
    w, h = font_medium.getsize(all_amount)
    draw.text(((image.size[0] - w) / 2, 1200), all_amount,
              (255, 255, 255), font=font_medium)

    img_path = f"rendered/{secrets.token_hex(6)}.png"
    image.save(img_path)
    return img_path


def render_profit(general: int, profit, share, service, username):
    image = Image.open(
        os.path.join(
            package_directory,
            'editable',
            'profit.jpg'
        )
    )

    general_text = "{:,}".format(general).replace(",", " ") + " RUB"

    font_general = ImageFont.truetype(
        os.path.join(
            package_directory,
            'fonts',
            'SFUIText-Semibold.ttf',
        ),
        85
    )

    font_analog = ImageFont.truetype(
        os.path.join(
            package_directory,
            'fonts',
            'SFUIText-Semibold.ttf',
        ),
        30
    )

    w, h = font_general.getsize(general_text)
    ligthText(
        image, ((image.size[0] - w) / 2, 350), general_text, font=font_general,
        width=15, fillMain=(255, 255, 255, 255), fillLight=(112, 191, 78, 191)
    )

    analog = get_random_analog(general)

    w, h = font_analog.getsize(analog)
    ligthText(
        image, ((image.size[0] - w) / 2, 440), analog, font=font_analog,
        width=15, fillMain=(255, 255, 255, 220), fillLight=(112, 191, 78, 255)
    )

    font_info = ImageFont.truetype(
        os.path.join(
            package_directory,
            'fonts',
            'SFUIText-Semibold.ttf',
        ),
        65
    )

    profit_text = "{:,}".format(profit).replace(",", " ") + " RUB"

    w, h = font_info.getsize(profit_text)
    ligthText(
        image, (1625 - w, 550), profit_text, font=font_info,
        width=15, fillMain=(255, 255, 255, 255), fillLight=(112, 191, 78, 255)
    )

    share_text = "{:,}".format(share).replace(",", " ") + " RUB"

    w, h = font_info.getsize(share_text)
    ligthText(
        image, (1625 - w, 680), share_text, font=font_info,
        width=15, fillMain=(255, 255, 255, 255), fillLight=(112, 191, 78, 255)
    )

    ligthText(
        image, (206, 550), service, font=font_info,
        width=15, fillMain=(255, 255, 255, 255), fillLight=(112, 191, 78, 255)
    )

    ligthText(
        image, (206, 680), username, font=font_info,
        width=15, fillMain=(255, 255, 255, 255), fillLight=(112, 191, 78, 255)
    )

    img_path = f"rendered/{secrets.token_hex(6)}.jpg"
    image.save(img_path)
    return img_path


def ligthText(image, pos, text, font, width, fillMain=(0, 0, 0, 255), fillLight=(0, 0, 0, 255)):
    imageligth = Image.new("RGBA", image.size, (0, 0, 0, 0))
    draw = ImageDraw.Draw(imageligth)
    draw.text(pos, text, fillMain, font=font)

    imageligth = textLightEffect(imageligth, pos, text, width, font=font,
                                 fill=fillLight)

    image.paste(imageligth, imageligth)


def textLightEffect(image, pos, text, width, font, fill):
    # Create piece of canvas to draw text on and blur
    blurred = Image.new('RGBA', image.size, (0, 0, 0, 0))
    draw = ImageDraw.Draw(blurred)
    draw.text(pos, text=text, fill=fill, font=font)
    blurred = blurred.filter(ImageFilter.BoxBlur(width))
    # Paste soft text onto background
    blurred.paste(image, image)

    return blurred
