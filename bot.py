''' Logging library for logging '''
import logging as log
from twitchio.ext import commands

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
        log.info('Logged in as %s', self.nick)
        log.info('User id is %s', self.user_id)

    async def event_message(self, message):
        if message.echo:
            return

        log.debug("Got message '%s' in '%s' by '%s'",
                    message.content,
                    message.channel.name,
                    message.author.display_name)

        await self.handle_commands(message)

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
