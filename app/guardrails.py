OFF_TOPIC_WORDS = [
    "weather",
    "temperature",
    "rain",
    "forecast",
    "cricket",
    "ipl",
    "football",
    "soccer",
    "movie",
    "cinema",
    "actor",
    "actress",
    "song",
    "music",
    "recipe",
    "food",
    "news",
    "politics",
    "election",
    "bitcoin",
    "crypto",
    "stock",
    "share market",
    "youtube",
    "instagram",
    "facebook",
    "twitter",
    "gmail",
    "google maps"
]

PROMPT_INJECTION = [
    "ignore previous instructions",
    "forget previous instructions",
    "system prompt",
    "reveal prompt",
    "act as",
    "jailbreak",
    "developer mode",
    "bypass",
    "ignore all instructions"
]


def is_off_topic(query: str):
    query = query.lower()
    return any(word in query for word in OFF_TOPIC_WORDS)


def is_prompt_injection(query: str):
    query = query.lower()
    return any(word in query for word in PROMPT_INJECTION)