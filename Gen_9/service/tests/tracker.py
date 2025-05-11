import imaplib
import email
from email.header import decode_header
from email.utils import parseaddr
import chardet
import threading
from datetime import datetime
import json
import os
from typing import List, Dict, Optional, Union


class IMAPClient:
    def __init__(self, host: str = 'imap.yandex.ru', port: int = 993):
        self.password = None
        self.username = None
        self.host = host
        self.port = port
        self.connection = None
        self.lock = threading.Lock()
        self.cache_file = 'imap_cache.json'

    def connect(self, username: str = None, password: str = None) -> bool:
        """Установка соединения с IMAP-сервером"""
        self.username = username
        if username is None:
            self.username = 'lpitn@ya.ru'
        self.password = password
        if password is None:
            self.password = 'zrhuyzsfvvvkztlf'
        try:
            with self.lock:
                self.connection = imaplib.IMAP4_SSL(self.host, self.port)
                self.connection.login(username, password)
                return True
        except Exception as e:
            print(f"Connection error: {str(e)}")
            return False

    def disconnect(self):
        """Закрытие соединения"""
        if self.connection:
            try:
                self.connection.close()
                self.connection.logout()
            except:
                pass
            finally:
                self.connection = None

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.disconnect()

    @staticmethod
    def decode_header(header: Union[str, bytes]) -> str:
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
            print(f"Header decode error: {str(e)}")
            return str(header)

    def get_messages(self, folder: str = 'INBOX', limit: int = 10, use_cache: bool = True) -> List[Dict]:
        """Получение списка сообщений с декодированием"""
        if use_cache and self._load_cache(folder, limit):
            return self.cached_messages

        if not self.connection:
            raise ConnectionError("Not connected to IMAP server")

        try:
            with self.lock:
                self.connection.select(folder)
                _, data = self.connection.search(None, 'ALL')
                message_ids = data[0].split()

                messages = []
                for num in message_ids[-limit:][::-1]:  # Последние N писем (новые сначала)
                    _, msg_data = self.connection.fetch(num, '(RFC822)')
                    raw_email = msg_data[0][1]
                    msg = email.message_from_bytes(raw_email)

                    messages.append(self._parse_message(msg))

                if use_cache:
                    self._save_cache(messages, folder, limit)

                return messages

        except Exception as e:
            print(f"Fetch error: {str(e)}")
            return []

    def _parse_message(self, msgs: email.message.Message) -> Dict:
        """Разбор отдельного сообщения"""
        subject = self.decode_header(msgs.get('Subject', ''))
        from_ = self.decode_header(msgs.get('From', ''))
        date = msgs.get('Date', '')
        to = self.decode_header(msgs.get('To', ''))

        # Парсинг отправителя
        sender_name, sender_email = parseaddr(from_)
        if not sender_email and '<' in from_:
            sender_email = from_.split('<')[-1].split('>')[0]

        # Получение текста письма
        body = self._get_message_body(msgs)

        return {
            'subject': subject,
            'from': from_,
            'sender_name': sender_name,
            'sender_email': sender_email,
            'to': to,
            'date': date,
            'body': body,
            'attachments': self._get_attachments(msgs)
        }

    def _get_message_body(self, msg: email.message.Message) -> str:
        """Извлечение текста письма"""
        if msg.is_multipart():
            for part in msg.walk():
                content_type = part.get_content_type()
                if content_type == "text/plain":
                    return part.get_payload(decode=True).decode('utf-8', errors='replace')
        else:
            return msg.get_payload(decode=True).decode('utf-8', errors='replace')
        return ""

    def _get_attachments(self, msg: email.message.Message) -> List[Dict]:
        """Получение вложений"""
        attachments = []
        if msg.is_multipart():
            for part in msg.walk():
                if part.get_content_disposition() == 'attachment':
                    filename = self.decode_header(part.get_filename())
                    if filename:
                        attachments.append({
                            'filename': filename,
                            'size': len(part.get_payload(decode=True)),
                            'content_type': part.get_content_type()
                        })
        return attachments

    def _save_cache(self, messages: List[Dict], folder: str, limit: int):
        """Сохранение в кеш"""
        cache_data = {
            'timestamp': datetime.now().isoformat(),
            'folder': folder,
            'limit': limit,
            'messages': messages
        }
        try:
            with open(self.cache_file, 'w') as f:
                json.dump(cache_data, f)
        except Exception as e:
            print(f"Cache save error: {str(e)}")

    def _load_cache(self, folder: str, limit: int) -> bool:
        """Загрузка из кеша"""
        if not os.path.exists(self.cache_file):
            return False

        try:
            with open(self.cache_file) as f:
                cache_data = json.load(f)

            if (cache_data['folder'] == folder and
                    cache_data['limit'] >= limit and
                    (datetime.now() - datetime.fromisoformat(cache_data['timestamp'])).seconds < 3600):
                self.cached_messages = cache_data['messages'][:limit]
                return True
        except Exception as e:
            print(f"Cache load error: {str(e)}")

        return False


# Пример использования
if __name__ == "__main__":
    with IMAPClient() as client:
        if client.connect():
            messages = client.get_messages(limit=5)

            for idx, msg in enumerate(messages, 1):
                print(f"\nПисьмо #{idx}")
                print(f"Тема: {msg['subject']}")
                print(f"От: {msg['sender_name']} <{msg['sender_email']}>")
                print(f"Кому: {msg['to']}")
                print(f"Дата: {msg['date']}")
                print(f"\nТекст:\n{msg['body'][:200]}...")

                if msg['attachments']:
                    print(f"\nВложения ({len(msg['attachments'])}):")
                    for att in msg['attachments']:
                        print(f"- {att['filename']} ({att['size']} bytes)")