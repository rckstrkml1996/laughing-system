import re
from secrets import token_hex
from os import path

from PIL import Image, ImageFont, ImageDraw
from loguru import logger


package_directory = path.dirname(path.abspath(__file__))


@logger.catch
def render_qiwibalance(balance, date):
    image = Image.open(path.join(package_directory, "editable", "qiwibalance.png"))
    image_w, image_h = image.size

    text_amount = f"{balance} ₽"

    font_medium = ImageFont.truetype(
        path.join(
            package_directory,
            "fonts",
            "SFUIDisplay-Medium.ttf",
        ),
        32,
    )

    font_semi = ImageFont.truetype(
        path.join(
            package_directory,
            "fonts",
            "SFUIText-Semibold.ttf",
        ),
        74,
    )

    image_editable = ImageDraw.Draw(image)

    amount_w, _ = font_semi.getsize(text_amount)

    # letter spacing -3% (97%)
    width = (image_w - amount_w * 0.97) / 2
    for letter in text_amount:
        image_editable.text(
            (width, 298), letter, (256, 256, 256), font=font_semi  # white color
        )

        w, _ = font_semi.getsize(letter)

        width += w * 0.965

    image_editable.text((64, 31), date, (0, 0, 0), font=font_medium)

    img_path = f"../media/qb{token_hex(6)}.png"
    image.save(img_path)
    return img_path


@logger.catch
def render_qiwitransfer(number: str, amount: str, date: str):
    image = Image.open(path.join(package_directory, "editable", "qiwitransfer.jpg"))
    image_w, _ = image.size

    text_transfer = f"- {amount} ₽"
    text_amount = f"{amount} ₽"

    font_bold = ImageFont.truetype(
        path.join(
            package_directory,
            "fonts",
            "SFUIText-Bold.ttf",
        ),
        36,
    )

    font_regular = ImageFont.truetype(
        path.join(
            package_directory,
            "fonts",
            "SBSansDisplay-Regular.otf",
        ),
        24,
    )

    image_editable = ImageDraw.Draw(image)

    transfer_w, _ = image_editable.textsize(text_transfer, font=font_bold)
    number_w, _ = image_editable.textsize(number, font=font_regular)

    width = (image_w - transfer_w) / 2
    image_editable.text((width, 376), text_transfer, (0, 0, 0), font=font_bold)

    width = (image_w - number_w) / 2
    image_editable.text((width, 342), number, (173, 173, 173), font=font_regular)

    image_editable.text((31, 1068), date, (0, 0, 0), font=font_regular)

    image_editable.text((31, 1167), text_amount, (0, 0, 0), font=font_regular)

    img_path = f"../media/qt{token_hex(6)}.jpg"
    image.save(img_path)
    return img_path


@logger.catch
def render_sbertransfer(amount, recipient, date):
    image = Image.open(path.join(package_directory, "editable", "sbertransfer.png"))
    image_w, _ = image.size

    text_amount = f"{amount} ₽"

    for i in re.findall(r"\d+", text_amount):
        text_amount = text_amount.replace(i, "{:,}".format(int(i)).replace(",", " "))

    font_bold = ImageFont.truetype(
        path.join(
            package_directory,
            "fonts",
            "SFUIText-Bold.ttf",
        ),
        60,
    )

    font_medium = ImageFont.truetype(
        path.join(
            package_directory,
            "fonts",
            "SFUIDisplay-Medium.ttf",
        ),
        34,
    )

    font_display = ImageFont.truetype(
        path.join(
            package_directory,
            "fonts",
            "SBSansDisplay-Regular.otf",
        ),
        26,
    )

    image_editable = ImageDraw.Draw(image)

    recipient_w, _ = font_display.getsize(recipient.upper())
    amount_w, _ = font_bold.getsize(text_amount)

    # letter spacing -3.5% (96.5%)
    width = (image_w - amount_w * 0.965) / 2
    for letter in text_amount:
        image_editable.text(
            (width, 441), letter, (255, 255, 255), font=font_bold  # white color
        )

        w, _ = font_bold.getsize(letter)

        width += w * 0.965

    width = (image_w - recipient_w) / 2

    image_editable.text(
        (width, 538), recipient.upper(), (255, 255, 255), font=font_display
    )

    image_editable.text((44, 28), date, (255, 255, 255), font=font_medium)

    img_path = f"../media/st{token_hex(6)}.png"
    image.save(img_path)
    return img_path
