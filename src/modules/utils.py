from telebot import types
import logging
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))
from db.card_manager import CardManager
from db.library_manager import LibraryManager
from src.constants.reponce_items import Msg, ButtonText, LoggerText, AdditionalItems


logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
handler = logging.StreamHandler()
formatter = logging.Formatter('%(asctime)s – %(message)s',
                              datefmt=LoggerText.TIME_FORMAT)
handler.setFormatter(formatter)
logger.addHandler(handler)

library = LibraryManager()
cards = CardManager()


def handler_show_user_card(message, bot):
    logger.info(LoggerText.SHOW_CARD.format(
        message.from_user.id
    ))
    show_card(message, bot)


def handler_back_to_main_menu(message, bot):
    logger.info(LoggerText.BACK_TO_MAIN_MENU_HANDLER.format(
        message.from_user.id
    ))
    bot.send_message(message.chat.id,
                     Msg.IN_MAIN,
                     reply_markup=main_menu(message))


def handler_search_book(message, bot):
    logger.info(LoggerText.SEARCH_BOOK_HANDLER.format(
        message.from_user.id
    ))
    show_subjects(message, bot)


def dinamic_handler_choose_variable(message, bot):
    logger.info(LoggerText.SELECT_VARIABLE.format(
        message.from_user.id
    ))
    subject = message.text
    show_search_options(message, subject, bot)
    return subject


def dinamic_handler_show_authors(message,
                                 bot,
                                 subject):
    logger.info(LoggerText.SELECT_AUTHOR.format(
        message.from_user.id
    ))
    show_authors(message, subject, bot)


def dinamic_handler_show_name(message,
                              bot,
                              subject):
    logger.info(LoggerText.SELECT_NAME.format(
        message.from_user.id
    ))
    show_books_by_subject(message, subject, bot)


def dinamic_handler_show_subject_author(message,
                                        bot,
                                        subject):
    author = message.text
    logger.info(LoggerText.CHOOSE_AUTHOR.format(
        message.from_user.id
    ))
    show_books_by_author(message,
                         author,
                         subject,
                         bot)

def dinamic_handler_book_details(message, bot):
    logger.info(LoggerText.CHOOSE_NAME.format(
        message.from_user.id
    ))
    book_name = message.text
    show_book_details(message, book_name, bot)


def dinamic_handler_back_to_menu(message, bot):
    logger.info(LoggerText.RETURN.format(
        message.from_user.id
    ))
    bot.send_message(message.chat.id,
                     Msg.IN_MAIN,
                     reply_markup=main_menu(message))


def main_menu(message):
    markup = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
    btn1 = types.KeyboardButton(ButtonText.SHOW_USER_CARD)
    btn2 = types.KeyboardButton(ButtonText.SEARCH_BOOK)
    markup.add(btn1, btn2)
    logger.info(LoggerText.MAIN.format(message.from_user.id))
    return markup


def back_to_main_menu(message):
    markup = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
    btn = types.KeyboardButton(ButtonText.BACK_TO_MAIN_MENU)
    markup.add(btn)
    logger.info(LoggerText.BACK_TO_MAIN_MENU.format(message.from_user.id))
    return markup


def show_card(message, bot):
    tg_id = message.from_user.id
    user_books = cards.get_books_by_tg_id(tg_id)
    logger.info(LoggerText.GET_BOOKS.format(message.from_user.id))
    response = Msg.SHOW_CARD.format(message.from_user.first_name,
                                    message.from_user.last_name or '')
    if user_books:
        for subject, books in user_books.items():
            response += f"{subject}:\n"
            for book in books:
                response += f"  {book['author']}\n    {book['name']}\n"
    else:
        response = Msg.SHOW_EMPTY_CARD
    bot.send_message(message.chat.id,
                     response,
                     reply_markup=back_to_main_menu(message))


