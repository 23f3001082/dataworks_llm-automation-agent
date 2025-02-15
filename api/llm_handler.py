import os
import openai

def parse_task(task_description: str):
    api_key = os.getenv("AIPROXY_TOKEN")
    response = openai.ChatCompletion.create(
        model="gpt-4o-mini",
        messages=[{"role": "system", "content": "Parse the given task into structured instructions."},
                  {"role": "user", "content": task_description}],
        api_key=api_key
    )
    return response['choices'][0]['message']['content']