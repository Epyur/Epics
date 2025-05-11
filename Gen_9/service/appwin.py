import sys
from openpyxl import load_workbook
import pandas as pd
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import (QMessageBox, QMainWindow, QApplication,
                             QVBoxLayout, QHBoxLayout, QWidget)
from PyQt6 import QtCore, QtGui, QtWidgets


from Gen_9.service.passw.passw import mail_login, mail_pass, tracker_adress
from Gen_9.service.rout_map import ns, closedtasks, alltasks
from Gen_9.service.sender import NotificationSender


class RequestDataModel:
    """Класс для работы с данными заявок"""

    def __init__(self):
        self.all_tasks_df = None
        self.closed_tasks_df = None
        self.combined_df = None
        self.current_request_id = None

    def load_data(self):
        """Загрузка данных из файлов"""
        try:
            self.all_tasks_df = pd.read_excel(alltasks)
            self.closed_tasks_df = pd.read_excel(closedtasks)

            print(f"Загружено из alltasks: {len(self.all_tasks_df)} записей")
            print(f"Загружено из closedtasks: {len(self.closed_tasks_df)} записей")

            self._combine_data()
            return True
        except Exception as e:
            print(f"Ошибка загрузки данных: {e}")
            return False

    def _combine_data(self):
        """Объединение данных с приоритетом alltasks"""
        if self.all_tasks_df is None or self.closed_tasks_df is None:
            return

        combined = pd.concat([self.all_tasks_df, self.closed_tasks_df])
        self.combined_df = combined.drop_duplicates(subset=[ns[8]], keep='first').copy()

        try:
            self.combined_df[ns[8]] = pd.to_numeric(self.combined_df[ns[8]])
            self.combined_df = self.combined_df.sort_values(by=ns[8], ascending=False)
        except:
            self.combined_df = self.combined_df.sort_values(by=ns[8], ascending=False, key=lambda x: x.astype(str))

    def get_request_data(self, request_id):
        """Получение данных конкретной заявки"""
        if self.combined_df is None:
            return None

        mask = self.combined_df[ns[8]].astype(str) == str(request_id)
        if mask.any():
            return self.combined_df[mask].iloc[0].to_dict()
        return None

    def update_request_field(self, request_id, field_name, new_value):
        """Обновление поля заявки"""
        if self.all_tasks_df is None:
            return False

        mask = self.all_tasks_df[ns[8]].astype(str) == str(request_id)
        if mask.any():
            self.all_tasks_df.loc[mask, field_name] = new_value
            try:
                self.all_tasks_df.to_excel(alltasks, index=False)
                self.load_data()  # Перезагружаем данные
                return True
            except Exception as e:
                print(f"Ошибка сохранения: {e}")
        return False

    def is_request_closed(self, request_id):
        """Проверка, закрыта ли заявка"""
        if self.closed_tasks_df is None:
            return False
        return request_id in self.closed_tasks_df[ns[8]].values


class RequestController:
    """Класс-контроллер для управления логикой работы с заявками"""

    def __init__(self, model, view):
        self.model = model
        self.view = view
        self.current_request_id = None

    def initialize(self):
        """Инициализация данных"""
        if not self.model.load_data():
            self.view.show_error_message("Ошибка загрузки данных")
            return False
        self.view.update_request_list(self.model.combined_df)
        return True

    def select_request(self, request_id):
        """Выбор заявки для отображения"""
        self.current_request_id = request_id
        request_data = self.model.get_request_data(request_id)
        if request_data:
            self.view.display_request_data(request_data)
            self.view.update_close_button_state(not self.model.is_request_closed(request_id))
        else:
            self.view.show_error_message("Данные заявки не найдены")

    def save_request_changes(self, field_name, new_value):
        """Сохранение изменений в заявке"""
        if self.current_request_id is None:
            return

        if self.model.update_request_field(self.current_request_id, field_name, new_value):
            self.view.show_success_message("Изменения сохранены")
            self.view.update_request_list(self.model.combined_df)  # Обновляем список
        else:
            self.view.show_error_message("Не удалось сохранить изменения")

    def close_current_request(self):
        """Закрытие текущей заявки"""
        if self.current_request_id is None:
            self.view.show_error_message("Не выбрана заявка для закрытия")
            return

        if self.model.is_request_closed(self.current_request_id):
            self.view.show_error_message("Эта заявка уже закрыта")
            return

        request_data = self.model.get_request_data(self.current_request_id)
        if not request_data:
            self.view.show_error_message("Данные заявки не найдены")
            return

        if self._send_close_notification(request_data):
            self.view.show_success_message("Уведомление о закрытии отправлено")
            self.view.update_close_button_state(False)
        else:
            self.view.show_error_message("Не удалось отправить уведомление")

    def _send_close_notification(self, request_data):
        """Отправка уведомления о закрытии заявки"""
        try:
            request_id = str(request_data.get(ns[8], ''))
            subject = f"Заявка LPIZAYAVKINAPRO-{request_id} закрыта"
            body = "end point"

            sender = NotificationSender(
                subject=subject,
                text=body,
                email=mail_login,
                password=mail_pass
            )

            return sender.send_email(
                subject=subject,
                text=body,
                recipient=tracker_adress
            )
        except Exception as e:
            print(f"Ошибка отправки уведомления: {e}")
            return False


