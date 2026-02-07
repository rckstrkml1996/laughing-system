from aiogram import types
from aiogram.dispatcher import FSMContext

from loader import dp, config
from data import texts, keyboards
from data.states import NewQiwi
from qiwiapi import Qiwi, UnexpectedResponse
from customutils import save_config
from customutils.config import Qiwi as ConfigQiwi


async def qiwi_command_wrapper():
    qiwi_acc_texts = []
    all_balance = 0
    wallets = []
    for qiwi_obj in config.qiwis:
        qiwi = Qiwi(
            token=qiwi_obj.token,
            wallet=qiwi_obj.wallet,
            proxy_url=qiwi_obj.proxy_url,
        )
        accounts = await qiwi.get_accounts()
        wallets.append(qiwi.wallet)
        amount = accounts[0].balance.amount
        currency = accounts[0].currency
        qiwi_acc_texts.append(
            texts.qiwi_account_text.format(
                number=qiwi.wallet, amount=amount, currency=Qiwi.get_currency(currency)
            )
        )
        if currency == 643:
            all_balance += amount
    # text, markup
    return texts.qiwi_tokens_info_text.format(
        qiwi_account_texts="\n".join(qiwi_acc_texts), all_amounts=all_balance
    ), keyboards.qiwi_keyboard(wallets)


@dp.message_handler(commands=["qiwi"], state="*", admins_chat=True, is_admin=True)
async def qiwi_command(message: types.Message, state: FSMContext):
    await state.finish()
    await message.reply(texts.qiwi_emoji)
    if config.qiwis:
        text, markup = await qiwi_command_wrapper()
        await message.answer(text, reply_markup=markup)
    else:
        await message.answer(
            texts.no_qiwis_text, reply_markup=keyboards.qiwi_keyboard()
        )


@dp.callback_query_handler(text="backqiwi", state="*", admins_chat=True, is_admin=True)
async def qiwi_command_back(query: types.CallbackQuery):
    await query.answer(texts.qiwi_emoji)
    if config.qiwis:
        text, markup = await qiwi_command_wrapper()
        await query.message.edit_text(text, reply_markup=markup)
    else:
        await query.message.edit_text(
            texts.no_qiwis_text, reply_markup=keyboards.qiwi_keyboard()
        )


@dp.callback_query_handler(
    lambda cb: cb.data.split("_")[0] == "qiwidelete",
    state="*",
    admins_chat=True,
    is_admin=True,
)
async def qiwi_delete(query: types.CallbackQuery):
    qiwi_num = int(query.data.split("_")[1])
    qiwi_obj = config.qiwis[qiwi_num]
    config.qiwis.pop(qiwi_num)
    save_config(config)
    await query.answer("Удалил!", show_alert=True)
    await qiwi_command_back(query)


@dp.callback_query_handler(
    lambda cb: cb.data.split("_")[0] == "qiwi", admins_chat=True, is_admin=True
)
async def qiwi_info(query: types.CallbackQuery):
    await query.answer("Выполняю!")
    qiwi_num = int(query.data.split("_")[1])
    qiwi_obj = config.qiwis[qiwi_num]
    qiwi = Qiwi(
        token=qiwi_obj.token,
        wallet=qiwi_obj.wallet,
        proxy_url=qiwi_obj.proxy_url,
    )
    try:
        accounts = await qiwi.get_accounts()
        profile = await qiwi.get_profile()
        history = await qiwi.get_payments(
            rows=6, operation=Qiwi.ALL
        )  # get 6 last payments
        qiwi_action_texts = []
        for transaction in history.data:
            transaction_type = "+" if transaction.trnsType == "IN" else "-"
            qiwi_action_texts.append(
                texts.qiwi_action_text.format(
                    going=f"{transaction_type}{transaction.trns_sum.amount}",
                    currency=Qiwi.get_currency(transaction.trns_sum.currency),
                    comment=transaction.comment,
                )
            )
        amount = accounts[0].balance.amount
        currency = accounts[0].currency
        await query.message.edit_text(
            texts.qiwi_info_text.format(
                number=qiwi.wallet,
                amount=amount,
                currency=Qiwi.get_currency(currency),
                status=Qiwi.get_identification_level(
                    profile.contractInfo.identificationInfo[-1].identificationLevel
                ),
                proxy="Есть" if qiwi.proxy else "Нету",
                qiwi_action_texts="\n".join(qiwi_action_texts),
            ),
            reply_markup=keyboards.qiwi_info_keyboard(qiwi_num),
        )
    finally:
        await qiwi.close()


