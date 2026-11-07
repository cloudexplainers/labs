import os

from google import genai

model = os.environ.get("MODEL", "gemini-3.8-flash")
for location in ["global", "us", "eu", "us-central1", "europe-west4"]:
    client = genai.Client(vertexai=True, project="ce-vertex-p048", location=location)
    try:
        client.models.generate_content(model=model, contents="Say hi in three words.")
        print(f"{location:16} answered")
    except genai.errors.ClientError as e:
        print(f"{location:16} {e.code} {e.status}")
