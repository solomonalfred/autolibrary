import telebot
from configuration import TOKEN
from db.card_manager import CardManager
from db.library_manager import LibraryManager
from telebot import types
from src.crutch.fill_table import fill_from_excel

api_token = TOKEN
bot = telebot.TeleBot(api_token)

library = LibraryManager()
cards = CardManager()

user_states = {}

# Главное меню
def main_menu():
    markup = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
    btn1 = types.KeyboardButton('Посмотреть карточку читателя')
    btn2 = types.KeyboardButton('Найти книгу')
    markup.add(btn1, btn2)
    return markup

# Вернуться в главное меню
def back_to_main_menu():
    markup = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
    btn = types.KeyboardButton('Вернуться в главное меню')
    markup.add(btn)
    return markup

# Обработка команды /start
@bot.message_handler(commands=['start'])
def send_welcome(message):
    fill_from_excel()
    bot.send_message(message.chat.id, "Добро пожаловать!", reply_markup=main_menu())

# Обработка нажатий кнопок
@bot.message_handler(func=lambda message: True)
def handle_buttons(message):
    if message.text == 'Посмотреть карточку читателя':
        show_card(message)
    elif message.text == 'Вернуться в главное меню':
        bot.send_message(message.chat.id, "Вы в главном меню", reply_markup=main_menu())
    elif message.text == 'Найти книгу':
        show_subjects(message)
    else:
        handle_dynamic_buttons(message)

# Показать карточку читателя
def show_card(message):
    tg_id = message.from_user.id
    user_books = cards.get_books_by_tg_id(tg_id)
    response = f"Книги которые прочитал: {message.from_user.first_name} {message.from_user.last_name or ''}\n"
    if user_books:
        for subject, books in user_books.items():
            response += f"{subject}:\n"
            for book in books:
                response += f"  {book['author']}\n    {book['name']}\n"
    else:
        response = "Вы пока нечего не выбирали"
    bot.send_message(message.chat.id, response, reply_markup=back_to_main_menu())

def show_subjects(message):
    subjects = library.get_all_subjects()
    markup = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
    for subject in subjects:
        markup.add(types.KeyboardButton(subject))
    markup.add(types.KeyboardButton('Вернуться в главное меню'))
    bot.send_message(message.chat.id, "Выберите тематику:", reply_markup=markup)


def handle_dynamic_buttons(message):
    tg_id = message.from_user.id
    if tg_id not in user_states:
        user_states[tg_id] = {}

    subjects = library.get_all_subjects()
    authors = get_all_authors()

    if message.text in subjects:
        subject = message.text
        user_states[tg_id]['subject'] = subject
        show_search_options(message, subject)
    elif message.text == 'Искать по автору':
        subject = user_states[tg_id].get('subject')
        if subject:
            show_authors(message, subject)
        else:
            bot.send_message(message.chat.id, "Ошибка: Тематика не определена. Пожалуйста, выберите тематику заново.",
                             reply_markup=main_menu())
    elif message.text == 'Искать по названию':
        subject = user_states[tg_id].get('subject')
        if subject:
            show_books_by_subject(message, subject)
        else:
            bot.send_message(message.chat.id, "Ошибка: Тематика не определена. Пожалуйста, выберите тематику заново.",
                             reply_markup=main_menu())
    elif message.text in authors:
        author = message.text
        subject = user_states[tg_id].get('subject')
        if subject:
            show_books_by_author(message, author, subject)
        else:
            bot.send_message(message.chat.id, "Ошибка: Тематика не определена. Пожалуйста, выберите тематику заново.",
                             reply_markup=main_menu())
    else:
        books = library.search_library(name=message.text)
        if books:
            book_name = message.text
            show_book_details(message, book_name)
        else:
            bot.send_message(message.chat.id, "Неизвестная команда. Пожалуйста, выберите действительную опцию.",
                             reply_markup=main_menu())
    if message.text == 'Вернуться в главное меню':
        bot.send_message(message.chat.id, "Вы в главном меню", reply_markup=main_menu())


def show_books_by_subject(message, subject):
    books = library.search_library(subject=subject)
    markup = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
    book_names = set()
    for book in books:
        if book['name'] not in book_names:
            markup.add(types.KeyboardButton(book['name']))
            book_names.add(book['name'])
    markup.add(types.KeyboardButton('Вернуться в главное меню'))
    bot.send_message(message.chat.id, f"Книги по тематике '{subject}':", reply_markup=markup)

# Показать опции поиска
def show_search_options(message, subject):
    markup = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
    markup.add(types.KeyboardButton(f'Искать по автору'), types.KeyboardButton(f'Искать по названию'))
    markup.add(types.KeyboardButton('Вернуться в главное меню'))
    bot.send_message(message.chat.id, f"Выберите способ поиска по тематике '{subject}':", reply_markup=markup)


# Показать авторов по тематике
def show_authors(message, subject):
    authors = library.get_authors_by_subject(subject)
    markup = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
    for author in authors:
        markup.add(types.KeyboardButton(author))
    markup.add(types.KeyboardButton('Вернуться в главное меню'))
    bot.send_message(message.chat.id, f"Авторы по тематике '{subject}':", reply_markup=markup)# Показать книги по автору и тематике
def show_books_by_author(message, author, subject):
    books = library.search_library(author=author, subject=subject)
    markup = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
    book_names = set()  # Используем множество для хранения уникальных названий книг
    for book in books:
        if book['name'] not in book_names:
            markup.add(types.KeyboardButton(book['name']))
            book_names.add(book['name'])
    markup.add(types.KeyboardButton('Вернуться в главное меню'))
    bot.send_message(message.chat.id, f"Книги автора '{author}' по тематике '{subject}':", reply_markup=markup)
# Показать детали книги
def show_book_details(message, book_name):
    book = library.search_library(name=book_name)
    if book:
        book = book[0]
        response = f"Название: {book['name']}\nАвтор: {book['author']}\n\nСкачать тут: {book['source']}"
        bot.send_message(message.chat.id, response, reply_markup=main_menu())
        add_book_to_user_card(message.from_user.id, book_name, book['author'], book['subject'])
    else:
        bot.send_message(message.chat.id, "Книга не найдена", reply_markup=back_to_main_menu())
def add_book_to_user_card(tg_id, book_name, author, subject):
    cards.add_book_info(tg_id, subject, book_name, author)

def get_all_authors():
    authors_cache = {}
    if 'authors' not in authors_cache:
        authors_cache['authors'] = library.get_all_authors()
    return authors_cache['authors']

# Запуск бота
if __name__ == "__main__":
    bot.polling(none_stop=True)
