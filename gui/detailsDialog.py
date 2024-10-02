from PySide6.QtWidgets import (
    QVBoxLayout, QHBoxLayout, QDialogButtonBox, QDialog, QFrame, QLabel, QWidget
)

class CustomDialog(QDialog):
    def __init__(self, parent=None, title="Dialog", size=(None, None)):
        super().__init__(parent)
        self.setModal(True)
        self.setWindowTitle(title)
        
        width, height = size
        layout = QVBoxLayout()
        self.content_frame = QFrame()

        buttons = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        buttons.accepted.connect(self.accept)
        buttons.rejected.connect(self.reject)

        layout.addWidget(self.content_frame, stretch=4)
        layout.addWidget(buttons, stretch=1)
        
        self.setLayout(layout)
        if width is not None and height is not None:
            self.setFixedSize(width, height)

class DetailField(QWidget):
    def __init__(self, label="A Detail", default="", data_type=str, required=False):
        self.label = QLabel(label)
        self.default = default
        self.data_type = data_type
        self.required = required

class DetailsDialog(CustomDialog):
    def __init__(self, parent=None, title="Details", size=(300,200), fields=None):
        super().__init__(parent, title, size)
        self.values = {}
        fields = fields if fields is not None else []

        for field in fields:
            label, default, data_type, required = field
            self.details.set(label, default)
            #field = DetailsField(label, data_type)