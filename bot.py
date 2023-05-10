''' Logging library for logging '''
import logging as log
import time
from datetime import datetime, timezone, timedelta
import unicodedata
import random
import json
import asyncio
from twitchio.ext import commands
from twitchio import message as msg
from icalevents.icalevents import events
import OpenaiHelper
import helper_functions
from database.Database import BotDatabase


class Bot(commands.Bot):
    ''' Bot class for the twitch chat bot '''

    def __init__(self, token: str, prefix: str, channels: list[str], openai_api_key: str, database_path: str):
        self.admin_users = ""
        self.openai_api_key = openai_api_key
        self.command_last_used = dict()
        self.command_global_cd = dict()
        self.user_pronouns = dict()
        self.fishh_odds = {}
        self.database = BotDatabase(database_path)
        with open("./fishh.json", "r", encoding="UTF-8") as odds:
            self.fishh_odds = json.load(odds)

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
        channel_user = await channel.user()
        channel_id = channel_user.id
        self.database.create_channel_settings_if_not_exists(
            channel_id=channel_id,
            channel_name=channel_name
        )
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

        if (message.content.casefold().startswith("fishh")):
            message.content = "?fishh"

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

    def get_command_cooldown(self, command_name: str, channel_name: str):
        ''' Method to return if a given command is on cooldown in a given channel '''
        old_time = self.get_command_last_used(command_name, channel_name)
        log.debug("Last used time: %s", old_time)
        remaining = 0
        if old_time is not None:
            new_time = time.time()
            log.debug("Now time: %s", old_time)
            if channel_name == self.nick:
                global_cooldown = 0
            else:
                global_cooldown = self.get_command_global_cd(
                    command_name, channel_name)
            difference = new_time - old_time
            remaining = global_cooldown - difference

            log.info("Global cooldown for %s: %i. Remaining time: %i",
                     command_name, global_cooldown, remaining)

            if difference >= global_cooldown:
                log.debug("Command no longer on cooldown")
            else:
                log.debug("Command still on cooldown")
        return remaining

    def clean_string(self, text: str):
        filtered_text = ""
        for ch in text:
            if unicodedata.category(ch)[0] != "C":
                filtered_text += ch
            else:
                filtered_text += " "
        return filtered_text

    @commands.command()
    async def fishh(self, ctx: commands.Context):
        channel_name = ctx.channel.name
        message_author = ctx.author.name
        message_tags = ctx.message.tags
        if channel_name.casefold() == "vanidor".casefold():

            total_weight = sum(self.fishh_odds.values())
            weights = [w/total_weight for w in self.fishh_odds.values()]

            result = random.choices(
                list(self.fishh_odds.keys()), weights=weights)[0]

            await ctx.reply(f"{message_author} caught a {result}")

    @commands.command()
    async def stream(self, ctx: commands.Context):
        ''' Get the next stream of the channel the bot is in '''
        channel_user = await ctx.channel.user()

        try:
            schedule = await channel_user.fetch_schedule()

            schedule_segment = schedule.segments[0]

            start_time = schedule_segment.start_time
            end_time = schedule_segment.end_time

            time_format = "%Y-%m-%d at %H:%M %Z"

            start_time_text = start_time.strftime(time_format)
            end_time_text = end_time.strftime(time_format)
            
            reply = f"The next stream is going to be on {start_time_text}. "

            if schedule_segment.category is not None:
                game_name = schedule_segment.category.name
                reply = reply + f"The category will be \"{game_name}\". "
            else:
                reply = reply + "The category has not been chosen yet. "

            if schedule_segment.title != '':
                stream_name = schedule_segment.title
                reply = reply + f"The stream title will be \"{stream_name}\". "
            else:
                reply = reply + "There is no stream title yet. "
            
            await ctx.reply(reply)
        except:
            await ctx.reply("There are no streams planned. ")

    @commands.command()
    async def chatgpt(self, ctx: commands.Context):
        original_message = ctx.message.content[8:]
        channel_name = ctx.channel.name
        message_author = ctx.author.name
        message_tags = ctx.message.tags

        do_answer = True
        command_name = "chatgpt"
        remaining = self.get_command_cooldown(command_name, channel_name)
        if remaining > 0:
            reply = f"I'm on cooldown right now. Please try again in {int(remaining)} seconds."
            await ctx.reply(reply)
            do_answer = False

        if do_answer:
            username = message_author

            channel_user = await ctx.channel.user()

            channel_settings = self.database.read_channel_settings_by_id(
                channel_user.id)
            system = channel_settings.chatgpt_prompt

            now = datetime.utcnow()

            channel = await self.fetch_channel(broadcaster=channel_name)

            game_name = channel.game_name
            title = channel.title

            current_datetime = now.strftime(
                "%Y-%m-%d %H:%M:%S UTC%z"
            )

            system = system.format(
                self.nick, # {0}
                channel_name, # {1}
                username, # {2}
                current_datetime, # {3}
                game_name,# {4}
                title # {5}
            )

            if self.is_message_thread(message_tags):
                # TODO: Add more system context (all messages from the thread for example)
                return None

            log.debug("System message: %s", system)
            openai = OpenaiHelper.OpenaiHelper(self.openai_api_key)
            answer = await openai.get_chat_completion(
                system,
                original_message,
                username)
            log.debug("Answer for chatgpt prompt '%s' in '%s' by '%s': '%s'",
                      original_message,
                      channel_name,
                      username,
                      answer)
            self.set_command_last_used(
                "chatgpt",
                channel_name
            )
            answer = self.clean_string(answer)
            log.debug("Cleaned answer: %s", answer)
            if len(answer) < 450:
                await ctx.reply(answer)
            else:
                log.info("Answer is too long for one message")
                result = []
                for i in range(0, len(answer), 450):
                    result.append(answer[i:i+450])

                i = 1
                log.info("Sending answer in %i messages", len(result))
                for split_string in result:
                    log.info("Sending message %i out of %i", i, len(result))
                    await asyncio.sleep(1)
                    await ctx.reply(f"({i}/{len(result)}) - " + split_string)
                    i = i + 1

    @ commands.command()
    async def setgcd(self, ctx: commands.Context):
        ''' Command for setting the global cooldown of commands. Usage: setgcd CommandName Time '''
        if (ctx.author.name in self.admin_users):
            command = f"{ctx.prefix}setgcd "
            args = ctx.message.content.replace(command, '')
            args = args.split(" ")
            args_count = len(args)
            error_message = f'You have to specify 2 arguments. Usage: {ctx.prefix}setgcd CommandName Time. For example {ctx.prefix}setgcd chatgpt 20'
            if args_count != 2:
                await ctx.reply(error_message)
            else:
                try:
                    command_name = str(args[0])
                    cooldown = int(args[1])
                    self.set_command_global_cd(
                        command_name, ctx.channel.name, cooldown)
                    await ctx.reply(f'Setting global cooldown of command {command_name} to {cooldown}!')
                except (Exception) as e:  # pylint: disable=broad-except
                    await ctx.reply(error_message)
                    log.error(
                        "Error while setting global cooldown. Type: %s Args: %s", type(e), args)
                    log.debug("Stacktrace: %s", e)

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
