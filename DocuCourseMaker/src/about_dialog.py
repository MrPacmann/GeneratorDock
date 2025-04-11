# src/about_dialog.py

from PySide6.QtWidgets import (
    QDialog, QVBoxLayout, QLabel, QFrame, QHBoxLayout
)
from PySide6.QtGui import QPixmap, Qt
from PySide6.QtCore import Signal, Slot
from src.animated_button import AnimatedButton


class AboutDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("О программе")
        self.setModal(True)
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout(self)

        # Основной текст
        about_text = QLabel(
            "Данная программа создана для генерации листов заданий<br>"
            "и титульных листов для курсовой работы.<br><br>"
        )
        about_text.setWordWrap(True)
        layout.addWidget(about_text)

        # Логотип
        logo_label = QLabel()
        logo_pixmap = QPixmap("resources/icons/Logo.png")
        if not logo_pixmap.isNull():
            scaled_logo = logo_pixmap.scaled(80, 80, Qt.KeepAspectRatio, Qt.SmoothTransformation)
            logo_label.setPixmap(scaled_logo)
            logo_label.setAlignment(Qt.AlignCenter)
            layout.addWidget(logo_label)

            # Подпись под логотипом
            footer_label = QLabel("Кафедра ПМ © 2025")
            footer_label.setAlignment(Qt.AlignCenter)
            layout.addWidget(footer_label)
        else:
            alt_label = QLabel("Логотип не найден")
            alt_label.setAlignment(Qt.AlignCenter)
            layout.addWidget(alt_label)

        # Добавим кликабельный текст для «авторы»
        authors_label = QLabel(
            "<a href='authors' style='color: #007BFF; text-decoration: underline;'>авторы</a>"
        )
        authors_label.setOpenExternalLinks(False)
        authors_label.setTextFormat(Qt.RichText)
        authors_label.setAlignment(Qt.AlignCenter)
        # Когда пользователь кликнет, вызовем слот show_authors
        authors_label.linkActivated.connect(self.show_authors_dialog)

        layout.addWidget(authors_label)

        # Горизонтальная линия
        separator = QFrame()
        separator.setFrameShape(QFrame.HLine)
        separator.setFrameShadow(QFrame.Sunken)
        layout.addWidget(separator)

        # Нижняя часть с кнопкой «Закрыть»
        button_layout = QHBoxLayout()
        layout.addLayout(button_layout)
        button_layout.addStretch()
        close_button = AnimatedButton("Закрыть")
        close_button.clicked.connect(self.accept)
        button_layout.addWidget(close_button)

    @Slot(str)
    def show_authors_dialog(self, _link=None):
        """ Открываем дополнительное окно со списком авторов. """
        authors_dialog = AuthorsDialog(self)
        authors_dialog.exec()


# Дополнительный диалог "Авторы"
class AuthorsDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Авторы")
        self.setModal(True)
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout(self)
        layout.setSpacing(15)
        layout.setContentsMargins(20, 20, 20, 20)

        # Заголовок
        title_label = QLabel("<b>Список авторов:</b>")
        layout.addWidget(title_label)

        # Список авторов (пример)
        authors_list = [
            "Крынецкий Б.",
            "Шкерин Л.",
            "Трушин С."
        ]
        # Выведем их простым текстом
        authors_text = "<br>".join(authors_list)
        authors_label = QLabel(authors_text)
        authors_label.setWordWrap(True)
        layout.addWidget(authors_label)

        # Кнопка закрытия
        button_layout = QHBoxLayout()
        layout.addLayout(button_layout)
        button_layout.addStretch()
        close_button = AnimatedButton("Закрыть")
        close_button.clicked.connect(self.accept)
        button_layout.addWidget(close_button)