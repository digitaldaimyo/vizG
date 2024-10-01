from macroVariable import MacroVariable
from numeric import Numeric 
from block import Block

class OperatorWord:
    """
    A class that represents operators like =, +, - in G-code expressions.
    These can be used to build more complex expressions.
    """
    VALID_OPERATORS = ['=', '+', '-', '*', '/']

    def __init__(self, operator: str):
        """
        Initialize an OperatorWord with the given operator.
        :param operator: The operator string (e.g., '=', '+', '-', etc.)
        """
        self.operator = operator
        self.validate(None)  # Validate the operator upon creation

    def validate(self, block=None):
        """
        Validate the operator to ensure it's one of the allowed types.
        """
        if self.operator not in self.VALID_OPERATORS:
            raise ValueError(f"Invalid operator: '{self.operator}'. Must be one of {self.VALID_OPERATORS}")

    def __repr__(self):
        """
        Return the string representation of the operator.
        """
        return self.operator
        
class Expression:
    """
    Represents an expression in a G-code block, such as `#101 = #102 + 5.02`.
    It can contain macro variables, numbers, and operators.
    """
    
    def __init__(self, left, operator: OperatorWord, right):
        """
        Initialize an expression.
        :param left: The left-hand side (either a macro variable or numeric value).
        :param operator: The operator (an instance of OperatorWord).
        :param right: The right-hand side (either a macro variable or numeric value).
        """
        self.left = left
        self.operator = operator
        self.right = right

    def validate(self, block=None):
        """
        Validate the expression by ensuring the left, right, and operator are valid.
        """
        # Validate the operator
        self.operator.validate(None)
        
        # Validate that the left and right sides are valid macro variables or numbers
        if not isinstance(self.left, (MacroVariable, Numeric)):
            raise ValueError(f"Invalid left operand: {self.left}")
        if not isinstance(self.right, (MacroVariable, Numeric)):
            raise ValueError(f"Invalid right operand: {self.right}")

    def __repr__(self):
        """
        Return a string representation of the expression.
        """
        return f"{self.left} {self.operator} {self.right}"
        
# Create an expression like #101 = #102 + 5.02
left_var = MacroVariable(101, num="#101")
right_var = MacroVariable(102, num="#102")
constant = Numeric(5.02)

# Create an expression with the "+" operator
expression = Expression(left_var, OperatorWord('+'), constant)

# Validate the expression
expression.validate()

# Add the expression's components to the block
block = Block()
block.add_word(left_var)      # Add left variable
block.add_word(OperatorWord('='))  # Add assignment operator
block.add_word(expression)    # Add the full expression (this will include the right side and operator)

# Validate the block
block.validate()

# Output the block
print(block)