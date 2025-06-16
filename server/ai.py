import json
import os
from typing import Iterable
import hashlib
import openai
from dotenv import load_dotenv
from openai import NOT_GIVEN, NotGiven
from openai.types.chat import ChatCompletionMessageParam
from openai.types.chat import completion_create_params, ChatCompletion


load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
OPENAI_API_BASE = os.getenv("OPENAI_API_BASE", "https://api.openai.com/v1")
CACHE_PATH = os.path.join(os.path.dirname(__file__), "cache")

if not OPENAI_API_KEY:
    raise ValueError("Error: 请在 .env 文件中设置 OPENAI_API_KEY！")

if not os.path.exists(CACHE_PATH):
    os.makedirs(CACHE_PATH)

client = openai.OpenAI(api_key=OPENAI_API_KEY, base_url=OPENAI_API_BASE)

def get_cache_file(params: dict) -> str:
    params_str = json.dumps(params, sort_keys=True)
    cache_key = hashlib.md5(params_str.encode()).hexdigest()
    return os.path.join(CACHE_PATH, f"{cache_key}.json")


def call_openai(
    messages: Iterable[ChatCompletionMessageParam],
    model: str = "gpt-4o-mini",
    temperature: float = 0.7,
    top_p: float = 1,
    frequency_penalty: float = 1,
    presence_penalty: float = 1,
    functions: Iterable[completion_create_params.Function] | NotGiven = NOT_GIVEN,
    use_cache: bool = False
) -> ChatCompletion:

    if use_cache:
        params = {
            "model": model,
            "messages": messages,
            "function_call": "auto",
            "temperature": temperature,
            "top_p": top_p,
            "frequency_penalty": frequency_penalty,
            "presence_penalty": presence_penalty
        }
        if functions is not NOT_GIVEN:
            params["functions"] = functions
        cache_file = get_cache_file(params)

        if os.path.exists(cache_file):
            with open(cache_file, 'r', encoding='utf-8') as f:
                return ChatCompletion.parse_obj(json.load(f)['response'])

    response = client.chat.completions.create(
        model=model,
        messages=messages,
        functions=functions,
        function_call="auto",
        temperature=temperature,
        top_p=top_p,
        frequency_penalty=frequency_penalty,
        presence_penalty=presence_penalty
    )

    if use_cache:
        cache_data = {
            "params": params,
            "response": response.model_dump()
        }
        with open(cache_file, 'wt', encoding='utf-8') as f:
            json.dump(cache_data, f, ensure_ascii=False, indent=2)

    return response


def extract_function_call(response: ChatCompletion):
    if not response.choices:
        return None, None

    message = response.choices[0].message
    function_call = message.function_call if hasattr(message, "function_call") else None

    if not function_call or not function_call.name or not function_call.arguments:
        return None, None

    tool_name = function_call.name
    try:
        args = json.loads(function_call.arguments)
    except Exception as e:
        raise ValueError(f"Failed to parse function arguments: {e}")

    return tool_name, args
