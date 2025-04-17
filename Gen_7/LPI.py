import wx
from Gen_7.service.router import *

from Gen_7.service.rout_map import *
from Gen_7.service.router import process_input_value

class ExampleApp(wx.Frame):
    def __init__(self, *args, **kwargs):
        super(ExampleApp, self).__init__(*args, **kwargs)
        self.initUI()

    def initUI(self):
        self.title = 'Лаборатория пожарных испытаний ver.7'
        self.size = (400, 300)
        self.SetSize(*self.size)
        self.SetTitle('LPI TN')

        self.panel = wx.Panel(self)

        # Создание поясняющего текста
        self.staticText = wx.StaticText(self.panel, label="Введите служебный идентификатор заявки:", pos=(70, 20))

        # Создание кнопки
        self.button = wx.Button(self.panel, label='Сформировать отчет', pos=(190, 50))

        # Создание поля ввода (текстового поля)
        self.textCtrl = wx.TextCtrl(self.panel, pos=(80, 50), size=(100, -1))

        # Привязка события нажатия на кнопку
        self.button.Bind(wx.EVT_BUTTON, self.onButtonClick)

        # Создание второго поля ввода для вывода сообщений
        self.messageCtrl = wx.TextCtrl(self.panel, pos=(0, 90), size=(400, 310),
                                       style=wx.TE_MULTILINE | wx.TE_READONLY)

        # Показать окно
        self.Show()

    def onButtonClick(self, event):
        # Попытка преобразования текста из поля ввода в целое число
        try:
            value = int(self.textCtrl.GetValue())
            # Вызов функции для обработки числа
            processed_value = process_input_value(value)

            self.messageCtrl.SetValue(f"ID заявки: {value}\n{processed_value}")
        except ValueError as e:
            self.messageCtrl.SetValue(f"Пожалуйста, введите целое число. {e}")
        finally:
            # Очистка поля ввода
            self.textCtrl.SetValue('')


# Создание экземпляра приложения перед главным циклом
app = wx.App()

if __name__ == '__main__':
    # for i in range(1, 67):
    #     process_input_value(i)
    ex = ExampleApp(None)
    app.MainLoop()

