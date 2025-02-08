import wx

class ExampleApp(wx.Frame):
    def __init__(self, *args, **kwargs):
        super(ExampleApp, self).__init__(*args, **kwargs)
        self.initUI()

    def initUI(self):
        self.title = 'Пример приложения WxPython с полем ввода'
        self.size = (400, 300)
        self.SetSize(*self.size)
        self.SetTitle('Пример приложения WxPython')

        self.panel = wx.Panel(self)

        # Создание кнопки
        self.button = wx.Button(self.panel, label='Нажми меня', pos=(100, 100))

        # Создание поля ввода (текстового поля)
        self.textCtrl = wx.TextCtrl(self.panel, pos=(100, 150), size=(200, -1))

        # Привязка события нажатия на кнопку
        self.button.Bind(wx.EVT_BUTTON, self.onButtonClick)

        # Показать окно
        self.Show()

    def onButtonClick(self, event):
        # Получение текста из поля ввода
        value = int(self.textCtrl.GetValue())
        return value

        # Обновление метки с текстом из поля ввода при нажатии на кнопку
        self.textCtrl.SetValue('')

app = wx.App()