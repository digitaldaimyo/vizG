from PySide6.QtWidgets import (QWidget, QHBoxLayout, QVBoxLayout,  QPushButton, QFrame)
from PySide6.QtCore import QPropertyAnimation, QRect

class SlidingMenu(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.option_frame = QWidget()
        self.option_frame.setStyleSheet("background-color: lightgrey;"
                    "border: 30px black;"
                    "border-top-left-radius :0px;"
                    "border-top-right-radius : 0px;"
                    "border-bottom-left-radius : 50px;"
                    "border-bottom-right-radius : 50px;")
        self.toggle_frame = QFrame()
        self.toggle_frame.setStyleSheet("background-color: rgba(0, 0, 0, 0);")
        self.is_toggled = False
        self.layout = QVBoxLayout(self)
        self.option_layout = QHBoxLayout(self.option_frame)
        self.toggle_layout = QHBoxLayout(self.toggle_frame)
        self.menu_button = QPushButton("☰")
        self.menu_button.setStyleSheet("color: black; background-color: grey;")
        self.menu_button.setFixedSize(50, 50)
        self.menu_button.clicked.connect(self.toggle_menu)
        self.toggle_layout.addWidget(self.menu_button)
           
        self.layout.addWidget(self.option_frame, stretch=4)
        self.layout.addWidget(self.toggle_frame, stretch=1)
        
    def toggle_menu(self):
        start = self.geometry()
        if self.is_toggled:
            end = QRect(0, -200 + self.menu_button.height(), self.width(), 200)
        else:
            end = QRect(0, 0, self.width(), 200)
        
        self.animation = QPropertyAnimation(self, b"geometry")
        self.animation.setDuration(300)
        self.animation.setStartValue(start)
        self.animation.setEndValue(end)
        self.animation.start()
        
        self.is_toggled = not self.is_toggled
        
    def resizeEvent(self, event):
        super().resizeEvent(event)
        


#self.sliding_menu.setGeometry(0, -200 + self.sliding_menu.menu_button.height(), self.width(), 200)
        
