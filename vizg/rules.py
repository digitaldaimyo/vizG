from abc import ABC, abstractmethod

from vizg.modals import is_word_in_group, ModalGroup
from vizg.address import Address 
from vizg.word import Word
from vizg.specialWords import SpecialWord
from vizg.macroVariable import MacroVariable
from vizg.rule import Rule, NumericRule, BlockRule

class NumericRangeRule(NumericRule):
    def __init__(self, min_value=None, max_value=None):
        self.min_value = min_value
        self.max_value = max_value

    def validate(self, numeric):
        """Validate that the numeric value falls within the allowed range."""
        if isinstance(numeric, SpecialWord):
            return  # Skip validation for special words
        
        if numeric is None:
            return  # No numeric value to validate

        # Extract the actual numeric value, whether it's a MacroVariable or a regular number
        value = numeric.value if not isinstance(numeric, MacroVariable) else float(numeric)

        if self.min_value is not None and value < self.min_value:
            raise ValueError(f"Numeric value {value} is below the minimum allowed value of {self.min_value}")
        if self.max_value is not None and value > self.max_value:
            raise ValueError(f"Numeric value {value} is above the maximum allowed value of {self.max_value}")

class NumericIntegerRule(NumericRule):
    """
    Rule to ensure that the numeric value is an integer (no decimal).
    """
    def validate(self, numeric):
        """Validate that the numeric value is an integer."""
        if numeric is None:
            return
        
        value = numeric.value if not isinstance(numeric, MacroVariable) else numeric.resolve()

        # Check if the value is integer-like
        if not value == value.to_integral_value():
            raise ValueError(f"Numeric value {value} must be an integer.")
        
        # For floats that are effectively integers (e.g., 50.0), pass the check
        # If it's already an int, we pass
class NumericPrecisionRule(NumericRule):
    """
    Rule to enforce specific precision on floating-point numbers.
    """
    def __init__(self, precision):
        self.precision = precision

    def validate(self, numeric):
        """Validate that the numeric value has the correct precision."""
        if numeric is None:
            return
            
            
        value_str = str(numeric.value)
        # Check if the value is a MacroVariable
        if isinstance(numeric.value, MacroVariable):
            value_str = str(numeric.value.value)
            
        # Extract the actual precision of the Decimal value (or numeric type)
        
        decimal_part = value_str.split('.')[1] if '.' in value_str else ''
        actual_precision = len(decimal_part)

        # Check for too few decimal places
        if actual_precision < self.precision:
            raise ValueError(f"Numeric value {numeric.value} has too few decimal places: expected {self.precision}, got {actual_precision}.")

        # Check for too many decimal places
        elif actual_precision > self.precision:
            raise ValueError(f"Numeric value {numeric.value} has too many decimal places: expected {self.precision}, got {actual_precision}.")

class NumericLeadingZeroRule(NumericRule):
    """
    Rule to ensure that the numeric value is an integer and has a leading zero if the value is 0-9.
    """
    def validate(self, numeric):
        """Validate that the numeric value has a leading zero if in the range 0-9."""
        if numeric is None:
            return
        value = numeric.value
        print(f"value in lead value rule = {numeric}")
        if 0 <= value <= 9:
            if not repr(numeric).startswith('0'):
                raise ValueError(f"Numeric value {value} must have a leading zero for values 0-9.")

class ExcludeModalGroup(BlockRule):
    def __init__(self, modal_group):
        if not isinstance(modal_group, ModalGroup):
            raise TypeError(f"modal_group must be of type ModalGroup, not {type(modal_group).__name__}")
        self.modal_group = modal_group
        
    def validate(self, block):
        """Validate that no words in the block belong to the excluded modal group."""
        count = 0
        for word in block:
            if not isinstance(word, Word):
                continue  # Skip special words
            
            if is_word_in_group(self.modal_group, word):
                count += 1
            if count > 1:
                raise ValueError(f"Word {word} belongs to the excluded modal group {self.modal_group.name}")
                
class LimitAddress(BlockRule):
    def __init__(self, address, num=1):
        # Ensure the provided address is a valid subclass of Address
        if not issubclass(address, Address):
            raise TypeError(f"Address must be a subclass of Address, not {type(address).__name__}")
        self.address = address
        self.max_num = num

    def validate(self, block):
        """Validate that no words in the block contain the excluded address."""
        count = 0
        for word in block:
            if not isinstance(word, Word):
                continue  # Skip special words
            
            if word.address == self.address:
                count += 1
            if count > self.max_num:
                raise ValueError(f"Word with address {self.address.letter()} is excluded from this block.")

