import tkinter as tk
from tkinter import simpledialog, messagebox
import inspect
from decimal import  Decimal
from typing import Union, Optional, List

from word import Word
from words import *
from words import CompoundWord, AxisWord 
from macroVariable import MacroVariable
from specialWords import *
from operators import *
from block import Block
from numeric import Numeric 

import tkinter as tk
from tkinter import simpledialog, messagebox
import inspect
from decimal import Decimal


class WordLikeDialog(simpledialog.Dialog):
    def __init__(self, parent, wordlike_class):
        self.wordlike_class = wordlike_class
        self.inputs = {}  # Store input widgets by parameter name
        super().__init__(parent, title=f"Create {self.wordlike_class.__name__}")

    def body(self, master):
        """Create the dynamic input form based on the init parameters."""
        # Introspect the __init__ signature
        init_signature = inspect.signature(self.wordlike_class.__init__)
        init_params = list(init_signature.parameters.items())[1:]  # Skip 'self'

        row = 0
        for param_name, param in init_params:
            param_type = param.annotation
            label = tk.Label(master, text=f"{param_name} ({param_type.__name__}):")
            label.grid(row=row, column=0, sticky="w")
            
            entry = tk.Entry(master)
            entry.grid(row=row, column=1)
            self.inputs[param_name] = entry  # Store reference to the input field
            row += 1

        return self.inputs[init_params[0][0]] if init_params else None

    def apply(self):
        """Called when OK is pressed; this method processes the input."""
        init_values = []
        for param_name, entry in self.inputs.items():
            value = entry.get()
            param_type = inspect.signature(self.wordlike_class.__init__).parameters[param_name].annotation

            # Try converting the value to the correct type
            try:
                if param_type == int:
                    value = int(value)
                elif param_type == float:
                    value = float(value)
                elif param_type == Decimal:
                    value = Decimal(value)
                elif param_type == str:
                    value = str(value)
                else:
                    raise ValueError(f"Unsupported type: {param_type}")
            except ValueError as e:
                messagebox.showerror("Invalid Input", f"Invalid value for {param_name}: {e}")
                self.result = None
                return

            init_values.append(value)

        # Create the WordLike object with the collected values
        self.result = self.wordlike_class(*init_values)


class ExpressionEditor(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("G-code Expression Editor")
        self.geometry("600x500")

        # Text area to display the G-code expression being built
        self.expression_entry = tk.Text(self, height=5, width=50)
        self.expression_entry.pack(pady=10)

        # Gather word classes for dropdown
        self.word_classes = self.gather_word_classes()

        # Dropdown for G-code words
        gcode_dropdown = tk.StringVar(self)
        gcode_dropdown.set("Select Word")
        word_dropdown_menu = tk.OptionMenu(self, gcode_dropdown, *self.word_classes.keys(), command=self.add_gcode_word)
        word_dropdown_menu.pack(pady=5)

        # List to store the G-code word objects for validation and G-code generation
        self.gcode_objects = []

    def gather_word_classes(self):
        """Function to gather valid word classes for the dropdown."""
        word_classes = {}

        # Example subclasses (replace with your actual classes)
        for cls in [Word, MacroVariable, OperatorWord]:  # Use your own classes here
            word_classes[cls.__name__] = cls

        return word_classes

    def add_gcode_word(self, word_name):
        """Open the custom dialog to create the corresponding G-code word object."""
        cls = self.word_classes[word_name]
        dialog = WordLikeDialog(self, cls)

        if dialog.result:
            word_object = dialog.result
            # Add to the expression and G-code objects list
            self.expression_entry.insert(tk.END, repr(word_object) + " ")
            self.gcode_objects.append(word_object)


# Run the Expression Editor
if __name__ == "__main__":
    app = ExpressionEditor()
    app.mainloop()