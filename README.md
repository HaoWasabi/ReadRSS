# ReadRSS
This is a Discord bot built with Python, ReadRSS bot brings RSS feeds to your Discord server.  Receive notifications from news sources including Facebook and much more. 

## Installation
1. Clone the repository
2. Create a virtual environment and activate it
3. Install the dependencies: `pip install -r requirements.txt`
4. Create a `.env` file and add your Discord bot token: `DISCORD_TOKEN=your_token_here`
5. Run the bot: `python main.py`

## Basic commands
+ /insert <channel_name> <link_feed> # register 1 feed in a channel based on links and name channel
+ /delete <channel_name> <link_feed> # cancel registration 1 feed in 1 channel based on link feed and name channel
+ /delelte <channel_name> # cancel registration of all feeds in a channel based on the name of the channel
+ /show # allows viewing all registered feed in channels
+ /show <link_feed> # allows viewing 1 feed registered in channel channels
+ /test <feed_link># send a notice of the latest post from a registered feed page to be checked to check
+ /test_all <feed_link> # send the entire post from a registered feed page to check
+ /clear # withdraw all messages




