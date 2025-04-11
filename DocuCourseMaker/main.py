import sys
from PySide6.QtWidgets import QApplication
from src.main_window import MainWindow

# Определим единую «светлую» тему (можно поправить под свой вкус)
SINGLE_THEME = """
/* Общие базовые стили */
QMainWindow {
    background-color: #FFFFFF;
}
QWidget {
    background-color: #FFFFFF;
    color: #333;
    font-family: Arial, sans-serif;
    font-size: 14px;
}

/* Групповые блоки (QGroupBox) */
QGroupBox {
    background-color: #FFFFFF;
    border: 1px solid #CCC;
    border-radius: 4px;
    margin-top: 8px;
}
QGroupBox::title {
    subcontrol-origin: margin;
    subcontrol-position: top left;
    padding: 2px 8px;
    color: #555;
    font-weight: bold;
}

/* Кнопки */
QPushButton {
    background-color: #F5F5F5;
    border: 1px solid #CCC;
    border-radius: 4px;
    padding: 6px 12px;
}
QPushButton:hover {
    background-color: #E8E8E8;
}
QPushButton:pressed {
    background-color: #D8D8D8;
}

/* Поля ввода */
QLineEdit, QTextEdit {
    background-color: #FFFFFF;
    border: 1px solid #CCC;
    border-radius: 4px;
    padding: 4px;
}

/* Всплывающие подсказки (ToolTips) */
QToolTip {
    font-size: 14px;
    color: #333;
    background-color: #FFFFE0;
    border: 1px solid #999;
    padding: 8px;
    border-radius: 4px;
}

/* Вкладки (QTabWidget / QTabBar) */
QTabWidget::pane {
    border: 1px solid #CCC;
    border-radius: 4px;
    background: #FFFFFF;
}
QTabBar::tab {
    background: #FFFFFF;
    border: 1px solid #CCC;
    border-top-left-radius: 4px;
    border-top-right-radius: 4px;
    padding: 6px 12px;
    margin: 2px;
    color: #333;
    font-weight: bold;
}
QTabBar::tab:hover {
    background: #F7F7F7;
}
QTabBar::tab:selected {
    background: #EAEAEA;
    border-bottom: 1px solid #FFFFFF;
}
"""

def main():
    app = QApplication(sys.argv)

    # Устанавливаем светлую (единую) тему на всё приложение
    app.setStyleSheet(SINGLE_THEME)

    window = MainWindow()
    window.show()
    sys.exit(app.exec())

if __name__ == '__main__':
    main()