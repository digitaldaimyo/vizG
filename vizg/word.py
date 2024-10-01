from decimal import Decimal

from vizg.address import Address
from vizg.numeric  import Numeric
from vizg.macroVariable import MacroVariable
from vizg.rule import NumericRule, BlockRule

class Word:
    def __init__(self, address: Address, numeric: Numeric, rules=None):
        """Represents a G-code word with an address (subclass of Address), a numeric value, and optional rules."""
        if not issubclass(address, Address):
            raise TypeError(f"Address must be a subclass of Address, not {type(address).__name__}")
        self.address = address
        
        is_numeric = isinstance(numeric, Numeric)
        is_var = isinstance(numeric, MacroVariable)
        if numeric is not None and not is_numeric and not is_var:
            raise TypeError(f"Numeric value must be of type Numeric, not {type(numeric).__name__}")
        self.numeric = numeric

        # Initialize rules if not provided, ensuring that the DuplicateAddress and NumericLeadingZeroRule are always applied
        self.rules = rules if rules is not None else []
        
        # Ensure that duplicate addresses are not allowed in a block
        #self.rules.append(DuplicateAddress(address))

    def __repr__(self):
        """Return the G-code word in its conventional format (e.g., G01 or F1500)."""
        address_str = self.address.letter()  # Assume Address subclasses have a 'letter()' method
        if self.numeric is not None:
            return f"{address_str}{str(self.numeric)}"
        return f"{address_str}"

    def validate(self, block=None):
        """Validate the word by applying only NumericRule-type rules."""
        for rule in self.rules:
            if isinstance(rule, NumericRule):
                rule.validate(self.numeric)
            if block is not None and isinstance(rule, BlockRule):
                rule.validate(block)
