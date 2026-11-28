# P184's lab: the help desk computer at Kari's Hardware. Stock python:3.12-slim (standard library only, nothing
# installed), Kari's account, the store's documents in ~/helpdesk/docs and one script, helpdesk.py, installed under
# the names of its steps: ask (the model alone), chunk, embed, similar, index, search and rag. The models run in a
# second container, the official ollama/ollama image, reached on the lab network as http://ollama:11434.
FROM python:3.12-slim
RUN useradd -m -s /bin/bash -c "Kari" kari
COPY --chown=kari docs /home/kari/helpdesk/docs
COPY helpdesk.py /usr/local/lib/helpdesk.py
RUN for n in ask chunk embed similar index search rag; do ln -s /usr/local/lib/helpdesk.py /usr/local/bin/$n; done \
 && chmod 755 /usr/local/lib/helpdesk.py
ENV OLLAMA_URL=http://ollama:11434
WORKDIR /home/kari/helpdesk
