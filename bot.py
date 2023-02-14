import logging as log
from twitchio.ext import commands

class Bot(commands.Bot):
    def __init__(self, token: str, prefix: str, channels: list[str]):
        super().__init__(
            token=token,
            prefix=prefix,
            initial_channels=channels
        )

    def SetAdminUsers(self, AdminUsers: list[str]):
        self.AdminUsers = AdminUsers

    async def event_ready(self):
        log.info(f'Logged in as | {self.nick}')
        log.info(f'User id is | {self.user_id}')

    async def event_message(self, message):
        if message.echo:
            return

        log.debug(f"Got message '{message.content}' in '{message.channel.name}'")

        await self.handle_commands(message)

    @commands.command()
    async def ping(self, ctx: commands.Context):
        log.debug(f"ping from '{ctx.author.display_name}'")
        await ctx.send(f'pong {ctx.author.name}!')
    
    @commands.command()
    async def stop(self, ctx: commands.Context):
        if ctx.author.name in self.AdminUsers:
            await ctx.send(f'Shutting down peepoSad')
            await self.close()
        else:
            await ctx.send(f"I'm sorry, {ctx.author.display_name}. I'm afraid I can't do that. https://youtu.be/ARJ8cAGm6JE?t=64")