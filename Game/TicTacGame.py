# Internship Project – Week 2: Tic-Tac-Toe Game
# By: Aditya Kumar | @Internpe Technologies
# June 2025
# I built a floating Tic-Tac-Toe game with modern iPad-style UI using PyQt6:

import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QPushButton, QGridLayout, QWidget, QMessageBox, QLabel, \
    QHBoxLayout, QVBoxLayout
from PyQt6.QtCore import Qt, QPoint


class TicTacToe(QMainWindow):
    def __init__(self):
        super().__init__()
        # Set window properties for frameless, translucent background
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint | Qt.WindowType.Window)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        self.setFixedSize(320, 350)
        self.setStyleSheet("""
            QMainWindow {
                background-color: rgba(255, 255, 255, 0.95);
                border-radius: 12px;
                border: 1px solid rgba(0, 0, 0, 0.1);
            }
        """)

        # Initialize game state
        self.current_player = 'X'
        self.board = [''] * 9
        self.winning_combo = []
        self.scores = {'X': 0, 'O': 0}

        # Create main widget and vertical layout
        self.central_widget = QWidget()
        self.central_widget.setStyleSheet("""
            background-color: transparent;
            border-radius: 12px;
        """)
        self.setCentralWidget(self.central_widget)
        self.main_layout = QVBoxLayout()
        self.main_layout.setContentsMargins(10, 10, 10, 10)
        self.main_layout.setSpacing(0)
        self.central_widget.setLayout(self.main_layout)

        # Create custom title bar
        self.title_bar = QWidget()
        self.title_bar.setFixedHeight(40)
        self.title_bar.setStyleSheet("""
            background: qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:1, stop:0 rgba(240, 240, 240, 0.8), stop:1 rgba(200, 200, 200, 0.8));
            border-top-left-radius: 12px;
            border-top-right-radius: 12px;
            border-bottom: 1px solid rgba(0, 0, 0, 0.1);
        """)
        title_layout = QHBoxLayout()
        title_layout.setContentsMargins(10, 0, 10, 0)
        title_layout.setSpacing(6)

        # Score display for X (left)
        self.score_x_label = QLabel(f"X: {self.scores['X']}")
        self.score_x_label.setStyleSheet("""
            font-size: 14px;
            font-family: 'San Francisco', -apple-system, BlinkMacSystemFont, sans-serif;
            font-weight: 600;
            color: #007aff;
            padding: 4px 10px;
            border-radius: 6px;
            background-color: rgba(255, 255, 255, 0.7);
            border: 1px solid rgba(0, 0, 0, 0.1);
        """)
        title_layout.addWidget(self.score_x_label)

        # Spacer to push restart button to center
        title_layout.addStretch()

        # Restart button (center)
        self.restart_button = QPushButton("↻")
        self.restart_button.setFixedSize(24, 24)
        self.restart_button.setStyleSheet("""
            QPushButton {
                font-size: 14px;
                background-color: #007aff;
                border-radius: 12px;
                border: none;
                color: #ffffff;
            }
            QPushButton:hover {
                background-color: #005bb5;
            }
        """)
        self.restart_button.clicked.connect(self.reset_game)
        title_layout.addWidget(self.restart_button)

        # Spacer to push O score to right
        title_layout.addStretch()

        # Score display for O (right)
        self.score_o_label = QLabel(f"O: {self.scores['O']}")
        self.score_o_label.setStyleSheet("""
            font-size: 14px;
            font-family: 'San Francisco', -apple-system, BlinkMacSystemFont, sans-serif;
            font-weight: 600;
            color: #ff2d55;
            padding: 4px 10px;
            border-radius: 6px;
            background-color: rgba(255, 255, 255, 0.7);
            border: 1px solid rgba(0, 0, 0, 0.1);
        """)
        title_layout.addWidget(self.score_o_label)

        self.title_bar.setLayout(title_layout)
        self.main_layout.addWidget(self.title_bar)

        # Create game grid
        self.grid_widget = QWidget()
        self.grid_layout = QGridLayout()
        self.grid_layout.setSpacing(8)
        self.grid_layout.setContentsMargins(10, 10, 10, 10)
        self.grid_widget.setLayout(self.grid_layout)
        self.main_layout.addWidget(self.grid_widget)

        # Create buttons
        self.buttons = []
        for i in range(9):
            button = QPushButton('')
            button.setFixedSize(90, 90)
            button.clicked.connect(lambda checked, idx=i: self.button_clicked(idx))
            self.grid_layout.addWidget(button, i // 3, i % 3)
            self.buttons.append(button)

        # Base styling for game buttons
        self.grid_widget.setStyleSheet("""
            QPushButton {
                font-size: 36px;
                font-family: 'San Francisco', -apple-system, BlinkMacSystemFont, sans-serif;
                font-weight: 600;
                background-color: rgba(255, 255, 255, 0.9);
                border-radius: 10px;
                border: 1px solid rgba(0, 0, 0, 0.1);
                color: #000000;
            }
            QPushButton:enabled:hover {
                background-color: rgba(240, 240, 240, 0.9);
            }
            QPushButton:disabled {
                background-color: rgba(255, 255, 255, 0.9);
            }
        """)

        # Variables for dragging
        self.dragging = False
        self.drag_position = QPoint()

    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton and self.title_bar.geometry().contains(event.pos()):
            self.dragging = True
            self.drag_position = event.globalPosition().toPoint() - self.pos()
            event.accept()

    def mouseMoveEvent(self, event):
        if self.dragging and event.buttons() & Qt.MouseButton.LeftButton:
            self.move(event.globalPosition().toPoint() - self.drag_position)
            event.accept()

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self.dragging = False
            event.accept()

    def button_clicked(self, index):
        if self.board[index] == '':
            self.board[index] = self.current_player
            self.buttons[index].setText(self.current_player)
            text_color = '#007aff' if self.current_player == 'X' else '#ff2d55'
            self.buttons[index].setStyleSheet(f"""
                color: {text_color};
                font-size: 36px;
                font-family: 'San Francisco', -apple-system, BlinkMacSystemFont, sans-serif;
                font-weight: 600;
                background-color: rgba(255, 255, 255, 0.9);
                border-radius: 10px;
                border: 1px solid rgba(0, 0, 0, 0.1);
            """)
            self.buttons[index].setEnabled(False)

            if self.check_winner():
                self.start_celebration()
            elif '' not in self.board:
                self.show_message("It's a draw!")
                self.disable_board()
            else:
                self.current_player = 'O' if self.current_player == 'X' else 'X'

    def check_winner(self):
        win_combinations = [
            [0, 1, 2], [3, 4, 5], [6, 7, 8],  # Rows
            [0, 3, 6], [1, 4, 7], [2, 5, 8],  # Columns
            [0, 4, 8], [2, 4, 6]  # Diagonals
        ]

        for combo in win_combinations:
            if self.board[combo[0]] == self.board[combo[1]] == self.board[combo[2]] != '':
                self.winning_combo = combo
                return True
        return False

    def start_celebration(self):
        self.scores[self.current_player] += 1
        self.score_x_label.setText(f"X: {self.scores['X']}")
        self.score_o_label.setText(f"O: {self.scores['O']}")

        for idx in self.winning_combo:
            text_color = '#007aff' if self.board[idx] == 'X' else '#ff2d55'
            self.buttons[idx].setStyleSheet(f"""
                color: {text_color};
                font-size: 36px;
                font-family: 'San Francisco', -apple-system, BlinkMacSystemFont, sans-serif;
                font-weight: 600;
                background: qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:1, stop:0 rgba(200, 200, 255, 0.9), stop:1 rgba(150, 150, 255, 0.9));
                border-radius: 10px;
                border: 1px solid rgba(0, 0, 0, 0.1);
            """)
        self.disable_board()
        self.show_message(f"Player {self.current_player} wins!")

    def show_message(self, message):
        msg = QMessageBox(self)
        msg.setWindowFlags(Qt.WindowType.FramelessWindowHint)
        msg.setStyleSheet("""
            QMessageBox {
                background: qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:1, stop:0 rgba(255, 255, 255, 0.95), stop:1 rgba(240, 240, 240, 0.95));
                font-size: 14px;
                font-family: 'San Francisco', -apple-system, BlinkMacSystemFont, sans-serif;
                border-radius: 10px;
                color: #000000;
                border: 1px solid rgba(0, 0, 0, 0.1);
            }
            QLabel {
                color: #000000;
            }
            QPushButton {
                background-color: #007aff;
                border-radius: 8px;
                border: none;
                padding: 6px 12px;
                min-width: 80px;
                font-size: 13px;
                font-family: 'San Francisco', -apple-system, BlinkMacSystemFont, sans-serif;
                color: #ffffff;
            }
            QPushButton:hover {
                background-color: #005bb5;
            }
        """)
        msg.setText(message)
        restart_button = msg.addButton("Restart Game", QMessageBox.ButtonRole.AcceptRole)
        ok_button = msg.addButton("New Game", QMessageBox.ButtonRole.AcceptRole)
        close_button = msg.addButton("Close", QMessageBox.ButtonRole.RejectRole)
        msg.exec()

        if msg.clickedButton() in [restart_button, ok_button]:
            self.reset_game()
        elif msg.clickedButton() == close_button:
            self.close()

    def disable_board(self):
        for button in self.buttons:
            button.setEnabled(False)

    def reset_game(self):
        self.board = [''] * 9
        self.winning_combo = []
        self.current_player = 'X'
        for button in self.buttons:
            button.setText('')
            button.setEnabled(True)
            button.setStyleSheet("""
                font-size: 36px;
                font-family: 'San Francisco', -apple-system, BlinkMacSystemFont, sans-serif;
                font-weight: 600;
                background-color: rgba(255, 255, 255, 0.9);
                border-radius: 10px;
                border: 1px solid rgba(0, 0, 0, 0.1);
                color: #000000;
            """)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setStyle('Fusion')
    game = TicTacToe()
    game.show()
    sys.exit(app.exec())