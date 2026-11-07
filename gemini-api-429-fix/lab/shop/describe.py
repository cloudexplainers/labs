from google import genai

client = genai.Client()  # finds the key in GEMINI_API_KEY
teas = open("teas.txt").read().splitlines()

for n, tea in enumerate(teas, 1):
    reply = client.models.generate_content(
        model="gemini-3.5-flash-lite",
        contents=f"One calm sentence about {tea} tea for our shop page.",
    )
    print(n, tea, "done")
