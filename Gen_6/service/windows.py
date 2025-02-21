import wx

def process_input_number(number):
    """Функция для обработки введенного целого числа."""
    print(f"Обработанное значение: {number}")
    return number * 2  # Пример обработки: умножение числа на 2

class ExampleApp(wx.Frame):
    def __init__(self, *args, **kwargs):
        super(ExampleApp, self).__init__(*args, **kwargs)
        self.initUI()

    def initUI(self):
        self.title = 'Пример приложения WxPython с полем ввода целого числа'
        self.size = (400, 300)
        self.SetSize(*self.size)
        self.SetTitle('Пример приложения WxPython')

        self.panel = wx.Panel(self)

        # Создание кнопки
        self.button = wx.Button(self.panel, label='Нажми меня', pos=(100, 100))

        # Создание поля ввода (текстового поля)
        self.textCtrl = wx.TextCtrl(self.panel, pos=(100, 150), size=(100, -1))

        # Привязка события нажатия на кнопку
        self.button.Bind(wx.EVT_BUTTON, self.onButtonClick)

        # Создание второго поля ввода для вывода сообщений
        self.messageCtrl = wx.TextCtrl(self.panel, pos=(100, 250), size=(200, -1),
                                       style=wx.TE_MULTILINE | wx.TE_READONLY)

        # Показать окно
        self.Show()

    def onButtonClick(self, event):
        # Попытка преобразования текста из поля ввода в целое число
        try:
            value = int(self.textCtrl.GetValue())

            # Вызов функции для обработки числа
            processed_value = process_input_number(value)

            self.messageCtrl.SetValue(f"Введенное значение: {value}\nОбработанное значение: {processed_value}")
        except ValueError:
            self.messageCtrl.SetValue("Пожалуйста, введите целое число.")
        finally:
            # Очистка поля ввода
            self.textCtrl.SetValue('')

# Создание экземпляра приложения перед главным циклом
app = wx.App()

if __name__ == '__main__':
    ex = ExampleApp(None)
    app.MainLoop()