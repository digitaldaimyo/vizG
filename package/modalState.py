from word import Word
from address import G
from numeric import Numeric
from modals import ModalGroup, MODAL_GROUPS

class ModalState:
    def __init__(self):
        self.active_commands = {
            ModalGroup.MOTION: Word(G, Numeric(0, precision=0, leading_zero=True)),  # G00
            ModalGroup.PLANE_SELECTION: Word(G, Numeric(17, precision=0)),  # G17
            ModalGroup.DISTANCE_MODE: Word(G, Numeric(90, precision=0)),  # G90
            ModalGroup.UNIT_SELECTION: Word(G, Numeric(20, precision=0)),  # G20
            ModalGroup.TOOL_RADIUS_COMPENSATION: Word(G, Numeric(40, precision=0)),  # G40
            ModalGroup.CANNED_CYCLES: Word(G, Numeric(80, precision=0)),  # G80
        }

    def _validate_group(self, group):
        """Check if an integer corresponds to a valid ModalGroup."""
        if isinstance(group, int):
            if group not in [modal_group.value for modal_group in ModalGroup]:
                raise ValueError(f"Group {group} is not a valid ModalGroup")
    
    def _validate_word_in_group(self, group, word):
        """Ensure the Word passed is in the correct group based on MODAL_GROUPS."""
        word_repr = repr(word)
        if word_repr not in MODAL_GROUPS[group]:
            raise ValueError(f"Word {word_repr} is not valid for group {group.name}")

    def update(self, group, word):
        """Update the active command for a given modal group with validation."""
        if not isinstance(word, Word):
            raise TypeError("Command must be of type Word")
        
        if isinstance(group, ModalGroup):
            self._validate_word_in_group(group, word)
            self.active_commands[group] = word
        elif isinstance(group, int):
            self._validate_group(group)
            modal_group = ModalGroup(group)
            self._validate_word_in_group(modal_group, word)
            self.active_commands[modal_group] = word
        else:
            raise ValueError("Group must be of type ModalGroup or int")

    def get_active(self, group):
        """Return the active command for a given group."""
        if isinstance(group, ModalGroup):
            return self.active_commands.get(group, None)
        elif isinstance(group, int):
            self._validate_group(group)
            return self.active_commands.get(ModalGroup(group), None)
        else:
            raise ValueError("Group must be of type ModalGroup or int")

    def __repr__(self):
        return str(self.active_commands)