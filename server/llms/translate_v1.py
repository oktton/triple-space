from ai import call_openai, extract_function_call


def translate_v1(text, target_language="english", use_cache=False):
    functions = [
        {
            "name": "process_text",
            "description": "Process the text and return the result in JSON format.",
            "parameters": {
                "type": "object",
                "properties": {
                    "processed_text": {"type": "string", "description": "Processed text"},
                    "source_text": {"type": "string", "description": "Original text"},
                    "operation": {"type": "string", "description": "Operation type: translate"}
                },
                "required": ["processed_text", "source_text", "operation"]
            }
        }
    ]
    messages = [
        {
            "role": "system",
            "content": "You are a professional language assistant " \
                       "and will return results in a JSON structure."
        },
        {
            "role": "user",
            "content": f"Please translate the following text into {target_language} and return it in JSON format:\n{text}"
        }
    ]

    # 调用 call_openai，并根据 return_params 决定返回内容
    response = call_openai(
        messages=messages,
        functions=functions,
        use_cache=use_cache
    )

    tool_name, function_call_args = extract_function_call(response)
    # 默认返回解析后的结果
    return function_call_args['processed_text']

