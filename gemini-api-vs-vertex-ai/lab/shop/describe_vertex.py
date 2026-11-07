from google import genai

client = genai.Client(vertexai=True, project="ce-vertex-p048", location="global")

reply = client.models.generate_content(
    model="gemini-3.8-flash",
    contents="Describe our Sencha green tea in one calm sentence.",
)
print(reply.text)
print("(through Vertex AI)" if client.vertexai else "(through the Gemini API)")
