from os import path

from PIL import Image

from loguru import logger


package_directory = path.dirname(path.abspath(__file__))


@logger.catch
def render_profile(profile_path: str, active: bool = True):
    image = Image.open(
        path.join(package_directory, "editable", "profilepic.png")
    ).convert("RGB")

    if active:
        profile_image = Image.open(profile_path)
        profile_image.thumbnail((355, 355))
        logger.debug(f"{profile_image.size=}")

        offset = (123, 138)

        image.paste(profile_image, offset)

    image.save(profile_path)

    return profile_path
