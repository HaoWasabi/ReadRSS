# Aiko (ReadRSS)
This is a Discord bot built with Python, Aiko brings RSS feeds to your Discord server. Receive notifications from news sources including Facebook and much more. 
This is link to invite Aiko bot:
```
https://discord.com/oauth2/authorize?client_id=1236720788187381760&permissions=0&integration_type=0&scope=bot
```

```
                        -- ABOUT US --
                                                       Summer 2024
         ██████╗  ██████╗██████╗ ███████╗██╗   ██╗     + HaoWasabi
        ██╔════╝ ██╔════╝██╔══██╗██╔════╝██║   ██║     + nguyluky
        ██║  ███╗██║     ██║  ██║█████╗  ██║   ██║     + NaelTuhline
        ██║   ██║██║     ██║  ██║██╔══╝  ╚██╗ ██╔╝     + tivibin789
        ╚██████╔╝╚██████╗██████╔╝███████╗ ╚████╔╝      + phusomnia
        ╚═════╝  ╚═════╝╚═════╝ ╚══════╝  ╚═══╝        + camdao
``` 
## Installation
1. Clone the repository
2. Create a virtual environment and activate it
3. Install the dependencies: `pip install -r requirements.txt`
4. Create a `.env` file and add your Discord bot token: `DISCORD_TOKEN=your_token_here`
5. Run the bot: `python main.py`

## Basic slash_commands
+ `/ping` # Check bot latency
+ `/help` # Show all commands
+ `/get_rss` # Get the RSS link of a website (if it has)
+ `/clear_channel_entry` # Clear channel post history
+ `/clear_channel_feed` # Clear channel feed settings
+ `/set_channel_feed` # Set the channel will send the feed
+ `/set_color` # Set the color of all embeds that you want it would send
+ `/show_feeds` # Show list of feeds in channels in your server
+ `/test_feed` # Test sending an RSS feed
+ `/premium` # Upgrade to use advanced packages

## Admin commands
+ `_shutdown` # Shut down the bot
+ `_ctrl` # show the control panel to to control the bot

## Gemini commands
+ `@Aiko` # answer your question. Ask as when you use Gemini.

## Other information
Đồ án được xây dựng theo mô hình 3 lớp mở rộng. Trong đó:
+ dal: xử lý logic truy cập dữ liệu.
+ bll: xử lý logic các yêu cầu từ lớp trình bày.
+ gui: xử lý giao diện
+ dto: chứa các lớp dùng để chuyển dữ liệu giữa các lớp hoặc tầng khác nhau. Mỗi lớp dto chứa có chứa các thuộc tính của các thực thể và các mối quan hệ.
+ utils: chứa các tệp tiện ích hoặc các hàm hỗ trợ mở rộng.
+ cogs: chứa các hàm sự kiện, lệnh bất đồng bộ tương tác với người dùng.


