from enum import Enum

class ModalGroup(Enum):
    MOTION = 1
    PLANE_SELECTION = 2
    DISTANCE_MODE = 3
    UNIT_SELECTION = 4
    CANNED_CYCLES = 6
    TOOL_RADIUS_COMPENSATION = 7

MODAL_GROUPS = {
    ModalGroup.MOTION: {"G00", "G01", "G02", "G03"},
    ModalGroup.PLANE_SELECTION: {"G17", "G18", "G19"},
    ModalGroup.DISTANCE_MODE: {"G90", "G91"},
    ModalGroup.UNIT_SELECTION: {"G20", "G21"},
    ModalGroup.CANNED_CYCLES: {"G80", "G81", "G83", "G84", "G85"},
    ModalGroup.TOOL_RADIUS_COMPENSATION: {"G40", "G41", "G42"},
}


def is_word_in_group(group, word):
    """Class method to return True if the given Word is part of the specified ModalGroup."""
    if not isinstance(group, ModalGroup):
        raise ValueError("Group must be of type ModalGroup")
   
    word_repr = repr(word)
    return word_repr in MODAL_GROUPS.get(group, set())
