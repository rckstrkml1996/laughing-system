from copy import deepcopy
import re
import secrets
import os

from PIL import Image, ImageFont, ImageDraw, ImageFilter
from loguru import logger

from config import config
from ..executional import get_random_analog

package_directory = os.path.dirname(os.path.abspath(__file__))


@logger.catch
def render_profit(
    all_profit: int, profit_sum: int, share_sum: int, service: str, username: str
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

    analog = get_random_analog(all_profit)

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
            "SFUIText-SemiboldItalic.ttf",
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

    img_path = f"rendered/{secrets.token_hex(6)}.jpg"
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


@logger.catch
def render_qiwibalance(balance, date):
    image = Image.open(os.path.join(package_directory, "editable", "qiwibalance.png"))
    image_w, image_h = image.size

    text_amount = f"{balance} ₽"

    font_medium = ImageFont.truetype(
        os.path.join(
            package_directory,
            "fonts",
            "SFUIDisplay-Medium.ttf",
        ),
        32,
    )

    font_semi = ImageFont.truetype(
        os.path.join(
            package_directory,
            "fonts",
            "SFUIText-Semibold.ttf",
        ),
        74,
    )

    image_editable = ImageDraw.Draw(image)

    amount_w, amount_h = font_semi.getsize(text_amount)

    # letter spacing -3% (97%)
    width = (image_w - amount_w * 0.97) / 2
    for letter in text_amount:
        image_editable.text(
            (width, 298), letter, (256, 256, 256), font=font_semi  # white color
        )

        w, h = font_semi.getsize(letter)

        width += w * 0.965

    image_editable.text((64, 31), date, (0, 0, 0), font=font_medium)

    img_path = f"rendered/{secrets.token_hex(6)}.png"
    image.save(img_path)
    return img_path


@logger.catch
def render_qiwitransfer(number: str, amount: str, date: str):
    image = Image.open(os.path.join(package_directory, "editable", "qiwitransfer.jpg"))
    image_w, image_h = image.size

    text_transfer = f"- {amount} ₽"
    text_amount = f"{amount} ₽"

    font_bold = ImageFont.truetype(
        os.path.join(
            package_directory,
            "fonts",
            "SFUIText-Bold.ttf",
        ),
        36,
    )

    font_regular = ImageFont.truetype(
        os.path.join(
            package_directory,
            "fonts",
            "SBSansDisplay-Regular.otf",
        ),
        24,
    )

    image_editable = ImageDraw.Draw(image)

    transfer_w, transfer_h = image_editable.textsize(text_transfer, font=font_bold)
    number_w, number_h = image_editable.textsize(number, font=font_regular)

    width = (image_w - transfer_w) / 2
    image_editable.text((width, 376), text_transfer, (0, 0, 0), font=font_bold)

    width = (image_w - number_w) / 2
    image_editable.text((width, 342), number, (173, 173, 173), font=font_regular)

    image_editable.text((31, 1068), date, (0, 0, 0), font=font_regular)

    image_editable.text((31, 1167), text_amount, (0, 0, 0), font=font_regular)

    img_path = f"rendered/{secrets.token_hex(6)}.jpg"
    image.save(img_path)
    return img_path


@logger.catch
def render_sbertransfer(amount, recipient, date):
    image = Image.open(os.path.join(package_directory, "editable", "sbertransfer.png"))
    image_w, image_h = image.size

    text_amount = f"{amount} ₽"

    for i in re.findall(r"\d+", text_amount):
        text_amount = text_amount.replace(i, "{:,}".format(int(i)).replace(",", " "))

    font_bold = ImageFont.truetype(
        os.path.join(
            package_directory,
            "fonts",
            "SFUIText-Bold.ttf",
        ),
        60,
    )

    font_medium = ImageFont.truetype(
        os.path.join(
            package_directory,
            "fonts",
            "SFUIDisplay-Medium.ttf",
        ),
        34,
    )

    font_display = ImageFont.truetype(
        os.path.join(
            package_directory,
            "fonts",
            "SBSansDisplay-Regular.otf",
        ),
        26,
    )

    image_editable = ImageDraw.Draw(image)

    recipient_w, recipient_h = font_display.getsize(recipient.upper())
    amount_w, amount_h = font_bold.getsize(text_amount)

    # letter spacing -3.5% (96.5%)
    width = (image_w - amount_w * 0.965) / 2
    for letter in text_amount:
        image_editable.text(
            (width, 441), letter, (255, 255, 255), font=font_bold  # white color
        )

        w, h = font_bold.getsize(letter)

        width += w * 0.965

    width = (image_w - recipient_w) / 2

    image_editable.text(
        (width, 538), recipient.upper(), (255, 255, 255), font=font_display
    )

    image_editable.text((44, 28), date, (255, 255, 255), font=font_medium)

    img_path = f"rendered/{secrets.token_hex(6)}.png"
    image.save(img_path)
    return img_path
