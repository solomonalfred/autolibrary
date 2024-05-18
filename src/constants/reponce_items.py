class Msg:
    SHOW_CARD = "Книги которые прочитал: {} {}\n"
    SHOW_EMPTY_CARD = "Вы пока нечего не выбирали"
    SUBJECT = "Выберите тематику:"
    SUBJECT_BOOKS = "Книги по тематике '{}':"
    SUBJECT_SEARCH_OPTIONS = "Выберите способ поиска по тематике '{}':"
    SUBJECT_AUTHORS = "Авторы по тематике '{}':"
    SUBJECT_AUTHORS_BOOKS = "Книги автора '{}' по тематике '{}':"
    BOOK_DETAILS = "Название: {}\nАвтор: {}\n\nСкачать тут: {}"
    BOOK_NOT_FOUND = "Книга не найдена"
    WELCOME = "Добро пожаловать!"
    IN_MAIN = "Вы в главном меню"


class ButtonText:
    SHOW_USER_CARD = 'Посмотреть карточку читателя'
    SEARCH_BOOK = 'Найти книгу'
    BACK_TO_MAIN_MENU = 'Вернуться в главное меню'
    SEARCH_BY_AUTHOR = 'Искать по автору'
    SEARCH_BY_NAME = 'Искать по названию'


class LoggerText:
    TIME_FORMAT = '%Y-%m-%d %H:%M:%S'
    MAIN = "Main menu: telegram id {}"
    BACK_TO_MAIN_MENU = "Return main menu: telegram id {}"
    GET_BOOKS = "Get taken books: telegram id {}"
    CHOOSE_SUBJECT = "Choose book's subject: telegram id {}"
    SUBJECT_BOOKS = "Show books by {}: telegram id {}"
    SEARCH_VARIABLE = "Choose how to search book by {}: telegram id {}"
    SEARCH_BY_AUTHOR = "Show author by {}: telegram id {}"
    SEARCH_BOOK_BY_SUBJECT_N_AUTHOR = "Show books by {} and {}: telegram id {}"
    BOOK_DETAILS = "Show {} record: telegram id {}"
    USER_CHOOSING = "User {} take {} {} {} for reading"
    START_CHAT = "Start chat: telegram id {}"
    SHOW_CARD = "Show library card: telegram id {}"
    BACK_TO_MAIN_MENU_HANDLER = "Return main menu (handler): telegram id {}"
    SEARCH_BOOK_HANDLER = "Search book (handler): telegram id {}"

    SELECT_VARIABLE = "User {} select variable"
    SELECT_AUTHOR = "User {} select books by author"
    SELECT_NAME = "User {} select books by name"

    CHOOSE_AUTHOR = "User {} select book's author"
    CHOOSE_NAME = "User {} select book's name"

    RETURN = "User {} return to main menu"

    LOAD_DATA = "Load library"


class AdditionalItems:
    SUBJECT_AUTHOR = "subject author"
