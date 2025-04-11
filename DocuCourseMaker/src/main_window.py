import os
import sys

from PySide6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QGroupBox,
    QStatusBar, QTabWidget, QFrame, QTextEdit, QMessageBox, QFileDialog, QLabel, QFormLayout, QLineEdit
)
from PySide6.QtGui import QIcon, QPixmap, QTextCursor, QPalette, QColor
from PySide6.QtCore import QPropertyAnimation, QEasingCurve, Qt, QRect

# Импорты модулей проекта:
from src.themes import LIGHT_THEME
from src.template_manager import extract_preview, format_loaded_templates
from src.template_loader import load_template
from src.date_picker import DatePicker
from src.institutes import institutes_departments
from src.animated_button import AnimatedButton
from src.about_dialog import AboutDialog
from src.input_panel import InputPanel
from src.templates_panel import TemplatesPanel

def to_html(text: str) -> str:
    """Преобразует текст для HTML (экранирование спецсимволов и переносов строк)."""
    text = text.replace("&", "&amp;")
    text = text.replace("<", "&lt;").replace(">", "&gt;")
    text = text.replace("\n", "<br>")
    return text

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("DocuCourseMaker")
        self.resize(1200, 700)
        self.setWindowIcon(QIcon("resources/icons/icon.jpeg"))

        # Пути к шаблонам (будут задаваться пользователем)
        self.title_template_file = ""
        self.assignment_template_file = ""
        self.excel_template_file = ""
        self.save_folder = ""

        # Используем импортированный словарь институтов и кафедр
        self.institutes_departments = institutes_departments

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

        # Логотип
        self.logo_label = QLabel()
        logo_pixmap = QPixmap("resources/icons/Logo.png")
        if not logo_pixmap.isNull():
            scaled_logo = logo_pixmap.scaled(80, 80, Qt.KeepAspectRatio, Qt.SmoothTransformation)
            self.logo_label.setPixmap(scaled_logo)
        else:
            self.logo_label.setText("LOGO")
        top_button_layout.addWidget(self.logo_label)

        self.about_btn = AnimatedButton("О программе")
        self.about_btn.setToolTip("Нажмите для отображения информации о программе")
        self.about_btn.clicked.connect(self.show_about_dialog)
        top_button_layout.addWidget(self.about_btn)

        self.save_folder_btn = AnimatedButton("Выбрать папку для сохранения")
        self.save_folder_btn.setToolTip("Выберите папку, куда будут сохраняться документы")
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

        # Вкладка "Входные данные" – панель входных данных вынесена в отдельный модуль
        data_tab = QWidget()
        data_layout = QVBoxLayout(data_tab)
        data_layout.setContentsMargins(10, 10, 10, 10)
        data_layout.setSpacing(10)
        self.input_panel = InputPanel()  # Создаём панель "Входные данные"
        data_layout.addWidget(self.input_panel)
        self.tab_widget.addTab(data_tab, "Входные данные")

        # Вкладка "Шаблоны документов" – панель шаблонов вынесена в отдельный модуль; передаем колбэки
        templates_tab = QWidget()
        templates_layout = QVBoxLayout(templates_tab)
        templates_layout.setContentsMargins(10, 10, 10, 10)
        templates_layout.setSpacing(10)
        self.templates_panel = TemplatesPanel(
            load_title_callback=self.load_title_template,
            load_assignment_callback=self.load_assignment_template,
            load_excel_callback=self.load_excel_template
        )
        templates_layout.addWidget(self.templates_panel)
        self.tab_widget.addTab(templates_tab, "Шаблоны документов")

        # Правая колонка: Предпросмотр содержимого
        right_col_layout = QVBoxLayout()
        right_col_layout.setSpacing(15)
        top_layout.addLayout(right_col_layout, 2)

        preview_group = QGroupBox("Предпросмотр")
        preview_layout = QVBoxLayout(preview_group)
        preview_layout.setContentsMargins(10, 10, 10, 10)
        preview_layout.setSpacing(10)
        self.preview_text = QTextEdit()
        self.preview_text.setReadOnly(True)
        self.preview_text.setToolTip("Здесь отображается информация о шаблонах и предпросмотр содержимого последнего файла")
        preview_layout.addWidget(self.preview_text)
        right_col_layout.addWidget(preview_group)

        # Нижняя панель: кнопки "Скачать титулы", "Скачать задания", "Выход"
        bottom_layout = QHBoxLayout()
        bottom_layout.setSpacing(20)
        main_layout.addLayout(bottom_layout)

        self.download_titles_btn = AnimatedButton("Скачать титулы")
        self.download_titles_btn.setToolTip("Генерировать и сохранить титульные листы")
        self.download_titles_btn.clicked.connect(self.download_titles)
        bottom_layout.addWidget(self.download_titles_btn)

        self.download_assignments_btn = AnimatedButton("Скачать задания")
        self.download_assignments_btn.setToolTip("Генерировать и сохранить листы заданий")
        self.download_assignments_btn.clicked.connect(self.download_assignments)
        bottom_layout.addWidget(self.download_assignments_btn)

        bottom_layout.addStretch()

        self.exit_btn = AnimatedButton("Выход")
        self.exit_btn.setToolTip("Завершить работу приложения")
        self.exit_btn.clicked.connect(self.confirm_exit)
        bottom_layout.addWidget(self.exit_btn)

    def show_about_dialog(self):
        dialog = AboutDialog(self)
        dialog.exec()
        self.status_bar.showMessage("Показано окно 'О программе'", 3000)

    def choose_save_folder(self):
        folder = QFileDialog.getExistingDirectory(self, "Выберите папку для сохранения")
        if folder:
            self.save_folder = folder
            self.status_bar.showMessage(f"Выбрана папка для сохранения: {folder}", 5000)
            # Обновляем предпросмотр: вставляем информацию о папке сверху с отступом и линией
            old_html = self.preview_text.toHtml()
            top_block = f"""
            <p><strong>Папка для сохранения:</strong> {folder}</p>
            <hr>
            """
            new_html = f"""
            <html>
              <head><meta charset="utf-8"/></head>
              <body style="font-family: Arial, sans-serif; font-size:14px; color:#333;">
                {top_block}
                {old_html}
              </body>
            </html>
            """
            self.preview_text.setHtml(new_html)
        else:
            self.status_bar.showMessage("Выбор папки отменён", 3000)

    def load_title_template(self):
        file_name = load_template(self, "Выберите шаблон титульного листа", "Документы (*.doc *.docx *.xls *.xlsx)")
        if file_name:
            self.title_template_file = file_name
            self.update_preview(file_name, "Титульный лист")
        else:
            self.status_bar.showMessage("Загрузка шаблона титульного листа отменена", 3000)

    def load_assignment_template(self):
        file_name = load_template(self, "Выберите шаблон листа задания", "Документы (*.doc *.docx *.xls *.xlsx)")
        if file_name:
            self.assignment_template_file = file_name
            self.update_preview(file_name, "Лист задания")
        else:
            self.status_bar.showMessage("Загрузка шаблона листа задания отменена", 3000)

    def load_excel_template(self):
        file_name = load_template(self, "Выберите Excel документ", "Excel документы (*.xls *.xlsx)")
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
        self.status_bar.showMessage("Титульные листы успешно сохранены", 3000)

    def download_assignments(self):
        self.status_bar.showMessage("Начало генерации листов заданий", 3000)
        self.preview_text.append("\nСкачивание (генерация) листов заданий...")
        if not self.save_folder:
            QMessageBox.warning(self, "Внимание", "Не выбрана папка для сохранения!")
            return
        self.status_bar.showMessage("Листы заданий успешно сохранены", 3000)

    def confirm_exit(self):
        reply = QMessageBox.question(
            self, "Подтверждение выхода", "Вы точно хотите закрыть приложение?",
            QMessageBox.Yes | QMessageBox.No, QMessageBox.No
        )
        if reply == QMessageBox.Yes:
            self.close()

if __name__ == "__main__":
    from PySide6.QtWidgets import QApplication, QTextCursor
    app = QApplication(sys.argv)
    app.setStyleSheet(LIGHT_THEME)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())