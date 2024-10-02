from PySide6.QtWidgets import QWidget, QVBoxLayout, QScrollArea, QPushButton, QFrame, QApplication
from PySide6.QtWidgets import QFrame, QVBoxLayout
from PySide6.QtCore import Qt, QMimeData
from PySide6.QtGui import QDrag

class CodeWord(QPushButton):
    def __init__(self, word: str):
        super().__init__(word)
        #self.setFixedSize(100, 40)
        self.setStyleSheet("background-color: lightgray; border: 1px solid black;")

        # Track the start position of the mouse press
        self._drag_start_position = None

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            # Store the start position of the press event
            self._drag_start_position = event.pos()
        super().mousePressEvent(event)  # Call the base class method to handle normal press

    def mouseMoveEvent(self, event):
        # Check if the left mouse button is held and moved beyond the threshold
        if event.buttons() == Qt.LeftButton:
            distance = (event.pos() - self._drag_start_position).manhattanLength()
            if distance > QApplication.startDragDistance():  # Default drag threshold
                # Trigger the drag operation
                drag = QDrag(self)
                mime_data = QMimeData()
                mime_data.setText(self.text())
                drag.setMimeData(mime_data)
                drag.exec(Qt.MoveAction)
        super().mouseMoveEvent(event)

    def mouseDoubleClickEvent(self, event):
        if event.button() == Qt.LeftButton:
            # Handle double-click action
            print(f"{self.text()} double-clicked!")
        super().mouseDoubleClickEvent(event)


class CodeBlock(QFrame):
    def __init__(self, on_change = None):
        super().__init__()
        self.setAcceptDrops(True)
        #self.setFixedSize(200, 100)
        self.setStyleSheet("background-color: white; border: 2px dashed black;")
        self.on_change = on_change

        # Layout to hold dropped WordWidgets
        self.layout = QVBoxLayout(self)
        self.setLayout(self.layout)

    def dragEnterEvent(self, event):
        if event.mimeData().hasText():
            event.acceptProposedAction()

    def dropEvent(self, event):
        word = event.mimeData().text()
        word_widget = CodeWord(word)
        self.layout.addWidget(word_widget)
        event.acceptProposedAction()
        if self.on_change is not None:
            self.on_change()
        
class CodeCanvas(QWidget):
    def __init__(self, minimum_empty=20):
        super().__init__()

        self.blocks = []
        self.minimum_empty = minimum_empty
        self.layout = QVBoxLayout(self)
        self.odd_style = "background-color: grey; border: 2px solid black;"
        self.even_style = "background-color: lightyellow; border: 2px solid black;"

        # Scroll area
        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)

        # Container widget to hold CodeBlocks
        self.container_widget = QWidget()
        self.container_layout = QVBoxLayout(self.container_widget)

        self.scroll_area.setWidget(self.container_widget)
        self.layout.addWidget(self.scroll_area)

        for _ in range(minimum_empty):
            self.add_code_block()

    def count_empties(self):
        num = 0
        count = 0
        for block in self.blocks:
            block.setStyleSheet = self.even_style if count % 2 == 0 else self.odd_style
            count += 1
            if not block.is_empty:
                continue
            num += 1

        return num

    def on_block_changed(self, block):
        empty_count = self.count_empties()
        if empty_count <= self.minimum_empty:
            needed_blocks = self.minimum_empty - empty_count

        for _ in range(needed_blocks):
            self.add_code_block(self.on_block_changed)

    def add_code_block(self):
        block = CodeBlock()
        block.setStyleSheet = self.odd_style if len(self.blocks) % 2 == 0 else self.even_style
        self.blocks.append(block)
        self.container_layout.addWidget(block)

