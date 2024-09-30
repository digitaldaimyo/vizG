class Loop:
    def __init__(self, condition_expression, machine=None, loop_id=None):
        """
        Represents a WHILE/DO loop block in the G-code program.
        :param condition_expression: The condition expression for the WHILE loop (e.g., #100 LT 50).
        :param machine: Optional reference to the Machine object to evaluate macro variables.
        :param loop_id: Optional ID to manage multiple loops.
        """
        self.condition_expression = condition_expression
        self.blocks = []  # Blocks inside the loop
        self.machine = machine
        self.loop_id = loop_id  # Unique loop ID for matching WHILE/END pairs

    def add_block(self, block):
        """Adds a block of G-code inside the loop."""
        self.blocks.append(block)

    def __repr__(self):
        """
        Returns the string representation of the loop (WHILE-DO/END format with loop ID numbers).
        """
        loop_id_str = f"{self.loop_id}" if self.loop_id else ""
        lines = []
        lines.append(f"WHILE{self.condition_expression}DO{loop_id_str}")  # Start of the loop

        for block in self.blocks:
            lines.append(str(block))  # Add each block inside the loop

        lines.append(f"END{loop_id_str}")  # End of the loop with the same loop ID
        return '\n'.join(lines)