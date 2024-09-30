from enum import Enum
from decimal import Decimal 

from numeric import Numeric 
from words import *
from words import AWord, FWord, HWord, G00, G43, G65, M03, M04, M06, PWord, SWord, TWord, XWord, YWord, ZWord
from address import *
from address import X, Y, Z ,A , F, S
from block import Block  # Import the Block class
from specialWords import Comment, DPRNT
from macroVariable import MacroVariable
from operators import OperatorWord, Expression

class SpindleDirection(Enum):
    """Enum representing spindle directions."""
    CW = 'clockwise'
    CCW = 'counterclockwise'

class Command:
    """Abstract base class for all G-code commands."""
    
    def __init__(self):
        """Initialize with an empty block of words."""
        self.block = Block()  # Use Block instance to store the words
        
    def to_numeric(self, value, precision):
        if isinstance(value, MacroVariable) or isinstance(value, Numeric):
            return value
        leading_zero = False
        if precision == 0:
            leading_zero = True
        return Numeric(Decimal(value), precision, leading_zero)

    def get_block(self):
        """Return the block of words that form the command."""
        return self.block

    def validate(self):
        """Validate the command by checking its block of words."""
        self.block.validate()  # Delegate validation to the Block class

    def __repr__(self):
        """Return a string representation of the command's block."""
        return str(self.block)  # Delegate string representation to Block class


class RapidMove(Command):
    """RapidMove class encapsulates the G00 rapid move command with optional X, Y, Z, A axis movements."""
    
    def __init__(self, x=None, y=None, z=None, a=None):
        super().__init__()
        self.block.add_word(G00())  # Add the G00 word to the block

        # Add X, Y, Z, A axis words if provided
        if x is not None:
            x = self.to_numeric(x, 4)
            self.block.add_word(XWord(x))
        if y is not None:
            y = self.to_numeric(y, 4)
            self.block.add_word(YWord(y))
        if z is not None:
            z = self.to_numeric(z, 4)
            self.block.add_word(ZWord(z))
        if a is not None:
            a = self.to_numeric(a, 4)
            self.block.add_word(AWord(a))

        self.validate()  # Validate the block


class LinearFeedMove(Command):
    """LinearFeedMove class encapsulates the G01 linear feed move command with optional X, Y, Z axis movements and feed rate."""
    
    def __init__(self, x=None, y=None, z=None, f=None):
        super().__init__()
        self.block.add_word(G01())  # Add the G01 word to the block

        # Add X, Y, Z axis words if provided
        if x is not None:
            self.block.add_word(XWord(self.to_numeric(x, 4)))
        if y is not None:
            self.block.add_word(YWord(self.to_numeric(y, 4)))
        if z is not None:
            self.block.add_word(ZWord(self.to_numeric(z, 4)))

        # Add feedrate word if provided
        if f is not None:
            self.block.add_word(FWord(self.to_numeric(f, 4)))

        self.validate()  # Validate the block


class SpindleOn(Command):
    """SpindleOnCommand encapsulates the spindle direction (CW or CCW) and requires an SWord (spindle speed)."""
    
    def __init__(self, direction: SpindleDirection, spindle_speed: float):
        super().__init__()

        # Add the spindle direction word (M03 for CW or M04 for CCW)
        if direction == SpindleDirection.CW:
            self.block.add_word(M03())
        elif direction == SpindleDirection.CCW:
            self.block.add_word(M04())
        else:
            raise ValueError(f"Invalid spindle direction: {direction}")
        
        # Add the spindle speed word (SWord)
        if spindle_speed is not None:
            self.block.add_word(SWord(self.to_numeric(spindle_speed, 4)))

        self.validate()  # Validate the block


class ToolChange(Command):
    """ToolChange class encapsulates the M06 tool change command and G43 tool length offset command."""
    
    def __init__(self, tool_number: int, tool_height_offset: int):
        super().__init__()

        self.block.add_word(M06())  # Add the M06 word for the tool change
        self.block.add_word(TWord(self.to_numeric(tool_number, 0)))  # Add the TWord for the tool selection
        self.block.add_word(G43())  # Add the G43 word for tool length offset
        self.block.add_word(HWord(self.to_numeric(tool_height_offset, 0))) # Add the HWord for tool height offset

        self.validate()  # Validate the block


class ProbeOn(Command):
    """ProbeOnCommand encapsulates the G65 P9832 word to turn on the probe."""
    
    def __init__(self):
        super().__init__()

        # Add the G65 P9832 word to the block
        self.block.add_word(G65())
        self.block.add_word(PWord(self.to_numeric(9832, 0)))  # P9832 for Probe On

        self.validate()  # Validate the block


class ProbeOff(Command):
    """ProbeOffCommand encapsulates the G65 P9833 word to turn off the probe."""
    
    def __init__(self):
        super().__init__()

        # Add the G65 P9833 word to the block
        self.block.add_word(G65())
        self.block.add_word(PWord(self.to_numeric(9833, 0)))  # P9833 for Probe Off

        self.validate()  # Validate the block


class SafeMove(Command):
    """SafeMoveCommand encapsulates the G65 P9810 word, which requires X, Y, Z axis movements and feedrate (F)."""
    
    def __init__(self, x=None, y=None, z=None, f=None):
        super().__init__()

        # Add the G65 P9810 word to the block
        self.block.add_word(G65())
        self.block.add_word(PWord(self.to_numeric(9810, 0)))  # P9810 for Safe Move

        # Add X, Y, Z axis words if provided
        if x is not None:
            self.block.add_word(XWord(self.to_numeric(x, 4)))
        if y is not None:
            self.block.add_word(YWord(self.to_numeric(y, 4)))
        if z is not None:
            self.block.add_word(ZWord(self.to_numeric(z, 4)))

        # Add feedrate word (FWord) if provided
        if f is not None:
            self.block.add_word(FWord(self.to_numeric(f, 4)))

        self.validate()  # Validate the block


