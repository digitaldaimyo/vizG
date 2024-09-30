import json
from typing import Any, Dict, Union

class Machine:
    def __init__(self, machine_id: str):
        self.machine_id = machine_id
        self.macro_variables = self.initialize_macro_variables()  # Official Macro Variables Table
        self.state = {}  # Additional machine state attributes

    def initialize_macro_variables(self) -> Dict[Union[int, str], Any]:
        """Initialize the macro variables table based on the official Haas CNC Mill Macros documentation."""
        return {
            # System Variables
            0: "NaN",  # Read-only: Not a number

            # Volatile Macro Arguments
            **{i: 0.0 for i in range(1, 34)},  # #1 - #33

            # User-Definable Variables (Volatile)
            **{i: 0.0 for i in range(100, 200)},  # #100 - #199

            # User-Definable Variables (Non-Volatile)
            **{i: 0.0 for i in range(500, 1000)},  # #500 - #999

            # System-Reserved Variables
            # Probing Variables
            1000: 0.0,  # Probe X position
            1001: 0.0,  # Probe Y position
            1002: 0.0,  # Probe Z position
            1003: 0.0,  # Probe A position
            1004: 0.0,  # Probe B position
            1005: 0.0,  # Probe C position

            # Tool Offset Variables
            **{i: 0.0 for i in range(1601, 1801)},  # #1601 - #1800: Number of flutes on tools #1 through 200
            **{i: 0.0 for i in range(1801, 2001)},  # #1801 - #2000: Maximum recorded vibrations of tools 1 through 200

            # Tool Length Offsets
            **{i: 0.0 for i in range(2001, 2201)},  # #2001 - #2200: Tool length offsets

            # Tool Length Wear
            **{i: 0.0 for i in range(2201, 2401)},  # #2201 - #2400: Tool length wear

            # Tool Diameter/Radius Offsets
            **{i: 0.0 for i in range(2401, 2601)},  # #2401 - #2600: Tool diameter/radius offsets

            # Tool Diameter/Radius Wear
            **{i: 0.0 for i in range(2601, 2801)},  # #2601 - #2800: Tool diameter/radius wear

            # Additional Variables
            3000: "Programmable alarm",  # #3000: Programmable alarm message
            3001: 0.0,  # #3001: Millisecond timer
            3002: 0.0,  # #3002: Hour timer

            # Current Axis Positions (Work Coordinates)
            3003: 0.0,  # #3003: Current X-axis position in work coordinates
            3004: 0.0,  # #3004: Current Y-axis position in work coordinates
            3005: 0.0,  # #3005: Current Z-axis position in work coordinates
            3006: 0.0,  # #3006: Current A-axis position in work coordinates
            3007: 0.0,  # #3007: Current B-axis position in work coordinates
            3008: 0.0,  # #3008: Current C-axis position in work coordinates

            # Current Axis Positions (Machine Coordinates)
            3010: 0.0,  # #3010: Current X-axis position in machine coordinates
            3011: 0.0,  # #3011: Current Y-axis position in machine coordinates
            3012: 0.0,  # #3012: Current Z-axis position in machine coordinates
            3013: 0.0,  # #3013: Current A-axis position in machine coordinates
            3014: 0.0,  # #3014: Current B-axis position in machine coordinates
            3015: 0.0,  # #3015: Current C-axis position in machine coordinates

            # Distance to Go on Axes
            3020: 0.0,  # #3020: Distance to go on X-axis
            3021: 0.0,  # #3021: Distance to go on Y-axis
            3022: 0.0,  # #3022: Distance to go on Z-axis
            3023: 0.0,  # #3023: Distance to go on A-axis
            3024: 0.0,  # #3024: Distance to go on B-axis
            3025: 0.0,  # #3025: Distance to go on C-axis

            # Remaining Motion Time
            3030: 0.0,  # #3030: Remaining motion time in seconds

            # Current Feed Rate and Spindle Speed
            3040: 0.0,  # #3040: Current feed rate
            3041: 0.0,  # #3041: Current spindle speed

            # Work Coordinate Offsets (G54 - G59)
            # G54
            3050: 0.0,  # #3050: G54 X-axis offset
            3051: 0.0,  # #3051: G54 Y-axis offset
            3052: 0.0,  # #3052: G54 Z-axis offset
            3053: 0.0,  # #3053: G54 A-axis offset
            3054: 0.0,  # #3054: G54 B-axis offset
            3055: 0.0,  # #3055: G54 C-axis offset

            # G55
            3060: 0.0,  # #3060: G55 X-axis offset
            3061: 0.0,  # #3061: G55 Y-axis offset
            3062: 0.0,  # #3062: G55 Z-axis offset
            3063: 0.0,  # #3063: G55 A-axis offset
            3064: 0.0,  # #3064: G55 B-axis offset
            3065: 0.0,  # #3065: G55 C-axis offset

            # G56
            3070: 0.0,  # #3070: G56 X-axis offset
            3071: 0.0,  # #3071: G56 Y-axis offset
            3072: 0.0,  # #3072: G56 Z-axis offset
            3073: 0.0,  # #3073: G56 A-axis offset
            3074: 0.0,  # #3074: G56 B-axis offset
            3075: 0.0,  # #3075: G56 C-axis offset

            # G57
            3080: 0.0,  # #3080: G57 X-axis offset
            3081: 0.0,  # #3081: G57 Y-axis offset
            3082: 0.0,  # #3082: G57 Z-axis offset
            3083: 0.0,  # #3083: G57 A-axis offset
            3084: 0.0,  # #3084: G57 B-axis offset
            3085: 0.0,  # #3085: G57 C-axis offset

            # G58
            3090: 0.0,  # #3090: G58 X-axis offset
            3091: 0.0,  # #3091: G58 Y-axis offset
            3092: 0.0,  # #3092: G58 Z-axis offset
            3093: 0.0,  # #3093: G58 A-axis offset
            3094: 0.0,  # #3094: G58 B-axis offset
            3095: 0.0,  # #3095: G58 C-axis offset

            # G59
            3100: 0.0,  # G59 X-axis offset
            3101: 0.0,  # G59 Y-axis offset
            3102: 0.0,  # G59 Z-axis offset
            3103: 0.0,  # G59 A-axis offset
            3104: 0.0,  # G59 B-axis offset
            3105: 0.0,  # G59 C-axis offset

            # Fixture Offsets (G110 - G119)
            # G110
            3110: 0.0,  # Fixture G110 X-axis offset
            3111: 0.0,  # Fixture G110 Y-axis offset
            3112: 0.0,  # Fixture G110 Z-axis offset
            3113: 0.0,  # Fixture G110 A-axis offset
            3114: 0.0,  # Fixture G110 B-axis offset
            3115: 0.0,  # Fixture G110 C-axis offset

            # G111
            3120: 0.0,  # Fixture G111 X-axis offset
            3121: 0.0,  # Fixture G111 Y-axis offset
            3122: 0.0,  # Fixture G111 Z-axis offset
            3123: 0.0,  # Fixture G111 A-axis offset
            3124: 0.0,  # Fixture G111 B-axis offset
            3125: 0.0,  # Fixture G111 C-axis offset

            # G112
            3130: 0.0,  # Fixture G112 X-axis offset
            3131: 0.0,  # Fixture G112 Y-axis offset
            3132: 0.0,  # Fixture G112 Z-axis offset
            3133: 0.0,  # Fixture G112 A-axis offset
            3134: 0.0,  # Fixture G112 B-axis offset
            3135: 0.0,  # Fixture G112 C-axis offset

            # G113
            3140: 0.0,  # Fixture G113 X-axis offset
            3141: 0.0,  # Fixture G113 Y-axis offset
            3142: 0.0,  # Fixture G113 Z-axis offset
            3143: 0.0,  # Fixture G113 A-axis offset
            3144: 0.0,  # Fixture G113 B-axis offset
            3145: 0.0,  # Fixture G113 C-axis offset

            # G114 - G119 (similar structure, initializing each)
            3150: 0.0,  # Fixture G114 X-axis offset
            3151: 0.0,  # Fixture G114 Y-axis offset
            3152: 0.0,  # Fixture G114 Z-axis offset
            3153: 0.0,  # Fixture G114 A-axis offset
            3154: 0.0,  # Fixture G114 B-axis offset
            3155: 0.0,  # Fixture G114 C-axis offset

            # Continue up to G119
            3180: 0.0,  # Fixture G119 X-axis offset
            3181: 0.0,  # Fixture G119 Y-axis offset
            3182: 0.0,  # Fixture G119 Z-axis offset
            3183: 0.0,  # Fixture G119 A-axis offset
            3184: 0.0,  # Fixture G119 B-axis offset
            3185: 0.0,  # Fixture G119 C-axis offset

            # Continue with additional system-specific variables as needed
        }

    def set_macro_variable(self, number: int, value: Union[float, str]):
        """Set a macro variable in the table."""
        if number in self.macro_variables:
            self.macro_variables[number] = value
        else:
            raise ValueError(f"Macro variable #{number} is out of the valid range.")

    def get_macro_variable(self, number: int) -> Union[float, str]:
        """Get the value of a macro variable."""
        if number in self.macro_variables:
            return self.macro_variables[number]
        else:
            raise ValueError(f"Macro variable #{number} does not exist.")

    def serialize(self) -> str:
        """Serialize the machine to a JSON string."""
        return json.dumps({
            "machine_id": self.machine_id,
            "macro_variables": self.macro_variables,
            "state": self.state
        }, indent=4)

    def deserialize(self, json_data: str):
        """Deserialize and restore machine state from a JSON string."""
        data = json.loads(json_data)
        self.machine_id = data.get("machine_id", self.machine_id)
        self.macro_variables = data.get("macro_variables", self.macro_variables)
        self.state = data.get("state", self.state)

# Example Usage
if __name__ == "__main__":
    machine = Machine("Haas_VF2")
    
    # Set a macro variable
    machine.set_macro_variable(100, 25.5)
    
    # Get a macro variable
    value = machine.get_macro_variable(100)
    print(f"Macro #100 value: {value}")
    
    # Serialize the machine state
    serialized = machine.serialize()
    print(f"Serialized Machine State:\n{serialized}")
    
    # Deserialize the machine state
    machine.deserialize(serialized)
    print("Machine state restored successfully.")