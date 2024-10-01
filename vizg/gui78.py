import tkinter as tk
from tkinter import simpledialog, messagebox
import inspect
from decimal import Decimal
from typing import Union, get_origin, get_args


from word import Word
from words import *
from words import CompoundWord, AxisWord 
from macroVariable import MacroVariable
from specialWords import *
from operators import *
from block import Block
from numeric import Numeric 



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
            label = tk.Label(master, text=f"{param_name} ({self.get_param_type_label(param_type)}):")
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

            # Handle Union types by trying each type in sequence
            if get_origin(param_type) is Union:
                param_value = self.try_convert_union(value, get_args(param_type))
            else:
                param_value = self.convert_value(value, param_type)

            if param_value is None:
                # If we couldn't convert, return early to avoid creating the object
                self.result = None
                return

            init_values.append(param_value)

        # Create the WordLike object with the collected values
        self.result = self.wordlike_class(*init_values)

    def try_convert_union(self, value, possible_types):
        """Attempt to convert the value to each type in the Union until successful."""
        if value == "None":
            return None  # Treat "None" string as None

        for param_type in possible_types:
            try:
                return self.convert_value(value, param_type)
            except ValueError:
                continue  # Try the next type if conversion fails

        messagebox.showerror("Invalid Input", f"Unable to convert value '{value}' to any of the types: {', '.join([t.__name__ for t in possible_types])}")
        return None

    def convert_value(self, value, param_type):
        """Convert the input value to the correct type."""
        if value == "None":
            return None  # Treat "None" string as None

        if param_type == int:
            return int(value)
        elif param_type == float:
            return float(value)
        elif param_type == Decimal:
            return Decimal(value)
        elif param_type == str:
            return str(value)
        else:
            raise ValueError(f"Unsupported type: {param_type}")

    def get_param_type_label(self, param_type):
        """Return a string representation of the parameter type, including handling for Union."""
        if get_origin(param_type) is Union:
            return f"Union[{', '.join(t.__name__ for t in get_args(param_type))}]"
        return param_type.__name__


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

        # Get all subclasses of Word and SpecialWord, excluding CompoundWord
        for cls in Word.__subclasses__() + SpecialWord.__subclasses__() + AxisWord.__subclasses__():
            if cls != CompoundWord:  # Exclude CompoundWord
                word_classes[cls.__name__] = cls

    # Add MacroVariable explicitly
            word_classes["MacroVariable"] = MacroVariable

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