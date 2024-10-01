import tkinter as tk
from tkinter import simpledialog, messagebox
import inspect
from word import *
from macroVariable import MacroVariable 

# Helper function to prompt for parameters
def prompt_for_params(cls):
    """Prompt the user for parameters based on the class's __init__ signature."""
    params = {}
    signature = inspect.signature(cls.__init__)
    
    for param_name, param in signature.parameters.items():
        if param_name == 'self':
            continue  # Skip 'self'

        # Determine the expected type or prompt the user with a default hint
        if param.default == inspect.Parameter.empty:
            prompt_message = f"Enter value for {param_name}:"
        else:
            prompt_message = f"Enter value for {param_name} (default {param.default}):"

        # Prompt for input based on the parameter type
        if param.annotation == float:
            user_input = simpledialog.askfloat(cls.__name__, prompt_message)
        elif param.annotation == int:
            user_input = simpledialog.askinteger(cls.__name__, prompt_message)
        else:
            user_input = simpledialog.askstring(cls.__name__, prompt_message)
        
        if user_input is None and param.default != inspect.Parameter.empty:
            user_input = param.default  # Use default if provided and user input is None

        params[param_name] = user_input

    return params

# Main Expression Editor class
class ExpressionEditor(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("G-code Expression Editor")
        self.geometry("600x500")

        # Text area to display the G-code expression being built
        self.expression_entry = tk.Text(self, height=5, width=50)
        self.expression_entry.pack(pady=10)

        # Button for validation
        validate_button = tk.Button(self, text="Validate Expression", command=self.validate_expression)
        validate_button.pack(pady=5)

        # Label to show validation status
        self.validation_label = tk.Label(self, text="")
        self.validation_label.pack(pady=5)

        # Frame for operator buttons
        operators_frame = tk.Frame(self)
        operators_frame.pack(pady=10)

        # Operator buttons
        tk.Button(operators_frame, text="+", width=5, command=lambda: self.add_operator('+')).grid(row=0, column=0)
        tk.Button(operators_frame, text="-", width=5, command=lambda: self.add_operator('-')).grid(row=0, column=1)
        tk.Button(operators_frame, text="*", width=5, command=lambda: self.add_operator('*')).grid(row=0, column=2)
        tk.Button(operators_frame, text="/", width=5, command=lambda: self.add_operator('/')).grid(row=0, column=3)
        tk.Button(operators_frame, text="=", width=5, command=lambda: self.add_operator('=')).grid(row=0, column=4)

        # Dropdown for G-code words
        gcode_dropdown = tk.StringVar(self)
        gcode_dropdown.set("Select Word")
        gcode_words = ["XWord", "YWord", "MacroVariable"]
        word_dropdown_menu = tk.OptionMenu(self, gcode_dropdown, *gcode_words, command=self.add_gcode_word)
        word_dropdown_menu.pack(pady=5)

        # Backspace button to remove last added word
        backspace_button = tk.Button(self, text="Backspace", command=self.remove_last_word)
        backspace_button.pack(pady=5)

        # Button to generate G-code output
        generate_gcode_button = tk.Button(self, text="Generate G-code", command=self.generate_gcode)
        generate_gcode_button.pack(pady=5)

        # Text area to display the generated G-code
        self.gcode_output = tk.Text(self, height=10, width=50)
        self.gcode_output.pack(pady=10)

        # List to store the G-code word objects for validation and G-code generation
        self.gcode_objects = []

    def add_operator(self, operator):
        """Insert the selected operator into the expression and create an OperatorWord object."""
        operator_word = OperatorWord(operator)
        self.gcode_objects.append(operator_word)  # Store the operator object
        self.expression_entry.insert(tk.END, repr(operator_word))

    def add_gcode_word(self, word):
        """Prompt the user for initialization variables and create the corresponding G-code word object."""
        word_classes = {
            "XWord": XWord,
            "YWord": YWord,
            "MacroVariable": MacroVariable,
        }

        selected_class = word_classes.get(word)
        if selected_class:
            params = prompt_for_params(selected_class)
            try:
                word_instance = selected_class(**params)
                self.gcode_objects.append(word_instance)
                self.expression_entry.insert(tk.END, repr(word_instance))
            except TypeError as e:
                messagebox.showerror("Error", f"Invalid parameters: {e}")

    def validate_expression(self):
        """Validate the entered expression by validating each G-code word object."""
        try:
            for obj in self.gcode_objects:
                if hasattr(obj, 'validate'):
                    obj.validate()  # Call validate if the object has a validate method
            self.validation_label.config(text="Valid Expression", fg="green")
        except Exception as e:
            self.validation_label.config(text=f"Invalid: {e}", fg="red")

    def generate_gcode(self):
        """Generate and display the G-code from the stored G-code word objects."""
        try:
            # Combine the objects' string representations to form the final G-code
            gcode = " ".join([repr(obj) for obj in self.gcode_objects])
            self.gcode_output.delete(1.0, tk.END)
            self.gcode_output.insert(tk.END, f"G-code Output:\n{gcode}\n")
        except Exception as e:
            messagebox.showerror("G-code Generation Error", str(e))

    def remove_last_word(self):
        """Remove the last added word from the expression and the list of G-code objects."""
        if self.gcode_objects:
            # Remove the last object from the list
            self.gcode_objects.pop()

            # Update the expression entry (clear and re-insert all remaining objects)
            self.expression_entry.delete(1.0, tk.END)
            for obj in self.gcode_objects:
                self.expression_entry.insert(tk.END, repr(obj))


# Run the Expression Editor
if __name__ == "__main__":
    app = ExpressionEditor()
    app.mainloop()