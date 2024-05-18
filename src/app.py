import telebot
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from src.crutch.fill_table import fill_from_excel
from configuration import TOKEN
from modules.utils import *


api_token = TOKEN
bot = telebot.TeleBot(api_token)

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
handler = logging.StreamHandler()
formatter = logging.Formatter('%(asctime)s – %(message)s',
                              datefmt=LoggerText.TIME_FORMAT)
handler.setFormatter(formatter)
logger.addHandler(handler)

library = LibraryManager()
cards = CardManager()

search = {ButtonText.SEARCH_BY_AUTHOR, ButtonText.SEARCH_BY_NAME}
show_function = {
    ButtonText.SEARCH_BY_AUTHOR: dinamic_handler_show_authors,
    ButtonText.SEARCH_BY_NAME: dinamic_handler_show_name,
    AdditionalItems.SUBJECT_AUTHOR: dinamic_handler_show_subject_author
}


@bot.message_handler(commands=['start'])
def send_welcome(message):
    logger.info(LoggerText.START_CHAT.format(
        message.from_user.id
    ))
    bot.send_message(message.chat.id,
                     Msg.WELCOME,
                     reply_markup=main_menu(message))


@bot.message_handler(func=lambda message: True)
def handle_buttons(message):
    if message.text == ButtonText.SHOW_USER_CARD:
        handler_show_user_card(message, bot)
    elif message.text == ButtonText.BACK_TO_MAIN_MENU:
        handler_back_to_main_menu(message,bot)
    elif message.text == ButtonText.SEARCH_BOOK:
        handler_search_book(message, bot)
    else:
        handle_dynamic_buttons(message)


def handle_dynamic_buttons(message):
    tg_id = message.from_user.id
    subjects = library.get_all_subjects()
    authors = get_all_authors()

    msg = message.text
    if msg in subjects:
        subject = dinamic_handler_choose_variable(message,
                                                  bot)
        cards.set_subject(tg_id, subject)
    elif msg in search or msg in authors:
        func = msg
        if show_function.get(msg) is None:
            func = AdditionalItems.SUBJECT_AUTHOR
        subject = cards.get_subject_by_tg_id(tg_id)
        show_func = show_function.get(func)
        try:
            show_func(message, bot, subject)
        except Exception as e:
            logger.error(e)
    else:
        dinamic_handler_book_details(message, bot)
    if msg == ButtonText.BACK_TO_MAIN_MENU:
        dinamic_handler_back_to_menu(message, bot)


if __name__ == "__main__":
    fill_from_excel()
    logger.info(LoggerText.LOAD_DATA)
    try:
        bot.polling(none_stop=True)
    except Exception as e:
        logger.error(e)
