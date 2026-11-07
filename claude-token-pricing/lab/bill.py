"""List prices of the Claude API in US dollars per million tokens (platform.claude.com pricing page, 2026-11-06).

Claude Code writes its cache with the 1-hour lifetime (2x the input price); a 5-minute write is 1.25x.
Cache reads on Opus 5.5 and Sonnet 5.5 are 0.05x the input price; Haiku 5.5's are 0.1x.
"""
PRICES = {  # input, 1h cache write, 5m cache write, cache read, output
    "haiku-5.5": (0.10, 0.20, 0.125, 0.01, 0.50),
    "sonnet-5.5": (2.00, 4.00, 2.50, 0.10, 10.00),
    "opus-5.5": (4.00, 8.00, 5.00, 0.20, 20.00),
}


def cost(model, fresh, write, read, out, batch=False):
    pi, pw, _, pr, po = PRICES[model]
    c = (fresh * pi + write * pw + read * pr + out * po) / 1e6
    return c / 2 if batch else c
