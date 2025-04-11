from PySide6.QtWidgets import QPushButton
from PySide6.QtCore import QPropertyAnimation, QEasingCurve, QRect

class AnimatedButton(QPushButton):
    """
    Кнопка с анимацией масштабирования при нажатии.
    При нажатии кнопка немного уменьшается, а при отпускании возвращается к исходной геометрии.
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._original_geometry = None

    def mousePressEvent(self, event):
        # Сохраняем исходную геометрию кнопки
        self._original_geometry = self.geometry()
        rect = self._original_geometry
        new_width = int(rect.width() * 0.95)
        new_height = int(rect.height() * 0.95)
        delta_w = (rect.width() - new_width) // 2
        delta_h = (rect.height() - new_height) // 2
        new_rect = QRect(rect.x() + delta_w, rect.y() + delta_h, new_width, new_height)
        self.anim = QPropertyAnimation(self, b"geometry")
        self.anim.setDuration(100)
        self.anim.setStartValue(rect)
        self.anim.setEndValue(new_rect)
        self.anim.setEasingCurve(QEasingCurve.InOutQuad)
        self.anim.start()
        super().mousePressEvent(event)

    def mouseReleaseEvent(self, event):
        if self._original_geometry:
            current_rect = self.geometry()
            self.anim = QPropertyAnimation(self, b"geometry")
            self.anim.setDuration(100)
            self.anim.setStartValue(current_rect)
            self.anim.setEndValue(self._original_geometry)
            self.anim.setEasingCurve(QEasingCurve.InOutQuad)
            self.anim.start()
        super().mouseReleaseEvent(event)