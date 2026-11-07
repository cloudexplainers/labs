from google import genai

client = genai.Client()  # Gemini API: a key, from GEMINI_API_KEY

reply = client.models.generate_content(
    model="gemini-3.8-flash",
    contents="Describe our Sencha green tea in one calm sentence.",
)
print(reply.text)
print("(through Vertex AI)" if client.vertexai else "(through the Gemini API)")
