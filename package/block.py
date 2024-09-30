class Block:
    """Encapsulates a block of G-code words."""
    
    def __init__(self):
        """Initialize an empty block of words."""
        self.words = []

    def add_word(self, word):
        """Add a word to the block."""
        self.words.append(word)

    def validate(self):
        """Validate all words in the block."""
        for word in self.words:
            word.validate(self)

    def __iter__(self):
        """Make the Block class iterable by returning an iterator over the words."""
        return iter(self.words)

    def __repr__(self):
        """Return the string representation of the block as a G-code block."""
        return ' '.join(str(word) for word in self.words)