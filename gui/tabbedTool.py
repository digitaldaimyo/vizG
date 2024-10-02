from PySide6.QtCore import Qt, QPoint, QSize
from PySide6.QtWidgets import (
    QApplication, QWidget, QTabWidget, QHBoxLayout, QVBoxLayout, QPushButton, QScrollArea, QLabel
)
from PySide6.QtGui import QMouseEvent, QTouchEvent, QIcon, QPixmap, QPainter, QPainterPath

class RoundIconButton(QPushButton):
    def __init__(self, icon_path, radius):
        super().__init__()

        # Layout
        #layout = QVBoxLayout(self)

        # Load a square image and create a circular mask to retain the center
        original_pixmap = QPixmap(icon_path)  # Replace with your icon path
        masked_pixmap = self.create_circular_mask(original_pixmap)

        # Create a button with no text
        #button_with_icon = QPushButton()
        self.setIcon(QIcon(masked_pixmap))
        self.setIconSize(QSize(radius*2, radius*2))  # Adjust to match your button size

        # Set the button size to match the icon size
        self.setFixedSize(radius*2, radius*2)

        # Make the button round using a stylesheet
        self.setStyleSheet(f"""
            QPushButton {{
                border-radius: {radius};   /* Round shape (half of 100px width/height) */
            }}
        """)

    def create_circular_mask(self, pixmap):
        """ Create a circular mask that clips the edges of a square pixmap using QPainterPath. """
        size = min(pixmap.width(), pixmap.height())
        circular_pixmap = QPixmap(size, size)
        circular_pixmap.fill(Qt.transparent)  # Start with transparent background

        # Create a painter to draw the circular mask
        painter = QPainter(circular_pixmap)
        painter.setRenderHint(QPainter.Antialiasing)

        # Create a circular path
        path = QPainterPath()
        path.addEllipse(0, 0, size, size)  # Draw an ellipse path

        # Set the clip path
        painter.setClipPath(path)

        # Draw the original pixmap within the circular clipping path
        painter.drawPixmap(0, 0, pixmap.scaled(size, size, Qt.KeepAspectRatio, Qt.SmoothTransformation))

        painter.end()
        return circular_pixmap

class ScrollableButtonTab(QWidget):
    def __init__(self, tab_name, buttons):
        super().__init__()

        # Create the layout for the widget
        self.layout = QVBoxLayout(self)

        # Create the scrollable area for buttons
        self.scroll_area = QScrollArea(self)
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)  # Disable the scrollbar for aesthetics
        self.layout.addWidget(self.scroll_area)

        # Create a container widget for the buttons
        self.button_container = QWidget()
        self.button_layout = QHBoxLayout(self.button_container)

        # Create buttons and add them to the container layout
        for button in buttons:
            #button = QPushButton(button, self)
            self.button_layout.addWidget(button)   

        # Set the container widget as the scroll area's widget
        self.scroll_area.setWidget(self.button_container)

        # Variables for scrolling on drag or touch
        self.drag_active = False
        self.last_position = QPoint()
        self.setAttribute(Qt.WA_AcceptTouchEvents)  # Enable touch events for this widget

    def mousePressEvent(self, event: QMouseEvent):
        """Capture the initial mouse position when pressed."""
        if event.button() == Qt.LeftButton:
            self.drag_active = True
            self.last_position = event.pos()

    def mouseMoveEvent(self, event: QMouseEvent):
        """Scroll the content when the mouse is dragged."""
        if self.drag_active:
            delta = event.pos() - self.last_position
            self.last_position = event.pos()
            self._scroll_by_delta(delta.x())

    def mouseReleaseEvent(self, event: QMouseEvent):
        """Stop the drag when the mouse is released."""
        if event.button() == Qt.LeftButton:
            self.drag_active = False

    def touchEvent(self, event: QTouchEvent):
        """Handle touch events for scrolling."""
        touch_points = event.touchPoints()
        if len(touch_points) == 1:  # Single finger scroll
            touch_point = touch_points[0]
            if event.type() == QTouchEvent.TouchBegin:
                self.last_position = touch_point.pos().toPoint()
            elif event.type() == QTouchEvent.TouchUpdate:
                delta = touch_point.pos().toPoint() - self.last_position
                self.last_position = touch_point.pos().toPoint()
                self._scroll_by_delta(delta.x())
            elif event.type() == QTouchEvent.TouchEnd:
                self.drag_active = False

        event.accept()

    def _scroll_by_delta(self, delta_x):
        """Helper function to scroll horizontally by a delta value."""
        current_scroll_position = self.scroll_area.horizontalScrollBar().value()
        self.scroll_area.horizontalScrollBar().setValue(current_scroll_position - delta_x)

class TabbedButtonWidget(QTabWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        # Main layout for the widget
        self.layout = QHBoxLayout(self)

        # Create Buttons
        raoid_icon_path = "/workspaces/vizG/assets/images/rapidMove.png"
        self.rapid_move_button = RoundIconButton(raoid_icon_path, 35)
        #self.layout.addWidget(self.rapid_move_button)

        linear_feed_icon_path = "/workspaces/vizG/assets/images/feedMove.png"
        self.linear_feed_button = RoundIconButton(linear_feed_icon_path, 35)
        #self.layout.addWidget(self.linear_feed_button)

        # Example tabs with buttons
        self.create_tab("Movement", [self.rapid_move_button, self.linear_feed_button])
        self.create_tab("Tab 2", [])
        self.create_tab("Tab 3", [])

    def create_tab(self, tab_name, button_names):
        # Create a new scrollable button tab
        tab = ScrollableButtonTab(tab_name, button_names)
        # Add the tab to the tab widget
        self.addTab(tab, tab_name)