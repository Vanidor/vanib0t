import logging as log
import bot

logFormat = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'

log.basicConfig(
    filename='py.log',
    level=log.DEBUG,
    format=logFormat
)

token = ""
prefix = "?"
channels = [
    "vanidor",
    "cisco_04"
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