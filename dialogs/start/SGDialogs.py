import logging

from aiogram import Router
from aiogram.types import ContentType, Message
from aiogram.filters import CommandStart
from aiogram_dialog import Dialog, DialogManager, Window, StartMode
from aiogram_dialog.widgets.media import StaticMedia, DynamicMedia
from aiogram_dialog.widgets.text import Const, Format
from aiogram_dialog.widgets.kbd import Back, SwitchTo, Row, Url, Column, Button
from aiogram_dialog.widgets.input import TextInput, MessageInput

from FSMcontext.fsm_machine import startSG
from dialogs.start.getters import menu_menu, menu_terms, menu_balance, menu_wallet, menu_tasks, menu_rewards, get_reward, add_wallet, error_handler, no_text


logger = logging.getLogger(__name__)
logger.warning(msg='Start dialogs')


def text_check(text: str):
    return text



start_dialog = Dialog(
    Window(
        Format('{text}'),
        DynamicMedia('image'),
        Row(
            SwitchTo(Format('{terms}'), id='terms', state=startSG.terms),
            SwitchTo(Format('{balance}'), id='balance', state=startSG.balance)
        ),
        Row(
            SwitchTo(Format('{wallet}'), id='wallet', state=startSG.wallet),
            SwitchTo(Format('{tasks}'), id='tasks', state=startSG.tasks)
        ),
        SwitchTo(Format('{rewards}'), id='daily_rewards', state=startSG.rewards),
        getter=menu_menu,
        state=startSG.start
    ),
    Window(
        Format('{text}'),
        DynamicMedia('image'),
        SwitchTo(Format('{back}'), id='back', state=startSG.start),
        getter=menu_terms,
        state=startSG.terms
    ),
    Window(
        Format('{text}'),
        DynamicMedia('image'),
        Column(
            Url(Format('{url_text}'), url=Format('{link}')),
            SwitchTo(Format('{back}'), id='back', state=startSG.start)
        ),
        getter=menu_balance,
        state=startSG.balance
    ),
    Window(
        Format('{text}'),
        DynamicMedia('image'),
        TextInput(
            id='address_input',
            type_factory=text_check,
            on_success=add_wallet,
            on_error=error_handler,
        ),
        MessageInput(
            func=no_text,
            content_types=ContentType.ANY
        ),
        SwitchTo(Format('{back}'), id='back', state=startSG.start),
        getter=menu_wallet,
        state=startSG.wallet
    ),
    Window(
        Format('{text}'),
        DynamicMedia('image'),
        SwitchTo(Format('{back}'), id='back', state=startSG.start),
        getter=menu_tasks,
        state=startSG.tasks
    ),
    Window(
        Format('{text}'),
        DynamicMedia('image'),
        Button(
            text=Format('{reward}'),
            id='get_reward',
            on_click=get_reward
        ),
        SwitchTo(Format('{back}'), id='back', state=startSG.start),
        getter=menu_rewards,
        state=startSG.rewards
    )
)