class RequestView:
    """Класс представления (интерфейса)"""

    def __init__(self, main_window):
        self.main_window = main_window
        self.ui = Ui_LPIApp()
        self.ui.setupUi(self.main_window)
        self.controller = None

    def set_controller(self, controller):
        """Установка контроллера"""
        self.controller = controller
        self._connect_signals()

    def _connect_signals(self):
        """Подключение сигналов"""
        self.ui.listWidget.itemClicked.connect(self._on_request_selected)
        self.ui.saveButton.clicked.connect(self._on_save_changes)
        self.ui.refreshButton.clicked.connect(self._on_refresh)
        self.ui.closeRequestButton.clicked.connect(self._on_close_request)
        self.ui.listWidget.itemDoubleClicked.connect(self._on_double_click)

    def update_request_list(self, requests_df):
        """Обновление списка заявок"""
        self.ui.listWidget.clear()

        if requests_df is None or requests_df.empty:
            return

        for _, row in requests_df.iterrows():
            request_id = str(row.get(ns[8], ''))
            ident_num = str(row.get(ns[13], ''))
            material_name = str(row.get(ns[15], ''))

            item_text = f"{request_id} | {ident_num}, {material_name}"
            item = QtWidgets.QListWidgetItem(item_text)

            if self.controller.model.is_request_closed(row[ns[8]]):
                item.setForeground(QtGui.QColor('orange'))
                item.setToolTip("Заявка закрыта")

            self.ui.listWidget.addItem(item)

    def display_request_data(self, request_data):
        """Отображение данных заявки"""
        self.ui.IncIDWidjget.setPlainText(str(request_data.get(ns[8], '')))
        self.ui.CustNameWidget.setPlainText(str(request_data.get(ns[11], '')).strip())
        self.ui.CustMailWidget.setPlainText(str(request_data.get(ns[10], '')).strip())
        self.ui.CustTelWidget.setPlainText(str(request_data.get(ns[95], '')).strip())
        self.ui.DateINWidget.setPlainText(str(request_data.get(ns[3], '')).strip())
        self.ui.EknNumWidget.setPlainText(str(request_data.get(ns[14], '')).strip())
        self.ui.IdentNumWidget.setPlainText(str(request_data.get(ns[13], '')).strip())
        self.ui.EknNum_2.setPlainText(str(request_data.get(ns[15], '')).strip())
        self.ui.AdditionalnfoWidget.setPlainText(str(request_data.get(ns[20], '')).strip())

        self._update_method_indicators(request_data)

    def _update_method_indicators(self, request_data):
        """Обновление индикаторов методов испытаний"""
        aim_value = str(request_data.get(ns[1], '')).strip().lower()

        comb_keywords = ['горючест', 'combust', 'ггру', 'гост 30244']
        flam_keywords = ['воспламеняемост', 'flammab', 'вспл', 'гост 30402']

        comb_active = any(keyword in aim_value for keyword in comb_keywords)
        flam_active = any(keyword in aim_value for keyword in flam_keywords)

        self._set_indicator_style(self.ui.CombGOSTButton, comb_active)
        self._set_indicator_style(self.ui.FlamGOSTButton, flam_active)

    def _set_indicator_style(self, indicator, is_active):
        """Установка стиля индикатора с сохранением круглой формы"""
        color = "green" if is_active else "red"
        indicator.setStyleSheet(f"""
            QRadioButton {{
                color: {color};
                font-weight: bold;
                text-decoration: underline;
                spacing: 8px;  /* Расстояние между индикатором и текстом */
            }}
            QRadioButton::indicator {{
                width: 16px;
                height: 16px;
                border-radius: 8px;  /* Круглая форма */
                background-color: {color};
                border: 1px solid dark{color};
            }}
            QRadioButton::indicator:checked {{
                image: none;  /* Отключаем стандартную галочку */
            }}
        """)

    def update_close_button_state(self, enabled):
        """Обновление состояния кнопки закрытия заявки"""
        self.ui.closeRequestButton.setEnabled(enabled)

    def show_error_message(self, message):
        """Показать сообщение об ошибке"""
        QMessageBox.critical(self.main_window, "Ошибка", message)

    def show_success_message(self, message):
        """Показать сообщение об успехе"""
        QMessageBox.information(self.main_window, "Успех", message)

    def _on_request_selected(self, item):
        """Обработчик выбора заявки"""
        if self.controller is None:
            return

        request_id = item.text().split('|')[0].strip()
        self.controller.select_request(request_id)

    def _on_double_click(self, item):
        """Обработчик двойного клика по заявке"""
        request_data = self.controller.model.get_request_data(item.text().split('|')[0].strip())
        if request_data:
            info = "\n".join([f"{col}: {val}" for col, val in request_data.items()])
            QMessageBox.information(self.main_window, "Полная информация", info)

    def _on_save_changes(self):
        """Обработчик сохранения изменений"""
        if self.controller is None or self.controller.current_request_id is None:
            self.show_error_message("Не выбрана заявка для сохранения")
            return

        ident_num = self.ui.IdentNumWidget.toPlainText().strip()
        material_name = self.ui.EknNum_2.toPlainText().strip()

        self.controller.save_request_changes(ns[13], ident_num)
        self.controller.save_request_changes(ns[15], material_name)

    def _on_refresh(self):
        """Обработчик обновления данных"""
        if self.controller is not None and self.controller.initialize():
            self.show_success_message("Данные успешно обновлены")

    def _on_close_request(self):
        """Обработчик закрытия заявки"""
        if self.controller is not None:
            reply = QMessageBox.question(
                self.main_window,
                "Подтверждение",
                "Вы уверены, что хотите закрыть эту заявку?",
                QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
            )

            if reply == QMessageBox.StandardButton.Yes:
                self.controller.close_current_request()


