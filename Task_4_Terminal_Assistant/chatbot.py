
import re


# -----------------------------------------
# RULE-BASED INTERACTIVE TERMINAL CHATBOT
# -----------------------------------------

BUSINESS_HOURS = """
Our business hours are:
Monday to Saturday: 9:00 AM - 6:00 PM
Sunday: Closed
"""

PRODUCT_FAQS = {
    "products": (
        "We offer electronics, accessories, and other daily-use products."
    ),
    "price": (
        "Product prices depend on the item. "
        "Please check the product listing for exact prices."
    ),
    "availability": (
        "Product availability depends on current stock. "
        "Please check the product listing."
    ),
    "shipping": (
        "Orders are normally delivered within 3-5 business days."
    ),
    "payment": (
        "We accept cash on delivery and online payments."
    )
}

RETURN_POLICY = """
Our sample return policy:
- Products can be returned within 7 days of delivery.
- Products must be unused and in their original packaging.
- Contact customer support to request a return.
"""

# Intent patterns using regular expressions
INTENT_PATTERNS = {
    "greeting": [
        r"\b(hello|hi|hey|good morning|good afternoon|good evening)\b"
    ],
    "business_hours": [
        r"\b(business hours|opening hours|working hours|timing|open|close|closed)\b"
    ],
    "products": [
        r"\b(products|product range|what do you sell|what do you offer)\b"
    ],
    "price": [
        r"\b(price|prices|cost|how much)\b"
    ],
    "availability": [
        r"\b(available|availability|in stock|stock)\b"
    ],
    "shipping": [
        r"\b(shipping|delivery|deliver|shipment)\b"
    ],
    "payment": [
        r"\b(payment|payments|pay|cash on delivery|cod)\b"
    ],
    "returns": [
        r"\b(return|returns|refund|exchange|replace)\b"
    ],
    "thanks": [
        r"\b(thank you|thanks|thank)\b"
    ]
}


# Responses for each recognized intent
INTENT_RESPONSES = {
    "business_hours": BUSINESS_HOURS,
    "products": PRODUCT_FAQS["products"],
    "price": PRODUCT_FAQS["price"],
    "availability": PRODUCT_FAQS["availability"],
    "shipping": PRODUCT_FAQS["shipping"],
    "payment": PRODUCT_FAQS["payment"],
    "returns": RETURN_POLICY,
    "thanks": "You're welcome! Is there anything else I can help you with?"
}


def normalize_input(user_input):
    """Normalize user input before processing."""
    return user_input.lower().strip()


def detect_intents(user_input):
    """Identify all matching intents in the user's message."""
    detected = []

    for intent, patterns in INTENT_PATTERNS.items():
        for pattern in patterns:
            if re.search(pattern, user_input):
                detected.append(intent)
                break

    return detected


def generate_response(intents, last_intent):
    """Generate responses for recognized intents."""

    if not intents:
        return (
            "I'm sorry, I didn't understand your question. "
            "You can ask about business hours, products, "
            "prices, shipping, payments, or returns."
        ), last_intent

    responses = []

    if "greeting" in intents:
        responses.append(
            "Hello! Welcome to our customer support assistant. "
            "How can I help you today?"
        )

    for intent in intents:
        if intent in INTENT_RESPONSES:
            responses.append(INTENT_RESPONSES[intent])
            last_intent = intent

    return "\n\n".join(responses), last_intent


def chatbot():
    """Run the interactive chatbot."""

    last_intent = None

    print("\n" + "=" * 55)
    print("       RULE-BASED CUSTOMER SUPPORT CHATBOT")
    print("=" * 55)

    print("\nBot: Hello! Welcome to our customer support.")
    print("Bot: You can ask me about products, business hours,")
    print("     prices, shipping, payments, and returns.")
    print("Bot: Type 'bye', 'exit', or 'quit' to end the chat.")

    while True:
        try:
            user_input = input("\nYou: ").strip()

            if not user_input:
                print("Bot: Please enter a message.")
                continue

            normalized_input = normalize_input(user_input)

            # Exit commands
            if re.fullmatch(r"(bye|exit|quit)", normalized_input):
                print("Bot: Thank you for chatting with us. Goodbye!")
                break

            # Detect multiple intents
            detected_intents = detect_intents(normalized_input)

            # Contextual follow-up handling
            if (
                not detected_intents
                and last_intent
                and re.search(
                    r"\b(tell me more|more details|explain more)\b",
                    normalized_input
                )
            ):
                detected_intents = [last_intent]

            response, last_intent = generate_response(
                detected_intents,
                last_intent
            )

            print("\nBot:", response)

        except (KeyboardInterrupt, EOFError):
            print("\nBot: Chat ended. Goodbye!")
            break

        except Exception as error:
            print("Bot: Something went wrong. Please try again.")
            print("Error:", error)


if __name__ == "__main__":
    chatbot()
