import sys
import pandas as pd
import configparser
import os
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QListWidget, QVBoxLayout, QWidget,
    QLabel, QLineEdit, QTextEdit, QPushButton, QHBoxLayout, QMessageBox
)
from PyQt6.QtCore import Qt, QTimer
import imaplib
import email
import chardet
from email.header import decode_header
from email.utils import parsedate_to_datetime
from typing import List, Dict, Optional
from email.message import Message


class GetMail:
    def __init__(self, folder: str = 'INBOX',
                 email_address: str = 'lpitn@ya.ru',
                 password: str = 'zrhuyzsfvvvkztlf'):
        self.folder = folder
        self.email_address = email_address
        self.password = password
        self.mail = None

    def connect(self):
        """Установка соединения с IMAP-сервером"""
        try:
            self.mail = imaplib.IMAP4_SSL("imap.yandex.ru")
            self.mail.login(self.email_address, self.password)
            self.mail.select(self.folder)
            return True
        except Exception as e:
            print(f"Ошибка подключения: {str(e)}")
            return False

    def fetch_mails(self, limit: int = 10) -> List[Dict]:
        """Получение писем с сервера"""
        messages = []

        if not self.mail:
            if not self.connect():
                return messages

        try:
            _, data = self.mail.search(None, "ALL")
            mail_ids = data[0].split()

            for num in mail_ids[-limit:]:
                _, msg_data = self.mail.fetch(num, "(RFC822)")
                raw_email = msg_data[0][1]
                msg = email.message_from_bytes(raw_email)

                text = self._extract_email_text(msg)

                messages.append({
                    "subject": self.decode_email_header(msg.get("Subject", "")),
                    "from": self.decode_email_header(msg.get("From", "")),
                    "date": msg.get("Date", ""),
                    "text": text
                })

        except Exception as e:
            print(f"Ошибка при получении писем: {str(e)}")
            self.mail = None  # Сброс соединения при ошибке

        return messages

    def _extract_email_text(self, msg: email.message.Message) -> str:
        """Улучшенное извлечение текста письма с обработкой разных форматов"""
        text = ""

        # Сначала пробуем найти plain text часть
        if msg.is_multipart():
            for part in msg.walk():
                content_type = part.get_content_type()
                content_disposition = str(part.get("Content-Disposition", ""))

                # Пропускаем вложения
                if "attachment" in content_disposition:
                    continue

                # Предпочтение отдаём plain text
                if content_type == "text/plain":
                    text = self._decode_payload(part)
                    if text.strip():  # Если нашли непустой текст - возвращаем
                        return text

                # Если plain text не найден, пробуем html
                elif content_type == "text/html":
                    html_text = self._decode_payload(part)
                    if html_text.strip():
                        # Упрощённая конвертация HTML в plain text
                        text = " ".join(html_text.replace("<br>", "\n").split())
                        return text
        else:
            # Для простых писем
            text = self._decode_payload(msg)

        return text if text.strip() else "Текст письма не найден"

    def _decode_payload(self, part: email.message.Message) -> str:
        """Улучшенное декодирование содержимого"""
        payload = part.get_payload(decode=True)
        if payload is None:
            return ""

        charset = part.get_content_charset() or 'utf-8'

        try:
            # Пробуем указанную кодировку
            return payload.decode(charset)
        except UnicodeDecodeError:
            try:
                # Автоопределение кодировки
                detected = chardet.detect(payload)
                return payload.decode(detected['encoding'] or 'utf-8', errors='replace')
            except:
                # Последняя попытка
                return payload.decode('utf-8', errors='replace')
        except AttributeError:
            # Если payload уже строка
            return str(payload)

    def decode_email_header(self, header: Optional[str] = None) -> str:
        """Декодирование email-заголовков"""
        if not header:
            return ""

        try:
            decoded_parts = decode_header(header)
            result = []
            for part, encoding in decoded_parts:
                if isinstance(part, bytes):
                    enc = encoding or chardet.detect(part)['encoding'] or 'utf-8'
                    part = part.decode(enc, errors='replace')
                result.append(part)
            return ' '.join(result).strip()
        except Exception as e:
            print(f"Ошибка декодирования заголовка: {str(e)}")
            return str(header)

    def close(self):
        """Закрытие соединения"""
        if self.mail:
            try:
                self.mail.close()
                self.mail.logout()
            except:
                pass
            self.mail = None


class EmailApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Автоматический IMAP-клиент")
        self.setGeometry(100, 100, 800, 600)

        # Конфигурация
        self.config_file = "email_config.ini"
        self.mail_client = None
        self.load_config()

        # Виджеты
        self.email_list = QListWidget()
        self.email_list.itemClicked.connect(self.load_email_data)

        self.subject_label = QLabel("Тема:")
        self.subject_input = QLineEdit()
        self.subject_input.setReadOnly(True)

        self.sender_label = QLabel("Отправитель:")
        self.sender_input = QLineEdit()
        self.sender_input.setReadOnly(True)

        self.date_label = QLabel("Дата:")
        self.date_input = QLineEdit()
        self.date_input.setReadOnly(False)

        self.body_label = QLabel("Текст письма:")
        self.body_input = QTextEdit()
        self.body_input.setReadOnly(True)

        self.refresh_button = QPushButton("Обновить")
        self.refresh_button.clicked.connect(self.refresh_emails)

        self.save_button = QPushButton("Сохранить в Excel")
        self.save_button.clicked.connect(self.save_to_excel)

        # Разметка
        left_layout = QVBoxLayout()
        left_layout.addWidget(QLabel("Письма:"))
        left_layout.addWidget(self.email_list)
        left_layout.addWidget(self.refresh_button)

        right_layout = QVBoxLayout()
        right_layout.addWidget(self.subject_label)
        right_layout.addWidget(self.subject_input)
        right_layout.addWidget(self.sender_label)
        right_layout.addWidget(self.sender_input)
        right_layout.addWidget(self.date_label)
        right_layout.addWidget(self.date_input)
        right_layout.addWidget(self.body_label)
        right_layout.addWidget(self.body_input)
        right_layout.addWidget(self.save_button, alignment=Qt.AlignmentFlag.AlignBottom)

        main_layout = QHBoxLayout()
        main_layout.addLayout(left_layout, stretch=1)
        main_layout.addLayout(right_layout, stretch=2)

        container = QWidget()
        container.setLayout(main_layout)
        self.setCentralWidget(container)

        # Таймер для автоматического обновления
        self.timer = QTimer()
        self.timer.timeout.connect(self.refresh_emails)
        self.timer.start(60000)  # Обновление каждые 60 секунд

        # Первоначальная загрузка писем
        self.refresh_emails()

    def load_config(self):
        """Загрузка конфигурации из файла"""
        config = configparser.ConfigParser()

        if os.path.exists(self.config_file):
            config.read(self.config_file)
            email = config.get('Credentials', 'Email', fallback='')
            password = config.get('Credentials', 'Password', fallback='')

            if email and password:
                self.mail_client = GetMail(
                    email_address=email,
                    password=password
                )
            else:
                self.show_config_error("Неверные учетные данные в конфигурационном файле")
        else:
            # Создание нового конфигурационного файла
            config['Credentials'] = {
                'Email': 'lpitn@yandex.ru',
                'Password': 'zrhuyzsfvvvkztlf'
            }
            with open(self.config_file, 'w') as configfile:
                config.write(configfile)
            self.show_config_error(
                f"Создан новый конфигурационный файл: {self.config_file}\nЗаполните его своими данными")

    def show_config_error(self, message):
        """Отображение ошибки конфигурации"""
        QMessageBox.critical(
            self,
            "Ошибка конфигурации",
            f"{message}\n\nПриложение будет закрыто",
            QMessageBox.StandardButton.Ok
        )
        sys.exit(1)

    def refresh_emails(self):
        """Обновление списка писем"""
        if not self.mail_client:
            return

        try:
            messages = self.mail_client.fetch_mails(limit=20)

            self.email_list.clear()
            for msg in messages:
                self.email_list.addItem(
                    f"{msg['subject']} | {msg['from']} | {msg['date']}"
                )

            if not messages:
                QMessageBox.information(self, "Информация", "Нет новых писем")

        except Exception as e:
            QMessageBox.critical(self, "Ошибка", f"Не удалось загрузить письма: {str(e)}")

    def load_email_data(self, item):
        """Загрузка данных выбранного письма"""
        if not self.mail_client:
            QMessageBox.warning(self, "Ошибка", "Нет подключения к почте!")
            return

        try:
            # Получаем ID письма из виджета
            email_id = self.email_list.row(item) + 1  # IMAP нумерация с 1

            # Загружаем конкретное письмо заново для точности
            status, msg_data = self.mail_client.mail.fetch(str(email_id), "(RFC822)")
            if status != "OK":
                raise Exception("Не удалось загрузить письмо")

            raw_email = msg_data[0][1]
            msg = email.message_from_bytes(raw_email)

            # Обновляем поля интерфейса
            self.subject_input.setText(self.mail_client.decode_email_header(msg.get("Subject", "")))
            self.sender_input.setText(self.mail_client.decode_email_header(msg.get("From", "")))
            self.date_input.setText(msg.get("Date", ""))

            # Получаем и устанавливаем текст
            email_text = self.mail_client._extract_email_text(msg)
            self.body_input.setPlainText(email_text)

        except Exception as e:
            QMessageBox.critical(self, "Ошибка", f"Не удалось загрузить письмо: {str(e)}")
            print(f"DEBUG: Ошибка при загрузке письма: {str(e)}")

    def save_to_excel(self):
        """Сохранение текущего письма в Excel"""
        if not all([
            self.subject_input.text(),
            self.sender_input.text(),
            self.date_input.text(),
            self.body_input.toPlainText()
        ]):
            QMessageBox.warning(self, "Предупреждение", "Нет данных для сохранения!")
            return

        data = {
            "Тема": [self.subject_input.text()],
            "Отправитель": [self.sender_input.text()],
            "Дата": [self.date_input.text()],
            "Текст": [self.body_input.toPlainText()]
        }

        df = pd.DataFrame(data)

        try:
            try:
                existing_df = pd.read_excel("письма.xlsx")
                updated_df = pd.concat([existing_df, df], ignore_index=True)
            except FileNotFoundError:
                updated_df = df

            updated_df.to_excel("письма.xlsx", index=False)
            QMessageBox.information(self, "Успех", "Письмо сохранено в письма.xlsx!")

        except Exception as e:
            QMessageBox.critical(self, "Ошибка", f"Не удалось сохранить в Excel: {str(e)}")

    def closeEvent(self, event):
        """Обработка закрытия приложения"""
        if self.mail_client:
            self.mail_client.close()
        event.accept()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = EmailApp()
    window.show()
    sys.exit(app.exec())