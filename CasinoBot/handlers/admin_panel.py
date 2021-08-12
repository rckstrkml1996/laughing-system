from datetime import datetime
from asyncio import sleep

from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.utils.exceptions import ChatNotFound
from aiogram.types import ChatType
from aiogram.dispatcher.filters.builtin import Text
from loguru import logger

from loader import dp, qiwis
from customutils.models import User
from data.states import AdminPanel
from data.config import ADMINS_ID, PAY_ROWS, PAYMENTS_MODE
from keyboards import *


""" admin panel """


def check_admin(chat_id: int):
    """
    Проверка являеться ли юзер админом
    """
    if chat_id in ADMINS_ID:
        return True
    else:
        logger.info(f"#{chat_id} - try admin panel")


@dp.message_handler(Text(startswith="админ", ignore_case=True), state="*")
async def admin_panel(message: types.Message, state: FSMContext):
    """
    Перевод на различные стейты из админ панели
    """
    if check_admin(message.chat.id):
        await message.answer("Админка, выберете действие...", reply_markup=admin_keyboard)
        # Set state
        await AdminPanel.main.set()


@dp.message_handler(Text(startswith="qiwi", ignore_case=True), state=AdminPanel.main)
async def qiwi_main(message: types.Message):
    if check_admin(message.chat.id):
        await message.answer("Выберите кошелек", reply_markup=qiwi_keyboard)


@dp.message_handler(Text(startswith="смена", ignore_case=True), state=AdminPanel.main)
async def change_payments_mode(message: types.Message):
    if check_admin(message.chat.id):
        global PAYMENTS_MODE  # SHIIIT
        PAYMENTS_MODE = not PAYMENTS_MODE
        mode = "Ручка" if PAYMENTS_MODE == False else "Автомат"
        await message.answer(f"Режим изменен | {mode}")


@dp.callback_query_handler(lambda cb: cb.data.split("_")[0] == "qiwi", state="*")
async def qiwi_lasttr(query: types.CallbackQuery):
    if check_admin(query.message.chat.id):
        balance = await qiwis[query.data.split("_")[1]].balance
        payments = await qiwis[query.data.split("_")[1]].last_recharges(PAY_ROWS)
        last_payments = f"Qiwi: {query.data.split('_')[1]}\n{balance['amount']} рублей ({balance['currency']})\nПоследние пополнения:"

        for payment in payments:
            dateptime = datetime.strptime(
                payment['date'], "%Y-%m-%dT%H:%M:%S+03:00")
            date = f"{dateptime.time()} {dateptime.date()}"

            currency = " RUB" if payment['sum'][
                'currency'] == 643 else f"({payment['sum']['currency']})"
            last_payments += f"\n{payment['sum']['amount']}{currency} - {payment['comment']} \
				{payment['account']} | {date}"

        await query.message.answer(last_payments)


@dp.message_handler(Text(startswith="ворк", ignore_case=True), state=AdminPanel.main)
async def parse_admin_panel(message: types.Message):
    """
    Стейт с воркерами
    """
    if check_admin(message.chat.id):
        await message.answer("Действия с воркерами...", reply_markup=admin_work_keyboard)
        await AdminPanel.workers.set()


@dp.message_handler(Text(startswith="добав", ignore_case=True), state=AdminPanel.workers)
async def admin_workers_add(message: types.Message):
    """
    Стейт с воркерами - добавить воркера
    """
    if check_admin(message.chat.id):
        await message.answer("Введите id воркера: ")
        await AdminPanel.workers_add.set()


@dp.message_handler(lambda message: not message.text.isdigit(), state=AdminPanel.workers_add)
async def procces_new_worker_invalid(message: types.Message):
    if check_admin(message.chat.id):
        logger.debug(f"#{message.text} not valid id")
        await message.reply("Id, должен состоять из чисел.")