class Ui_LPIApp(object):
    def setupUi(self, LPIApp):
        LPIApp.setObjectName("LPIApp")
        LPIApp.resize(1123, 950)

        # Центральный виджет и основной layout
        self.central_widget = QtWidgets.QWidget(LPIApp)
        self.main_layout = QtWidgets.QHBoxLayout(self.central_widget)

        # Левая панель (список заявок)
        self.left_panel = QtWidgets.QVBoxLayout()

        self.label_15 = QtWidgets.QLabel("Перечень заявок")
        font = QtGui.QFont()
        font.setPointSize(13)
        font.setBold(True)
        self.label_15.setFont(font)
        self.label_15.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.left_panel.addWidget(self.label_15)

        self.listWidget = QtWidgets.QListWidget()
        self.listWidget.setMinimumWidth(290)
        self.left_panel.addWidget(self.listWidget)

        # Кнопки внизу левой панели
        self.button_layout = QtWidgets.QHBoxLayout()
        self.saveButton = QtWidgets.QPushButton("Сохранить изменения")
        self.refreshButton = QtWidgets.QPushButton("Обновить список")

        self.button_layout.addWidget(self.saveButton)
        self.button_layout.addWidget(self.refreshButton)
        self.left_panel.addLayout(self.button_layout)

        self.main_layout.addLayout(self.left_panel)

        # Правая панель (информация о заявке)
        self.right_panel = QtWidgets.QVBoxLayout()

        # Заголовок
        self.label = QtWidgets.QLabel("Лаборатория пожарных испытаний СБЕ ПМиПИР")
        font = QtGui.QFont()
        font.setPointSize(17)
        font.setBold(True)
        font.setItalic(True)
        self.label.setFont(font)
        self.label.setStyleSheet("color: red;")
        self.label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.right_panel.addWidget(self.label)

        # Разделительная линия
        self.line = QtWidgets.QFrame()
        self.line.setFrameShape(QtWidgets.QFrame.Shape.HLine)
        self.line.setFrameShadow(QtWidgets.QFrame.Shadow.Sunken)
        self.right_panel.addWidget(self.line)

        # Основная информация о заявке
        self.form_layout = QtWidgets.QFormLayout()

        # Номер заявки и дата
        self.h_layout_1 = QtWidgets.QHBoxLayout()
        self.label_3 = QtWidgets.QLabel("№ заявки:")
        self.IncIDWidjget = QtWidgets.QPlainTextEdit()
        self.IncIDWidjget.setReadOnly(True)
        self.IncIDWidjget.setFixedHeight(30)
        self.label_6 = QtWidgets.QLabel("Дата поступления:")
        self.DateINWidget = QtWidgets.QPlainTextEdit()
        self.DateINWidget.setReadOnly(True)
        self.DateINWidget.setFixedHeight(30)

        self.h_layout_1.addWidget(self.label_3)
        self.h_layout_1.addWidget(self.IncIDWidjget)
        self.h_layout_1.addWidget(self.label_6)
        self.h_layout_1.addWidget(self.DateINWidget)
        self.form_layout.addRow(self.h_layout_1)

        # Разделитель
        self.line_2 = QtWidgets.QFrame()
        self.line_2.setFrameShape(QtWidgets.QFrame.Shape.HLine)
        self.line_2.setFrameShadow(QtWidgets.QFrame.Shadow.Sunken)
        self.form_layout.addRow(self.line_2)

        # Информация о заказчике
        self.label_5 = QtWidgets.QLabel("Информация о заказчике")
        font = QtGui.QFont()
        font.setPointSize(14)
        font.setItalic(True)
        self.label_5.setFont(font)
        self.label_5.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.form_layout.addRow(self.label_5)

        # ФИО заказчика
        self.label_8 = QtWidgets.QLabel("ФИО заказчика:")
        self.CustNameWidget = QtWidgets.QPlainTextEdit()
        self.CustNameWidget.setReadOnly(True)
        self.CustNameWidget.setFixedHeight(30)
        self.form_layout.addRow(self.label_8, self.CustNameWidget)

        # Почта и телефон
        self.h_layout_2 = QtWidgets.QHBoxLayout()
        self.label_4 = QtWidgets.QLabel("Почта заказчика:")
        self.CustMailWidget = QtWidgets.QPlainTextEdit()
        self.CustMailWidget.setReadOnly(True)
        self.CustMailWidget.setFixedHeight(30)
        self.label_7 = QtWidgets.QLabel("Телефон заказчика:")
        self.CustTelWidget = QtWidgets.QPlainTextEdit()
        self.CustTelWidget.setReadOnly(True)
        self.CustTelWidget.setFixedHeight(30)

        self.h_layout_2.addWidget(self.label_4)
        self.h_layout_2.addWidget(self.CustMailWidget)
        self.h_layout_2.addWidget(self.label_7)
        self.h_layout_2.addWidget(self.CustTelWidget)
        self.form_layout.addRow(self.h_layout_2)

        # Разделитель
        self.line_3 = QtWidgets.QFrame()
        self.line_3.setFrameShape(QtWidgets.QFrame.Shape.HLine)
        self.line_3.setFrameShadow(QtWidgets.QFrame.Shadow.Sunken)
        self.form_layout.addRow(self.line_3)

        # Информация об объекте
        self.label_9 = QtWidgets.QLabel("Информация об объекте исследования")
        self.label_9.setFont(font)
        self.label_9.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.form_layout.addRow(self.label_9)

        # ЕКН и идентификатор
        self.h_layout_3 = QtWidgets.QHBoxLayout()
        self.label_10 = QtWidgets.QLabel("ЕКН:")
        self.EknNumWidget = QtWidgets.QPlainTextEdit()
        self.EknNumWidget.setReadOnly(True)
        self.EknNumWidget.setFixedHeight(30)
        self.label_11 = QtWidgets.QLabel("Идентификатор:")
        self.IdentNumWidget = QtWidgets.QPlainTextEdit()
        self.IdentNumWidget.setFixedHeight(30)

        self.h_layout_3.addWidget(self.label_10)
        self.h_layout_3.addWidget(self.EknNumWidget)
        self.h_layout_3.addWidget(self.label_11)
        self.h_layout_3.addWidget(self.IdentNumWidget)
        self.form_layout.addRow(self.h_layout_3)

        # Название материала
        self.label_13 = QtWidgets.QLabel("Название материала:")
        self.EknNum_2 = QtWidgets.QPlainTextEdit()
        self.EknNum_2.setFixedHeight(60)
        self.form_layout.addRow(self.label_13, self.EknNum_2)

        # Разделитель
        self.line_4 = QtWidgets.QFrame()
        self.line_4.setFrameShape(QtWidgets.QFrame.Shape.HLine)
        self.line_4.setFrameShadow(QtWidgets.QFrame.Shadow.Sunken)
        self.form_layout.addRow(self.line_4)

        # Методы испытаний
        self.label_12 = QtWidgets.QLabel("Информация о предмете исследования")
        self.label_12.setFont(font)
        self.label_12.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.form_layout.addRow(self.label_12)

        # Кнопки методов
        self.CombGOSTButton = QtWidgets.QRadioButton("Метод 2 ГОСТ 30244")
        self.CombLookButton = QtWidgets.QPushButton("Смотреть/редактировать результаты")
        self.CombAddButton = QtWidgets.QPushButton("Внести результаты")

        self.FlamGOSTButton = QtWidgets.QRadioButton("ГОСТ 30402")
        self.FlamLookButton = QtWidgets.QPushButton("Смотреть/редактировать результаты")
        self.FlamAddButton = QtWidgets.QPushButton("Внести результаты")

        self.form_layout.addRow(self.CombGOSTButton)
        self.form_layout.addRow(self.CombLookButton, self.CombAddButton)
        self.form_layout.addRow(self.FlamGOSTButton)
        self.form_layout.addRow(self.FlamLookButton, self.FlamAddButton)

        # Разделитель
        self.line_5 = QtWidgets.QFrame()
        self.line_5.setFrameShape(QtWidgets.QFrame.Shape.HLine)
        self.line_5.setFrameShadow(QtWidgets.QFrame.Shadow.Sunken)
        self.form_layout.addRow(self.line_5)

        # Дополнительная информация
        self.label_14 = QtWidgets.QLabel("Дополнительная информация от заказчика")
        self.label_14.setFont(font)
        self.label_14.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.form_layout.addRow(self.label_14)

        self.AdditionalnfoWidget = QtWidgets.QPlainTextEdit()
        self.AdditionalnfoWidget.setReadOnly(True)
        self.form_layout.addRow(self.AdditionalnfoWidget)

        # Кнопка закрытия заявки
        self.closeRequestButton = QtWidgets.QPushButton("Закрыть заявку")
        self.closeRequestButton.setEnabled(False)
        self.closeRequestButton.setFixedHeight(30)
        self.form_layout.addRow(self.closeRequestButton)

        self.right_panel.addLayout(self.form_layout)
        self.main_layout.addLayout(self.right_panel)

        # Установка центрального виджета
        LPIApp.setCentralWidget(self.central_widget)

        # Настройка стилей
        self._setup_styles()

        self.retranslateUi(LPIApp)
        QtCore.QMetaObject.connectSlotsByName(LPIApp)

    def _setup_styles(self):
        """Настройка стилей элементов интерфейса"""
        self.saveButton.setStyleSheet("""
            QPushButton {
                background-color: #4CAF50;
                color: white;
                border: none;
                padding: 5px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #45a049;
            }
        """)

        self.refreshButton.setStyleSheet("""
            QPushButton {
                background-color: #2196F3;
                color: white;
                border: none;
                padding: 5px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #0b7dda;
            }
        """)

        self.closeRequestButton.setStyleSheet("""
            QPushButton {
                background-color: #ff4444;
                color: white;
                border: none;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #cc0000;
            }
            QPushButton:disabled {
                background-color: #aaaaaa;
            }
        """)

    def retranslateUi(self, LPIApp):
        _translate = QtCore.QCoreApplication.translate
        LPIApp.setWindowTitle(_translate("LPIApp", "LPI TN"))


def main():
    app = QApplication(sys.argv)
    main_window = QMainWindow()

    # Инициализация MVC
    model = RequestDataModel()
    view = RequestView(main_window)
    controller = RequestController(model, view)
    view.set_controller(controller)

    # Загрузка данных
    if not controller.initialize():
        QMessageBox.critical(main_window, "Ошибка", "Не удалось загрузить данные заявок")
        sys.exit(1)

    main_window.show()
    sys.exit(app.exec())


