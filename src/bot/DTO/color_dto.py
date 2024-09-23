class ColorDTO:
    def __init__(self, color: str):
        color_mapping = {
            "red": "0xFF0000",
            "orange": "0xFFA500",
            "yellow": "0xF1C40F",
            "green": "0x2ECC71",
            "blue": "0x3498DB",
            "purple": "0x9B59B6",
            "gray": "0x808080",
            "black": "0x2F3136",
            "darkkhaki": "0xBDB76B"
        }

        # Set the color, or default to white if the color is not in the mapping
        self.hex_color = color_mapping[color] if color in color_mapping else "0x808080"
        self.name_color = color if color in color_mapping else "gray"

    def __str__(self):
        return f"ColorDTO(name_color={self.name_color}, hex_color={self.hex_color})"

    def __eq__(self, other):
        return self.hex_color == other.hex_color
