from pathlib import Path
import wx
import threading
import asyncio
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    MessageHandler,
    CallbackContext,
    filters,
    CallbackQueryHandler
)
import queue
from enum import Enum, auto
import pandas as pd
from tabulate import tabulate

from service.rout_map import tg_users, alltascks, ns
from service.tg import token_kod, test_token
from service.router import process_input_value

# Очередь для обмена сообщениями между Telegram ботом и GUI
message_queue = queue.Queue()


# Загрузка разрешённых user_id из файла
def load_allowed_users():
    try:
        with open(tg_users, 'r') as f:
            return {int(line.strip()) for line in f if line.strip().isdigit()}
    except FileNotFoundError:
        print("Файл allowed_users.txt не найден. Создан новый файл.")
        Path(tg_users).touch()
        return set()


ALLOWED_USERS = load_allowed_users()


class UserState(Enum):
    START = auto()
    AWAITING_METHOD_CHOICE = auto()
    AWAITING_SEND_OPTIONS = auto()


class ExampleApp(wx.Frame):
    def __init__(self, *args, **kwargs):
        super(ExampleApp, self).__init__(*args, **kwargs)
        self.should_exit = False  # Добавьте этот флаг
        self.initUI()

        # Загружаем DataFrame при инициализации
        self.df = self.load_dataframe()

        # Запускаем Telegram бота в отдельном потоке
        self.telegram_thread = threading.Thread(
            target=self.run_telegram_bot,
            daemon=True
        )
        self.telegram_thread.start()

        # Таймер для проверки сообщений от бота
        self.timer = wx.Timer(self)
        self.Bind(wx.EVT_TIMER, self.check_telegram_messages, self.timer)
        self.timer.Start(1000)

        # Обработчик закрытия окна
        self.Bind(wx.EVT_CLOSE, self.OnClose)

    def initUI(self):
        self.title = 'Лаборатория пожарных испытаний ver.8&3/4'
        self.size = (450, 500)
        self.SetSize(*self.size)
        self.SetTitle('LPI TN')

        self.panel = wx.Panel(self)

        # Создание поясняющего текста
        self.staticText = wx.StaticText(self.panel, label="Введите служебный идентификатор заявки:", pos=(70, 20))

        # Создание поля ввода
        self.textCtrl = wx.TextCtrl(self.panel, pos=(50, 50), size=(350, -1))

        # Создание чекбоксов
        self.checkbox1 = wx.CheckBox(self.panel, label='Отправить результаты по ГОСТ 30244 на shoya.vs@tn.ru',
                                     pos=(50, 80))
        self.checkbox4 = wx.CheckBox(self.panel, label='Отправить результаты по ГОСТ 30402 на shoya.vs@tn.ru',
                                     pos=(50, 100))
        self.checkbox2 = wx.CheckBox(self.panel, label='Отправить результаты по ГОСТ 30244 в Телеграмм', pos=(50, 120))
        self.checkbox5 = wx.CheckBox(self.panel, label='Отправить результаты по ГОСТ 30402 в Телеграмм', pos=(50, 140))
        self.checkbox3 = wx.CheckBox(self.panel, label='Закрыть заявку(ки)', pos=(50, 160))

        # Создание кнопки
        self.button = wx.Button(self.panel, label='Сформировать отчет', pos=(190, 180))
        self.button.Bind(wx.EVT_BUTTON, self.onButtonClick)

        # Создание поля для вывода сообщений
        self.messageCtrl = wx.TextCtrl(self.panel, pos=(50, 210), size=(350, 220),
                                       style=wx.TE_MULTILINE | wx.TE_READONLY)

        self.Show()

    def load_dataframe(self):
        """Загружает DataFrame с данными для поиска"""
        try:
            # Для Excel файлов
            df = pd.read_excel(alltascks)
            # Или для CSV:
            # df = pd.read_csv(alltascks, encoding='windows-1251', sep=';')
            print(f"Успешно загружено {len(df)} записей")
            return df
        except Exception as e:
            print(f"Ошибка при загрузке DataFrame: {e}")
            # Возвращаем пустой DataFrame с ожидаемыми колонками
            return pd.DataFrame(columns=['ID', 'identity'])

    async def telegram_info(self, update: Update, context: CallbackContext):
        """Обработчик команды /info с поиском, игнорирующим пробелы"""
        if not await self.check_access(update, context):
            return

        if not context.args:
            await update.message.reply_text("Использование: /info <идентификатор>\nПример: /info 8250")
            return

        try:
            keyword = ' '.join(context.args)

            # Удаляем все пробелы из поискового запроса
            clean_keyword = keyword.replace(" ", "")

            # Проверяем загрузку DataFrame
            if self.df.empty:
                await update.message.reply_text("База данных не загружена")
                return

            # Функция для сравнения значений с учетом удаления пробелов
            def contains_ignoring_spaces(col):
                return col.astype(str).str.replace(" ", "").str.contains(clean_keyword, case=False, na=False)

            # Поиск в числовых колонках (если они есть)
            result = pd.DataFrame()
            if 'identity' in self.df.columns:
                result = self.df[self.df['identity'].apply(
                    lambda x: str(x).replace(" ", "") == clean_keyword if pd.notnull(x) else False)]

            # Если в колонке identity не нашли, ищем во всех колонках
            if result.empty:
                mask = self.df.apply(lambda col: contains_ignoring_spaces(col))
                result = self.df[mask.any(axis=1)]

            if result.empty:
                await update.message.reply_text(f"По запросу '{keyword}' ничего не найдено")
                return

            # Транспонируем DataFrame для инвертированного отображения
            transposed = result.T.reset_index()
            transposed.columns = ['Параметр'] + [f"Значение {i + 1}" for i in range(len(transposed.columns) - 1)]

            # Форматируем таблицу
            table = tabulate(transposed,
                             headers='keys',
                             tablefmt='psql',
                             showindex=False,
                             stralign='left',
                             numalign='left')

            # Отправляем результат
            if len(table) <= 4000:
                await update.message.reply_text(f"<pre>{table}</pre>", parse_mode='HTML')
            else:
                with open('search_results.txt', 'w', encoding='utf-8') as f:
                    f.write(table)
                await update.message.reply_document(
                    document=open('search_results.txt', 'rb'),
                    caption=f"Результаты поиска по '{keyword}'"
                )

        except Exception as e:
            await update.message.reply_text(f"Произошла ошибка: {str(e)}")
            print(f"Ошибка в telegram_info: {e}")
            import traceback
            traceback.print_exc()

    def onButtonClick(self, event):
        text_in = self.textCtrl.GetValue()
        try:
            input_list = [item.strip() for item in text_in.split(',')]
            for val in input_list:
                value = int(val)
                selected_options = self.get_selected_options()
                processed_value = process_input_value(value, selected_options)
                self.messageCtrl.SetValue(f"ID заявки: {value}\n"
                                          f"Выбранные опции: {', '.join(selected_options)}\n"
                                          f"{processed_value}")
        except ValueError:
            try:
                value = int(text_in)
                selected_options = self.get_selected_options()
                processed_value = process_input_value(value, selected_options)
                self.messageCtrl.SetValue(f"ID заявки: {value}\n"
                                          f"Выбранные опции: {', '.join(selected_options)}\n"
                                          f"{processed_value}")
            except ValueError:
                self.messageCtrl.SetValue("Пожалуйста, введите целое число или список целых чисел через запятую.")
        finally:
            self.textCtrl.SetValue('')
            # Сбрасываем состояния чекбоксов
            self.checkbox1.SetValue(False)
            self.checkbox2.SetValue(False)
            self.checkbox3.SetValue(False)
            self.checkbox4.SetValue(False)
            self.checkbox5.SetValue(False)

    def get_selected_options(self):
        """Возвращает список выбранных опций"""
        selected_options = []
        if self.checkbox1.GetValue():
            selected_options.append('a1')
        if self.checkbox2.GetValue():
            selected_options.append('a2')
        if self.checkbox3.GetValue():
            selected_options.append('a3')
        if self.checkbox4.GetValue():
            selected_options.append('a4')
        if self.checkbox5.GetValue():
            selected_options.append('a5')
        return selected_options

    async def check_access(self, update: Update, context: CallbackContext) -> bool:
        """Проверяет доступ пользователя и выводит информацию о неавторизованных попытках"""
        user_id = update.effective_user.id
        if user_id not in ALLOWED_USERS:
            # Отправляем сообщение в GUI о неавторизованной попытке
            user_info = f"Неавторизованная попытка доступа:\nID: {user_id}\n"
            if update.effective_user.username:
                user_info += f"Username: @{update.effective_user.username}\n"
            if update.effective_user.first_name:
                user_info += f"Имя: {update.effective_user.first_name}"
                if update.effective_user.last_name:
                    user_info += f" {update.effective_user.last_name}"

            # Добавляем информацию о типе запроса
            if hasattr(update, 'message') and update.message:
                user_info += f"\nКоманда: {update.message.text}"
            elif hasattr(update, 'callback_query') and update.callback_query:
                user_info += f"\nCallback: {update.callback_query.data}"

            # Отправляем в очередь сообщений для GUI
            message_queue.put(('unauthorized', user_info))

            # Отправляем ответ пользователю
            if hasattr(update, 'message'):
                await update.message.reply_text("⛔ Доступ запрещен!")
            elif hasattr(update, 'callback_query'):
                await update.callback_query.answer("⛔ Доступ запрещен!", show_alert=True)
            return False
        return True

    def run_telegram_bot(self):
        """Запускает Telegram бота с использованием nest_asyncio"""
        try:
            import nest_asyncio
            nest_asyncio.apply()

            self.application = ApplicationBuilder().token(token_kod).build()

            # Добавляем обработчики команд
            self.application.add_handler(CommandHandler("start", self.telegram_start))
            self.application.add_handler(CommandHandler("help", self.telegram_help))
            self.application.add_handler(CommandHandler("info", self.telegram_info))  # Добавлен новый обработчик
            self.application.add_handler(
                MessageHandler(filters.TEXT & ~filters.COMMAND, self.telegram_process_message)
            )
            # Добавляем обработчики callback-ов
            self.application.add_handler(
                CallbackQueryHandler(self.handle_method_callback, pattern="^method_")
            )
            self.application.add_handler(
                CallbackQueryHandler(self.handle_option_callback, pattern="^option_")
            )

            # Запускаем бота
            self.application.run_polling()
        except Exception as e:
            print(f"Ошибка в потоке Telegram бота: {e}")

        finally:
            print("Поток Telegram бота завершен")

    async def telegram_start(self, update: Update, context: CallbackContext):
        """Обработчик команды /start"""
        if not await self.check_access(update, context):
            return

        await update.message.reply_text(
            "Привет! Я бот для управления программой LPI.\n"
            "Отправьте мне ID заявки, чтобы начать работу."
        )

    async def telegram_help(self, update: Update, context: CallbackContext):
        """Обработчик команды /help"""
        if not await self.check_access(update, context):
            return
        await self.telegram_start(update, context)

    async def telegram_process_message(self, update: Update, context: CallbackContext):
        """Обработчик текстовых сообщений"""
        if not await self.check_access(update, context):
            return

        text = update.message.text.strip()

        # Проверяем, есть ли сохраненное состояние для пользователя
        user_data = context.user_data
        user_data['state'] = UserState.START
        user_data['request_id'] = None
        user_data['available_methods'] = []

        if not text:
            await update.message.reply_text("Пожалуйста, введите ID заявки")
            return

        try:
            request_id = int(text)
            user_data['request_id'] = request_id
            user_data['state'] = UserState.AWAITING_METHOD_CHOICE

            # Проверяем доступные методы
            available_methods = self.check_available_methods(request_id)
            user_data['available_methods'] = available_methods

            if not available_methods:
                await update.message.reply_text(
                    f"Для заявки {request_id} нет доступных отчетов.\n"
                    "Попробуйте другой ID заявки."
                )
                user_data['state'] = UserState.START
                return

            # Создаем клавиатуру с доступными методами
            keyboard = []
            for method in available_methods:
                keyboard.append([
                    InlineKeyboardButton(
                        self.get_method_name(method),
                        callback_data=f"method_{method}"
                    )
                ])

            if len(available_methods) > 1:
                keyboard.append([
                    InlineKeyboardButton(
                        "Все отчеты",
                        callback_data="method_all"
                    )
                ])

            reply_markup = InlineKeyboardMarkup(keyboard)

            await update.message.reply_text(
                f"Выберите метод, по которому хотите получить отчет для заявки {request_id}:",
                reply_markup=reply_markup
            )

        except ValueError:
            await update.message.reply_text("ID заявки должен быть целым числом")

    async def handle_method_callback(self, update: Update, context: CallbackContext):
        """Обработчик нажатия кнопок выбора метода"""
        if not await self.check_access(update, context):
            return

        query = update.callback_query
        await query.answer()

        user_data = context.user_data
        request_id = user_data['request_id']
        available_methods = user_data['available_methods']

        if query.data == "method_all":
            user_data['selected_methods'] = available_methods
        else:
            method = query.data.split("_")[1]
            user_data['selected_methods'] = [method]

        # Показываем опции отправки (этот блок должен выполняться в любом случае)
        keyboard = []

        # Добавляем только релевантные опции для выбранных методов
        if any(m in ['30244', '30402'] for m in user_data['selected_methods']):
            keyboard.append([
                InlineKeyboardButton("📧 На почту", callback_data="option_email"),
                InlineKeyboardButton("📨 В Телеграм", callback_data="option_telegram"),
                InlineKeyboardButton("💬 В чат", callback_data="option_chat")
            ])

        keyboard.append([
            InlineKeyboardButton("🔒 Закрыть заявку", callback_data="option_close")
        ])

        keyboard.append([
            InlineKeyboardButton("✅ Подтвердить", callback_data="option_confirm")
        ])

        reply_markup = InlineKeyboardMarkup(keyboard)

        methods_text = ", ".join(self.get_method_name(m) for m in user_data['selected_methods'])
        await query.edit_message_text(
            text=f"Выбраны отчеты: {methods_text}\nВыберите опции:",
            reply_markup=reply_markup
        )

        # Инициализируем список выбранных опций
        user_data['selected_options'] = []
        user_data['state'] = UserState.AWAITING_SEND_OPTIONS

    async def handle_option_callback(self, update: Update, context: CallbackContext):
        """Обработчик нажатия кнопок выбора опций"""
        if not await self.check_access(update, context):
            return

        query = update.callback_query
        await query.answer()

        user_data = context.user_data
        chat_id = update.effective_chat.id
        message_thread_id = update.effective_message.message_thread_id if hasattr(update.effective_message,
                                                                                  'message_thread_id') else None

        if query.data == "option_confirm":
            request_id = user_data['request_id']
            selected_methods = user_data['selected_methods']
            selected_options = user_data['selected_options']

            full_options = []
            for opt in selected_options:
                opt_type = opt.split("_")[1]
                if opt_type == "email":
                    if '30244' in selected_methods:
                        full_options.append('a1')
                    if '30402' in selected_methods:
                        full_options.append('a4')
                elif opt_type == "telegram":
                    if '30244' in selected_methods:
                        full_options.append('a2')
                    if '30402' in selected_methods:
                        full_options.append('a5')
                elif opt_type == "chat":
                    if '30244' in selected_methods:
                        full_options.append('a6')
                    if '30402' in selected_methods:
                        full_options.append('a7')
                elif opt_type == "close":
                    full_options.append('a3')

            full_options = list(set(full_options))

            # Передаем message_thread_id в очередь сообщений
            message_queue.put(('process', request_id, full_options, chat_id, message_thread_id))

            await query.edit_message_text(
                text=f"Заявка {request_id} с опциями {', '.join(full_options)} принята в обработку"
            )
            user_data['state'] = UserState.START
            return

        # Добавляем/удаляем опцию из списка
        if query.data in user_data['selected_options']:
            user_data['selected_options'].remove(query.data)
        else:
            user_data['selected_options'].append(query.data)

        # Обновляем сообщение с текущим выбором
        selected_methods = user_data['selected_methods']
        selected_options = user_data['selected_options']

        # Создаем новый текст сообщения
        methods_text = ", ".join(self.get_method_name(m) for m in selected_methods)
        options_text = "Выбранные опции:\n" + "\n".join(
            self.get_option_name(o.split("_")[1])
            for o in selected_options
        ) if selected_options else "Опции не выбраны"

        # Создаем обновленную клавиатуру
        keyboard = []

        if any(m in ['30244', '30402'] for m in selected_methods):
            email_selected = "option_email" in selected_options
            telegram_selected = "option_telegram" in selected_options
            chat_selected = "option_chat" in selected_options

            keyboard.append([
                InlineKeyboardButton(
                    f"{'✅ ' if email_selected else ''}📧 На почту",
                    callback_data="option_email"
                ),
                InlineKeyboardButton(
                    f"{'✅ ' if telegram_selected else ''}📨 В Телеграм",
                    callback_data="option_telegram"
                ),
                InlineKeyboardButton(
                    f"{'✅ ' if chat_selected else ''}💬 В чат",
                    callback_data="option_chat"
                )
            ])

        close_selected = "option_close" in selected_options
        keyboard.append([
            InlineKeyboardButton(
                f"{'✅ ' if close_selected else ''}🔒 Закрыть заявку",
                callback_data="option_close"
            )
        ])

        keyboard.append([
            InlineKeyboardButton("✅ Подтвердить", callback_data="option_confirm")
        ])

        reply_markup = InlineKeyboardMarkup(keyboard)

        await query.edit_message_text(
            text=f"Выбраны отчеты: {methods_text}\n{options_text}",
            reply_markup=reply_markup
        )

    def check_available_methods(self, request_id: int) -> list:
        """Проверяет доступные методы для заявки (заглушка)"""
        return ['30244', '30402']

    def get_method_name(self, method_code: str) -> str:
        """Возвращает читаемое название метода"""
        names = {
            '30244': 'ГОСТ 30244 (Горючесть)',
            '30402': 'ГОСТ 30402 (Воспламеняемость)'
        }
        return names.get(method_code, method_code)

    def get_option_name(self, option_code: str) -> str:
        """Возвращает читаемое название опции"""
        names = {
            'email': '📧 На почту',
            'telegram': '📨 В Телеграм',
            'chat': '💬 В чат',
            'close': '🔒 Закрыть заявку'
        }
        return names.get(option_code, option_code)

    def check_telegram_messages(self, event):
        """Проверяет сообщения от Telegram бота"""
        if self.should_exit:
            return
        while not message_queue.empty():
            message = message_queue.get()
            if message[0] == 'process':
                _, request_id, options, chat_id, message_thread_id = message
                self.process_telegram_request(request_id, options, chat_id, message_thread_id)
            elif message[0] == 'unauthorized':
                _, user_info = message
                self.append_to_gui_log(user_info)

    def process_telegram_request(self, request_id, options, chat_id, message_thread_id=None):
        """Обрабатывает запрос от Telegram бота с учетом message_thread_id"""
        # Устанавливаем только стандартные опции (a1-a5)
        self.checkbox1.SetValue('a1' in options)
        self.checkbox2.SetValue('a2' in options)
        self.checkbox3.SetValue('a3' in options)
        self.checkbox4.SetValue('a4' in options)
        self.checkbox5.SetValue('a5' in options)

        # a6 и a7 не устанавливаем в GUI, но передаем в process_input_value
        processed_value = process_input_value(
            request_id,
            options,
            chat_id=chat_id,
            message_thread_id=message_thread_id
        )

        output = (f"Telegram запрос:\n"
                  f"ID заявки: {request_id}\n"
                  f"ID чата: {chat_id}\n"
                  f"Thread ID: {message_thread_id if message_thread_id else 'N/A'}\n"
                  f"Выбранные опции: {', '.join(options)}\n"
                  f"{processed_value}")

        self.messageCtrl.SetValue(output)

    def append_to_gui_log(self, text):
        """Добавляет текст в лог GUI с временной меткой"""
        timestamp = wx.DateTime.Now().Format("%H:%M:%S")
        formatted_text = f"[{timestamp}] {text}\n"
        current_text = self.messageCtrl.GetValue()
        self.messageCtrl.SetValue(formatted_text + current_text)

    def OnClose(self, event):
        """Обработчик закрытия окна"""
        # Остановка таймера
        self.timer.Stop()

        # Завершение Telegram бота
        if hasattr(self, 'application'):
            try:
                loop = asyncio.new_event_loop()
                asyncio.set_event_loop(loop)
                loop.run_until_complete(self.application.shutdown())
                loop.run_until_complete(self.application.stop())
                loop.close()
            except Exception as e:
                print(f"Ошибка при остановке бота: {e}")

        # Убедимся, что поток Telegram бота завершен
        if hasattr(self, 'telegram_thread'):
            self.telegram_thread.join(timeout=1.0)

        # Уничтожение окна
        self.Destroy()


# Создание экземпляра приложения перед главным циклом
app = wx.App()

if __name__ == '__main__':
    ex = ExampleApp(None)
    app.MainLoop()