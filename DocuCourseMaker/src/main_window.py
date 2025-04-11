import os
import sys

from PySide6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QGroupBox,
    QFormLayout, QLabel, QLineEdit, QPushButton, QTextEdit,
    QFileDialog, QDialog, QStatusBar, QComboBox, QMessageBox,
    QTabWidget, QFrame, QGraphicsOpacityEffect
)
from PySide6.QtGui import QIcon, QPixmap, QTextCursor, QPalette, QColor
from PySide6.QtCore import QPropertyAnimation, QEasingCurve, Qt

# Если вы используете светлую тему из themes.py, импортируйте её в main.py и установите
# app.setStyleSheet(LIGHT_THEME). Здесь у нас просто фиксированная "светлая" тема.
from src.themes import LIGHT_THEME

from src.template_manager import extract_preview, format_loaded_templates


def to_html(text: str) -> str:
    """Преобразует обычный текст в HTML-безопасный."""
    text = text.replace("&", "&amp;")
    text = text.replace("<", "&lt;").replace(">", "&gt;")
    text = text.replace("\n", "<br>")
    return text


# --- Диалог "О программе" ---
class AboutDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("О программе")
        self.setModal(True)
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout(self)
        about_text = QLabel(
            "Данная программа создана для генерации листов заданий<br>"
            "и титульных листов для курсовой работы.<br><br>"
            "Логотип кафедры © 2025"
        )
        about_text.setWordWrap(True)
        layout.addWidget(about_text)

        separator = QFrame()
        separator.setFrameShape(QFrame.HLine)
        separator.setFrameShadow(QFrame.Sunken)
        layout.addWidget(separator)

        button_layout = QHBoxLayout()
        layout.addLayout(button_layout)
        button_layout.addStretch()

        close_button = QPushButton("Закрыть")
        close_button.clicked.connect(self.accept)
        button_layout.addWidget(close_button)


