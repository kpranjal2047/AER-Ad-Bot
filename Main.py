import os
import random
from glob import glob

import discord
from discord.ext import tasks


class DiscordClient(discord.Client):
    def __init__(self):
        super().__init__()
        self.target_channel = None

    async def on_ready(self):
        self.find_channel.start()

    @tasks.loop(hours=1)
    async def find_channel(self):
        self.target_channel = self.get_channel(int(os.environ["TARGET_CHANNEL_A9"]))
        if self.target_channel is not None:
            print("Target found!")
            self.send_message.start()
            print("Messaging started!")
            self.find_channel.stop()
        else:
            print("Target not found!")

    @tasks.loop(hours=12)
    async def send_message(self):
        await self.target_channel.send(
            """Our team is ÆR™ (All Elite Racers) and we are a friendly, highly motivated group on Android looking \
for some new active members! 

Team 1 - ÆR™ (4K /Day)
Team 2 - ÆR™ Wolves (2.5K /Day)
Team 3 - ÆR™ Demons (1K /Day)
Team 4 - ÆR™ Hailstorm (500 /Day)

• We have jokes, share tips for races and find insider info to make sure we all get as many rewards as possible.
• We have club tournaments where all the club members can participate.
• We have photo competitions where we get stunning pics and top three goes in ÆR™ club banner

We're currently looking for active players to fill ALL TEAMS, if you're interested and can meet the requirements, \
you can hit us up and join our discord server below! 

Join us on discord - https://discord.gg/hwdC7YZ""",
            file=discord.File(random.choice(glob("images/*.jpg"))),
        )
        print("Message sent!")


if __name__ == "__main__":
    dc = DiscordClient()
    dc.run(os.environ["DISCORD_TOKEN_BOT"], bot=False)
