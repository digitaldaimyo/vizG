from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QFrame, QPushButton, QDialogButtonBox, QDialog, QLabel
)
from PySide6.QtCore import Qt
import sys

class CustomDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Modal Dialog")
        
        layout = QVBoxLayout()
        label = QLabel("This is a modal dialog.")
        layout.addWidget(label)

        buttons = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        buttons.accepted.connect(self.accept)
        buttons.rejected.connect(self.reject)
        
        menu_button = QPushButton("Menu")  # Placeholder for sliding menu button
        #menu_button.clicked.connect(self.show_modal_dialog)
        menu_button.setStyleSheet("background-color: #1abc9c; color: white; border-radius: 5px;")

        layout.addWidget(buttons)
        layout.addWidget(menu_button)
        
        self.setLayout(layout)
        self.setFixedSize(300, 200)  # Set dialog size


class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.setWindowTitle("Styled Layout Example")

        # Central widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        # Layout for the main window
        main_layout = QVBoxLayout(central_widget)

        # Menu Frame (Top)
        self.menu_frame = QFrame()
        self.menu_frame.setFrameShape(QFrame.Box)
        self.menu_frame.setFixedHeight(50)  # Fixed height for the menu area
        self.menu_frame.setStyleSheet("background-color: #2c3e50; border: 1px solid #34495e;")
        menu_button = QPushButton("Menu", self.menu_frame)  # Placeholder for sliding menu button
        menu_button.clicked.connect(self.show_modal_dialog)
        menu_button.setStyleSheet("background-color: #1abc9c; color: white; border-radius: 5px;")
        menu_button.setGeometry(10, 10, 80, 30)  # Positioning the button
        main_layout.addWidget(self.menu_frame)

        # Work Frame (Middle, Largest)
        self.work_frame = QFrame()
        self.work_frame.setFrameShape(QFrame.Box)
        self.work_frame.setStyleSheet("background-color: #ecf0f1; border: 1px solid #bdc3c7;")
        main_layout.addWidget(self.work_frame, stretch=8)  # Occupy the most height

        # Tool Frame (Bottom, Taller)
        self.tool_frame = QFrame()
        self.tool_frame.setFrameShape(QFrame.Box)
        self.tool_frame.setFixedHeight(170)  # Increased height for toolbar
        self.tool_frame.setStyleSheet("background-color: #34495e; border: 1px solid #2c3e50;")
        main_layout.addWidget(self.tool_frame)

        self.setGeometry(100, 100, 800, 600)  # Set initial size of the window
        
    def show_modal_dialog(self):
        dialog = CustomDialog(self)
        if dialog.exec() == QDialog.Accepted:
            print("Dialog accepted")
        else:
            print("Dialog canceled")


if __name__ == "__main__":
    app = QApplication(sys.argv)

    window = MainWindow()
    window.show()

    sys.exit(app.exec())
