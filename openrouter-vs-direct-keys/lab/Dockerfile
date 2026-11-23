# Kari's laptop for P051: a stock Ubuntu 24.04 with curl, jq and Python, plus the official OpenAI Python library in a
# virtual environment. The same library talks to both doors: Google's own OpenAI-compatible Gemini API endpoint and
# OpenRouter. No key is baked in: demo.sh passes GOOGLE_API_KEY and OPENROUTER_API_KEY at run time.
FROM ubuntu:24.04
RUN apt-get update && DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
      curl jq ca-certificates python3 python3-venv && rm -rf /var/lib/apt/lists/*
RUN userdel -r ubuntu 2>/dev/null; useradd -m -s /bin/bash kari
USER kari
RUN python3 -m venv /home/kari/.venv && /home/kari/.venv/bin/pip install -q openai==3.46.0
ENV PATH=/home/kari/.venv/bin:$PATH
COPY --chown=kari:kari grocery /home/kari/grocery
WORKDIR /home/kari/grocery