@dp.callback_query_handler(text="qiwiadd", admins_chat=True, is_admin=True)
async def qiwi_add(query: types.CallbackQuery):
    await query.message.edit_text(texts.qiwi_to_bot_text)
    await dp.bot.send_message(
        query.from_user.id,
        texts.wanna_add_qiwi_text,
        reply_markup=keyboards.qiwi_keyboard(),
    )


@dp.callback_query_handler(text="qiwiadd", is_admin=True)  # in bot chat
async def qiwi_add_in_bot(query: types.CallbackQuery):
    await query.message.edit_text(
        texts.add_qiwi_text, reply_markup=keyboards.qiwi_add_cancel_keyboard
    )
    await NewQiwi.main.set()


@dp.callback_query_handler(text="qiwiaddcancel", state="*", admins_chat=True)
@dp.callback_query_handler(text="qiwiaddcancel", state="*", admins_chat=False)
async def qiwi_add_cancel(query: types.CallbackQuery, state: FSMContext):
    await state.finish()
    await query.message.edit_text(texts.add_qiwi_cancel_text)


@dp.message_handler(state=NewQiwi.main, is_admin=True)
async def qiwi_add_value(message: types.Message, state: FSMContext):
    payload = message.text.split("\n")
    if len(payload) < 2:
        await message.answer(
            texts.invalid_newqiwi_text, reply_markup=keyboards.qiwi_add_cancel_keyboard
        )

    token = payload[0]
    public_key = payload[1]

    if token in map(lambda qw: qw.token, config.qiwis):
        await message.answer(
            texts.qiwi_already_exists_text,
            reply_markup=keyboards.qiwi_add_cancel_keyboard,
        )
        return

    proxy_url = None
    if len(payload) >= 3:
        proxy_url = payload[2]

    try:
        Qiwi.validate(token, proxy_url)
        qiwi = Qiwi(token, proxy_url=proxy_url)

        if proxy_url:
            msg = await message.answer(texts.qiwi_checking_proxy_text.format(timeout=3))
            proxy_valid = await qiwi.check_proxy(3)  # timeout

            if not proxy_valid:
                await msg.edit_text(texts.qiwi_checking_proxy_invalid_text)
                await qiwi.close()
                await state.finish()
                return
            await msg.edit_text(texts.qiwi_checking_proxy_valid_text)

        try:
            profile = await qiwi.get_profile()
        except UnexpectedResponse:
            await message.answer(texts.qiwi_invalid_token_text)
            await qiwi.close()
            await state.finish()
            return
        await qiwi.close()

        wallet = profile.contractInfo.contractId
        config.qiwis.append(
            ConfigQiwi(
                token=token, proxy_url=proxy_url, wallet=wallet, public_key=public_key
            )
        )
        save_config(config)
        await message.answer(texts.valid_newqiwi_text.format(number=wallet))
        text, markup = await qiwi_command_wrapper()
        await dp.bot.send_message(config.admins_chat, text, reply_markup=markup)
        await state.finish()
    except ValueError:  # raises in Qiwi.validate, if wrong token or proxy format
        await message.answer(
            texts.invalid_newqiwi_text, reply_markup=keyboards.qiwi_add_cancel_keyboard
        )
