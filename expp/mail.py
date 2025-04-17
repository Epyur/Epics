import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders

# Настройки для Яндекс.Почты
smtp_server = 'smtp.yandex.ru'
smtp_port = 465  # Для SSL-подключения

# Данные для авторизации
email = 'lpitn@ya.ru'
password = 'zrhuyzsfvvvkztlf'

# Создаем сообщение
msg = MIMEMultipart()
msg['From'] = email
msg['To'] = 'epyur@ya.ru'  # Адрес получателя
msg['Subject'] = 'Тема письма'

# Текст письма
msg.attach(MIMEText('Текст вашего сообщения', 'plain'))

# Добавляем вложение
file_path = r'C:\Users\epyur\PycharmProjects\PythonProject\Gen_8\out\91\91v.docx'
with open(file_path, 'rb') as file:
    part = MIMEBase('application', 'octet-stream')
    part.set_payload(file.read())
    encoders.encode_base64(part)
    part.add_header('Content-Disposition', f"attachment; filename={file_path}")
    msg.attach(part)

# Отправляем письмо
try:
    with smtplib.SMTP_SSL(smtp_server, smtp_port) as server:
        server.login(email, password)
        server.send_message(msg)
        print("Письмо успешно отправлено!")
except Exception as e:
    print(f"Ошибка при отправке письма: {str(e)}")
