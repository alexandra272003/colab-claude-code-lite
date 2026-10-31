import os
from dotenv import load_dotenv
from dataclasses import dataclass
from langchain_openai import ChatOpenAI


load_dotenv()


@dataclass(frozen=True)
class Provider:
    name: str
    env_var: str
    is_free: bool
    base_url: str | None
    model: str


def _providers() -> list[Provider]:
    providers: list[Provider] = []

    # Any OpenAI-compatible endpoint: local Ollama, Groq, OpenRouter, vLLM, ...
    if os.getenv("CUSTOM_BASE_URL"):
        providers.append(Provider(
            os.getenv("CUSTOM_NAME", "Custom"),
            "CUSTOM_API_KEY",
            True,
            os.getenv("CUSTOM_BASE_URL"),
            os.getenv("CUSTOM_MODEL", ""),
        ))

    providers.append(Provider(
        "HuggingFace", "HF_TOKEN", True,
        "https://router.huggingface.co/v1",
        os.getenv("HF_MODEL", "meta-llama/Llama-3.1-8B-Instruct"),
    ))
    providers.append(Provider("OpenAI", "OPENAI_API_KEY", False, None, "gpt-4o-mini"))
    return providers


def select_provider() -> Provider:
    for provider in _providers():
        if os.getenv(provider.env_var):
            return provider
    raise RuntimeError("No provider found. Set CUSTOM_BASE_URL+CUSTOM_API_KEY, HF_TOKEN or OPENAI_API_KEY.")


def build_chat_model() -> tuple[ChatOpenAI, Provider]:
    provider = select_provider()
    kwargs: dict = {
        "model": provider.model,
        "api_key": os.getenv(provider.env_var),
        "temperature": 0.1,
    }
    if provider.base_url is not None:
        kwargs["base_url"] = provider.base_url
    return ChatOpenAI(**kwargs), provider
