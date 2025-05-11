import sys

from Gen_9.service.appwin import window, app

if __name__ == "__main__":

    # mail_exp = GetMail(search='SUBJECT "111"')
    # # Получение и обработка писем
    # messages = mail_exp.process_messages()

   window.show()
   sys.exit(app.exec())




