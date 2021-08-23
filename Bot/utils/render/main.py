from copy import deepcopy
import re
import secrets
import os

from PIL import Image, ImageFont, ImageDraw, ImageFilter
from loguru import logger

from ..executional import get_random_analog

package_directory = os.path.dirname(os.path.abspath(__file__))


@logger.catch
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


@logger.catch
def ligthText(image, pos, text, font, width, fillMain=(0, 0, 0, 255), fillLight=(0, 0, 0, 255)):
    imageligth = Image.new("RGBA", image.size, (0, 0, 0, 0))
    draw = ImageDraw.Draw(imageligth)
    draw.text(pos, text, fillMain, font=font)

    imageligth = textLightEffect(imageligth, pos, text, width, font=font,
                                 fill=fillLight)

    image.paste(imageligth, imageligth)


@logger.catch
def textLightEffect(image, pos, text, width, font, fill):
    # Create piece of canvas to draw text on and blur
    blurred = Image.new('RGBA', image.size, (0, 0, 0, 0))
    draw = ImageDraw.Draw(blurred)
    draw.text(pos, text=text, fill=fill, font=font)
    blurred = blurred.filter(ImageFilter.BoxBlur(width))
    # Paste soft text onto background
    blurred.paste(image, image)

    return blurred
