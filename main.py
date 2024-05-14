import logging
import random
import os
from dotenv import load_dotenv
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

# из .env файла
load_dotenv()
TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")

#  данных с книгами
book_recommendations = {
    "фантастика": [
        "'Дюна' Фрэнк Герберт",
        "'451 градус по Фаренгейту' Рэй Брэдбери",
        "'Игра Эндера' Орсон Скотт Кард",
        "'Основатели' Айзек Азимов"
    ],
    "детектив": [
        "'Шерлок Холмс' Артур Конан Дойл",
        "'Десять негритят' Агата Кристи",
        "'Девушка с татуировкой дракона' Стиг Ларссон",
        "'Молчание ягнят' Томас Харрис"
    ],
    "роман": [
        "'Гордость и предубеждение' Джейн Остин",
        "'Анна Каренина' Лев Толстой",
        "'1984' Джордж Оруэлл",
        "'Поющие в терновнике' Колин Маккалоу"
    ],
    "программирование": [
        "'Изучаем Python' Марк Лутц",
        "'Чистый код' Роберт Мартин",
        "'JavaScript: The Good Parts' Дуглас Крокфорд",
        "'Design Patterns' Эрич Гамма, Ричард Хелм, Ральф Джонсон, Джон Влиссидес"
    ],
    "история": [
        "'Краткая история времени' Стивен Хокинг",
        "'Сапиенс: Краткая история человечества' Юваль Ной Харари",
        "'Ганнибал: Враг Рима' Ливий",
        "'Древний Рим' Мэри Бирд"
    ]
}

# функция для  общения с пользователем
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user = update.effective_user
    await update.message.reply_text(
        f"Привет, {user.first_name}! Я помогу вам выбрать книгу. Какую книгу вы ищете? Например: фантастика, детектив, роман, программирование, история."
    )

# для получения жанра от пользователя и рекомендации книги
async def recommend_book(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    genre = update.message.text.lower()
    if genre in book_recommendations:
        book = random.choice(book_recommendations[genre])
        await update.message.reply_text(f"Рекомендую прочитать: {book}")
    else:
        await update.message.reply_text("Извините, я не знаю книг в этом жанре. Попробуйте выбрать другой жанр.")

def main() -> None:
    # Создание и запуск приложения
    application = Application.builder().token(TOKEN).build()

    # Обработчик команды /start
    application.add_handler(CommandHandler("start", start))

    # Обработчик текстовых сообщений (жанров)
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, recommend_book))

    # Запуск бота
    application.run_polling()

if __name__ == '__main__':
    main()
