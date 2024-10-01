from decimal import Decimal, InvalidOperation
from macroVariable import MacroVariable

class Numeric:
    def __init__(self, value, precision=4, leading_zero=False):
        """
        Initialize a Numeric object using Decimal for precise arithmetic.
        The value can be a number or a MacroVariable.
        
        :param value: Numeric value (can be a MacroVariable or a number).
        :param precision: Precision for floating-point numbers (default: 4).
        :param leading_zero: If True, force a leading zero (for G-code like G01 to be G01 instead of G1).
        """
        self.precision = precision
        self.leading_zero = leading_zero
        
        if isinstance(value, MacroVariable):
            self.value = value  # Store the MacroVariable instance
            self.original_value = str(value)  # Keep the original string representation
        else:
            try:
                # Store the value as a Decimal for precision handling
                self.value = Decimal(value).quantize(Decimal(f'1.{"0" * precision}'))
            except (InvalidOperation, ValueError):
                raise ValueError(f"Invalid numeric value: {value}")
                
    def validate(self, block=None):
        pass

    def __repr__(self):
        """
        For G-code output, if it's a MacroVariable, show the variable reference (e.g., #101).
        Otherwise, format the numeric value with the specified precision.
        """
        if isinstance(self.value, MacroVariable):
            return repr(self.value)  # This will call MacroVariable's __repr__ method (e.g., #101)
    
        # Handle leading zero for integer-like values
        sign = '-' if self.value < 0 else ''
        abs_value = abs(self.value)
        
        if abs_value == abs_value.to_integral_value() and self.leading_zero:
            if not self.precision == 0:
                return f"{sign}{int(abs_value):02d}.{'0' * self.precision}"  # Ensure proper formatting with leading zero
            else:
                return f"{sign}{int(abs_value):02d}"
    
        # Ensure consistent formatting for floating-point values
        value_str = f"{abs_value:{self.precision}f}"
        
        # Handle the case where Decimal might not include a decimal point (e.g., integers)
        if '.' in value_str:
            integer_part, decimal_part = value_str.split('.')
            return f"{sign}{int(integer_part)}.{decimal_part[:self.precision]}"
        else:
        # No decimal part; return the integer value
            return f"{sign}{int(abs_value):02d}"

    def __eq__(self, other):
        """Override equality to compare with both Decimal and float values."""
        if isinstance(other, (float, int)):
            return self.value == Decimal(other)
        if isinstance(other, Decimal):
            return self.value == other
        return False