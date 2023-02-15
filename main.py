''' Logging library for logging '''
import logging as log
import sys
import getopt
import bot

LOGFORMAT = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'

LOGLEVEL = log.DEBUG

log.basicConfig(
    filename='py.log',
    level=LOGLEVEL,
    format=LOGFORMAT
)

console = log.StreamHandler()
console.setLevel(LOGLEVEL)
log.getLogger('').addHandler(console)

opts, args = getopt.getopt(sys.argv[1:], "t:p:", ["token=", "prefix="])

TOKEN = ""
PREFIX = ""

for opt, arg in opts:
    if opt == '--token':
        log.info("Token: %s", arg)
        TOKEN = arg
    elif opt == '--prefix':
        log.info("Prefix: %s", arg)
        PREFIX = arg

if TOKEN == "":
    log.error("Token can't be empty!")
    raise AttributeError

if PREFIX == "":
    log.error("Prefix can't be empty!")
    raise AttributeError


channels = [
    "vanidor",
    "vanib0t"
]
AdminUsers=[
    "vanidor"
]
log.info(
    "Creating bot with token '%s' and prefix '%s' for channel channels '%s'", 
    TOKEN, PREFIX, channels)

bot = bot.Bot(
    token=TOKEN,
    prefix=PREFIX,
    channels=channels
)
bot.set_admin_users(
    admin_users=AdminUsers
)
log.info("Created bot, starting mainloop")

try:
    bot.run()
except (Exception) as e: # pylint: disable=broad-except
    log.error("Error in bot mainloop. Type: %s", type(e))
    log.error("Stacktrace: %s", e)
