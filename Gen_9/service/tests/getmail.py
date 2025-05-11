import imaplib
import email
from email.header import decode_header
import chardet

class GetMail:
    def __init__(self, folder=None, email_adress=None, password=None):
        if folder is None:
            self.folder = 'LPITrack'
        else:
            self.folder = folder
        if email_adress is None:
            self.email_adress = 'lpitn@ya.ru'
        else:
            self.email_adress = email_adress
        if password is None:
            self.password = 'zrhuyzsfvvvkztlf'

    def fetch_yandex_mails(self):
        with imaplib.IMAP4_SSL("imap.yandex.ru") as mail:
            mail.login(self.email_adress, self.password)
            mail.select(self.folder)  # Или другая папка

            _, data = mail.search(None, "ALL")
            mail_ids = data[0].split()

            messages = []
            for num in mail_ids[-10:]:  # Последние 10 писем
                _, data = mail.fetch(num, "(RFC822)")
                raw_email = data[0][1]
                msg = email.message_from_bytes(raw_email)

                text = ''
                if msg.is_multipart():
                    for part in msg.walk():
                        if part.get_content_type() == 'text/plain':
                            text = part.get_payload(decode=True).decode()
                            break
                else:
                    text = msg.get_payload(decode=True).decode()

                messages.append({
                    "subject": msg["Subject"],
                    "text": text
                })
            return messages

    def decode_email_header(self, header = None):
        if header is None:
            return ""

        try:
            decoded_parts = decode_header(header)
            result = []
            for part, encoding in decoded_parts:
                if isinstance(part, bytes):
                    # Автоопределение кодировки, если не указана
                    if not encoding:
                        encoding = chardet.detect(part)['encoding'] or 'utf-8'
                    part = part.decode(encoding)
                result.append(part)
            return ' '.join(result).strip()
        except:
            return str(header)

    def process_messages(self, messages=None):
        if messages is None:
            messages = self.fetch_yandex_mails()

        readable_messages = []
        for msgs in messages:
            readable_messages.append({
                'subject': self.decode_email_header(msgs['subject'])
            })
        return readable_messages

r = GetMail()
f = r.process_messages()
print(f)
inc_list = []
for i in f:
    k = i['subject']
    n = k.split(',')
    n = [x.replace('LPIZAYAVKINAPRO-', '') for x in n]
    inc_list.append(n)
    [idn, ekn, num] = n
print(inc_list)