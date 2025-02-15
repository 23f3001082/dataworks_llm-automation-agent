import openai
import os

# ✅ Get API key from environment variable
api_key = os.getenv("AIPROXY_TOKEN")

# ✅ Ensure API key is set
if not api_key:
    raise ValueError("Missing OpenAI API key. Set AIPROXY_TOKEN environment variable.")

# ✅ Use AI Proxy instead of OpenAI default
client = openai.OpenAI(
    api_key=api_key,
    base_url="https://aiproxy.sanand.workers.dev/openai/v1"  # ✅ AI Proxy URL
)

def parse_task(task_description: str):
    """Uses OpenAI GPT via AI Proxy to parse a natural language task into structured steps."""
    
    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "Parse the given task into structured instructions."},
                {"role": "user", "content": task_description}
            ]
        )
        return response.choices[0].message.content
    except openai.OpenAIError as e:
        return f"OpenAI API Error: {str(e)}"