class ProbeSingle(Command):
    """ProbeSingleCommand encapsulates the G65 P9811 word, which requires X, Y, or Z axis movement."""
    
    def __init__(self, x=None, y=None, z=None):
        super().__init__()

        # Add the G65 P9811 word to the block
        self.block.add_word(G65())
        self.block.add_word(PWord(self.to_numeric(9811, 0)))  # P9811 for single surface measurement cycle

        # Add X, Y, Z axis words if provided
        if x is not None:
            self.block.add_word(XWord(self.to_numeric(x, 4)))
        if y is not None:
            self.block.add_word(YWord(self.to_numeric(y, 4)))
        if z is not None:
            self.block.add_word(ZWord(self.to_numeric(z, 4)))

        self.validate()  # Validate the block


class ProbePocket(Command):
    """ProbePocket command encapsulates the G65 P9812 compound word behavior for probing pockets."""
    
    def __init__(self, x=None, y=None, z=None):
        super().__init__()

        # Add G65 P9812 word to the block
        self.block.add_word(G65())
        self.block.add_word(PWord(self.to_numeric(9812, 0)))  # P9812 for Probe Pocket

        # Add either X or Y, but not both
        if x is not None and y is None:
            self.block.add_word(XWord(self.to_numeric(x , 4)))
        elif y is not None and x is None:
            self.block.add_word(YWord(self.to_numeric(y, 4)))
        else:
            raise ValueError("ProbePocket requires either X or Y, but not both.")
        
        # Z is required
        if z is not None:
            self.block.add_word(ZWord(self.to_numeric(z, 4)))
        else:
            raise ValueError("ProbePocket requires Z.")

        self.validate()  # Validate the block


class ProbeWeb(Command):
    """ProbeWeb command encapsulates the G65 P9812 compound word behavior for probing webs."""
    
    def __init__(self, x=None, y=None):
        super().__init__()

        # Add G65 P9812 word to the block
        self.block.add_word(G65())
        self.block.add_word(PWord(self.to_numeric(9812, 0)))  # P9812 for Probe Web

        # Add either X or Y, but not both
        if x is not None and y is None:
            self.block.add_word(XWord(self.to_numeric(x, 4)))
        elif y is not None and x is None:
            self.block.add_word(YWord(self.to_numeric(y, 4)))
        else:
            raise ValueError("ProbeWeb requires either X or Y, but not both.")

        self.validate()  # Validate the block

class RemoteSub(Command):
    """
    RemoteSub encapsulates M98 subprogram calls.
    Subprogram calls require an O-number (P) and optionally a repeat count (L-word).
    """
    def __init__(self, o_number, repeat_count=None):
        """
        Initialize RemoteSub with the subprogram O-number and optional repeat count.
        
        :param o_number: The O-number of the subprogram to call (P).
        :param repeat_count: Optional repeat count (L). If None, subprogram is called once.
        """
        super().__init__()
        numeric_o = self.to_numeric(o_number, 0)
        # Add the M98 word to the block with the required subprogram O-number
        self.block.add_word(M98(subprogram_o_number=numeric_o))

        # Add the required P-word for subprogram O-number
        self.block.add_word(PWord(numeric_o))

        # Optionally add the L-word for repeat count if provided
        if repeat_count is not None:
            self.block.add_word(LWord(self.to_numeric(repeat_count, 0)))

        # Validate the block at the end of initialization
        self.validate()

class AddComment(Command):
    """
    AddComment encapsulates adding a comment to a G-code block.
    The comment will appear in the G-code output as a comment within parentheses.
    """
    def __init__(self, comment_text: str):
        super().__init__()

        # Add the Comment word to the block
        self.block.add_word(Comment(comment_text))

        # Validate the block after adding the comment
        self.validate()


class LogDPrint(Command):
    """
    LogDPrint encapsulates the DPRINT special command used for logging messages.
    The message will be printed with DPRINT["message"] format.
    """
    def __init__(self, log_message: str):
        super().__init__()

        # Add the DPRINT word to the block
        self.block.add_word(DPRNT(log_message))

        # Validate the block after adding the DPRINT word
        self.validate()
        


class SetVariable(Command):
    """
    Command to set a macro variable to a specific value (either a number or another macro variable).
    """
    
    def __init__(self, var_num_to_set: int, set_to: int or float, is_var: bool):
        """
        Initialize the SetVariable command.
        
        :param var_num_to_set: The macro variable number to set (e.g., #101).
        :param set_to: The value to set the variable to (either a number or another macro variable).
        :param is_var: If True, set_to represents another macro variable number, otherwise it is a numeric value.
        """
        super().__init__()
        
        # Create a MacroVariable for the variable to be set
        self.var_to_set = MacroVariable(alias=f"#{var_num_to_set}", num=self.to_numeric(var_num_to_set, 0))

        # Depending on is_var, create either a MacroVariable or a Numeric value for the set_to part
        if is_var:
            self.value_to_set = MacroVariable(alias=f"#{set_to}", num=self.to_numeric(set_to, 0))
        else:
            self.value_to_set = Numeric(self.to_numeric(set_to, 4))

        # Add the variable and the operator word '=' to the block
        self.block.add_word(self.var_to_set)
        self.block.add_word(OperatorWord("="))

        # Add the value (either MacroVariable or Numeric) to the block
        self.block.add_word(self.value_to_set)

        # Validate the block
        self.validate()