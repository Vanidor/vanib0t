import logging as log
import bot
import sys
import getopt

logFormat = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'

log.basicConfig(
    filename='py.log',
    level=log.INFO,
    format=logFormat
)

opts, args = getopt.getopt(sys.argv[1:], "t:p:", ["token=", "prefix="])

token = ""
prefix = ""

for opt, arg in opts:
    if opt == '--token':
        log.info("Token: " + arg)
        token = arg
    elif opt == '--prefix':
        log.info("Prefix: " + arg)
        prefix = arg

if token == "":
    log.error("Token can't be empty!")
    raise Exception

if prefix == "":
    log.error("Prefix can't be empty!")
    raise Exception


channels = [
    "vanidor",
    "vanib0t"
]
AdminUsers=[
    "vanidor"
]
log.info(f"Creating bot with token '{token}' and prefix '{prefix}' for channel channels '{channels}'")

bot = bot.Bot(
    token=token,
    prefix=prefix,
    channels=channels
)
log.info(f"Admin users: {AdminUsers}")
bot.SetAdminUsers(
    AdminUsers=AdminUsers
)
log.info(f"Created bot, starting mainloop")

try:
    bot.run()
except Exception as e:
      log.error(f"Error in bot mainloop. Type: {type(e)}")
      log.error(f"Stacktrace: {e}")