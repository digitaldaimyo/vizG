import tkinter as tk
from tkinter import simpledialog, messagebox
import inspect
from decimal import  Decimal

from vizg.words import *
from vizg.words import CompoundWord, AxisWord 
from vizg.macroVariable import MacroVariable
from vizg.specialWords import *
from vizg.operators import *
from vizg.block import Block
from vizg.numeric import Numeric 

# Function to gather valid word classes for the dropdown
def gather_word_classes():
    word_classes = {}

    # Get all subclasses of Word and SpecialWord, excluding CompoundWord
    for cls in Word.__subclasses__() + SpecialWord.__subclasses__() + AxisWord.__subclasses__():
        if cls != CompoundWord:  # Exclude CompoundWord
            word_classes[cls.__name__] = cls

    # Add MacroVariable explicitly
    word_classes["MacroVariable"] = MacroVariable

    return word_classes

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

        # Gather word classes for dropdown
        self.word_classes = gather_word_classes()

        # Dropdown for G-code words
        gcode_dropdown = tk.StringVar(self)
        gcode_dropdown.set("Select Word")
        word_dropdown_menu = tk.OptionMenu(self, gcode_dropdown, *self.word_classes.keys(), command=self.add_gcode_word)
        word_dropdown_menu.pack(pady=5)

        # Button to generate G-code output
        generate_gcode_button = tk.Button(self, text="Generate G-code", command=self.generate_gcode)
        generate_gcode_button.pack(pady=5)

        # Text area to display the generated G-code
        self.gcode_output = tk.Text(self, height=10, width=50)
        self.gcode_output.pack(pady=10)

        # List to store the G-code word objects for validation and G-code generation
        self.gcode_objects = []

        # List to store MacroVariables that the user creates
        self.macro_variables = []

    def add_operator(self, operator):
        """Insert the selected operator into the expression."""
        self.expression_entry.insert(tk.END, f" {operator} ")
        self.gcode_objects.append(OperatorWord(operator))

    def add_gcode_word(self, word):
        """Prompt the user for initialization variables and create the corresponding G-code word object."""
        cls = self.word_classes[word]
        
        # Introspect to see the init parameters
        init_signature = inspect.signature(cls.__init__)
        init_params = list(init_signature.parameters.items())[1:]  # Skip 'self'
        
        # Collect values for init parameters via a prompt
        init_values = []
        for param_name, param in init_params:
            param_type = param.annotation
            print(f"Word {word}'s {param_name} type is {param_type}")

            # Determine the type of prompt based on the expected type
            if param_type == float or param_type == Decimal or param_type == Numeric:
                print(f"param inside numbers if type dialoque ")
                value = simpledialog.askfloat(f"{cls.__name__}", f"Enter value for {param_name}:")
                if value is not None and param_type == Decimal:
                    value = Decimal(value)
            elif param_type == int:
                value = simpledialog.askinteger(f"{cls.__name__}", f"Enter value for {param_name}:")
            elif param_type == str:
                value = simpledialog.askstring(f"{cls.__name__}", f"Enter value for {param_name}:")
            elif param_type == MacroVariable:
                # Allow the user to select an existing macro variable or create a new one
                if messagebox.askyesno(f"{cls.__name__}", f"Use existing MacroVariable for {param_name}?"):
                    value = self.select_macro_variable()
                else:
                    value = self.create_macro_variable()
            else:
                ##value = simpledialog.askstring(f"{cls.__name__}", f"Enter value for {param_name}:")
                messagebox.showerror("Error", f"Unsupported type for {param_name}: {param_type}")
                return

            if value is None:
                return  # Cancel the word addition if user cancels input
            init_values.append(value)

        # Create the word object
        word_object = cls(*init_values)

        # Add to the expression and G-code objects list
        self.expression_entry.insert(tk.END, repr(word_object))
        self.gcode_objects.append(word_object)

    def select_macro_variable(self):
        """Let the user select an existing macro variable from the list."""
        if not self.macro_variables:
            messagebox.showerror("Error", "No MacroVariables available. Create one first.")
            return None
        
        options = [repr(var) for var in self.macro_variables]
        selected = simpledialog.askstring("Select MacroVariable", f"Choose one:\n{', '.join(options)}")
        
        # Find and return the matching macro variable
        for var in self.macro_variables:
            if repr(var) == selected:
                return var
        
        return None

    def create_macro_variable(self):
        """Create a new MacroVariable and add it to the list."""
        var_num = simpledialog.askinteger("MacroVariable", "Enter macro variable number (e.g., 101):")
        if var_num is not None:
            macro_var = MacroVariable("", var_num, default_value=10.0)
            self.macro_variables.append(macro_var)  # Store the macro variable
            return macro_var
        return None

    def validate_expression(self):
        """Validate the entered expression by validating each G-code word object."""
        try:
            block = Block()
            for obj in self.gcode_objects:
                block.add_word(obj)
                #if hasattr(obj, 'validate'):
                     #obj.validate()  # Call validate if the object has a validate method
            block.validate()
            self.validation_label.config(text="Valid Expression", fg="green")
        except Exception as e:
            self.validation_label.config(text=f"Invalid: {e}", fg="red")

    def generate_gcode(self):
        """Generate and display the G-code from the stored G-code word objects."""
        try:
            gcode = " ".join([repr(obj) for obj in self.gcode_objects])
            self.gcode_output.delete(1.0, tk.END)
            self.gcode_output.insert(tk.END, f"G-code Output:\n{gcode}\n")
        except Exception as e:
            tk.messagebox.showerror("G-code Generation Error", str(e))


# Run the Expression Editor
if __name__ == "__main__":
    app = ExpressionEditor()
    app.mainloop()