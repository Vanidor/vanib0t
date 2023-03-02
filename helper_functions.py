import logging as log
import requests
import json


def get_user_pronoun(username: str):
    ''' Get user pronouns from pronouns extension '''

    # Make request to the user API endpoint
    user_api_url = f"https://pronouns.alejo.io/api/users/{username}"
    response = requests.get(user_api_url, timeout=1)

    # Check if the request was successful
    if response.status_code != 200:
        print(f"Error: {response.status_code}")
        exit()

    pronoun_display = None

    if response.text != "[]":
        # Parse the response as JSON
        user_data = json.loads(response.text)

        # Get the pronoun ID from the user data
        pronoun_id = user_data[0].get("pronoun_id")

        # Make request to the pronouns API endpoint
        pronouns_api_url = "https://pronouns.alejo.io/api/pronouns"
        response = requests.get(pronouns_api_url, timeout=1)

        # Check if the request was successful
        if response.status_code != 200:
            print(f"Error: {response.status_code}")
            exit()

        # Parse the response as JSON
        pronouns_data = json.loads(response.text)

        # Find the pronoun that matches the ID from the user data
        for pronoun in pronouns_data:
            if pronoun.get("name") == pronoun_id:
                pronoun_display = pronoun.get("display")
                break

    # Print the result
    if pronoun_display:
        log.info(
            "The pronouns for %s is %s.", username, pronoun_display)
    else:
        log.info("No pronouns found for %s.", username)
    return pronoun_display
