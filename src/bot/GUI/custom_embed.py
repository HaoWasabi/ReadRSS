import nextcord

# Custom Embed class with default color and methods to set/get color
class CustomEmbed(nextcord.Embed):
    def __init__(self, **kwargs):
        # Set a default color if none is provided
        if 'color' not in kwargs:
            kwargs['color'] = nextcord.Color.blue()  # Default color set to blue
        super().__init__(**kwargs)

    def set_color(self, color):
        # Set the color of the embed. Color should be a nextcord.Color instance.
        if isinstance(color, nextcord.Color):
            self.color = color
        else:
            raise ValueError("color must be an instance of nextcord.Color")

    def get_color_hex(self):
        # Returns the hex code of the embed color as a string.
        return hex(self.color.value)