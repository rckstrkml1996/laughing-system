import math
from os import path

# from secrets import token_hex

from PIL import Image

from loguru import logger


package_directory = path.dirname(path.abspath(__file__))


@logger.catch
def render_profile(profile_path: str, active: bool = True):
    image = Image.open(
        path.join(package_directory, "editable", "profilepic.png")
    ).convert("RGB")

    if active:
        image_w, image_h = image.size
        logger.debug(f"{image.size=}")

        profile_image = Image.open(profile_path)
        profile_image.thumbnail((355, 355))
        logger.debug(f"{profile_image.size=}")

        profile_image_w, profile_image_h = profile_image.size

        # Center the image

        offset = (123, 138)

        image.paste(profile_image, offset)

    image.save(profile_path)

    return profile_path