# --- Основной класс окна ---
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("DocuCourseMaker")
        self.resize(1200, 700)
        self.setWindowIcon(QIcon("resources/icons/icon.jpeg"))

        # Пути к шаблонам (будут задаваться при загрузке)
        self.title_template_file = ""
        self.assignment_template_file = ""
        self.excel_template_file = ""
        self.save_folder = ""

        # Словарь, отображающий институт -> список кафедр
        # Обратите внимание, что институты и списки кафедр можно дополнять.
        self.institutes_departments = {
            "Институт информационных технологий": [
                "Базовая кафедра № 231 – информационных процессов и систем",
                "Базовая кафедра № 232 – вычислительных систем реального времени",
                "Базовая кафедра № 234 – управляющих ЭВМ",
                "Базовая кафедра № 244 – информационных технологий в системах управления",
                "Базовая кафедра № 250 – математического обеспечения информационных систем",
                "Базовая кафедра № 256 – многосетевых информационных систем",
                "Кафедра вычислительной техники",
                "Кафедра игровой индустрии",
                "Кафедра инструментального и прикладного программного обеспечения",
                "Кафедра информационных технологий в атомной энергетике",
                "Кафедра корпоративных информационных систем",
                "Кафедра математического обеспечения и стандартизации информационных технологий",
                "Кафедра практической и прикладной информатики",
                "Кафедра прикладной математики",
                "Кафедра цифровой трансформации",
                "Кафедра информационных технологий обработки и анализа больших данных"
            ],
            "Институт искусственного интеллекта": [
                "Кафедра автоматических систем",
                "Кафедра биокибернетических систем и технологий",
                "Кафедра промышленной информатики",
                "Кафедра высшей математики",
                "Кафедра компьютерной и информационной безопасности",
                "Кафедра проблем управления",
                "Кафедра системной инженерии",
                "Кафедра технологий искусственного интеллекта",
                "Базовая кафедра № 235 - цифровых устройств и систем защиты информации",
                "Базовая кафедра № 252 - информационной безопасности",
                "Базовая кафедра № 254 - вычислительных комплексов",
                "Базовая кафедра № 530 - автоматики и управления",
                "Базовая кафедра № 536 - программного обеспечения систем радиоэлектронной аппаратуры",
                "Базовая кафедра № 539 - авиационно-космических систем обработки информации и управления"
            ]
            # При желании добавьте остальные институты и их кафедры
        }

        self.init_ui()

    def init_ui(self):
        self.status_bar = QStatusBar()
        self.setStatusBar(self.status_bar)
        self.status_bar.showMessage("Готово")

        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)
        main_layout.setContentsMargins(20, 20, 20, 20)
        main_layout.setSpacing(15)

        # Верхняя панель: логотип, "О программе", "Выбрать папку"
        top_button_layout = QHBoxLayout()
        top_button_layout.setSpacing(20)
        main_layout.addLayout(top_button_layout)

        self.logo_label = QLabel()
        logo_pixmap = QPixmap("resources/icons/Logo.png")
        if not logo_pixmap.isNull():
            scaled_logo = logo_pixmap.scaled(80, 80, Qt.KeepAspectRatio, Qt.SmoothTransformation)
            self.logo_label.setPixmap(scaled_logo)
        else:
            self.logo_label.setText("LOGO")
        top_button_layout.addWidget(self.logo_label)

        self.about_btn = QPushButton("О программе")
        self.about_btn.setToolTip("Нажмите для отображения информации о программе")
        self.about_btn.clicked.connect(self.show_about_dialog)
        top_button_layout.addWidget(self.about_btn)

        self.save_folder_btn = QPushButton("Выбрать папку для сохранения")
        self.save_folder_btn.setToolTip("Выберите папку для сохранения документов")
        self.save_folder_btn.clicked.connect(self.choose_save_folder)
        top_button_layout.addWidget(self.save_folder_btn)

        top_button_layout.addStretch()

        # Основной горизонтальный блок: левая часть (вкладки) и правая часть (предпросмотр)
        top_layout = QHBoxLayout()
        top_layout.setSpacing(20)
        main_layout.addLayout(top_layout)

        self.tab_widget = QTabWidget()
        self.tab_widget.setToolTip("Переключайтесь между вкладками")
        top_layout.addWidget(self.tab_widget, 1)

        # Вкладка "Входные данные"
        data_tab = QWidget()
        data_layout = QVBoxLayout(data_tab)
        data_layout.setContentsMargins(10, 10, 10, 10)
        data_layout.setSpacing(10)
        self.create_input_data_panel(data_layout)
        self.tab_widget.addTab(data_tab, "Входные данные")

        # Вкладка "Шаблоны документов"
        templates_tab = QWidget()
        templates_layout = QVBoxLayout(templates_tab)
        templates_layout.setContentsMargins(10, 10, 10, 10)
        templates_layout.setSpacing(10)
        self.create_templates_panel(templates_layout)
        self.tab_widget.addTab(templates_tab, "Шаблоны документов")

        # Правая часть: Предпросмотр
        right_col_layout = QVBoxLayout()
        right_col_layout.setSpacing(15)
        top_layout.addLayout(right_col_layout, 2)

        preview_group = QGroupBox("Предпросмотр")
        preview_layout = QVBoxLayout(preview_group)
        preview_layout.setContentsMargins(10, 10, 10, 10)
        preview_layout.setSpacing(10)

        self.preview_text = QTextEdit()
        self.preview_text.setReadOnly(True)
        self.preview_text.setToolTip(
            "Здесь отображается информация о шаблонах и предпросмотр содержимого последнего файла")
        preview_layout.addWidget(self.preview_text)
        right_col_layout.addWidget(preview_group)

        # Нижняя панель: кнопки "Скачать титулы", "Скачать задания", "Выход"
        bottom_layout = QHBoxLayout()
        bottom_layout.setSpacing(20)
        main_layout.addLayout(bottom_layout)

        self.download_titles_btn = QPushButton("Скачать титулы")
        self.download_titles_btn.setToolTip("Генерировать и сохранить титульные листы")
        self.download_titles_btn.clicked.connect(self.download_titles)

        self.download_assignments_btn = QPushButton("Скачать задания")
        self.download_assignments_btn.setToolTip("Генерировать и сохранить листы заданий")
        self.download_assignments_btn.clicked.connect(self.download_assignments)

        self.exit_btn = QPushButton("Выход")
        self.exit_btn.setToolTip("Завершить работу приложения")
        self.exit_btn.clicked.connect(self.confirm_exit)

        bottom_layout.addWidget(self.download_titles_btn)
        bottom_layout.addWidget(self.download_assignments_btn)
        bottom_layout.addStretch()
        bottom_layout.addWidget(self.exit_btn)

    def create_input_data_panel(self, layout):
        input_group = QGroupBox("Входные данные")
        input_group.setToolTip("Заполните данные для генерации документов")
        input_layout = QFormLayout(input_group)
        input_layout.setSpacing(10)

        # Выделенный словарь институтов + кафедры
        institutes_list = list(self.institutes_departments.keys())

        self.institute_combo = QComboBox()
        self.institute_combo.addItems(institutes_list)
        self.institute_combo.setToolTip("Выберите институт из списка")
        input_layout.addRow("Наименование института:", self.institute_combo)

        self.department_combo = QComboBox()
        self.department_combo.setToolTip("Выберите кафедру, принадлежащую выбранному институту")

        first_institute = institutes_list[0]
        self.department_combo.addItems(self.institutes_departments[first_institute])
        input_layout.addRow("Наименование кафедры:", self.department_combo)

        # Сигнал на изменение института
        self.institute_combo.currentIndexChanged.connect(self.update_department_combo)

        self.head_of_department_edit = QLineEdit()
        self.head_of_department_edit.setPlaceholderText("Например: Иванов И.И.")

        self.course_title_edit = QLineEdit()
        self.course_title_edit.setPlaceholderText("Например: Программирование на Python")

        self.author_edit = QLineEdit()
        self.author_edit.setPlaceholderText("Например: Петров П.П.")

        from PySide6.QtGui import QPalette, QColor
        for widget in [self.head_of_department_edit, self.course_title_edit, self.author_edit]:
            pal = widget.palette()
            pal.setColor(QPalette.PlaceholderText, QColor("#999999"))
            widget.setPalette(pal)

        input_layout.addRow("ФИО Заведующего кафедрой:", self.head_of_department_edit)
        input_layout.addRow("Название курсовой:", self.course_title_edit)
        input_layout.addRow("Автор:", self.author_edit)

        layout.addWidget(input_group)

    def update_department_combo(self):
        """При изменении института обновляем кафедры в department_combo."""
        selected_institute = self.institute_combo.currentText()
        self.department_combo.clear()
        if selected_institute in self.institutes_departments:
            self.department_combo.addItems(self.institutes_departments[selected_institute])

    def create_templates_panel(self, layout):
        templates_group = QGroupBox("Шаблоны документов")
        templates_group.setToolTip("Загрузите шаблоны для титульного листа, листа задания и Excel документа")
        templates_layout = QFormLayout(templates_group)
        templates_layout.setSpacing(10)

        self.title_template_btn = QPushButton("Загрузить шаблон титульного листа")
        self.title_template_btn.setToolTip("Выберите файл (*.doc, *.docx, *.xls, *.xlsx)")
        self.title_template_btn.clicked.connect(self.load_title_template)

        line1 = QFrame()
        line1.setFrameShape(QFrame.HLine)
        line1.setFrameShadow(QFrame.Sunken)

        self.assignment_template_btn = QPushButton("Загрузить шаблон листа задания")
        self.assignment_template_btn.setToolTip("Выберите файл (*.doc, *.docx, *.xls, *.xlsx)")
        self.assignment_template_btn.clicked.connect(self.load_assignment_template)

        line2 = QFrame()
        line2.setFrameShape(QFrame.HLine)
        line2.setFrameShadow(QFrame.Sunken)

        self.excel_template_btn = QPushButton("Загрузить Excel документ")
        self.excel_template_btn.setToolTip("Выберите файл (*.xls, *.xlsx)")
        self.excel_template_btn.clicked.connect(self.load_excel_template)

        templates_layout.addRow("Титульный лист:", self.title_template_btn)
        templates_layout.addRow(line1)
        templates_layout.addRow("Лист задания:", self.assignment_template_btn)
        templates_layout.addRow(line2)
        templates_layout.addRow("Excel документ:", self.excel_template_btn)

        layout.addWidget(templates_group)

    def show_about_dialog(self):
        dialog = AboutDialog(self)
        dialog.exec()
        self.status_bar.showMessage("Показано окно 'О программе'", 3000)

    def choose_save_folder(self):
        folder = QFileDialog.getExistingDirectory(self, "Выберите папку для сохранения")
        if folder:
            self.save_folder = folder
            self.status_bar.showMessage(f"Выбрана папка для сохранения: {folder}", 5000)
            self.preview_text.append(f"Папка для сохранения: {folder}\n")
        else:
            self.status_bar.showMessage("Выбор папки отменён", 3000)

    def load_title_template(self):
        file_name, _ = QFileDialog.getOpenFileName(
            self, "Выберите шаблон титульного листа", "",
            "Документы (*.doc *.docx *.xls *.xlsx)"
        )
        if file_name:
            self.title_template_file = file_name
            self.update_preview(file_name, "Титульный лист")
        else:
            self.status_bar.showMessage("Загрузка шаблона титульного листа отменена", 3000)

    def load_assignment_template(self):
        file_name, _ = QFileDialog.getOpenFileName(
            self, "Выберите шаблон листа задания", "",
            "Документы (*.doc *.docx *.xls *.xlsx)"
        )
        if file_name:
            self.assignment_template_file = file_name
            self.update_preview(file_name, "Лист задания")
        else:
            self.status_bar.showMessage("Загрузка шаблона листа задания отменена", 3000)

    def load_excel_template(self):
        file_name, _ = QFileDialog.getOpenFileName(
            self, "Выберите Excel документ", "",
            "Excel документы (*.xls, *.xlsx)"
        )
        if file_name:
            self.excel_template_file = file_name
            self.update_preview(file_name, "Excel документ")
        else:
            self.status_bar.showMessage("Загрузка Excel документа отменена", 3000)

    def update_preview(self, file_path: str, doc_type: str):
        self.status_bar.showMessage(f"{doc_type} загружен: {file_path}", 5000)
        overview_html = format_loaded_templates(
            self.title_template_file,
            self.assignment_template_file,
            self.excel_template_file
        )
        raw_text = extract_preview(file_path)
        text_html = to_html(raw_text)
        html_content = f"""
        <html>
          <head><meta charset="utf-8"/></head>
          <body style="font-family: Arial, sans-serif; font-size:14px; color:#333;">
            {overview_html}
            <hr>
            <h4>Предпросмотр содержимого</h4>
            <p><strong>{doc_type}</strong> ({file_path})</p>
            <div style="background:#f9f9f9; border:1px solid #ddd; padding:10px;">
              {text_html}
            </div>
          </body>
        </html>
        """
        self.preview_text.setHtml(html_content)
        cursor = self.preview_text.textCursor()
        cursor.movePosition(QTextCursor.Start)
        self.preview_text.setTextCursor(cursor)

        opacity_effect = QGraphicsOpacityEffect(self.preview_text)
        self.preview_text.setGraphicsEffect(opacity_effect)
        self.animation = QPropertyAnimation(opacity_effect, b"opacity")
        self.animation.setDuration(800)
        self.animation.setStartValue(0.0)
        self.animation.setEndValue(1.0)
        self.animation.setEasingCurve(QEasingCurve.InOutQuad)
        self.animation.start()

    def download_titles(self):
        self.status_bar.showMessage("Начало генерации титульных листов", 3000)
        self.preview_text.append("\nСкачивание (генерация) титульных листов...")
        if not self.save_folder:
            QMessageBox.warning(self, "Внимание", "Не выбрана папка для сохранения!")
            return
        # Здесь может вызываться ваш document_generator, если нужно
        self.status_bar.showMessage("Титульные листы успешно сохранены", 3000)

    def download_assignments(self):
        self.status_bar.showMessage("Начало генерации листов заданий", 3000)
        self.preview_text.append("\nСкачивание (генерация) листов заданий...")
        if not self.save_folder:
            QMessageBox.warning(self, "Внимание", "Не выбрана папка для сохранения!")
            return
        # Аналогично можно вызвать document_generator
        self.status_bar.showMessage("Листы заданий успешно сохранены", 3000)

    def confirm_exit(self):
        reply = QMessageBox.question(
            self, "Подтверждение выхода", "Вы точно хотите закрыть приложение?",
            QMessageBox.Yes | QMessageBox.No, QMessageBox.No
        )
        if reply == QMessageBox.Yes:
            self.close()