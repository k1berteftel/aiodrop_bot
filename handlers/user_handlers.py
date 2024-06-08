import logging

from aiogram import Router, F, Bot
from aiogram.types import Message, CallbackQuery, InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.filters import CommandStart, or_f, CommandObject
from aiogram_dialog import DialogManager, StartMode
from fluentogram import TranslatorRunner

from FSMcontext.fsm_machine import startSG
from utils.moduls import sub_check, add_refferal, get_random_deeplink
from database.db_conf import database

logger = logging.getLogger(__name__)

db = database('users_database')
chat_id = '-1002075409660'
user_router = Router()

@user_router.message(CommandStart())
async def start_dialog(msg: Message, bot: Bot, command: CommandObject, dialog_manager: DialogManager, i18n: TranslatorRunner):
    if not db.check_user(user_id=msg.from_user.id):
        args = command.args
        if args:
            add_refferal(deeplink=args, db=db)
        db.add_user(user_id=msg.from_user.id, deep_link=get_random_deeplink(db=db))
        button = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text=i18n.button.sub(), callback_data='check_sub')]])
        await msg.answer(text=i18n.sub.hello(), reply_markup=button)
    else:
        await dialog_manager.start(state=startSG.start, mode=StartMode.RESET_STACK)

# subscribe = sub_check(await bot.get_chat_member(chat_id=chat_id, user_id=msg.from_user.id))
@user_router.callback_query(F.data == 'check_sub')
async def check_sub(clb: CallbackQuery, bot: Bot, dialog_manager: DialogManager, i18n: TranslatorRunner):
    if sub_check(await bot.get_chat_member(chat_id=chat_id, user_id=clb.from_user.id)):
        await dialog_manager.start(state=startSG.start, mode=StartMode.RESET_STACK)
    else:
        await clb.answer(text=i18n.sub.again())

@user_router.message(F.photo)
async def get_photo(message: Message):
    await message.answer(text=message.photo[-1].file_id)
