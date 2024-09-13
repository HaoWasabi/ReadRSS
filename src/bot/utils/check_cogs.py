from nextcord import DMChannel, TextChannel

class CheckCogs:
    @staticmethod
    def check_dm_channel(ctx):
        if isinstance(ctx.channel, DMChannel):
            return True
        return False
    
    @staticmethod
    def check_text_channel(ctx):
        if isinstance(ctx.channel, TextChannel):
            return True
        return False