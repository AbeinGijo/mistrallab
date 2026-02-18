import os
from mistralai import Mistral, UserMessage
from dotenv import load_dotenv
load_dotenv()

def mistral(user_message, model="mistral-small-latest", is_json=False):
    api_key = os.getenv("MISTRAL_API_KEY")

    model = "mistral-large-latest"
    client = Mistral(api_key=api_key)
    messages = [    UserMessage(content=user_message),    ]
    chat_response = client.chat.complete(
                                        model=model,
                                        messages=messages,
                                        )
    return chat_response.choices[0].message.content

INTENTS = [
    "card arrival",
    "change pin",
    "exchange rate",
    "country support",
    "cancel transfer",
    "charge dispute",
    "customer service",
]

def classify_intent(inquiry: str) -> str:
    prompt = f"""
You are a bank customer service bot.
Classify the customer's inquiry into ONE category:
card arrival
change pin
exchange rate
country support
cancel transfer
charge dispute
If none fit, return: customer service

Return ONLY the category text. No explanation.

Inquiry: {inquiry}
Category:
""".strip()

    raw = mistral(prompt).lower()
    for c in INTENTS:
        if c in raw:
            return c
    return "customer service"

def generate_reply(inquiry: str, intent: str) -> str:
    prompt = f"""
You are a helpful bank customer support assistant.

Intent: {intent}

Rules:
- Be clear and friendly.
- Give general guidance (do not invent exact bank policy).
- Ask at most ONE follow-up question if needed (e.g., country, transfer id, date).
- Keep it short: 4-8 sentences.

Customer inquiry:
{inquiry}

Assistant reply:
""".strip()

    return mistral(prompt)

def summarize_conversation(convo_text: str) -> str:
    prompt = f"""
Summarize this chat into 4-6 bullet points.
Include: user's issue, detected intents, key actions suggested, and missing info requested.

Chat:
{convo_text}

Bullets:
""".strip()

    return mistral(prompt)
