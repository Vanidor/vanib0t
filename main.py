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
parser.add_argument(
    '--database_path',
    required=False,
    default="settings/bot.sqlite",
    help="The path where the DB will be saved"
)
parser.add_argument(
    '--chatgpt_max_tokens',
    required=False,
    default=60,
    help="The maximum amount of tokens for chatgpt"
)
parser.add_argument(
    '--chatgpt_temperature',
    required=False,
    default=1,
    help="The temperature for chatgpt"
)
parser.add_argument(
    '--chatgpt_n',
    required=False,
    default=1,
    help="The n value for chatgpt"
)
parser.add_argument(
    '--chatgpt_top_p',
    required=False,
    default=1,
    help="The top p value for chatgpt"
)
parser.add_argument(
    '--chatgpt_presence_penalty',
    required=False,
    default=0,
    help="The presence penalty for chatgpt"
)
parser.add_argument(
    '--chatgpt_frequency_penalty',
    required=False,
    default=0,
    help="The frequency penalty for chatgpt"
)
parser.add_argument(
    '--chatgpt_maximum_words',
    required=False,
    default=30,
    help="The maximum words for chatgpt"
)

args = parser.parse_args()

TOKEN = args.token
PREFIX = args.prefix
LOGLEVEL = args.loglevel
OPENAI_API_KEY = args.openai_api_key
DATABASE_PATH = args.database_path

CHATGPT_MAX_TOKENS = args.chatgpt_max_tokens
CHATGPT_TEMPERATURE = args.chatgpt_temperature
CHATGPT_N = args.chatgpt_n
CHATGPT_TOP_P = args.chatgpt_top_p
CHATGPT_PRESENCE_PENALTY = args.chatgpt_presence_penalty
CHATGPT_FREQUENCY_PENALTY = args.chatgpt_frequency_penalty
CHATGPT_MAXIMUM_WORDS = args.chatgpt_maximum_words

chatgpt_info = "chatgpt info:\r\n"
chatgpt_info = chatgpt_info + f"CHATGPT_MAX_TOKENS: {CHATGPT_MAX_TOKENS}\r\n"
chatgpt_info = chatgpt_info + f"CHATGPT_TEMPERATURE: {CHATGPT_TEMPERATURE}\r\n"
chatgpt_info = chatgpt_info + f"CHATGPT_N: {CHATGPT_N}\r\n"
chatgpt_info = chatgpt_info + f"CHATGPT_TOP_P: {CHATGPT_TOP_P}\r\n"
chatgpt_info = chatgpt_info + f"CHATGPT_PRESENCE_PENALTY: {CHATGPT_PRESENCE_PENALTY}\r\n"
chatgpt_info = chatgpt_info + f"CHATGPT_FREQUENCY_PENALTY: {CHATGPT_FREQUENCY_PENALTY}\r\n"
chatgpt_info = chatgpt_info + f"CHATGPT_MAXIMUM_WORDS: {CHATGPT_MAXIMUM_WORDS}\r\n"

print(f"Token: {TOKEN}\r\nPREFIX: {PREFIX}\r\nLOGLEVEL: {LOGLEVEL}\r\nOPENAI_API_KEY: {OPENAI_API_KEY}")
print("----------")
print(chatgpt_info)

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
    openai_api_key=OPENAI_API_KEY,
    database_path=DATABASE_PATH,
    max_tokens=CHATGPT_MAX_TOKENS,
    temperature=CHATGPT_TEMPERATURE,
    n=CHATGPT_N,
    top_p=CHATGPT_TOP_P,
    presence_penalty=CHATGPT_PRESENCE_PENALTY,
    frequency_penalty=CHATGPT_FREQUENCY_PENALTY,
    max_words=CHATGPT_MAXIMUM_WORDS
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
