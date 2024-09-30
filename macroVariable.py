from decimal import Decimal, InvalidOperation, ROUND_HALF_UP
from typing import Optional, Union

class MacroVariable:
    def __init__(self, alias: Union[int, float, Decimal, str], num: int, default_value: Optional[Union[Decimal, int, float]] = None, machine: Optional[object] = None, precision: int = 4) -> None:
        """
        Initialize a MacroVariable instance.

        :param alias: The alias for the variable (could be int or str)
        :param num: The macro variable number (e.g., 101 for #101)
        :param default_value: Optional default value if no machine or value is provided
        :param machine: Optional machine object for resolving the macro variable value
        :param precision: Precision to use when formatting the value (default 4)
        """
        self.alias = alias
        self.num = num
        self.default_value = default_value
        self.machine = machine
        self.precision = precision

    def resolve(self) -> Decimal:
        """
        Resolve the macro variable value, using the machine or the default value if provided.

        :return: The resolved value as a Decimal, rounded to the specified precision.
        """
        if self.machine is not None:
            value = Decimal(self.machine.get_macro_variable(self.num))
        elif self.default_value is not None:
            try:
                value = Decimal(self.default_value)
            except InvalidOperation:
                raise ValueError(f"Invalid default value for macro variable {self.num}: {self.default_value}")
        else:
            raise ValueError(f"Macro variable #{self.num} has no machine or default value.")
        
        return value.quantize(Decimal(f'1.{"0" * self.precision}'), rounding=ROUND_HALF_UP)

    @property
    def value(self) -> Decimal:
        """Get the resolved value of the macro variable."""
        print("var value get")
        return self.resolve()

    def __repr__(self) -> str:
        """Return the string representation of the macro variable as #<num>."""
        print("var repr")
        return f"#{self.num}"

    def validate(self, block: Optional[object] = None) -> None:
        """Placeholder validation function. Can be extended for specific validation logic."""
        pass
        
    def __string__(self):
        return f"#{sellf.num}"

    def __format__(self, format_spec: str) -> str:
        """
        Handle the formatting of the macro variable.

        :param format_spec: The format specifier.
        :return: The formatted value of the macro variable or its G-code representation if formatting fails.
        """
        try:
            resolved_value = self.resolve()
            return format(resolved_value, format_spec)
        except Exception:
            return repr(self)

    def _get_precision(self, other: Union[int, float, Decimal]) -> int:
        """
        Get the precision (number of decimal places) for a given number.

        :param other: The number to analyze.
        :return: The number of decimal places.
        """
        other_str = str(other)
        if '.' in other_str:
            return len(other_str.split('.')[1])
        return 0

    def _convert_to_decimal(self, other: Union[int, float]) -> Decimal:
        """
        Convert a number to a Decimal, adjusting for precision.

        :param other: The number to convert.
        :return: The number as a Decimal, with appropriate precision.
        """
        try:
            other_decimal = Decimal(other)
            other_precision = self._get_precision(other)
            return other_decimal.quantize(Decimal(f'1.{"0" * other_precision}'), rounding=ROUND_HALF_UP)
        except InvalidOperation:
            raise ValueError(f"Cannot convert {other} to Decimal.")

    def __eq__(self, other: Union[int, float, Decimal]) -> bool:
        """Compare if two macro variables are equal."""
        if isinstance(other, (float, int, Decimal)):
            other_value = self._convert_to_decimal(other)
            return self.value == other_value
        return NotImplemented

    def __ne__(self, other: Union[int, float, Decimal]) -> bool:
        """Compare if two macro variables are not equal."""
        return not self.__eq__(other)

    def __lt__(self, other: Union[int, float, Decimal]) -> bool:
        """Compare if the macro variable is less than the other."""
        if isinstance(other, (float, int, Decimal)):
            other_value = self._convert_to_decimal(other)
            return self.value < other_value
        return NotImplemented

    def __le__(self, other: Union[int, float, Decimal]) -> bool:
        """Compare if the macro variable is less than or equal to the other."""
        if isinstance(other, (float, int, Decimal)):
            other_value = self._convert_to_decimal(other)
            return self.value <= other_value
        return NotImplemented

    def __gt__(self, other: Union[int, float, Decimal]) -> bool:
        """Compare if the macro variable is greater than the other."""
        if isinstance(other, (float, int, Decimal)):
            other_value = self._convert_to_decimal(other)
            return self.value > other_value
        return NotImplemented

    def __ge__(self, other: Union[int, float, Decimal]) -> bool:
        """Compare if the macro variable is greater than or equal to the other."""
        if isinstance(other, (float, int, Decimal)):
            other_value = self._convert_to_decimal(other)
            return self.value >= other_value
        return NotImplemented