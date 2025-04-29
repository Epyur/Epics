import wx
import service.def_lib
from service.router import *
from service.rout_map import *
from service.router import process_input_value


class ExampleApp(wx.Frame):
    def __init__(self, *args, **kwargs):
        super(ExampleApp, self).__init__(*args, **kwargs)
        self.initUI()

    def initUI(self):
        self.title = 'Лаборатория пожарных испытаний ver.8&3/4'
        self.size = (450, 500)  # Увеличили высоту окна для размещения чекбоксов
        self.SetSize(*self.size)
        self.SetTitle('LPI TN')

        self.panel = wx.Panel(self)

        # Создание поясняющего текста
        self.staticText = wx.StaticText(self.panel, label="Введите служебный идентификатор заявки:", pos=(70, 20))

        # Создание поля ввода
        self.textCtrl = wx.TextCtrl(self.panel, pos=(50, 50), size=(350, -1))

        # Создание чекбоксов
        self.checkbox1 = wx.CheckBox(self.panel, label='Отправить результаты по ГОСТ 30244 на shoya.vs@tn.ru', pos=(50, 80))
        self.checkbox4 = wx.CheckBox(self.panel, label='Отправить результаты по ГОСТ 30402 на shoya.vs@tn.ru', pos=(50, 100))
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

    def onButtonClick(self, event):
        try:
            text_in = self.textCtrl.GetValue()
            try:
                input_list = [item.strip() for item in text_in.split(',')]
                for val in input_list:
                    value = int(val)

                    # Проверяем состояния чекбоксов
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

                    processed_value = process_input_value(value, selected_options)

                    self.messageCtrl.SetValue(f"ID заявки: {value}\n"
                                              f"Выбранные опции: {', '.join(selected_options)}\n"
                                              f"{processed_value}")
            except:
                value = int(text_in)


                # Проверяем состояния чекбоксов
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

                processed_value = process_input_value(value, selected_options)

                self.messageCtrl.SetValue(f"ID заявки: {value}\n"
                                          f"Выбранные опции: {', '.join(selected_options)}\n"
                                          f"{processed_value}")
        except ValueError as e:
            self.messageCtrl.SetValue(f"Пожалуйста, введите целое число или список целых чисел через запятую. {e}")
        finally:
            self.textCtrl.SetValue('')
            # Сбрасываем состояния чекбоксов
            self.checkbox1.SetValue(False)
            self.checkbox2.SetValue(False)
            self.checkbox3.SetValue(False)


# Создание экземпляра приложения перед главным циклом
app = wx.App()

if __name__ == '__main__':
    # start_list = [40]
    # for i in start_list:
    #     process_input_value(i)
    ex = ExampleApp(None)
    app.MainLoop()

