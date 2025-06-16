import json
import traceback

def parse_openai_response(response):
    """解析 OpenAI API 的响应，返回 JSON 结构数据"""
    try:
        # 确保 OpenAI 返回结果
        if not response.choices:
            raise Exception("OpenAI 返回空的 choices")

        function_call = response.choices[0].message.function_call
        if not function_call:
            raise Exception("OpenAI 没有调用 function_call")

        result_json = function_call.arguments  # JSON 字符串
        return json.loads(result_json)  # 转换为字典

    except Exception as e:
        traceback.print_exc()
        return {"error": f"Processing Error: {str(e)}"}
