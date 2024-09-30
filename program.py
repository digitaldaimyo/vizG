class Program:
    def __init__(self, o_number, comment="", line_ending=";"):
        """
        Represents a G-code program.
        :param o_number: Program O-number.
        :param comment: Program comment.
        :param line_ending: Line-ending character (default is ';').
        """
        self.o_number = o_number
        self.comment = comment
        self.blocks = []  # Stores the blocks of G-code commands
        self.line_ending = line_ending  # Line-ending character

    def add_block(self, block):
        """Adds a block of G-code to the program."""
        self.blocks.append(block)

    def __repr__(self):
        """
        Generates the G-code program as a string, with each block ending with the line-ending character.
        """
        lines = []
        lines.append(f"%{self.line_ending}")  # Start the program with %
        lines.append(f"O{self.o_number} ({self.comment}){self.line_ending}")  # O-number line with comment

        for block in self.blocks:
            block_str = str(block).split('\n')  # Split the block into individual lines
            for line in block_str:
                lines.append(f"{line}{self.line_ending}")  # Add line-ending to each G-code line

        lines.append(f"%{self.line_ending}")  # End the program with %
        return '\n'.join(lines)