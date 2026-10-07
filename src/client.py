import os
import json

from dataclasses import dataclass

from dotenv import load_dotenv

load_dotenv()

@dataclass(frozen=True)
class Provider:
    """
    Represents one LLM provider as DATA.

    Instead of scattering provider information throughout
    the code, we keep everything related to a provider
    inside this simple class.

    Example:
        Provider(
            name="Groq",
            env_var="GROQ_API_KEY",
            is_free=True,
            base_url=None,
            model="openai/gpt-oss-20b"
        )

    frozen=True means that once a Provider object is created,
    its values cannot be changed accidentally.
    """

    name: str
    env_var: str
    is_free: bool
    base_url: str | None
    model: str

PROVIDERS=[
    Provider("Groq", "GROQ_API_KEY", True, None, "openai/gpt-oss-20b"),
]


def select_provider()->Provider:
    """
    Find which LLM provider is configured.

    The function checks each provider and asks:

        "Does the required API key exist?"

    The first provider with a valid API key is selected.

    This means our application doesn't need to know
    which provider the user configured.
    """
    for provider in PROVIDERS:
        if os.environ.get(provider.env_var):
            return provider
    expected=", ".join(p.env_var for p in PROVIDERS)
    raise RuntimeError(f"No provider key set. Add one of {expected} to your .env file")


def build_client(provider: Provider):
    """
    Create and return the SDK client for the selected provider.

    The provider object tells us:
        - which environment variable contains the API key
        - whether a custom base URL should be used

    For Groq, this creates a Groq client.
    """
    from groq import Groq

    api_key=os.environ[provider.env_var]
    if provider.base_url is None:
        return Groq(api_key=api_key)
    return Groq(api_key=api_key, base_url=provider.base_url)


def llm_reply(prompt: str,*,max_tokens: int=300)->str:
    """
    Send a user's prompt to the selected LLM
    and return the model's response as a string.

    Example:

        response = llm_reply("Explain Python classes")

    The overall flow is:

        1. Find a configured provider
        2. Create its API client
        3. Send the prompt to the model
        4. Extract the assistant's response
        5. Return the response as a string
    """

    provider=select_provider()
    client=build_client(provider)

    result=client.chat.completions.create(
        model=provider.model,
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ]
    )

    return result.choices[0].message.content