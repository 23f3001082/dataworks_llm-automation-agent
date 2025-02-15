import openai
import os

api_key = os.getenv("AIPROXY_TOKEN")
if not api_key:
    raise ValueError("Missing OpenAI API key. Set AIPROXY_TOKEN environment variable.")

client = openai.OpenAI(
    api_key=api_key,
    base_url="https://aiproxy.sanand.workers.dev/openai/v1"
)

def parse_task(task_description: str):
    """Uses OpenAI GPT via AI Proxy to parse a natural language task into structured steps."""
    model = os.getenv("LLM_MODEL", "gpt-4o-mini")
    try:
        response = client.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": "Parse the given task into structured instructions."},
                {"role": "user", "content": task_description}
            ]
        )
        return response.choices[0].message.content
    except openai.OpenAIError as e:
        return f"OpenAI API Error: {str(e)}"