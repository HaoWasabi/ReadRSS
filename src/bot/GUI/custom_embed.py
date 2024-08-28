import nextcord
from ..BLL.server_color_bll import ServerColorBLL
from ..DTO.server_dto import ServerDTO

# Custom Embed class with default color and methods to set/get color
class CustomEmbed(nextcord.Embed):
    def __init__(self, id_server: str, **kwargs):
        # Fetch the default color from the server's settings
        server_color_bll = ServerColorBLL()
        server_dto = ServerDTO(id_server, "")
        server_color_dto = server_color_bll.get_server_color_by_id_server(server_dto.get_id_server())

        if 'color' not in kwargs:
            # If no color is provided, use the server's default color
            default_color = server_color_dto.get_color().get_hex_color() # type: ignore
            kwargs['color'] = nextcord.Color(int(default_color, 16))  # Convert hex to int
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