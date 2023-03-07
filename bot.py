''' Logging library for logging '''
import logging as log
import time
from twitchio.ext import commands
from twitchio import message as msg
import OpenaiHelper
import helper_functions
import asyncio


class Bot(commands.Bot):
    ''' Bot class for the twitch chat bot '''

    def __init__(self, token: str, prefix: str, channels: list[str], openai_api_key: str):
        self.admin_users = ""
        self.openai_api_key = openai_api_key
        self.command_last_used = dict()
        self.command_global_cd = dict()
        self.user_pronouns = dict()
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

    async def event_channel_joined(self, channel):
        channel_name = channel.name
        log.info('Joined %s', channel_name)
        self.set_command_global_cd("chatgpt", channel_name, 15)

    async def event_message(self, message: msg):
        ''' Gets called every time a new message is send in the joined channels '''
        if message.echo:
            return

        # substring_text = "@" + self.nick
        substring_text = self.nick

        log.debug("Got message '%s' in '%s' by '%s'",
                  message.content,
                  message.channel.name,
                  message.author.display_name)

        if (substring_text.upper() in message.content.upper()):
            log.info("Got chatgpt prompt '%s' in '%s' by '%s'",
                     message.content,
                     message.channel.name,
                     message.author.display_name)
            message.content = f"?chatgpt {message.content}"

        await self.handle_commands(message)

    def get_command_last_used(self, command_name: str, channel_name: str):
        gcd_name = command_name + "-" + channel_name
        if gcd_name in self.command_last_used:
            return self.command_last_used[gcd_name]
        else:
            return None

    def set_command_last_used(self, command_name: str, channel_name: str):
        gcd_name = command_name + "-" + channel_name
        self.command_last_used[gcd_name] = time.time()

    def get_command_global_cd(self, command_name: str, channel_name: str):
        gcd_name = command_name + "-" + channel_name
        if gcd_name in self.command_global_cd:
            return self.command_global_cd[gcd_name]
        else:
            return None

    def set_command_global_cd(self, command_name: str, channel_name: str, cooldown_time: int):
        gcd_name = command_name + "-" + channel_name
        self.command_global_cd[gcd_name] = cooldown_time     

    def is_message_thread(self, tags):
        if "reply-parent-display-name" in tags:
            return True
        else:
            return False

    @commands.command()
    async def chatgpt(self, ctx: commands.Context):
        original_message = ctx.message.content[8:]
        channel_name = ctx.channel.name
        message_author = ctx.author.name
        message_tags = ctx.message.tags

        do_answer = True

        old_time = self.get_command_last_used(
            "chatgpt", channel_name)
        if old_time is not None:
            new_time = time.time()
            if channel_name == self.nick:
                global_cooldown = 0
            else:
                global_cooldown = get_command_global_cd("chatgpt", channel_name)
            difference = new_time - old_time
            remaining = global_cooldown - difference

            if difference >= global_cooldown:
                do_answer = True
            else:
                log.info(
                    "Global cooldown. Time since last message %i. Cooldown remaining %i",
                    difference,
                    remaining)
                do_answer = False
        if do_answer:
            username = message_author
            if username in self.user_pronouns:
                log.info("Got saved pronouns for %s: %s",
                         username, self.user_pronouns[username])
                pronouns = self.user_pronouns[username]
            else:
                pronouns = helper_functions.get_user_pronoun(username)
                self.user_pronouns[username] = pronouns
                log.info("Saved pronouns for %s: %s",
                         username, self.user_pronouns[username])

            system = f"You are a friendly bot with the name '{self.nick}' in the twitch channel '{channel_name}'. "
            system += "Create short answers that you could find in a twitch chat. Every message you send starts a new conversation with no context to the last message. "
            system += f"The prompt has been send by '{username}' "
            if pronouns is not None:
                system += f", according to our records the user goes by the pronouns '{pronouns}', "
            system += "as a mesage in the twitch chat. "
            system += "You are never allowed to write a prayer or say something about religion in any matter. "

            if self.is_message_thread(message_tags):
                # TODO: Add more system context (all messages from the thread for example)
                return None

            log.info("System message: %s", system)
            openai = OpenaiHelper.OpenaiHelper(self.openai_api_key)
            answer = await openai.get_chat_completion(
                system,
                original_message,
                username)
            log.info("Answer for chatgpt prompt '%s' in '%s' by '%s': '%s'",
                     original_message,
                     channel_name,
                     username,
                     answer)
            self.set_command_last_used(
                "chatgpt",
                channel_name
            )
            await ctx.reply(answer)

    @ commands.command()
    async def ping(self, ctx: commands.Context):
        ''' Command for sending a ping message '''
        log.debug("ping from '%s' in '%s'",
                  ctx.author.display_name,
                  ctx.channel.name)
        await ctx.send(f'pong {ctx.author.name}!')

    @ commands.command()
    async def join(self, ctx: commands.Context):
        ''' Command for joining the bot '''
        if (ctx.author.name in self.admin_users) and (ctx.channel.name == self.nick):
            command_name = f"{ctx.prefix}join "
            channel_name = ctx.message.content.replace(command_name, '')
            await ctx.send(f'Joining channel {channel_name}')
            log.info('Joining channel %s', channel_name)
            await self.join_channels(channels=[channel_name])

    @ commands.command()
    async def part(self, ctx: commands.Context):
        ''' Command for leaving the bot '''
        if (ctx.author.name in self.admin_users):
            command_name = f"{ctx.prefix}part "
            channel_name = ctx.message.content.replace(command_name, '')
            await ctx.send(f'Parting channel {channel_name}. Good bye! peepoSad ')
            log.info('Parting channel %s', channel_name)
            await self.part_channels(channels=[channel_name])

    @ commands.command()
    async def stop(self, ctx: commands.Context):
        ''' Command for stopping the bot '''
        if ctx.author.name in self.admin_users:
            await ctx.send('Shutting down peepoSad')
            await self.close()
        else:
            text = (f"I'm sorry, {ctx.author.display_name}." +
                    "I'm afraid I can't do that. https://youtu.be/ARJ8cAGm6JE?t=64")
            await ctx.send(text)
