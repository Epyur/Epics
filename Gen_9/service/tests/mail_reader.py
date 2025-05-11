import imaplib
import email
from email.header import decode_header
import chardet
from typing import List, Dict, Optional
from email.message import Message


class GetMail:
    def __init__(self, folder: str = 'LPITrack',
                 email_address: str = 'lpitn@ya.ru',
                 password: str = 'zrhuyzsfvvvkztlf'):
        """
        Инициализация подключения к почте

        :param folder: Папка для поиска писем (по умолчанию 'LPITrack')
        :param email_address: Адрес электронной почты
        :param password: Пароль или токен приложения
        """
        self.folder = folder
        self.email_address = email_address
        self.password = password

    def fetch_yandex_mails(self, limit: int = 10) -> List[Dict]:
        """
        Получение писем с сервера

        :param limit: Количество последних писем
        :return: Список сообщений
        """
        messages = []

        try:
            with imaplib.IMAP4_SSL("imap.yandex.ru") as mail:
                mail.login(self.email_address, self.password)
                mail.select(self.folder)

                _, data = mail.search(None, "ALL")
                mail_ids = data[0].split()

                for num in mail_ids[-limit:]:  # Последние limit писем
                    _, msg_data = mail.fetch(num, "(RFC822)")
                    raw_email = msg_data[0][1]
                    msg = email.message_from_bytes(raw_email)

                    # Обработка текста письма
                    text = self._extract_email_text(msg)

                    messages.append({
                        "subject": self.decode_email_header(msg.get("Subject", "")),
                        "from": self.decode_email_header(msg.get("From", "")),
                        "date": msg.get("Date", ""),
                        "text": text
                    })

        except Exception as e:
            print(f"Ошибка при получении писем: {str(e)}")

        return messages

    def _extract_email_text(self, msg: email.message.Message) -> str:
        """Извлечение текста письма с обработкой кодировки"""
        text = ""

        if msg.is_multipart():
            for part in msg.walk():
                content_type = part.get_content_type()
                content_disposition = str(part.get("Content-Disposition", ""))

                if "attachment" not in content_disposition and content_type == "text/plain":
                    text = self._decode_payload(part)
                    break
        else:
            text = self._decode_payload(msg)

        return text

    def _decode_payload(self, part: email.message.Message) -> str:
        """Декодирование содержимого письма"""
        payload = part.get_payload(decode=True)
        charset = part.get_content_charset() or 'utf-8'

        try:
            return payload.decode(charset)
        except UnicodeDecodeError:
            try:
                # Попробуем определить кодировку автоматически
                detected = chardet.detect(payload)
                return payload.decode(detected['encoding'] or 'utf-8', errors='replace')
            except:
                return payload.decode('utf-8', errors='replace')

    def decode_email_header(self, header: Optional[str] = None) -> str:
        """
        Декодирование email-заголовков

        :param header: Заголовок для декодирования
        :return: Декодированная строка
        """
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

    def process_messages(self, messages: Optional[List[Dict]] = None) -> List[Dict]:
        """
        Обработка сообщений с декодированием заголовков

        :param messages: Список сообщений (если None, будет загружен из почты)
        :return: Обработанные сообщения
        """
        if messages is None:
            messages = self.fetch_yandex_mails()

        return [{
            'subject': self.decode_email_header(msg.get('subject', '')),
            'from': self.decode_email_header(msg.get('from', '')),
            'date': msg.get('date', ''),
            'text': msg.get('text', '')
        } for msg in messages]


# Пример использования
if __name__ == "__main__":
    mail_client = GetMail()

    # Получаем и обрабатываем письма
    messages = mail_client.process_messages()

    strq = messages[0]['subject'].replace('|', ',').replace('FW: ', '').replace(' LPIZAYAVKINAPRO-', '').replace('Наименование материала/ЕКН:', '').split(',')
    print(strq)