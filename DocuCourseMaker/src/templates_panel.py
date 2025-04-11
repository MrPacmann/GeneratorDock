# src/templates_panel.py

from PySide6.QtWidgets import QWidget, QGroupBox, QFormLayout, QVBoxLayout
from src.animated_button import AnimatedButton

class TemplatesPanel(QWidget):
    def __init__(self,
                 load_title_callback,
                 load_assignment_callback,
                 load_excel_callback,
                 parent=None):
        super().__init__(parent)
        self.load_title_callback = load_title_callback
        self.load_assignment_callback = load_assignment_callback
        self.load_excel_callback = load_excel_callback
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        self.group = QGroupBox("Шаблоны документов")
        form_layout = QFormLayout(self.group)
        form_layout.setSpacing(10)

        self.title_template_btn = AnimatedButton("Загрузить шаблон титульного листа")
        self.title_template_btn.clicked.connect(self.load_title_callback)
        form_layout.addRow("Титульный лист:", self.title_template_btn)

        self.assignment_template_btn = AnimatedButton("Загрузить шаблон листа задания")
        self.assignment_template_btn.clicked.connect(self.load_assignment_callback)
        form_layout.addRow("Лист задания:", self.assignment_template_btn)

        self.excel_template_btn = AnimatedButton("Загрузить Excel документ")
        self.excel_template_btn.clicked.connect(self.load_excel_callback)
        form_layout.addRow("Excel документ:", self.excel_template_btn)

        layout.addWidget(self.group)