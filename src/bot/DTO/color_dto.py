class ColorDTO:
    def __init__(self, color: str):
        color_mapping = {
            "RED": "0xFF0000",
            "ORANGE": "0xFFA500",
            "YELLOW": "0xFFFF00",
            "GREEN": "0x00FF00",
            "BLUE": "0x0000FF",
            "PURPLE": "0xFF00FF",
        }
        
        # Set the color, or default to white if the color is not in the mapping
        self.__hex_color = color_mapping[color] if color in color_mapping else "0xFFFFFF"
        self.__name_color = color if color in color_mapping else "WHITE"
        
    def __str__(self):
        return f"ColorDTO(name_color={self.__name_color}, hex_color={self.__hex_color})"
    
    def __eq__(self, other):
        return self.__hex_color == other.__hex_color
    
    def get_hex_color(self):
        return self.__hex_color
    
    def get_name_color(self):
        return self.__name_color