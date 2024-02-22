import json

from airtoolclassifier.config import Config
import openai


class OpenAIService:
    def __init__(self):
        """
        Initializes an instance of the OpenAIService class.
        """
        config = Config.load_configuration(use_1password=True)
        self.client_openai = openai.OpenAI(api_key=config["openai_api_key"])

    def create_classification(self, role: str, task: str) -> json:
        """
        Creates a classification using OpenAI's GPT-3.5 Turbo model.

        Args:
            role (str): The role of the system in the conversation.
            task (str): The user's task or input.

        Returns:
            json: The classification response in JSON format.

        Raises:
            OpenAIError.APIError: If there is an error with the OpenAI API.
            OpenAIError.APIConnectionError: If there is an error connecting to the OpenAI API.
            OpenAIError.RateLimitError: If the OpenAI API request exceeds the rate limit.
            json.JSONDecodeError: If there is an error while decoding the OpenAI response into JSON format.
        """
        try:
            response = self.client_openai.chat.completions.create(
                model="gpt-3.5-turbo-0125",
                response_format={"type": "json_object"},
                messages=[
                    {"role": "system", "content": role},
                    {"role": "user", "content": task},
                ],
            )
        except openai.APIError as e:
            print(f"OpenAI API returned an API Error: {e}")
            pass
        except openai.APIConnectionError as e:
            print(f"Failed to connect to OpenAI API: {e}")
            pass
        except openai.RateLimitError as e:
            print(f"OpenAI API request exceeded rate limit: {e}")
            pass

        text_response = response.choices[0].message.content

        if len(text_response) > 0:
            try:
                return json.loads(text_response)
            except json.JSONDecodeError:
                print(
                    f"Error while decoding OpenAI response into JSON-format:\n{text_response}"
                )
        else:
            print(f"Error in OpenAI response:\n{text_response}")
