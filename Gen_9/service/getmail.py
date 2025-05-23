import os
import json
import imaplib
import email
import chardet
from email.header import decode_header
from typing import List, Dict, Optional
import pandas as pd
from email.message import Message
from bs4 import BeautifulSoup
import re

from Gen_9.service.rout_map import ns, inc_book
from Gen_9.service.passw.passw import *




class GetMail:
    def __init__(self, folder: str = 'LPITrack',
                 email_address: str = mail_login,
                 password: str = mail_pass,
                 search: str = "UNSEEN",
                 attachment_dir: str = "attachments"):
        """
        Инициализация подключения к почте

        :param folder: Папка для поиска писем
        :param email_address: Адрес электронной почты
        :param password: Пароль или токен приложения
        :param search: Критерий поиска писем
        :param attachment_dir: Папка для сохранения вложений
        """

        self.folder = folder
        self.email_address = email_address
        self.password = password
        self.search = search
        self.attachment_dir = attachment_dir
        self.messages = []

        # Создаем папку для вложений если не существует
        os.makedirs(self.attachment_dir, exist_ok=True)

    def fetch_yandex_mails(self, limit: int = 10) -> List[Dict]:
        """
        Получение писем с сервера с обработкой вложений

        :param limit: Количество последних писем
        :return: Список сообщений
        """
        messages = []

        try:
            with imaplib.IMAP4_SSL("imap.yandex.ru") as mail:
                mail.login(self.email_address, self.password)
                mail.select(self.folder)

                _, data = mail.search(None, self.search)
                mail_ids = data[0].split()

                for num in mail_ids[-limit:]:
                    _, msg_data = mail.fetch(num, "(RFC822)")
                    raw_email = msg_data[0][1]
                    msg = email.message_from_bytes(raw_email)

                    # Обработка текста письма и JSON
                    text = self._extract_email_text(msg)
                    json_data = self._extract_json_from_text(text)
                    html = self._get_html_part(msg)

                    # Обработка вложений
                    attachments = self._save_attachments(msg)

                    messages.append({
                        "id": num.decode(),
                        "subject": self.decode_email_header(msg.get("Subject", "")),
                        "from": self.decode_email_header(msg.get("From", "")),
                        "date": msg.get("Date", ""),
                        "text": text,
                        "html": html,
                        "json": json_data,
                        "attachments": attachments,
                        "links": self._extract_links_from_html(html) if html else [],
                        "tables": self._extract_tables_from_html(html) if html else []
                    })

        except Exception as e:
            print(f"Ошибка при получении писем: {str(e)}")

        return messages

    def _extract_tables_from_html(self, html: str) -> List[pd.DataFrame]:
        """Извлечение таблиц из HTML в DataFrame"""
        try:
            soup = BeautifulSoup(html, 'html.parser')
            tables = []
            for table in soup.find_all('table'):
                df = pd.read_html(str(table))[0]
                tables.append(df)
            return tables
        except:
            return []

    def _extract_links_from_html(self, html: str) -> List[str]:
        """Извлечение всех ссылок из HTML"""
        try:
            soup = BeautifulSoup(html, 'html.parser')
            return [a['href'] for a in soup.find_all('a', href=True)]
        except:
            return []

    def _extract_json_from_text(self, text: str) -> Optional[Dict]:
        """Извлечение JSON данных из текста письма"""
        try:
            # Ищем JSON в тексте (может быть в начале, середине или конце)
            json_start = text.find('{')
            json_end = text.rfind('}') + 1
            if json_start != -1 and json_end != -1:
                json_str = text[json_start:json_end]
                return json.loads(json_str)
        except json.JSONDecodeError as e:
            print(f"Ошибка декодирования JSON: {str(e)}")
        return None

    def _save_attachments(self, msg: email.message.Message) -> List[str]:
        """Сохранение вложений письма в папку"""
        attachments = []
        for part in msg.walk():
            content_disposition = str(part.get("Content-Disposition", ""))
            if "attachment" in content_disposition:
                filename = part.get_filename()
                if filename:
                    filename = self._clean_filename(filename)
                    filepath = os.path.join(self.attachment_dir, f"{filename}")
                    with open(filepath, "wb") as f:
                        f.write(part.get_payload(decode=True))
                    attachments.append(filepath)
        return attachments

    def _clean_filename(self, filename: str) -> str:
        """Очистка имени файла от недопустимых символов"""
        invalid_chars = '<>:"/\\|?*'
        for char in invalid_chars:
            filename = filename.replace(char, '_')
        return filename

    def _extract_email_text(self, msg: email.message.Message) -> str:
        """Извлечение текста из письма с обработкой HTML"""
        text = ""
        html = ""

        if msg.is_multipart():
            for part in msg.walk():
                content_type = part.get_content_type()
                content_disposition = str(part.get("Content-Disposition", ""))

                if "attachment" not in content_disposition:
                    if content_type == "text/plain":
                        text = self._decode_payload(part)
                    elif content_type == "text/html":
                        html = self._decode_payload(part)
        else:
            if msg.get_content_type() == "text/html":
                html = self._decode_payload(msg)
            else:
                text = self._decode_payload(msg)

        # Если есть HTML - обрабатываем его
        if html:
            return self._clean_html_content(html)
        return text

    def _clean_html_content(self, html: str) -> str:
        """Очистка HTML и преобразование в читаемый текст"""
        try:
            soup = BeautifulSoup(html, 'html.parser')

            # Удаляем ненужные элементы
            for element in soup(['script', 'style', 'meta', 'link', 'head']):
                element.decompose()

            # Заменяем HTML-сущности
            text = soup.get_text(separator='\n', strip=True)

            # Очищаем от лишних пробелов и переносов
            text = re.sub(r'\n{3,}', '\n\n', text)
            text = re.sub(r'[ \t]{2,}', ' ', text)

            return text.strip()

        except Exception as e:
            print(f"Ошибка обработки HTML: {str(e)}")
            return html  # Возвращаем исходный HTML если не удалось обработать

    def _decode_payload(self, part: email.message.Message) -> str:
        """Декодирование содержимого письма"""
        payload = part.get_payload(decode=True)
        if payload is None:
            return ""

        charset = part.get_content_charset() or 'utf-8'
        try:
            return payload.decode(charset)
        except UnicodeDecodeError:
            try:
                detected = chardet.detect(payload)
                return payload.decode(detected['encoding'] or 'utf-8', errors='replace')
            except:
                return payload.decode('utf-8', errors='replace')

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

    def _get_html_part(self, msg: email.message.Message) -> Optional[str]:
        """Получение HTML-части письма"""
        if msg.is_multipart():
            for part in msg.walk():
                if part.get_content_type() == "text/html":
                    return self._decode_payload(part)
        elif msg.get_content_type() == "text/html":
            return self._decode_payload(msg)
        return None

    def process_messages(self, messages: Optional[List[Dict]] = None) -> List[Dict]:
        """
        Обработка сообщений с декодированием заголовков

        :param messages: Список сообщений (если None, будет загружен из почты)
        :return: Обработанные сообщения
        """
        if messages is None:
            self.messages = self.fetch_yandex_mails()
        else:
            self.messages = messages

        return [{
            'id': msg.get('id', ''),
            'subject': self.decode_email_header(msg.get('subject', '')),
            'from': self.decode_email_header(msg.get('from', '')),
            'date': msg.get('date', ''),
            'text': msg.get('text', ''),
            'json': msg.get('json', {}),
            'attachments': msg.get('attachments', [])
        } for msg in self.messages]

    def save_to_excel(self, file: str):
        """
        Сохранение данных в Excel файл

        :param file: Путь к файлу Excel
        """
        if not self.messages:
            print("Нет данных для сохранения")
            return

        try:
            # Создаем DataFrame из JSON данных
            json_data = [msg['json'] for msg in self.messages if msg.get('json')]
            print(json_data)
            if json_data:
                df = pd.DataFrame(json_data)

                # Сохраняем в Excel
                if os.path.exists(file):
                    existing_df = pd.read_excel(file)
                    updated_df = pd.concat([existing_df, df], ignore_index=True)
                else:
                    updated_df = df

                # updated_df['ID'] = updated_df['ID'].str.extract(r'(\d+)')[0]
                mask = updated_df['ID'].astype(str).str.contains("LPIZAYAVKINAPRO-", na=False)
                updated_df.loc[mask, 'ID'] = updated_df.loc[mask, 'ID'].str.replace(r'LPIZAYAVKINAPRO-(\d+)', r'\1', regex=True)

                updated_df.to_excel(file, index=False)
                print(f"Данные успешно сохранены в {file}")
            else:
                print("Нет JSON данных для сохранения")
        except Exception as e:
            print(f"Ошибка при сохранении в Excel: {str(e)}")

    @property
    def GetDf(self):
        """
        Сохранение данных в Excel файл

        :param file: Путь к файлу Excel
        """
        if not self.messages:
            print("Нет данных для сохранения")
            return

        try:
            # Создаем DataFrame из JSON данных
            json_data = [msg['json'] for msg in self.messages if msg.get('json')]
            print(json_data)
            if json_data:
                df = pd.DataFrame(json_data)

                df['ID'] = df['ID'].str.extract(r'(\d+)')[0]
                print("Таблица успешно сформирована")
                return df

            else:
                print("Нет JSON данных для сохранения")
        except Exception as e:
            print(f"Ошибка чтения информации: {str(e)}")

