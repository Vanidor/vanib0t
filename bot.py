''' Logging library for logging '''
import logging as log
import time
from twitchio.ext import commands
from twitchio import message as msg
import OpenaiHelper
import helper_functions


class Bot(commands.Bot):
    ''' Bot class for the twitch chat bot '''

    def __init__(self, token: str, prefix: str, channels: list[str]):
        self.admin_users = ""
        self.global_cd = dict()
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

        if (substring_text.upper() in message.content.upper()) and (not "reply-parent-display-name" in message.tags):
            log.info("Got chatgpt prompt '%s' in '%s' by '%s'",
                     message.content,
                     message.channel.name,
                     message.author.display_name)
            do_answer = True
            if "chatgpt-" + message.channel.name in self.global_cd:
                old_time = self.global_cd["chatgpt-" + message.channel.name]
                new_time = time.time()
                if message.channel.name == self.nick:
                    global_cooldown = 0
                else:
                    global_cooldown = 15
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
                username = message.author.name
                if username in self.user_pronouns:
                    log.info("Got saved pronouns for %s: %s",
                             username, self.user_pronouns[username])
                    pronouns = self.user_pronouns[username]
                else:
                    pronouns = helper_functions.get_user_pronoun(username)
                    self.user_pronouns[username] = pronouns
                    log.info("Saved pronouns for %s: %s",
                             username, self.user_pronouns[username])
                pronouns = None
                system = f"You are a friendly bot with the name '{self.nick}' in the twitch channel '{message.channel.name}'."
                system += "Create short answers that you could find in a twitch chat."
                system += f"The prompt has been send by '{username}' "
                if pronouns is not None:
                    system += f", according to our records the user goes by the pronouns '{pronouns}', "
                system += "as a mesage in the twitch chat."

                # log.info("System message: %s", system)
                openai = OpenaiHelper.OpenaiHelper()
                answer = openai.get_chat_completion(
                    system,
                    message.content,
                    username)
                log.info("Answer for chatgpt prompt '%s' in '%s' by '%s': '%s'",
                         message.content,
                         message.channel.name,
                         username,
                         answer)
                self.global_cd["chatgpt-" + message.channel.name] = time.time()
                await message.channel.send(answer)

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
