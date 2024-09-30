import asyncio
import nextcord, os, logging
from nextcord.ext import commands, tasks
from nextcord.message import Message
import google.generativeai as genai

from ..BLL.user_premium_bll import UserPremiumBLL
from ..DTO.channel_dto import ChannelDTO
from ..DTO.server_dto import ServerDTO
from ..DTO.color_dto import ColorDTO

from ..BLL.channel_bll import ChannelBLL
from ..BLL.server_bll import ServerBLL
from ..BLL.feed_bll import FeedBLL
from ..BLL.emty_bll import EmtyBLL

from ..GUI.embed_feed import EmbedFeed
from ..GUI.embed_custom import EmbedCustom
from ..utils.commands_cog import CommandsCog
from ..utils.handle_rss import read_rss_link
from ..utils.datetime_format import *

logger = logging.getLogger("Events")


class Events(CommandsCog):
    def __init__(self, bot: commands.Bot):
        super().__init__(bot)

    async def load_guilds(self):
        try:
            guilds = self.bot.guilds
            channel_bll = ChannelBLL()
            server_bll = ServerBLL()
            list_channel = channel_bll.get_all_channel()
            list_server = server_bll.get_all_server()

            for guild in guilds:
                id_server = str(guild.id)
                name_server = str(guild.name)
                server_dto = ServerDTO(id_server, name_server)

                # Insert or update server if necessary
                if server_dto not in list_server:
                    server_bll.insert_server(server_dto)
                else:
                    matching_server = next(
                        (s for s in list_server if s.get_server_id() == server_dto.get_server_id()), None
                    )
                    if matching_server and matching_server.get_server_name() != server_dto.get_server_name():
                        server_bll.update_server(server_dto)

                # Handle each channel in guild
                for channel in guild.channels:
                    id_channel = str(channel.id)
                    name_channel = channel.name
                    channel_dto = ChannelDTO(id_channel, name_channel, id_server)

                    matching_channel = next(
                        (ch for ch in list_channel if ch.get_channel_id() == channel_dto.get_channel_id()), None
                    )
                    if matching_channel and matching_channel.get_channel_name() != channel_dto.get_channel_name():
                        channel_bll.update_channel(channel_dto)

        except Exception as e:
            logger.error(f"Error loading guilds: {e}")

    async def load_dm_feed(self, list_feed, channel_send_id):
        """Load và gửi feed đến DMChannel."""
        emty_bll = EmtyBLL()

        try:
            # Fetch user for DMChannel
            channel_send = await self.bot.fetch_user(channel_send_id)

            # Process each feed
            for feed in list_feed:
                try:
                    feed_data = read_rss_link(rss_link=feed.get_link_atom_feed())
                    if not feed_data or not all(feed_data):
                        logger.warning(f"Incomplete feed data for {feed.get_link_atom_feed()}")
                        continue  # Skip to the next feed

                    feed_dto, emty_dto = feed_data
                    emty_dto.set_channel_id(channel_send_id)

                    # Check if emty already exists
                    if emty_bll.insert_emty(emty_dto):

                        # Create and send embed message
                        embed = EmbedFeed(
                            id_server=str(channel_send.id),
                            feed_dto=feed_dto,
                            emty_dto=emty_dto,
                        )

                        await channel_send.send(embed=embed)
                        logger.info(f"DM sent to {channel_send_id}")
                        logger.info(f"Inserted emty: {emty_dto.__dict__}")

                except Exception as e:
                    logger.error(f"Error processing feed {feed.get_link_atom_feed()}: {e}")

        except Exception as e:
            logger.error(f"Error fetching user for DMChannel {channel_send_id}: {e}")

    async def load_server_feed(self, list_feed, channel_send):
        """Load và gửi feed đến channel của server."""
        emty_bll = EmtyBLL()

        try:
            # Process each feed
            for feed in list_feed:
                try:
                    feed_data = read_rss_link(rss_link=feed.get_link_atom_feed())
                    if not feed_data or not all(feed_data):
                        logger.warning(f"Incomplete feed data for {feed.get_link_atom_feed()}")
                        continue  # Skip to the next feed

                    feed_dto, emty_dto = feed_data
                    emty_dto.set_channel_id(str(channel_send.id))

                    # Check if emty already exists
                    if emty_bll.insert_emty(emty_dto):

                        # Create and send embed message
                        embed = EmbedFeed(
                            id_server=str(channel_send.guild.id),
                            feed_dto=feed_dto,
                            emty_dto=emty_dto,
                        )

                        await channel_send.send(embed=embed)
                        logger.info(f"Message sent to channel {channel_send.id}")
                        logger.info(f"Inserted emty: {emty_dto.__dict__}")

                except Exception as e:
                    logger.error(f"Error processing feed {feed.get_link_atom_feed()}: {e}")

        except Exception as e:
            logger.error(f"Error processing server channel {channel_send.id}: {e}")

    async def load_list_feed(self):
        """Main function to load feeds and distribute to DM and server channels."""
        try:
            channel_bll = ChannelBLL()
            feed_bll = FeedBLL()

            list_channel = channel_bll.get_all_channel()
            # Process each channel
            for channel in list_channel:
                channel_id = channel.get_channel_id()
                channel_send_id = int(channel_id) 
                channel_send = self.bot.get_channel(channel_send_id)
                list_feed = feed_bll.get_all_feed_by_channel_id(channel_id)

                # If it's a DM channel, load and send to DM
                if not channel_send:
                    await self.load_dm_feed(list_feed, channel_send_id)
                else:  # If it's a server channel, load and send to server channel
                    await self.load_server_feed(list_feed, channel_send)

            # Gửi tin nhắn đến các kênh đã đăng ký của server
            for guild in self.bot.guilds:
                for channel in guild.text_channels:
                    # Kiểm tra xem kênh này có nằm trong danh sách kênh đã đăng ký không
                    if channel.id in [int(c.get_channel_id()) for c in list_channel]:
                        await self.load_server_feed(list_feed, channel)

        except Exception as e:
            logger.error(f"Error loading feed list: {e}")

    # async def load_list_feed_in_thread(self):
    #     """Run load_list_feed in a separate thread to avoid blocking the main event loop."""
    #     await asyncio.to_thread(self.load_list_feed)

    async def load_user_premium(self):
        try:
            user_premium_bll = UserPremiumBLL()
            list_user_premium = user_premium_bll.get_all_userpremiums()
            for user_premium in list_user_premium:
                time_registered = user_premium.get_date_registered()
                duration = user_premium.get_premium().get_duration()  # Giả sử đây là số phút hoặc số giây

                # Tính số giây đã trôi qua từ thời gian đăng ký
                if isinstance(time_registered, datetime):
                    elapsed_time_seconds = (datetime.now() - time_registered).total_seconds()
                elif isinstance(time_registered, int):
                    # Nếu time_registered là int, chuyển nó thành datetime
                    time_registered = datetime.fromtimestamp(time_registered / 1000)  # Chuyển đổi từ timestamp nếu cần
                    elapsed_time_seconds = (datetime.now() - time_registered).total_seconds()
                elif isinstance(time_registered, str):
                    # Nếu time_registered là str, chuyển nó thành datetime
                    time_registered = datetime.strptime(time_registered, "%Y-%m-%d %H:%M:%S.%f")
                    elapsed_time_seconds = (datetime.now() - time_registered).total_seconds()
                else:
                    logger.error(f"Invalid time_registered type: {type(time_registered)} for user {user_premium.get_user().get_user_id()}")
                    continue

                # So sánh thời gian đã trôi qua với duration
                if elapsed_time_seconds >= duration:
                    user_id = user_premium.get_user().get_user_id()
                    premium_id = user_premium.get_premium().get_premium_id()
                    if user_id and premium_id:
                        user_premium_bll.delete_user_premium_by_user_id_and_premium_id(user_id=user_id, premium_id=premium_id)
                        logger.info(f"Deleting premium for User ID: {user_id}, Premium ID: {premium_id}, Resistered at: {time_registered}")
        except Exception as e:
            logger.error(f"Error loading userpremium list: {e}")


    @tasks.loop(seconds=25)
    async def push_noti(self):
        logger.debug('Running background task push_noti...')
        await self.load_guilds()
        await self.load_list_feed()
        await self.load_user_premium()

    @push_noti.before_loop
    async def await_bot_ready(self):
        # Wait for the bot to be fully ready
        await self.bot.wait_until_ready()

    @commands.Cog.listener()
    async def on_ready(self):
        logger.info(f"Bot {self.bot.user} is ready")
        logger.info("Current commands: %s", str([command.name for command in self.bot.commands]))
        logger.info("Current slash commands: %s", str([command.name for command in self.bot.get_application_commands()]))

        await self.bot.sync_all_application_commands()
        logger.info(f'Bot {self.bot.user} is ready and commands are synced.')

        if not self.push_noti.is_running():
            self.push_noti.start()

    @commands.Cog.listener()
    async def on_message(self, message: Message):
        if message.author == self.bot.user:
            return

        if self.bot.user is None:
            await message.channel.send('Bot is not fully ready yet.')
            return

        if message.content.startswith(f'<@{self.bot.user.id}>'):
            prompt = message.content[len(f'<@{self.bot.user.id}> '):]
            try:
                history = []

                # Fetch the last 20 messages for context
                async for message1 in message.channel.history(limit=20):
                    if message1.author.id != self.bot.user.id:
                        prompt1 = message1.content
                        if prompt1.startswith(f'<@{self.bot.user.id}> '):
                            prompt1 = prompt1[len(f'<@{self.bot.user.id}> '):]
                        if len(prompt1) > 0:
                            history.append({"role": "user", "parts": f'{message1.author.name}: "{prompt1}"'})
                    else:
                        history.append({"role": "model", "parts": message1.content})

                prompt_message = await message.channel.send('Creating prompt...')

                genai.configure(api_key=os.getenv("GEMINI_TOKEN"))

                model = genai.GenerativeModel("gemini-1.5-flash")
                chat = model.start_chat(history=history[::-1])
                response = chat.send_message(f'{message.author.name}: "{prompt}"')
                response_text = response.text

                # Split the response into chunks to avoid exceeding Discord's message limit
                chunk_size = 2000
                chunks = [response_text[i:i + chunk_size] for i in range(0, len(response_text), chunk_size)]
                response_message = await message.reply(f'@{message.author.name}, here is your response:')
                for chunk in chunks:
                    await response_message.channel.send(chunk)

            except Exception as e:
                logger.error(f"Error while processing message: {e}")
                await message.channel.send('Sorry, there was an error processing your request.')

def setup(bot: commands.Bot):
    bot.add_cog(Events(bot))
