import os
import functools
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()


class MockModel:
    msg = "This is just a mock reply (set model: /cfg model=default)"
    choices: list = [{"message": {"role": "assistant", "content": msg}}]

    def __call__(self, messages, *_args, **_kwargs):
        self.choices = [{"message": {"role": "assistant", "content": f"{self.msg}. You: {messages[-1]['content']}"}}]
        return self


gpt3_5 = functools.partial(
    OpenAI(api_key=os.getenv("OPENAI_API_KEY")).chat.completions.create,
    model="gpt-3.5-turbo",
)
gpt4 = functools.partial(
    OpenAI(api_key=os.getenv("OPENAI_API_KEY")).chat.completions.create,
    model="gpt-4",
)
models = {
    "default": gpt3_5,
    "mock": MockModel(),
    "gpt3.5": gpt3_5,
    "gpt4": gpt4,
}


def get_model(model_name: str):
    model = models[model_name]
    return model
