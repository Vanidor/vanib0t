# Vanib0t

This is a twitch bot that I use for my twitch channel at twitch.tv/vanidor.

It's features are

- Ask questions that it answers using chatgpt
- Use `?stream` to ask for the streaming schedule and when the next stream is going to happen
- Use `fishh` to try catching fish with weighted randomness

## Running the bot

1) Create a Bot Chat Token on https://twitchtokengenerator.com/
2) Create an API key on https://platform.openai.com/account/api-keys
3) Install the dependencies (in a venv): `pip install -r requirements.txt`
4) Run the bot with `python main.py --token=<BotChatToken> --prefix=? --openai_api_key=<OpenAIApiKey> --loglevel=INFO`. Replace the placeholders with your API keys
