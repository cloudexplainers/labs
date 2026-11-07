# Ana's tea describer: one question to one model, through the official OpenAI Python library.
import os, sys
from openai import OpenAI

client = OpenAI(base_url="https://openrouter.ai/api/v1", api_key=os.environ["OPENROUTER_API_KEY"])
reply = client.chat.completions.create(
    model=sys.argv[1],
    messages=[{"role": "user", "content": "Describe our Sencha green tea in one calm sentence."}],
)
print(reply.choices[0].message.content.strip())
print("model:", reply.model)