@dp.message_handler(lambda mes: mes.text.isdigit(), state=AdminPanel.workers_add)
async def procces_new_worker(message: types.Message):
    """
    Добавления воркера - ставим воркер статус
    """
    if check_admin(message.chat.id):
        try:
            user = User.get(cid=message.text)
            user.worker = True
            user.save()
        except User.DoesNotExist:
            User.create(cid=message.text, worker=True)
        finally:
            logger.info(f"#{message.text} - became new worker")
            await message.answer(f"{message.text} - Успешно назначен воркером",
                                 reply_markup=admin_work_keyboard)
            await AdminPanel.workers.set()


@dp.message_handler(Text(startswith="удал", ignore_case=True), state=AdminPanel.workers)
async def admin_workers_del(message: types.Message):
    """
    Удаление воркера
    """
    if check_admin(message.chat.id):
        await message.answer("Введите id воркера: ")
        await AdminPanel.workers_delete.set()


@dp.message_handler(lambda message: not message.text.isdigit(), state=AdminPanel.workers_delete)
async def procces_del_worker_invalid(message: types.Message):
    if check_admin(message.chat.id):
        logger.debug(f"#{message.text} not valid id")
        await message.reply("Id, должен состоять из чисел.")


@dp.message_handler(lambda mes: mes.text.isdigit(), state=AdminPanel.workers_delete)
async def procces_del_worker(message: types.Message):
    """
    Убираем воркер статус в базе данных
    """
    if check_admin(message.chat.id):
        try:
            user = User.get(cid=message.text)
            user.worker = False
            user.save()
            logger.info(f"#{message.text} - deleted from workers")
            await message.answer(f"{message.text} - Успешно удален из воркеров",
                                 reply_markup=admin_work_keyboard)
        except User.DoesNotExist:
            User.create(cid=message.text, worker=False)

# User.select().order_by(User.id.desc())


@dp.message_handler(Text(startswith="посл", ignore_case=True), state=AdminPanel.main)
async def last_users(message: types.Message):
    if check_admin(message.chat.id):
        users = User.select().order_by(User.id.desc())
        text = "Последние юзеры:\n"

        for i in range(PAY_ROWS):
            try:
                user = users[i]
                text += f"\n{user.username} {user.balance} #{user.cid}:{user.id}"
            except IndexError:
                break

        await message.answer(text, reply_markup=admin_keyboard)


@dp.message_handler(Text(startswith="оповещ", ignore_case=True), state=AdminPanel.main)
async def notify_all(message: types.Message, state: FSMContext):
    if check_admin(message.chat.id):
        await message.answer("Введите текст для оповещения")
        await AdminPanel.notify.set()


@dp.message_handler(state=AdminPanel.notify)
async def notify_sure(message: types.Message, state: FSMContext):
    if check_admin(message.chat.id):
        await message.answer(f"{message.text}", reply_markup=notify_keyboard)
        async with state.proxy() as data:
            data['msg'] = message.text
        await AdminPanel.notify_sure.set()


@dp.callback_query_handler(text="sure", state=AdminPanel.notify_sure)
async def admin_down(query: types.CallbackQuery, state: FSMContext):
    if check_admin(query.message.chat.id):
        async with state.proxy() as data:
            data['msg']
            await query.message.edit_text("Рассылка пошла\nСообщений отправлено: <b>0</b>")

            msges = 0
            for user in User.select().order_by(User.id.desc()):
                try:
                    await dp.bot.send_message(user.cid, data['msg'])
                    logger.debug(f"send message to {user.cid}")
                    msges += 1
                    await query.message.edit_text(f"Рассылка пошла\nСообщений отправлено: <b>{msges}</b>")
                    await sleep(0.15)
                except Exception:
                    logger.debug("Чат с пользователем не найден")


@dp.callback_query_handler(lambda cb: cb.data.split("_")[0] == "sure", state="*")
async def admin_down(query: types.CallbackQuery):
    if check_admin(query.message.chat.id):
        await query.message.edit_text(query.message.text + "\nТы даун")
