from glob import glob
from os import environ
from random import choice
from sys import stderr

from discord.client import Client
from discord.errors import Forbidden, HTTPException
from discord.ext.tasks import loop
from discord.file import File

account = environ["DISCORD_TOKEN"]
a9_channel = int(environ["TARGET_CHANNEL_A9"])
looptime = int(environ["LOOP_HOUR"])
teams = set(environ["TEAMS"])


def create_message():
    with open("text/message.txt", "r", encoding="utf8") as fp:
        message = fp.read()
    if all(str(x) in teams for x in range(1, 6)):
        message = message.format("ALL TEAMS")
        return message
    num = len(teams)
    added = 0
    for i in range(1, 6):
        if str(i) in teams:
            if added == 0:
                message = message.format("Team " + str(i) + "{}")
            elif added == num - 1:
                message = message.format(" and " + str(i) + "{}")
            else:
                message = message.format(", " + str(i) + "{}")
            added += 1
    return message.format("")


class DiscordClient(Client):
    def __init__(self):
        super().__init__()
        self.target_channel = None
        self.message = create_message()

    async def on_ready(self):
        self.find_channel.start()

    @loop(hours=looptime / 2)
    async def find_channel(self):
        self.target_channel = self.get_channel(a9_channel)
        if self.target_channel is not None:
            print("Target found!")
            self.send_message.start()
            print("Messaging started!")
            self.find_channel.stop()
        else:
            print("Target not found!", file=stderr)

    @loop(hours=looptime)
    async def send_message(self):
        try:
            await self.target_channel.send(
                self.message, file=File(choice(glob("images/*.jpg")))
            )
            print("Message sent!")
        except Forbidden as f:
            print(
                "You do not have the proper permissions to send the message.",
                f,
                sep="\n",
                file=stderr,
            )
        except HTTPException as h:
            print("Sending the message failed.", h, sep="\n", file=stderr)


if __name__ == "__main__":
    dc = DiscordClient()
    dc.run(account, bot=False)
