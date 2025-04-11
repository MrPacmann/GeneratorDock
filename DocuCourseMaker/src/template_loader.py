# src/template_loader.py

from PySide6.QtWidgets import QFileDialog

def load_template(parent, title: str, file_filter: str) -> str:
    """
    Открывает диалог выбора файла шаблона.

    :param parent: Родительский виджет.
    :param title: Заголовок диалога.
    :param file_filter: Фильтр для файлов (например, "Документы (*.doc *.docx *.xls *.xlsx)").
    :return: Путь выбранного файла или пустая строка, если выбор отменён.
    """
    file_name, _ = QFileDialog.getOpenFileName(parent, title, "", file_filter)
    return file_name