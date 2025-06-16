from ai import call_openai, extract_function_call


def polish_v1(text, use_cache=False):
    functions = [
        {
            "name": "process_text",
            "description": "Polish the text and return the result in JSON format.",
            "parameters": {
                "type": "object",
                "properties": {
                    "processed_text": {"type": "string", "description": "Polished text"},
                    "source_text": {"type": "string", "description": "Original text"},
                    "operation": {"type": "string", "description": "Operation type: polish"}
                },
                "required": ["processed_text", "source_text", "operation"]
            }
        }
    ]
    messages = [
        {
            "role": "system",
            "content": "You are a professional language assistant "\
                       "and will return results in a JSON structure."
        },
        {
            "role": "user",
            "content": f"Please polish the following text and return it in JSON format:\n{text}"
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