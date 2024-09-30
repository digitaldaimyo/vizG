# Import necessary classes
from program import Program
from loop import Loop
from commands import LinearFeedMove, RemoteSub 
from machine import Machine
from macroVariable import  MacroVariable 
from word import M99
from program import Program

# Initialize the Machine
machine = Machine("Haas_VF2")

# Set initial macro variable values in the machine
machine.set_macro_variable(100, 15.0000)
machine.set_macro_variable(101, 20.0000)

# Create some macro variables and set them in the machine
x_var = MacroVariable(alias="X_start", num=100, default_value="#100 + 5", machine=machine)
y_var = MacroVariable(alias="Y_start", num=101, default_value="#101 + 10", machine=machine)

# Initialize a G-code program
gcode_program = Program(o_number=1005, comment="Subprogram Test")

# Add a subprogram call using M98
gcode_program.add_block(RemoteSub(o_number=1010, repeat_count=3))  # Calls O1010 three times

# Add some blocks before and after the subprogram call
gcode_program.add_block(LinearFeedMove(x=x_var, y=y_var, f=100))

# End the program with M99 to signify the end of a loop or subprogram
gcode_program.add_block(M99())

# Print the final G-code program
print(gcode_program)