def show_subjects(message, bot):
    subjects = library.get_all_subjects()
    markup = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
    logger.info(LoggerText.CHOOSE_SUBJECT.format(message.from_user.id))
    for subject in subjects:
        markup.add(types.KeyboardButton(subject))
    markup.add(types.KeyboardButton(ButtonText.BACK_TO_MAIN_MENU))
    bot.send_message(message.chat.id,
                     Msg.SUBJECT,
                     reply_markup=markup)


def show_books_by_subject(message, subject, bot):
    books = library.search_library(subject=subject)
    markup = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
    logger.info(LoggerText.SUBJECT_BOOKS.format(subject,
                                                message.from_user.id))
    book_names = set()
    for book in books:
        if book['name'] not in book_names:
            markup.add(types.KeyboardButton(book['name']))
            book_names.add(book['name'])
    markup.add(types.KeyboardButton(ButtonText.BACK_TO_MAIN_MENU))
    bot.send_message(message.chat.id,
                     Msg.SUBJECT_BOOKS.format(subject),
                     reply_markup=markup)


def show_search_options(message, subject, bot):
    markup = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
    logger.info(LoggerText.SEARCH_VARIABLE.format(subject,
                                                  message.from_user.id))
    markup.add(types.KeyboardButton(ButtonText.SEARCH_BY_AUTHOR),
               types.KeyboardButton(ButtonText.SEARCH_BY_NAME))
    markup.add(types.KeyboardButton(ButtonText.BACK_TO_MAIN_MENU))
    bot.send_message(message.chat.id,
                     Msg.SUBJECT_SEARCH_OPTIONS.format(subject),
                     reply_markup=markup)


def show_authors(message, subject, bot):
    authors = library.get_authors_by_subject(subject)
    logger.info(LoggerText.SEARCH_BY_AUTHOR.format(subject,
                                                   message.from_user.id))
    markup = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
    for author in authors:
        markup.add(types.KeyboardButton(author))
    markup.add(types.KeyboardButton(ButtonText.BACK_TO_MAIN_MENU))
    bot.send_message(message.chat.id,
                     Msg.SUBJECT_AUTHORS.format(subject),
                     reply_markup=markup)


def show_books_by_author(message, author, subject, bot):
    books = library.search_library(author=author, subject=subject)
    logger.info(LoggerText.SEARCH_BOOK_BY_SUBJECT_N_AUTHOR.format(
        subject,
        author,
        message.from_user.id
    ))
    markup = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
    book_names = set()
    for book in books:
        if book['name'] not in book_names:
            markup.add(types.KeyboardButton(book['name']))
            book_names.add(book['name'])
    markup.add(types.KeyboardButton(ButtonText.BACK_TO_MAIN_MENU))
    bot.send_message(message.chat.id,
                     Msg.SUBJECT_AUTHORS_BOOKS.format(author, subject),
                     reply_markup=markup)


def show_book_details(message, book_name, bot):
    book = library.search_library(name=book_name)
    logger.info(LoggerText.BOOK_DETAILS.format(
        book_name,
        message.from_user.id
    ))
    if book:
        book = book[0]
        response = Msg.BOOK_DETAILS.format(book['name'],
                                           book['author'],
                                           book['source'])
        bot.send_message(message.chat.id, response, reply_markup=main_menu(message))
        add_book_to_user_card(message.from_user.id,
                              book_name,
                              book['author'],
                              book['subject'])
    else:
        bot.send_message(message.chat.id,
                         Msg.BOOK_NOT_FOUND,
                         reply_markup=back_to_main_menu(message))


def add_book_to_user_card(tg_id, book_name, author, subject):
    logger.info(LoggerText.USER_CHOOSING.format(
        tg_id,
        subject,
        book_name,
        author
    ))
    cards.add_book_info(tg_id, subject, book_name, author)


def get_all_authors():
    authors_cache = {}
    if 'authors' not in authors_cache:
        authors_cache['authors'] = library.get_all_authors()
    return authors_cache['authors']
