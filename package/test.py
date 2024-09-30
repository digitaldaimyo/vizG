# Import necessary classes and enums
from commands import ProbeSingle
from numeric import Numeric


# Create a ProbeSingle command with X-axis movement for surface probing
probe_command = ProbeSingle(x=10)

# Get the G-code block for this command
print("G-code block:", probe_command.get_block())

# Validate the block
try:
    probe_command.validate()
    print("Validation passed.")
except ValueError as e:
    print("Validation failed:", str(e))

# Get the string representation of the command (i.e., the final G-code)
print("Final G-code:", repr(probe_command))