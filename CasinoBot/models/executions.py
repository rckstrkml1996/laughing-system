from loguru import logger

from data.config import SHARE
from .models import User

# зачисление баланса с пополнения мамонта воркеру

def enroll_refer_share(amount: int, cid: int):
	if cid != 0:
		try:
			user = User.get(cid=cid)
			user.ref_balance += amount * SHARE / 100
			user.save()
			logger.debug(f"{cid} - refer has succesfuly enrolled on {amount}")
		except User.DoesNotExist:
			logger.warning(f"{cid} - refer does not exist!")
