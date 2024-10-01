import tkinter as tk
from tkinter import messagebox
from specialWords import DPRNT
from macroVariable import MacroVariable
from block import Block
from program import Program
from words import M99
from specialWords import DPRNT
from dPrnt_utils import DPRNTTableBuilder  # Importing from the dPrnt_utils module

class App:
    def __init__(self, root):
        self.root = root
        self.root.title("DPRNT Table Builder")
        self.builder = DPRNTTableBuilder()  # Use the imported class

        # Configure grid to be responsive
        self.root.grid_columnconfigure(1, weight=1)  # Make column 1 (widgets column) responsive
        self.root.grid_rowconfigure(7, weight=1)     # Make the last row (output) responsive

        # Row inputs
        self.o_number_var = tk.StringVar()
        self.report_name_var = tk.StringVar()
        self.label_var = tk.StringVar()
        self.result_var_number = tk.IntVar()
        self.pass_fail_var_number = tk.IntVar()

        # Build the GUI
        self.create_widgets()

    def create_widgets(self):
        row = 0
        # O Number Input
        tk.Label(self.root, text="O Number:").grid(row=row, column=0, sticky="e", padx=5, pady=5)
        tk.Entry(self.root, textvariable=self.o_number_var).grid(row=row, column=1, columnspan=2, sticky="ew", padx=5, pady=5)

        row += 1
        # Report Name Input
        tk.Label(self.root, text="Report Name:").grid(row=row, column=0, sticky="e", padx=5, pady=5)
        tk.Entry(self.root, textvariable=self.report_name_var).grid(row=row, column=1, columnspan=2, sticky="ew", padx=5, pady=5)

        row += 1
        # Label, Result Var, Pass/Fail Var inputs
        tk.Label(self.root, text="Label:").grid(row=row, column=0, sticky="e", padx=5, pady=5)
        tk.Entry(self.root, textvariable=self.label_var).grid(row=row, column=1, columnspan=2, sticky="ew", padx=5, pady=5)

        row += 1
        tk.Label(self.root, text="Result Var Number:").grid(row=row, column=0, sticky="e", padx=5, pady=5)
        tk.Entry(self.root, textvariable=self.result_var_number).grid(row=row, column=1, columnspan=2, sticky="ew", padx=5, pady=5)

        row += 1
        tk.Label(self.root, text="Pass/Fail Var Number:").grid(row=row, column=0, sticky="e", padx=5, pady=5)
        tk.Entry(self.root, textvariable=self.pass_fail_var_number).grid(row=row, column=1, columnspan=2, sticky="ew", padx=5, pady=5)

        # Add Row and Build buttons
        row += 1
        tk.Button(self.root, text="Add Row", command=self.add_row).grid(row=row, column=0, padx=5, pady=10)
        tk.Button(self.root, text="Build Program", command=self.build_program).grid(row=row, column=1, columnspan=2, sticky="ew", padx=5, pady=10)

        # Listbox for displaying rows (Full Width)
        row += 1
        tk.Label(self.root, text="Added Rows:").grid(row=row, column=0, sticky="nw", padx=5, pady=5)
        self.rows_listbox = tk.Listbox(self.root, height=10)
        self.rows_listbox.grid(row=row, column=0, columnspan=3, sticky="nsew", padx=5, pady=5)

        # Remove selected row button (Centered)
        row += 1
        tk.Button(self.root, text="Remove Selected Row", command=self.remove_selected_row).grid(row=row, column=0, columnspan=3, sticky="ew", padx=5, pady=10)
        
        # Text widget for program output (Full Width)
        row += 1
        tk.Label(self.root, text="Output:").grid(row=row, column=0, sticky="nw", padx=5, pady=5)
        self.output_text = tk.Text(self.root, height=15)
        self.output_text.grid(row=row, column=0, columnspan=3, sticky="nsew", padx=5, pady=5)

        # Add "Copy to Clipboard" button
        row += 1
        tk.Button(self.root, text="Copy to Clipboard", command=self.copy_to_clipboard).grid(row=row, column=0, columnspan=3, sticky="ew", padx=5, pady=10)

        # Make row and column expandable
        self.root.grid_rowconfigure(row, weight=1)
        self.root.grid_columnconfigure(1, weight=1)
        self.root.grid_columnconfigure(2, weight=1)

    def add_row(self):
        try:
            label = self.label_var.get().upper()  # Convert the label to uppercase
            result_var = MacroVariable(
                "ResultVar",  # No name input anymore, so we provide a default name
                self.result_var_number.get()
            )
            pass_fail_var = MacroVariable(
                "PassFailVar",  # No name input anymore, so we provide a default name
                self.pass_fail_var_number.get()
            )

            # Set default whole digits and fractional digits to 4
            whole_digits = 4
            fraction_digits = 4

            # Add row to DPRNT table builder
            self.builder.add_row(label, result_var, whole_digits, fraction_digits, pass_fail_var)

            # Add row to Listbox for display
            display_text = f"{label}: ResultVar#{self.result_var_number.get()} PassFailVar#{self.pass_fail_var_number.get()}"
            self.rows_listbox.insert(tk.END, display_text)

            self.clear_fields()
        except Exception as e:
            messagebox.showerror("Error", str(e))  # Only show errors

    def remove_selected_row(self):
        try:
            selected_index = self.rows_listbox.curselection()
            if not selected_index:
                messagebox.showwarning("Warning", "No row selected to remove!")
                return
    
            selected_index = selected_index[0]  # Get the first (and only) selected item index
    
            # Remove row from the builder
            self.builder.remove_row(selected_index)
    
            # Remove row from the Listbox
            self.rows_listbox.delete(selected_index)
            
        except Exception as e:
            messagebox.showerror("Error", str(e))  # Only show errors
            
    def build_program(self):
        try:
            prog = Program(int(self.o_number_var.get()), self.report_name_var.get())

            # Insert O Number and Report Name at the start of the program
            header_block = Block()
            header_text = "TIME*#3012[11]****DATE*#3012[11]"
            header_dprnt = DPRNT(header_text)
            header_block.add_word(header_dprnt)
            prog.add_block(header_block)
            # Add user-defined rows
            dprint_table = self.builder.build()
            for row in dprint_table:
                block = Block()
                block.add_word(row)
                prog.add_block(block)

            # Add M99 as the end block
            end_block = Block()
            end_block.add_word(M99())
            prog.add_block(end_block)

            # Display the generated program
            self.output_text.delete(1.0, tk.END)
            self.output_text.insert(tk.END, str(prog))

        except Exception as e:
            messagebox.showerror("Error", str(e))  # Only show errors

    def copy_to_clipboard(self):
        try:
            # Copy the program text in the output Text widget to the clipboard
            program_text = self.output_text.get(1.0, tk.END).strip()  # Get the text from the widget
            if program_text:
                self.root.clipboard_clear()  # Clear the clipboard
                self.root.clipboard_append(program_text)  # Append program text to the clipboard
                self.root.update()  # Keeps the clipboard updated with the copied text
                messagebox.showinfo("Copied", "Program copied to clipboard!")
            else:
                messagebox.showwarning("Warning", "No program to copy!")
        except Exception as e:
            messagebox.showerror("Error", str(e))  # Only show errors

    def clear_fields(self):
        self.label_var.set("")
        self.result_var_number.set(0)
        self.pass_fail_var_number.set(0)

if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    root.mainloop()