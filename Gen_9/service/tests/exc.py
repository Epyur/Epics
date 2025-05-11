import sys
import pandas as pd
from PyQt6.QtWidgets import (QApplication, QMainWindow, QListWidget, QVBoxLayout,
                             QWidget, QLabel, QLineEdit, QPushButton, QHBoxLayout,
                             QFormLayout)
from PyQt6.QtCore import Qt


class ExcelViewer(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Excel Data Viewer")
        self.setGeometry(100, 100, 800, 600)

        # Основные переменные
        self.df = None
        self.current_file = None

        # Создаем интерфейс
        self.init_ui()

    def init_ui(self):
        # Основные виджеты
        self.list_widget = QListWidget()
        self.list_widget.itemClicked.connect(self.on_item_selected)

        # Текстовые поля для отображения данных
        self.fields = {}
        form_layout = QFormLayout()

        # Создаем несколько полей для разных данных
        field_names = ["ID", "Name", "Email", "Phone", "Address", "Status"]
        for name in field_names:
            self.fields[name] = QLineEdit()
            self.fields[name].setReadOnly(True)
            form_layout.addRow(QLabel(f"{name}:"), self.fields[name])

        # Кнопки управления
        self.load_btn = QPushButton("Load Excel File")
        self.load_btn.clicked.connect(self.load_excel)

        # Размещение виджетов
        left_layout = QVBoxLayout()
        left_layout.addWidget(QLabel("Items:"))
        left_layout.addWidget(self.list_widget)
        left_layout.addWidget(self.load_btn)

        right_layout = QVBoxLayout()
        right_layout.addLayout(form_layout)
        right_layout.addStretch()

        main_layout = QHBoxLayout()
        main_layout.addLayout(left_layout, stretch=1)
        main_layout.addLayout(right_layout, stretch=2)

        container = QWidget()
        container.setLayout(main_layout)
        self.setCentralWidget(container)

    def load_excel(self):
        """Загрузка данных из Excel файла"""
        try:
            # В реальном приложении лучше использовать QFileDialog
            file_path = "data.xlsx"  # Укажите путь к вашему файлу

            # Чтение данных
            self.df = pd.read_excel(file_path)
            self.current_file = file_path

            # Очищаем список
            self.list_widget.clear()

            # Заполняем список комбинацией двух колонок (например, Name и Email)
            if len(self.df.columns) >= 2:
                for _, row in self.df.iterrows():
                    item_text = f"{row[0]} - {row[1]}"  # Первые две колонки
                    self.list_widget.addItem(item_text)

            print(f"Loaded {len(self.df)} records from {file_path}")

        except Exception as e:
            print(f"Error loading Excel file: {str(e)}")

    def on_item_selected(self, item):
        """Обработка выбора элемента в списке"""
        if self.df is None:
            return

        # Получаем индекс выбранного элемента
        index = self.list_widget.row(item)

        # Получаем соответствующую строку из DataFrame
        row = self.df.iloc[index]

        # Заполняем текстовые поля данными из строки
        for i, (field_name, field) in enumerate(self.fields.items()):
            if i < len(row):
                field.setText(str(row[i]))
            else:
                field.clear()


if __name__ == "__main__":
    app = QApplication(sys.argv)

    # Создаем тестовый Excel файл если его нет
    try:
        sample_data = {
            "ID": [1, 2, 3],
            "Name": ["Alice", "Bob", "Charlie"],
            "Email": ["alice@example.com", "bob@example.com", "charlie@example.com"],
            "Phone": ["123-456", "234-567", "345-678"],
            "Address": ["Street 1", "Street 2", "Street 3"],
            "Status": ["Active", "Inactive", "Active"]
        }
        pd.DataFrame(sample_data).to_excel("data.xlsx", index=False)
    except:
        pass

    window = ExcelViewer()
    window.show()
    sys.exit(app.exec())