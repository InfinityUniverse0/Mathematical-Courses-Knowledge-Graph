'''backend.py
    This file contains the backend code for the web application.
    复杂的后端处理函数代码
    被views.py调用
'''

import openai
import json
from django.conf import settings

openai.api_key = settings.OPENAI_API_KEY

# 和chatgpt交互的接口
def Chat(message: str):
    try:
        response = openai.ChatCompletion.create(
            model='gpt-3.5-turbo',
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {'role': 'user', 'content': message}
            ]
        )
        completion = response['choices'][0]['message']['content']
    except Exception as e:
        completion = 'ERROR: ' + str(e)
    return completion


def Chat_json(json_data):
    try:
        data = json.loads(json_data)
        message = data.get('message')
    except json.JSONDecodeError:
        return 'ERROR: Invalid JSON data.'
    return Chat(message)
