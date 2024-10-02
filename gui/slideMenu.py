import sys
from PySide6.QtWidgets import (QApplication, QMainWindow, QWidget, QHBoxLayout, QVBoxLayout,  QPushButton, QLabel, QLayout, QFrame, QSizePolicy)
from PySide6.QtCore import Qt, QPropertyAnimation, QRect, QSize, QPoint

class QFlowLayout(QLayout):
    def __init__(self, parent=None, margin=0, spacing=-1):
        super().__init__(parent)
        self.itemList = []
        self.setContentsMargins(margin, margin, margin, margin)
        self.setSpacing(spacing)

    def addItem(self, item):
        self.itemList.append(item)

    def count(self):
        return len(self.itemList)

    def itemAt(self, index):
        if 0 <= index < len(self.itemList):
            return self.itemList[index]
        return None

    def takeAt(self, index):
        if 0 <= index < len(self.itemList):
            return self.itemList.pop(index)
        return None

    def expandingDirections(self):
        return Qt.Orientations(0)

    def hasHeightForWidth(self):
        return True

    def heightForWidth(self, width):
        height = self.doLayout(QRect(0, 0, width, 0), True)
        return height

    def setGeometry(self, rect):
        super().setGeometry(rect)
        self.doLayout(rect, False)

    def sizeHint(self):
        return self.minimumSize()

    def minimumSize(self):
        size = QSize()
        for item in self.itemList:
            size = size.expandedTo(item.minimumSize())
        left, top, right, bottom = self.getContentsMargins()
        size += QSize(left + right, top + bottom)
        return size

    def doLayout(self, rect, testOnly):
        left, top, right, bottom = self.getContentsMargins()
        effectiveRect = rect.adjusted(+left, +top, -right, -bottom)
        x = effectiveRect.x()
        y = effectiveRect.y()
        lineHeight = 0

        for item in self.itemList:
            wid = item.widget()
            spaceX = self.spacing()
            spaceY = self.spacing()
            nextX = x + item.sizeHint().width() + spaceX
            if nextX - spaceX > effectiveRect.right() and lineHeight > 0:
                x = effectiveRect.x()
                y = y + lineHeight + spaceY
                nextX = x + item.sizeHint().width() + spaceX
                lineHeight = 0

            if not testOnly:
                item.setGeometry(QRect(QPoint(x, y), item.sizeHint()))

            x = nextX
            lineHeight = max(lineHeight, item.sizeHint().height())

        return y + lineHeight - rect.y() + bottom



class SlidingMenu(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setStyleSheet("background-color: #f0f0f0;")
        self.option_frame = QWidget()
        self.toggle_frame = QFrame()
        self.toggle_frame.setStyleSheet("background-color: rgba(0, 0, 0, 0); ")
        self.is_toggled = False
        self.layout = QVBoxLayout(self)
        self.option_layout = QFlowLayout(self.option_frame, 10, 10)
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
        

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Sliding Menu Example")
        self.setGeometry(100, 100, 400, 500)

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        
        self.layout = QVBoxLayout(self.central_widget)
        
        
        self.sliding_menu = SlidingMenu(self)
        self.sliding_menu.setGeometry(0, -200 + self.sliding_menu.menu_button.height(), self.width(), 200)
        
        #self.menu_visible = False
        
    def resizeEvent(self, event):
        super().resizeEvent(event)
        self.sliding_menu.setGeometry(0, -200 + self.sliding_menu.menu_button.height(), self.width(), 200)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
