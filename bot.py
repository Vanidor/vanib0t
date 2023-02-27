''' Logging library for logging '''
import logging as log
import regex
import requests
from twitchio.ext import commands
from twitchio import message as msg

class Bot(commands.Bot):
    ''' Bot class for the twitch chat bot '''
    def __init__(self, token: str, prefix: str, channels: list[str]):
        self.admin_users = ""
        super().__init__(
            token=token,
            prefix=prefix,
            initial_channels=channels
        )

    def set_admin_users(self, admin_users: list[str]):
        ''' Method for setting the admin users '''
        self.admin_users = admin_users

    async def event_ready(self):
        ''' Specifies that the bot is ready '''
        log.info('Logged in as %s', self.nick)
        log.info('User id is %s', self.user_id)

    async def event_message(self, message: msg):
        ''' Gets called every time a new message is send in the joined channels '''
        if message.echo:
            return

        substring_text = "@" + self.nick
        substring_text = self.nick


        log.debug("Got message '%s' in '%s' by '%s'",
            message.content,
            message.channel.name,
            message.author.display_name)

        if substring_text.upper() in message.content.upper():
            await self.chatgpt_message(message.channel, message.content)

        await self.handle_commands(message)

    async def chatgpt_message(self, ctx, message: str):
        url = "https://vanidor-twitch.azurewebsites.net/api/chatgpt"
        prompt = "Create a short answer that you could find in twitch chat to the following prompt: "
        clean_text = message.replace('?chatgpt ', '')
        clean_text = message.replace(self.nick, '')
        text_param = prompt + clean_text
        log.info("Input: %s", clean_text)
        log.info("Combined prompt: %s", text_param)
        params = {
            "text": text_param
        }
        headers = {
            "x-fossabot-channellogin": "vanidor"
        }
        try:
            result = requests.get(
                url=url,
                params=params,
                headers=headers,
                timeout=10)
        except (Exception) as e:  # pylint: disable=broad-except
            log.warn("Error: %s", type(e))
            log.warn("Stacktrace: %s", e)
            await ctx.send("Timeout while trying to get an aswer Sadge")

        result_text = result.text
        fixed_result_text = regex.sub(r'\p{C}', '', result_text)
        log.info("Result: %s", fixed_result_text)
        await ctx.send(fixed_result_text)

    @commands.command()
    async def ping(self, ctx: commands.Context):
        ''' Command for sending a ping message ''' 
        log.debug("ping from '%s' in '%s'",
                    ctx.author.display_name,
                    ctx.channel.name)
        await ctx.send(f'pong {ctx.author.name}!')

    @commands.command()
    async def stop(self, ctx: commands.Context):
        ''' Command for stopping the bot '''
        if ctx.author.name in self.admin_users:
            await ctx.send('Shutting down peepoSad')
            await self.close()
        else:
            text = (f"I'm sorry, {ctx.author.display_name}." +
                    "I'm afraid I can't do that. https://youtu.be/ARJ8cAGm6JE?t=64")
            await ctx.send(text)
