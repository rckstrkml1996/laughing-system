from git import Repo
from loguru import logger

from loader import config



def check_on_update():
    config.updated = check_repo_on_update("..")


def check_repo_on_update(path: str) -> bool:
    repo = Repo(path)

    current = str(repo.head.commit)  # repo class to string
    last_commit = config("last_commit", str)
    config.last_commit = current

    logger.debug(f"Curr = {current:.15}, Last = {last_commit:.15}")

    if current != last_commit:
        logger.warning(f"Repo updated!")
        return True
    else:
        logger.info(f"Repo not updated!")
        return False
