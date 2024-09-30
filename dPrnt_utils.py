from specialWords import DPRNT
from macroVariable import MacroVariable
from block import Block
from program import Program

def pad_text_for_column(text, total_width):
    """
    Pad text with asterisks (*) to fit into a column of the specified width.
    DPRNT replaces '*' with spaces, so this ensures alignment in the output.
    
    :param text: The text to pad.
    :param total_width: The total width of the column.
    :return: The text padded with '*' (or truncated if too long).
    """
    if len(text) > total_width:
        return text[:total_width]  # Truncate if too long
    else:
        return text + "*" * (total_width - len(text))

class DPRNTTableBuilder:
    """
    DPRNTTableBuilder helps to format a table with label, result, and pass/fail macro variables.
    It builds a valid DPRNT statement.
    """
    
    def __init__(self):
        self.rows = []

    def add_row(self, label: str, result_var: MacroVariable, whole_digits: int, fraction_digits: int, pass_fail_var: MacroVariable):
        """
        Add a row to the DPRNT table with label, result variable, and pass/fail status.
        
        Args:
        - label: The text label for the measurement.
        - result_var: A MacroVariable instance for the measurement result.
        - whole_digits: The number of whole digits to display.
        - fraction_digits: The number of fractional digits to display.
        - pass_fail_var: A MacroVariable instance for pass/fail (0 = fail, 1 = pass).
        """
        # Validate digits range
        if not (1 <= whole_digits <= 9) or not (0 <= fraction_digits <= 8):
            raise ValueError("Whole digits must be 1-9, and fractional digits must be 0-8.")
        
        # Format for result (e.g., #101[4.2] for 4 whole digits, 2 fractional digits)
        result_format = f"{str(result_var)}[{whole_digits}{fraction_digits}]"
        # Format for pass/fail (e.g., #201 == 1 for pass, #201 == 0 for fail)
        pass_fail_label = "FAIL"
        
        # Add the formatted row
        row = f"{pad_text_for_column(label,15)}{result_format}***{pass_fail_label}*{str(pass_fail_var)}[10]"
        self.rows.append(row)
        
    def remove_row(self, index: int):
        """
        Remove a row from the DPRNT table by its index.
        
        Args:
        - index: The index of the row to remove.
        """
        if 0 <= index < len(self.rows):
            self.rows.pop(index)  # Remove the row at the specified index
        else:
            raise IndexError("Row index out of range.")

    def build(self) -> str:
        """
        Build and return the complete DPRNT statement as a list of DPRNT objects.
        """
        prnts = []
        for row in self.rows:
            dprnt = DPRNT(row)
            prnts.append(dprnt)
        return prnts


# Create MacroVariable instances
diameter_result = MacroVariable("Diameter", 101, default_value=42.345)
height_result = MacroVariable("Height", 102, default_value=31.2)
width_result = MacroVariable("Width", 103, default_value=32.456)

pass_fail_1 = MacroVariable("PassFail1", 201, default_value=1)
pass_fail_2 = MacroVariable("PassFail2", 202, default_value=0)
pass_fail_3 = MacroVariable("PassFail3", 203, default_value=1)

# Create an instance of the table builder
builder = DPRNTTableBuilder()

# Add rows to the table
builder.add_row("DIAMETER", diameter_result, 4, 2, pass_fail_1)   # Label: Diameter, Result: #101[42], Pass/Fail: #201
builder.add_row("HEIGHT", height_result, 3, 1, pass_fail_2)       # Label: Height, Result: #102[31], Pass/Fail: #202
builder.add_row("WIDTH", width_result, 3, 2, pass_fail_3)         # Label: Width, Result: #103[32], Pass/Fail: #203

# Build the DPRNT statement
prog = Program(1234, "Probe Results Table")
dprint_table = builder.build()
for row in dprint_table:
    block = Block()
    block.add_word(row)
    prog.add_block(block)
    #print(str(row))
print(prog)