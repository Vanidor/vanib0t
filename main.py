''' Logging library for logging '''
import logging as log
import argparse
import bot

LOGFORMAT = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'

parser = argparse.ArgumentParser()
parser.add_argument(
    '-t',
    '--token',
    required=True,
    help='The twitch OAuth token for the bot. https://twitchtokengenerator.com'
)
parser.add_argument(
    '-p',
    '--prefix',
    required=True,
    help='The prefix of the bot.'
)
parser.add_argument(
    '--openai_api_key',
    required=True,
    help='The API key for OpenAI'
)
parser.add_argument(
    '--loglevel',
    default=log.INFO,
    choices=log._nameToLevel.keys()  # pylint: disable=W0212
)

args = parser.parse_args()

TOKEN = args.token
PREFIX = args.prefix
LOGLEVEL = args.loglevel
OPENAI_API_KEY = args.openai_api_key

print(f"Token: {TOKEN}\r\nPREFIX: {PREFIX}\r\nLOGLEVEL: {LOGLEVEL}\r\nOPENAI_API_KEY: {OPENAI_API_KEY}")

log.basicConfig(
    filename='py.log',
    level=LOGLEVEL,
    format=LOGFORMAT
)

console = log.StreamHandler()
console.setLevel(LOGLEVEL)
log.getLogger('').addHandler(console)

channels = [
    "vanidor",
    "vanib0t"
]
AdminUsers = [
    "vanidor",
    "cisco_04",
]
log.info(
    "Creating bot with token '%s' and prefix '%s' for channel channels '%s'",
    TOKEN, PREFIX, channels)

bot = bot.Bot(
    token=TOKEN,
    prefix=PREFIX,
    channels=channels,
    openai_api_key=OPENAI_API_KEY
)
bot.set_admin_users(
    admin_users=AdminUsers
)
log.info("Created bot, starting mainloop")

try:
    bot.run()
except (Exception) as e:  # pylint: disable=broad-except
    log.error("Error in bot mainloop. Type: %s", type(e))
    log.error("Stacktrace: %s", e)
