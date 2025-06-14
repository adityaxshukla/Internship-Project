# Internship Project – Week 1: Digital Clock
# By: Aditya Kumar | @Internpe Technologies
# jUN 2025
# I built a simple floating digital clock using PyQt6:

import sys
from PyQt6 import QtCore, QtGui, QtWidgets
from PyQt6.QtCore import Qt, QTimer, QDate, QTime
from PyQt6.QtWidgets import QApplication, QLabel, QWidget, QMenu, QVBoxLayout
from PyQt6.QtGui import QFont, QPainter, QBrush, QColor, QMouseEvent


class DigitalClock(QWidget):
    def __init__(self):
        super().__init__()
        self.offset = None
        self.pinned = False
        self.init_ui()

    def init_ui(self):
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint | Qt.WindowType.WindowStaysOnTopHint)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(5)
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # Time label with new color and font
        self.time_label = QLabel(self)
        self.time_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.time_label.setTextFormat(Qt.TextFormat.RichText)
        self.time_label.setStyleSheet('color: #00FFFF;')  # Cyan accent
        layout.addWidget(self.time_label)

        # Date label with softer gray
        self.date_label = QLabel(self)
        self.date_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        date_font = QFont('Fira Code', 12, QFont.Weight.Normal)
        self.date_label.setFont(date_font)
        self.date_label.setStyleSheet('color: #CCCCCC;')
        layout.addWidget(self.date_label)

        self.setLayout(layout)

        timer = QTimer(self)
        timer.timeout.connect(self.update_time)
        timer.start(1000)
        self.update_time()

        self.resize(300, 150)

    def update_time(self):
        t = QTime.currentTime()
        time_str = t.toString('hh:mm:ss')
        ampm = t.toString('AP')
        html = (
            f'<span style="font-family: Fira Code, monospace; font-size:52px; font-weight:600;">{time_str}</span>'
            f'<span style="font-family: Fira Code, monospace; font-size:18px; vertical-align:super;"> {ampm}</span>'
        )
        self.time_label.setText(html)

        current_date = QDate.currentDate().toString('dddd, MMMM d, yyyy')
        self.date_label.setText(current_date)
        self.update()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        rect = self.rect()

        gradient = QtGui.QLinearGradient(0, 0, 0, rect.height())
        gradient.setColorAt(0.0, QColor(30, 30, 30, 220))  # Dark gray
        gradient.setColorAt(1.0, QColor(0, 0, 0, 220))     # Blackish

        brush = QBrush(gradient)
        painter.setBrush(brush)
        painter.setPen(Qt.PenStyle.NoPen)
        painter.drawRoundedRect(rect, 10, 10)

    def mousePressEvent(self, event: QMouseEvent):
        if event.button() == Qt.MouseButton.LeftButton:
            self.offset = event.globalPosition().toPoint() - self.frameGeometry().topLeft()
        elif event.button() == Qt.MouseButton.RightButton:
            self.show_context_menu(event.pos())

    def mouseMoveEvent(self, event: QMouseEvent):
        if self.offset is not None and event.buttons() & Qt.MouseButton.LeftButton:
            new_pos = event.globalPosition().toPoint() - self.offset
            self.move(new_pos)

    def mouseReleaseEvent(self, event: QMouseEvent):
        self.offset = None

    def show_context_menu(self, pos):
        menu = QMenu(self)
        pin_action = menu.addAction('Pin/Unpin')
        reset_action = menu.addAction('Reset Position')
        action = menu.exec(self.mapToGlobal(pos))
        if action == pin_action:
            self.toggle_pin()
        elif action == reset_action:
            self.default_position()

    def toggle_pin(self):
        self.pinned = not self.pinned
        flags = self.windowFlags()
        if self.pinned:
            flags |= Qt.WindowType.WindowStaysOnTopHint
        else:
            flags &= ~Qt.WindowType.WindowStaysOnTopHint
        self.setWindowFlags(flags)
        self.show()

    def default_position(self):
        screen = QApplication.primaryScreen().availableGeometry()
        x = screen.x() + (screen.width() - self.width()) // 2
        y = screen.y() + 60
        self.move(x, y)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    clock = DigitalClock()
    clock.default_position()
    clock.show()
    sys.exit(app.exec())
