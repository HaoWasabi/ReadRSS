
from nextcord import DMChannel


def check_dm_channel(ctx):
    if isinstance(ctx.channel, DMChannel):
        return True
    return False