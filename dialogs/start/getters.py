import random
import datetime

from aiogram.types import User, CallbackQuery, Message, ContentType
from aiogram_dialog import DialogManager
from aiogram_dialog.widgets.kbd import Button
from aiogram_dialog.widgets.input import ManagedTextInput, MessageInput
from aiogram_dialog.widgets.media import DynamicMedia
from aiogram_dialog.api.entities import MediaId, MediaAttachment
from fluentogram import TranslatorRunner

from database.db_conf import database
from utils.date_functions import get_state


db = database('users_database')


async def menu_menu(dialog_manager: DialogManager, i18n: TranslatorRunner, **kwargs):
    image_id = "AgACAgIAAxkBAAMNZln8EDymC3G4Abrr5ZQme-oJdbMAAunYMRsHbtBKMH02Pj1V-6IBAAMCAAN5AAM1BA"  # Your file_id
    image = MediaAttachment(ContentType.PHOTO, file_id=MediaId(image_id))
    return {'text': i18n.menu.menu(),
            'terms': i18n.button.terms(),
            'balance': i18n.button.balance(),
            'wallet': i18n.button.wallet(),
            'tasks': i18n.button.tasks(),
            'rewards': i18n.button.rewards(),
            'image': image}


async def menu_terms(dialog_manager: DialogManager, i18n: TranslatorRunner, event_from_user: User, **kwargs):
    image_id = "AgACAgIAAxkBAAMPZln8FOVBYHG01KauKJ5FHA5dE5oAAurYMRsHbtBKrTYErnGh2h0BAAMCAAN5AAM1BA"  # Your file_id
    image = MediaAttachment(ContentType.PHOTO, file_id=MediaId(image_id))
    return {'text': i18n.get('menu-terms', deeplink=db.get_deeplink(event_from_user.id)),
            'back': i18n.button.back(),
            'image': image}


async def menu_balance(dialog_manager: DialogManager, i18n: TranslatorRunner, event_from_user: User,  **kwargs):
    image_id = "AgACAgIAAxkBAAMVZln8H6EdNd4WElHgUnmK_NYMOEAAAu7YMRsHbtBKIgtLzA2RBAcBAAMCAAN5AAM1BA"  # Your file_id
    image = MediaAttachment(ContentType.PHOTO, file_id=MediaId(image_id))
    return {'text': i18n.get('menu-balance', balance=db.get_balance(event_from_user.id)),
            'url_text': i18n.button.invite(),
            'link': 'https://t.me/share/url?url=' + db.get_deeplink(event_from_user.id),
            'back': i18n.button.back(),
            'image': image}


async def menu_wallet(dialog_manager: DialogManager, i18n: TranslatorRunner, **kwargs):
    image_id = "AgACAgIAAxkBAAMTZln8G9WhFB0b_EEJZxCQt_4xvQYAAu3YMRsHbtBKbc_N2rJQu80BAAMCAAN5AAM1BA"  # Your file_id
    image = MediaAttachment(ContentType.PHOTO, file_id=MediaId(image_id))
    return {'text': i18n.menu.wallet(),
            'back': i18n.button.back(),
            'image': image}


async def menu_tasks(dialog_manager: DialogManager, i18n: TranslatorRunner, **kwargs):
    image_id = "AgACAgIAAxkBAAMZZln89UHcCo3eMvRhx5u_mmp_VLAAAvLYMRsHbtBKCkl_NoLuTjABAAMCAAN5AAM1BA"  # Your file_id
    image = MediaAttachment(ContentType.PHOTO, file_id=MediaId(image_id))
    return {'text': i18n.menu.tasks(),
            'back': i18n.button.back(),
            'image': image}


async def menu_rewards(dialog_manager: DialogManager, i18n: TranslatorRunner, **kwargs):
    image_id = "AgACAgIAAxkBAAMRZln8F3D9YCIaGD16zrQ2NAMS0BoAAuvYMRsHbtBKwhV9WFhM138BAAMCAAN5AAM1BA"  # Your file_id
    image = MediaAttachment(ContentType.PHOTO, file_id=MediaId(image_id))
    return {'text': i18n.menu.rewards(),
            'reward': i18n.reward.button(),
            'back': i18n.button.back(),
            'image': image}

async def get_reward(clb: CallbackQuery, button: Button, dialog_manager: DialogManager):
    i18n: TranslatorRunner = dialog_manager.middleware_data.get('i18n')
    if get_state(user_id=clb.from_user.id, db=db):
        db.update_balance_without_deeplink(user_id=clb.from_user.id, balance=random.randint(20, 100))
        db.update_data(user_id=clb.from_user.id, data=str(datetime.date.today()))
        await clb.answer(text=i18n.reward.yes())
    else:
        await clb.answer(text=i18n.reward.no())


async def add_wallet(message: Message, widget: ManagedTextInput, dialog_manager: DialogManager, text: str):
    i18n: TranslatorRunner = dialog_manager.middleware_data.get('i18n')
    db.update_wallet(user_id=message.from_user.id, wallet_adress=text)
    await message.answer(text=i18n.get('wallet-correct', adress=text))

async def error_handler(message: Message, widget: ManagedTextInput, dialog_manager: DialogManager, error: ValueError):
    i18n: TranslatorRunner = dialog_manager.middleware_data.get('i18n')
    await message.answer(text=i18n.wallet.incorrect())

async def no_text(message: Message, widget: MessageInput, dialog_manager: DialogManager):
    i18n: TranslatorRunner = dialog_manager.middleware_data.get('i18n')
    await message.answer(text=i18n.wallet.incorrect())