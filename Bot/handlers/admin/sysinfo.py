from aiogram import types
from aiogram.utils.exceptions import MessageNotModified

import psutil
from time import time

from loader import dp
from data import payload
from data.keyboards import update_sysinfo_keyboard
from utils.systeminfo import cpu_usage
from utils.executional import get_correct_str


@dp.message_handler(commands="sysinfo", admins_type=True)
async def system_info_command(message: types.Message):
    a = time()
    memory = psutil.virtual_memory()
    memory_percent = memory.percent
    memory_amount = '{:.2f}'.format(memory.total / 1024 / 1024)

    work_time = get_correct_str(
        round((time() - psutil.boot_time()) / 60 / 60, 2),
        "час", "часа", "часов"
    )

    await message.answer(payload.sys_info_text.format(
        cpu_count=psutil.cpu_count(),
        ram_count=memory_amount,
        ram_usage=memory_percent,
        cpu_usage=cpu_usage['usage'],
        computer_work=work_time
    ), reply_markup=update_sysinfo_keyboard)

    print(time() - a)


@ dp.callback_query_handler(text="update_sys", admins_type=True)
async def update_system_info(query: types.CallbackQuery):
    a = time()
    memory = psutil.virtual_memory()
    memory_percent = memory.percent
    memory_amount = '{:.2f}'.format(memory.total / 1024 / 1024)

    work_time = get_correct_str(
        round((time() - psutil.boot_time()) / 60 / 60, 2),
        "час", "часа", "часов"
    )

    try:
        await query.message.edit_text(payload.sys_info_text.format(
            cpu_count=psutil.cpu_count(),
            ram_count=memory_amount,
            ram_usage=memory_percent,
            cpu_usage=cpu_usage['usage'],
            computer_work=work_time
        ), reply_markup=update_sysinfo_keyboard)
    except MessageNotModified:
        pass

    print(time() - a)
