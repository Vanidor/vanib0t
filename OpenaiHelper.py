import logging as log
import openai
import asyncio


class OpenaiHelper:
    ''' Openai helper class '''

    def __init__(self, api_key: str, image_dimensions: str, max_tokens: int, temperature: int, n:int, top_p: int, presence_penalty: int, frequency_penalty: int, max_words: int):
        self.image_dimensions = image_dimensions
        self.max_tokens = max_tokens
        self.temperature = temperature
        self.n = n
        self.top_p = top_p
        self.presence_penalty = presence_penalty
        self.frequency_penalty = frequency_penalty
        self.max_words = max_words
        self.api_key = api_key

    async def get_image_url(self, prompt: str):
        log.debug("Prompt: %s", prompt)
        image = openai.Image.create(
            api_key=self.api_key,
            prompt=prompt,
            n=1,
            size=self.image_dimensions
        )
        image_url = image['data'][0]['url']
        return image_url

    async def get_chat_completion(self, system: str, user: str, username: str):
        ''' Get chat completion - https://platform.openai.com/docs/guides/chat/introduction '''
        openai.api_key = self.api_key
        log.debug("System: %s", system)
        if(int(self.max_words) >= 0):
            user = user + f". Use {self.max_words} words or less."
        log.debug("User: %s", user)
        try:
            completion = await openai.ChatCompletion.acreate(
                model="gpt-3.5-turbo",
                messages=[
                    {
                        "role": "system",
                        "content": system
                    },
                    {
                        "role": "user",
                        "content": user
                    }
                ],
                temperature=self.temperature,
                top_p=self.top_p,
                n=self.n,
                max_tokens=self.max_tokens,
                presence_penalty=self.presence_penalty,
                frequency_penalty=self.frequency_penalty,
                user=username
            )
        except (Exception) as exc:  # pylint: disable=broad-except
            log.error(
                "Error while contacting chat completion api. Type: %s", type(exc))
            # log.error("Stacktrace: %s", exc)
            return "Sorry I wasn't able to get an answer to your request Sadge"

        result = completion.choices[0].message.content
        log.debug('ChatCompletion output: %s', str(completion))

        try:
            moderation = await openai.Moderation.acreate(
                input=result,
                model="text-moderation-latest"
            )
        except (Exception) as exc:  # pylint: disable=broad-except
            log.error(
                "Error while contacting moderation API. Type: %s", type(exc))
            return "Sorry I wasn't able to get an answer to your request Sadge . Please try again."
        moderation_output = moderation["results"][0]

        log.debug('Moderation output: %s', str(moderation_output))

        moderation_flagged = moderation_output.flagged
        if moderation_flagged:
            response_text = "Generated text blocked because of "
            moderation_hate = moderation_output["categories"]["hate"]
            moderation_hate_threatening = moderation_output["categories"]["hate/threatening"]
            moderation_self_harm = moderation_output["categories"]["self-harm"]
            moderation_sexual = moderation_output["categories"]["sexual"]
            moderation_sexual_minors = moderation_output["categories"]["sexual/minors"]
            moderation_violence = moderation_output["categories"]["violence"]
            moderation_violence_graphic = moderation_output["categories"]["violence/graphic"]
            if moderation_hate:
                response_text += "'Hate' "
            if moderation_hate_threatening:
                response_text += "'Hate Threatening' "
            if moderation_self_harm:
                response_text += "'Self Harm' "
            if moderation_sexual:
                response_text += "'Sexual' "
            if moderation_sexual_minors:
                response_text += "'Sexual Minors' "
            if moderation_violence:
                response_text += "'Violence' "
            if moderation_violence_graphic:
                response_text += "'Violence Graphic' "
        else:
            response_text = result

        return response_text
