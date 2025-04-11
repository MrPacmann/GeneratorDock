# src/input_panel.py

from PySide6.QtWidgets import QWidget, QGroupBox, QFormLayout, QComboBox, QLineEdit, QVBoxLayout
from PySide6.QtGui import QPalette, QColor
from src.institutes import institutes_departments
from src.date_picker import DatePicker

class InputPanel(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.institutes_departments = institutes_departments
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        self.group = QGroupBox("Входные данные")
        self.group.setToolTip("Заполните данные для генерации документов")
        form_layout = QFormLayout(self.group)
        form_layout.setSpacing(10)

        # Выпадающий список для институтов
        institutes_list = list(self.institutes_departments.keys())
        self.institute_combo = QComboBox()
        self.institute_combo.addItems(institutes_list)
        self.institute_combo.setToolTip("Выберите институт из списка")
        form_layout.addRow("Наименование института:", self.institute_combo)

        # Выпадающий список для кафедр (зависимый)
        self.department_combo = QComboBox()
        self.department_combo.setToolTip("Выберите кафедру, принадлежащую выбранному институту")
        first_institute = institutes_list[0]
        self.department_combo.addItems(self.institutes_departments[first_institute])
        form_layout.addRow("Наименование кафедры:", self.department_combo)
        self.institute_combo.currentIndexChanged.connect(self.update_department_combo)

        # Поле ФИО заведующего кафедрой
        self.head_of_department_edit = QLineEdit()
        self.head_of_department_edit.setPlaceholderText("Например: Иванов И.И.")
        form_layout.addRow("ФИО заведующего кафедрой:", self.head_of_department_edit)

        # Поле Название дисциплины
        self.discipline_edit = QLineEdit()
        self.discipline_edit.setPlaceholderText("Например: Математический анализ")
        form_layout.addRow("Название дисциплины:", self.discipline_edit)

        # Поля для выбора дат с календарём
        self.date1_edit = DatePicker()
        form_layout.addRow("Дата 1:", self.date1_edit)

        self.date2_edit = DatePicker()
        form_layout.addRow("Дата 2:", self.date2_edit)

        self.date3_edit = DatePicker()
        form_layout.addRow("Дата 3:", self.date3_edit)

        self.date4_edit = DatePicker()
        form_layout.addRow("Дата 4:", self.date4_edit)

        # Настройка цвета placeholder для QLineEdit'ов
        for widget in [self.head_of_department_edit, self.discipline_edit]:
            pal = widget.palette()
            pal.setColor(QPalette.PlaceholderText, QColor("#999999"))
            widget.setPalette(pal)

        layout.addWidget(self.group)

    def update_department_combo(self):
        selected_institute = self.institute_combo.currentText()
        self.department_combo.clear()
        if selected_institute in self.institutes_departments:
            self.department_combo.addItems(self.institutes_departments[selected_institute])