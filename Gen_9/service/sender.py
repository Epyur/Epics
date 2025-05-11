import requests
import smtplib
import os
from requests.exceptions import RequestException
from typing import Dict, Any, Optional, List, Union
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders

from Gen_9.service.passw.passw import *




class NotificationSender:
    def __init__(
            self,
            subject,
            text,
            smtp_server: str = 'smtp.yandex.ru',
            smtp_port: int = 465,
            email: str = None,
            password: str = None,
            telegram_token: str = None,
            telegram_chat_id: str = None,
            file_path = None
    ):
        """
        Инициализация отправителя уведомлений

        :param smtp_server: SMTP сервер для email
        :param smtp_port: Порт SMTP сервера
        :param email: Email отправителя
        :param password: Пароль от почты
        :param telegram_token: Токен бота Telegram
        :param telegram_chat_id: ID чата/канала Telegram
        """
        self.text = text
        self.smtp_server = smtp_server
        self.smtp_port = smtp_port
        self.subject = subject
        self.email = email
        if self.email is None:
            self.email = mail_login
        self.password = password
        if self.password is None:
            self.password = mail_pass
        self.telegram_token = telegram_token
        if self.telegram_token is None:
            self.telegram_token = tg_token
        self.telegram_chat_id = telegram_chat_id
        if self.telegram_chat_id is None:
            self.telegram_chat_id = '-1002668536527'
        self.file_path = file_path

    def send_email(
            self,
            subject: str,
            text: str,
            recipient: str,
            attachments: Optional[List[dict]] = None,
            cc_recipients: Optional[List[str]] = None,
            bcc_recipients: Optional[List[str]] = None
    ) -> bool:
        """
        Отправка email с вложениями

        :param subject: Тема письма
        :param recipient: Получатель (или список получателей)
        :param attachments: Список вложений [{'path': 'file.txt', 'name': 'doc.txt'}]
        :param cc_recipients: Копия письма
        :param bcc_recipients: Скрытая копия
        :return: Успешность отправки
        """
        self.text = text
        self.attachment = attachments
        if self.file_path is not None:
            self.attachment = {'path': self.file_path}
        # Создаем сообщение
        msg = MIMEMultipart()
        msg['From'] = self.email
        msg['To'] = recipient if isinstance(recipient, str) else ', '.join(recipient)
        msg['Subject'] = subject

        if cc_recipients:
            msg['Cc'] = ', '.join(cc_recipients)
        if bcc_recipients:
            msg['Bcc'] = ', '.join(bcc_recipients)

        # Текст письма
        msg.attach(MIMEText(self.text, 'plain'))

        # Добавляем вложения
        if attachments:
            for attachment in attachments:
                self._add_attachment(msg, self.attachment['path'], self.attachment.get('name'))

        # Отправляем письмо
        try:
            with smtplib.SMTP_SSL(self.smtp_server, self.smtp_port) as server:
                server.login(self.email, self.password)
                recipients = self._prepare_recipients(recipient, cc_recipients, bcc_recipients)
                server.sendmail(self.email, recipients, msg.as_string())
                print("Письмо успешно отправлено!")
                return True
        except Exception as e:
            print(f"Ошибка при отправке письма: {str(e)}")
            return False

    def _add_attachment(self, msg: MIMEMultipart, file_path: str, file_name: Optional[str] = None) -> None:
        self.file_path = file_path
        """Добавляет вложение к письму"""
        if not os.path.exists(self.file_path):
            raise FileNotFoundError(f"Файл не найден: {self.file_path}")

        with open(self.file_path, 'rb') as file:
            part = MIMEBase('application', 'octet-stream')
            part.set_payload(file.read())
            encoders.encode_base64(part)

            filename = file_name if file_name else os.path.basename(self.file_path)
            part.add_header(
                'Content-Disposition',
                f'attachment; filename="{filename}"'
            )
            msg.attach(part)

    def _prepare_recipients(
            self,
            to: Union[str, List[str]],
            cc: Optional[List[str]] = None,
            bcc: Optional[List[str]] = None
    ) -> List[str]:
        """Подготавливает список всех получателей"""
        recipients = [to] if isinstance(to, str) else to.copy()
        if cc:
            recipients.extend(cc)
        if bcc:
            recipients.extend(bcc)
        return recipients

    def send_telegram_message(
            self,
            text: str,
            topic_id: Optional[int] = None,
            file_path: Optional[str] = None,
            parse_mode: Optional[str] = None,
            disable_notification: bool = False
    ) -> Optional[Dict[str, Any]]:
        """
        Отправка сообщения в Telegram

        :param text: Текст сообщения
        :param topic_id: ID темы в группе/канале (опционально)
        :param file_path: Путь к файлу для отправки (опционально)
        :param parse_mode: Форматирование ('Markdown', 'HTML' или None)
        :param disable_notification: Отключить уведомление
        :return: Ответ API Telegram или None при ошибке
        """
        self.file_path = file_path
        self.text = text
        if not self.telegram_token or not self.telegram_chat_id:
            print("Ошибка: не заданы токен или chat_id Telegram")
            return None

        method = 'sendDocument' if self.file_path else 'sendMessage'
        url = f'https://api.telegram.org/bot{self.telegram_token}/{method}'

        params = {
            'chat_id': self.telegram_chat_id,
            'text': self.text,
            'disable_notification': str(disable_notification).lower()
        }

        if topic_id:
            params['message_thread_id'] = topic_id
        if parse_mode:
            params['parse_mode'] = parse_mode

        try:
            if self.file_path:
                if not os.path.exists(self.file_path):
                    print(f"Ошибка: файл {self.file_path} не существует")
                    return None

                with open(self.file_path, 'rb') as file:
                    files = {'document': file}
                    params['caption'] = self.text
                    response = requests.post(url, data=params, files=files)
            else:
                response = requests.post(url, params=params)

            response.raise_for_status()
            return response.json()

        except RequestException as e:
            print(f"Ошибка при отправке сообщения в Telegram: {e}")
            return None
        except Exception as e:
            print(f"Неожиданная ошибка: {e}")
            return None


# Пример использования
if __name__ == "__main__":
    notifier = NotificationSender(
        email="your_email@yandex.ru",
        password="your_password",
        telegram_token="your_telegram_bot_token",
        telegram_chat_id="your_chat_id"
    )

    # Отправка текстового сообщения
    notifier.send_telegram_message(
        text="Важное уведомление!",
        topic_id=123  # Если нужно отправить в конкретную тему
    )

    # Отправка файла с подписью
    notifier.send_telegram_message(
        text="Отчет во вложении",
        file_path="/path/to/report.pdf"
    )