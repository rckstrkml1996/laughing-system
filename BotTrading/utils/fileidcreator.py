from loader import dp


from aiogram.types.input_file import InputFile


async def file_ids():
    for file_name in photos:
        message = await dp.bot.send_photo(config.admins_id[0], InputFile(photos[file_name]))
        file_id = message.photo[-1].file_id
        photos[file_name] = file_id
