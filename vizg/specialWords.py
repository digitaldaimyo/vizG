import re

class SpecialWord():
    """
    A subclass of Word that represents special words like DPRINT or comments.
    These words do not follow the typical G-code address + numeric structure.
    """
    def __init__(self, text: str):
        self.text = text

    def validate(self, block):
        pass

    def __repr__(self):
        return f"<SpecialWord: {self.text}>"
        

class DPRNT(SpecialWord):
    def validate(self, block):
        """
        Validate the DPRNT statement based on the Haas format.
        Ensure text and variables follow the correct format.
        """
        # Ensure the statement starts with "DPRNT["
        dprnt_str = str(self)
        if not dprnt_str.startswith("DPRNT["):
            raise ValueError(f"DPRNT statement must start with 'DPRNT['. Got: {dprnt_str}")

        # Ensure the statement ends with a closing bracket ']'
        if not dprnt_str.endswith(']'):
            print("raising error")
            raise ValueError(f"DPRNT statement must end with ']'. Got: {dprnt_str}")

        # Strip 'DPRNT[' and the closing ']'
        inner_content = dprnt_str[7:-1]  # Remove "DPRNT[" at the start and "]" at the end

        # Regular expression to match macro variables in the form #nnnn[wf]
        variable_format_regex = re.compile(r"#\d{1,4}\[\d{1}[0-8]\]")

        # Split the inner content into potential variables and text components
        parts = inner_content.split()

        for part in parts:
            # Check if the part is a macro variable
            if part.startswith("#"):
                # Ensure it matches the variable format #nnnn[wf]
                if not variable_format_regex.match(part):
                    raise ValueError(f"Invalid macro variable format in DPRNT: {part}")
            # Ensure no invalid characters in non-variable parts
            elif not re.match(r"^[A-Za-z0-9\s\+\-\*\/#\[\]]*$", part):
                raise ValueError(f"Invalid characters in DPRNT statement: {part}")
    def __repr__(self):
        return f'DPRNT[{self.text}]'

class Comment(SpecialWord):
    """
    Comment is a subclass of SpecialWord that represents G-code comments.
    It ensures that the comment starts and ends with parentheses ( ).
    """

    def validate(self, block):
        """
        Validate that the comment starts with '(' and ends with ')'.
        """
        if not str(self).startswith('(') or not str(self).endswith(')'):
            raise ValueError(f"Comment must start with '(' and end with ')'. Got: {self.text}")

    def __repr__(self):
        """
        Ensure that the comment text is wrapped in parentheses.
        If it's not, it will be handled during validation.
        """
        return f"({self.text})"
