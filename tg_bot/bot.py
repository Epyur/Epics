import logging
from telegram import Update, Bot
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext, UpdateQueue

from tg_bot.config.t import bot_token


# Функция для обработки команды /start
def start(update: Update, context: CallbackContext) -> None:
    update.message.reply_text('Привет! Я ваш телеграм-бот. Как я могу помочь?')

# Функция для обработки команды /help
def help_command(update: Update, context: CallbackContext) -> None:
    update.message.reply_text('Команды: /start, /help, /ping, /stop')

# Функция для обработки команды /ping
def ping(update: Update, context: CallbackContext) -> None:
    update.message.reply_text('Pong! Бот работает нормально.')

# Функция для обработки команды /stop
def stop(update: Update, context: CallbackContext) -> None:
    update.message.reply_text('Бот остановлен.')
    context.bot.stop_polling()

# Функция для обработки любого сообщения
def echo(update: Update, context: CallbackContext) -> None:
    user_id = update.message.from_user.id
    user_chat = update.message.chat_id
    user_exists = False

    # Проверка существования пользователя в базе данных (например, в словаре)
    if user_chat in users_database:
       user_exists = users_databaseuser_chat

    update.message.reply_text(f'Вы, {update.message.from_user.username} из чата {user_chat}, написали: ' + update.message.text)

    # Добавление пользователя в базу данных, если его там еще нет
    if not user_exists:
       users_databaseuser_chat = True

def main() -> None:
    # Вставьте ваш токен бота здесь
    TOKEN = bot_token
    logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

    # Создание очереди обновлений
    update_queue = UpdateQueue()

    # Инициализация Updater с передачей токена и очереди обновлений
    updater = Updater(TOKEN, update_queue=update_queue)

    # Создание Dispatcher
    dp = updater.dispatcher

    # Обработчики команд
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("help", help_command))
    dp.add_handler(CommandHandler("ping", ping))
    dp.add_handler(CommandHandler("stop", stop))

    # Обработчики сообщений
    dp.add_handler(MessageHandler(Filters.text & ~Filters.command, echo))

    # Запуск бота
    updater.start_polling()

    # Дождитесь завершения работы бота
    updater.idle()

    # Пример базы данных пользователей
    users_database = {}
    # Сохранение базы данных в файл
    with open('users_database.json', 'w') as outfile:
        json.dump(users_database, outfile)

if __name__ == '__main__':
 main()