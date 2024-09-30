from abc import ABC, abstractmethod 

class Rule(ABC):
    """Base class for rules that can be applied to a Word or G-code block."""
    @abstractmethod
    def validate(self, value):
        """Subclasses must implement this method."""
        
class NumericRule(Rule):
    @abstractmethod
    def validate(self, numeric):
        """Subclasses of NumericRule must implement this method."""
        pass  # Abstract method to enforce implementation

class BlockRule(Rule):
    @abstractmethod
    def validate(self, block):
        """Subclasses of BlockRule must implement this method."""
        pass  # Abstract method to enforce implementation
