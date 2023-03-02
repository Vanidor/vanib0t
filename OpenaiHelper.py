import logging as log
import openai


class OpenaiHelper:
    ''' Openai helper class '''

    def get_chat_completion(self, system: str, user: str, username: str):
        ''' Get chat completion - https://platform.openai.com/docs/guides/chat/introduction '''
        openai.api_key = "sk-..."
        log.debug("System: %s", system)
        log.debug("User: %s", user)
        completion = openai.ChatCompletion.create(
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
            temperature=1,
            top_p=1,
            n=1,
            max_tokens=100,
            presence_penalty=0,
            frequency_penalty=0,
            user=username
        )
        result = completion.choices[0].message.content
        log.debug('ChatCompletion output: %s', str(completion))

        moderation = openai.Moderation.create(
            input=result,
            model="text-moderation-latest"
        )

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
