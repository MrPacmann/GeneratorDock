# src/date_picker.py
from PySide6.QtWidgets import QDateEdit
from PySide6.QtCore import QDate

class DatePicker(QDateEdit):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setCalendarPopup(True)         # Включает всплывающий календарь
        self.setDisplayFormat("dd.MM.yyyy")   # Устанавливает формат даты
        self.setDate(QDate.currentDate())     # По умолчанию текущая дата