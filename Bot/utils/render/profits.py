import re
from secrets import token_hex
import os

from PIL import Image, ImageFont, ImageDraw, ImageFilter
from loguru import logger



package_directory = os.path.dirname(os.path.abspath(__file__))


@logger.catch
def render_profit(
    all_profit: int, profit_sum: int, share_sum: int, service: str, username: str, analog: str
):
    image = Image.open(os.path.join(package_directory, "editable", "profit.jpg"))

    profit_color = tuple(config("profit_render_color", int))  # 240,230,100,255
    profit_light = (112, 191, 78, 255)

    general_text = "{:,}".format(all_profit).replace(",", " ") + " RUB"

    font_general = ImageFont.truetype(
        os.path.join(
            package_directory,
            "fonts",
            "SFUIText-Semibold.ttf",
        ),
        85,
    )

    font_analog = ImageFont.truetype(
        os.path.join(
            package_directory,
            "fonts",
            "SFUIText-Semibold.ttf",
        ),
        30,
    )

    w, h = font_general.getsize(general_text)
    ligthText(
        image,
        ((image.size[0] - w) / 2, 350),
        general_text,
        font=font_general,
        width=15,
        fillMain=profit_color,
        fillLight=profit_light,
    )

    w, h = font_analog.getsize(analog)
    ligthText(
        image,
        ((image.size[0] - w) / 2, 440),
        analog,
        font=font_analog,
        width=15,
        fillMain=profit_color,
        fillLight=profit_light,
    )

    font_info = ImageFont.truetype(
        os.path.join(
            package_directory,
            "fonts",
            "SFUIText-Semibold.ttf",
        ),
        65,
    )

    profit_text = "{:,}".format(profit_sum).replace(",", " ") + " RUB"

    w, h = font_info.getsize(profit_text)
    ligthText(
        image,
        (1625 - w, 550),
        profit_text,
        font=font_info,
        width=15,
        fillMain=profit_color,
        fillLight=profit_light,
    )

    share_text = "{:,}".format(share_sum).replace(",", " ") + " RUB"

    w, h = font_info.getsize(share_text)
    ligthText(
        image,
        (1625 - w, 680),
        share_text,
        font=font_info,
        width=15,
        fillMain=profit_color,
        fillLight=profit_light,
    )

    ligthText(
        image,
        (206, 550),
        service,
        font=font_info,
        width=15,
        fillMain=profit_color,
        fillLight=profit_light,
    )

    ligthText(
        image,
        (206, 680),
        username,
        font=font_info,
        width=15,
        fillMain=profit_color,
        fillLight=profit_light,
    )

    img_path = f"media/{token_hex(6)}.jpg"
    image.save(img_path)
    return img_path


@logger.catch
def ligthText(
    image, pos, text, font, width, fillMain=(0, 0, 0, 255), fillLight=(0, 0, 0, 255)
):
    imageligth = Image.new("RGBA", image.size, (0, 0, 0, 0))
    draw = ImageDraw.Draw(imageligth)
    draw.text(pos, text, fillMain, font=font)

    imageligth = textLightEffect(
        imageligth, pos, text, width, font=font, fill=fillLight
    )

    image.paste(imageligth, imageligth)


@logger.catch
def textLightEffect(image, pos, text, width, font, fill):
    # Create piece of canvas to draw text on and blur
    blurred = Image.new("RGBA", image.size, (0, 0, 0, 0))
    draw = ImageDraw.Draw(blurred)
    draw.text(pos, text=text, fill=fill, font=font)
    blurred = blurred.filter(ImageFilter.BoxBlur(width))
    # Paste soft text onto background
    blurred.paste(image, image)

    return blurred