class ExcludeAddress(BlockRule):
    def __init__(self, address):
        # Ensure the provided address is a valid subclass of Address
        if not issubclass(address, Address):
            raise TypeError(f"Address must be a subclass of Address, not {type(address).__name__}")
        self.address = address

    def validate(self, block):
        """Validate that no words in the block contain the excluded address."""
        
        for word in block:
            if not isinstance(word, Word):
                continue  # Skip special words
            
            if word.address == self.address:
                raise ValueError(f"Word with address {self.address.letter()} is excluded from this block.")
                
class RequireAddress(BlockRule):
    def __init__(self, address):
        # Ensure the provided address is a valid subclass of Address
        if not issubclass(address, Address):
            raise TypeError(f"Address must be a subclass of Address, not {type(address).__name__}")
        self.address = address

    def validate(self, block):
        """Validate that at least one word in the block contains the required address."""
        for word in block:
            if not isinstance(word, Word):
                continue  # Skip special words
            
            if word.address == self.address:
                return  # Found a word with the required address, validation passed
        raise ValueError(f"Block does not contain a word with address {self.address.letter()}.")
        
class RequireOneOfAddresses(BlockRule):
    def __init__(self, addresses):
        # Ensure each address in the list is a valid subclass of Address
        for address in addresses:
            if not issubclass(address, Address):
                raise TypeError(f"All addresses must be subclasses of Address, found {type(address).__name__}")
        self.addresses = addresses

    def validate(self, block):
        """Validate that at least one word in the block contains one of the required addresses."""
        for word in block:
            if not isinstance(word, Word):
                continue  # Skip special words
            
            if any(word.address == address for address in self.addresses):
                return  # Found at least one address, validation passed
        # If none of the required addresses were found, raise an error
        address_letters = [address.letter() for address in self.addresses]
        raise ValueError(f"Block does not contain a word with any of the addresses {', '.join(address_letters)}.")

class RequireExactlyOneOfAddresses(BlockRule):
    def __init__(self, addresses):
        """
        Initializes the rule to enforce that exactly one of the given addresses must be present in the block.
        
        :param addresses: List of Address classes to check in the block.
        """
        # Ensure each address in the list is a valid subclass of Address
        for address in addresses:
            if not issubclass(address, Address):
                raise TypeError(f"All addresses must be subclasses of Address, found {type(address).__name__}")
        self.addresses = addresses

    def validate(self, block):
        """
        Validates that exactly one of the given addresses is present in the block.
        """
        matching_addresses = []

        for word in block:
            if not isinstance(word, Word):
                continue  # Skip special words

            # Check if the word's address matches any of the given addresses
            if any(word.address == address for address in self.addresses):
                matching_addresses.append(word.address)

        # Ensure exactly one address was found
        if len(matching_addresses) == 0:
            raise ValueError(f"Block must contain exactly one of the addresses: {', '.join([address.letter() for address in self.addresses])}. None found.")
        elif len(matching_addresses) > 1:
            raise ValueError(f"Block must contain exactly one of the addresses: {', '.join([address.letter() for address in self.addresses])}. Found multiple: {', '.join([address.letter() for address in matching_addresses])}.")

class RequireAllAddresses(BlockRule):
    def __init__(self, addresses):
        # Ensure each address in the list is a valid subclass of Address
        for address in addresses:
            if not issubclass(address, Address):
                raise TypeError(f"All addresses must be subclasses of Address, found {type(address).__name__}")
        self.addresses = addresses

    def validate(self, block):
        """Validate that the block contains all of the required addresses."""
        missing_addresses = []
        for address in self.addresses:
            if not any(word.address == address for word in block if isinstance(word, Word)):
                missing_addresses.append(address.letter())
        
        if missing_addresses:
            raise ValueError(f"Block is missing required addresses: {', '.join(missing_addresses)}.")
            
class DuplicateAddress(ExcludeAddress):
    """Rule that ensures no duplicate addresses appear in the block."""
    
    def validate(self, block):
        """Validate that no words in the block contain duplicate addresses."""
        address_count = {}
        
        for word in block:
            if not isinstance(word, Word):
                continue  # Skip special words
            
            # Count occurrences of each address
            if word.address in address_count:
                address_count[word.address] += 1
            else:
                address_count[word.address] = 1
        
        # Check for duplicates
        duplicates = [address.letter() for address, count in address_count.items() if count > 1]
        
        if duplicates:
            raise ValueError(f"Duplicate addresses found in the block: {', '.join(duplicates)}.")