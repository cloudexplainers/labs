import json
from google import genai

client = genai.Client()
chat = client.chats.create(model="gemini-3.5-flash-lite")
catalog = open("catalog.txt").read()
questions = [catalog + "\nWhich Sencha lot is cheapest?",
             "And which was harvested first?",
             "Any Matcha under 30 a kilo?",
             "Which Assam lot has the most kilos?"]
for q in questions:
    try:
        reply = chat.send_message(q)
    except genai.errors.ClientError as e:
        json.dump(e.details, open("error.json", "w"))
        exit(f"error {e.code} {e.status}")
    print(f"{reply.usage_metadata.prompt_token_count:,} tokens sent")
