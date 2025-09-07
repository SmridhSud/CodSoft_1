import re

def chatbot_response(user_input):
    # Convert to lowercase for easier matching
    user_input = user_input.lower().strip()

    # Greeting rules
    if re.search(r"\b(hi|hello|hey)\b", user_input):
        return "Hello! How can I help you today?"

    # Asking about chatbot
    elif re.search(r"who (are|r) you", user_input):
        return "I’m a simple rule-based chatbot built to talk with you!"

    # Asking about wellbeing
    elif re.search(r"how are you", user_input):
        return "I’m doing great, thanks for asking! How about you?"

    # User saying goodbye
    elif re.search(r"(bye|goodbye|see you)", user_input):
        return "Goodbye! Have a wonderful day ahead!"

    # Asking about time
    elif re.search(r"(time|current time)", user_input):
        from datetime import datetime
        return f"The current time is {datetime.now().strftime('%H:%M:%S')}."

    # Asking about weather (simple rule-based)
    elif re.search(r"(weather|temperature)", user_input):
        return "I can’t check live weather, but I hope it’s nice where you are!"

    # Default response
    else:
        return "I’m not sure how to respond to that. Could you rephrase?"

# Main loop
def run_chatbot():
    print("Chatbot: Hi, I’m your assistant. Type 'bye' to exit.")
    while True:
        user_input = input("You: ")
        if user_input.lower() in ["bye", "exit", "quit"]:
            print("Chatbot: Goodbye! Talk to you later.")
            break
        response = chatbot_response(user_input)
        print("Chatbot:", response)

# Run the chatbot
if __name__ == "__main__":
    run_chatbot()

