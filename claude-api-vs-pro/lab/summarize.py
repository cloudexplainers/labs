import sys
import anthropic

email = open(sys.argv[1]).read()
client = anthropic.Anthropic()   # looks for ANTHROPIC_API_KEY
reply = client.messages.create(
    model="claude-sonnet-5-5",
    max_tokens=300,
    system="You summarize customer emails for a small coffee shop.",
    messages=[{"role": "user",
               "content": "Summarize in one sentence:\n" + email}],
)
print(reply.content[0].text)
