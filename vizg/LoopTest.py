from machine import Machine
from macroVariable import MacroVariable
from program import Program
from loop import Loop
from commands import LinearFeedMove
from decimal import  Decimal

# Initialize the Machine
machine = Machine("Haas_VF2")

# Set initial macro variable values in the machine
machine.set_macro_variable(100, Decimal(10.0000))
machine.set_macro_variable(101, Decimal(20.0000))

# Create some macro variables
x_var = MacroVariable(alias="X_start", num=100, default_value="#100", machine=machine)
y_var = MacroVariable(alias="Y_start", num=101, default_value="#101", machine=machine)

# Initialize a G-code program
gcode_program = Program(o_number=1005, comment="Nested Loop Test Program")

# Create the outer WHILE loop
outer_loop = Loop(condition_expression="[#100 LT 50]", machine=machine, loop_id=1)

# Add blocks inside the outer WHILE loop
outer_loop.add_block(LinearFeedMove(x=x_var, y=y_var))

# Create an inner WHILE loop
inner_loop = Loop(condition_expression="[#101 LT 100]", machine=machine, loop_id=2)

# Add blocks inside the inner WHILE loop
inner_loop.add_block(LinearFeedMove(x=x_var, y=y_var, f=100))

# Add the inner loop to the outer loop
outer_loop.add_block(inner_loop)

# Add the outer WHILE loop to the program
gcode_program.add_block(outer_loop)

# Print the program with nested loops
print(gcode_program)