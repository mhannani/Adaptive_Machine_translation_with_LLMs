import os
import openai
from typing import List
from dotenv import load_dotenv
import datetime
from langchain.schema.messages import AIMessage
from langchain import ChatOpenAI


class GPT:
    """
    GPT as translator model
    """

    def __init__(self, config, openai_api_key: str, model: str = 'gpt-3.5-turbo', temperature: float = 0.0, max_tokens: int = 50) -> None:
        """
        Class constructor for GPT model as API.

        :param config
            Configuration object
        :param openai_api_key str
            OpenAI API key
        :param model str
            Model name
        :param temperature float
            Temperature
        :param max_tokens int
            Max tokens
        :param messages List
            Messages to pass to the model

        return None
        """

        # configuration object
        self.config = config

        # openai_api_key
        self.openai_api_key: str = openai_api_key

        # model name
        self.model: str = model

        # temperator
        self.temperature: float = temperature

        # max_tokens
        self.max_tokens: int = max_tokens

        # setting openai api key
        openai.api_key = self.openai_api_key

        # openAI API key
        self.openai_api_key = self.openai_api_key


    def translate_legacy(self, messages: List = [{"role": "user", "content": "Hi!"}]) -> dict:
        """
        Make the translation job

        :param messages List
            List of messages for model input

        :return dict
        """

        # call the openAI API
        response = openai.ChatCompletion.create(model=self.model, temperature=self.temperature, max_tokens=self.max_tokens, messages=messages)

        # return only text
        text = response["choices"][0]["message"]["content"]

        # clean text
        return ' '.join([word for word in text.split() if word.lower() != "arabic"])

    def translate(self, chat_prompt: List) -> AIMessage:
        """
        Translate sentence using Chain-of-thoughts with Langchain

        :param messages List
            List of messages to the LLM

        :return
        """

        chat_llm = ChatOpenAI(openai_api_key = self.openai_api_key)

        llm_output = chat_llm.predict_messages(chat_prompt)

        return llm_output


# For testing purposes
if __name__ == "__main__":

    # OpenAI API key
    openai_api_key: str = os.getenv("OPENAI_API_KEY")

    # configuration object
    config = {"languages": {
        "source_language": "English",
        "target_language": "Arabic"
    }}
    
    # gpt instance
    gpt: GPT = GPT(config, openai_api_key)

    # source_lang
    source_lang: str = "English"

    # target_lang
    target_lang: str = "Arabic"

    # source sentence
    source_sentence: str = "The weather is the last truly wild thing on Earth."

    # messages
    messages: List = [
        {"role": "user", "content": f"Translate the following {source_lang} sentence to {target_lang}"},
        {"role": "assistant", "content": source_sentence},
        {"role": "user", "content": "Arabic:"},
    ]

    # invoke model
    output: dict = gpt.translate(messages)

    # Get the current date and time
    timestamp: str = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")

    # Specify the directory to save the file
    output_directory: str = "../../data/output_translations/"

    # Create the output directory if it doesn't exist
    os.makedirs(output_directory, exist_ok=True)

    # Define the filename with the timestamp
    filename: str = os.path.join(output_directory, f"translation_{timestamp}.txt")

    # translated text
    translated_text: str = output["choices"][0]["message"]["content"] # الطقس هو آخر شيء بريء حقا على وجه الأر

    # Write the translated text to the file
    with open(filename, "w", encoding="utf-8") as file:
        file.write(f"{source_sentence}, {translated_text}")
