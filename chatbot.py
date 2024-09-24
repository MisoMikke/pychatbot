#tuo json ja random kirjastot jotta ohjelma toimii halutulla tavalla
import json
import random
#lukee jsonia jotta saa vastaukset
def load_responses(filename):
    try:
        with open(filename, 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        return {}
#tallettaa uuden vastauksen
def save_responses(filename, responses):
    with open(filename, 'w') as file:
        json.dump(responses, file, indent=4)

def clean_input(user_input):
    #muuttaa käyttäjän tekstin lowercaselle ja poistaa merkit
    translation_table = str.maketrans('', '', "!?,'.")
    return user_input.lower().translate(translation_table).strip()
#arrayt joista vastaus haetaan
def generate_response(user_input, responses, responses_file):
    cleaned_input = clean_input(user_input)
    greeting_responses = responses.get("greetings", [])
    question_responses = responses.get("questions", [])
    request_responses = responses.get("requests", [])
    ask_responses = responses.get("ask", [])
    comment_responses = responses.get("comments", [])

    #valisee sopivista vastauksista yhden satunnaisesti
    for responses_dict in [greeting_responses, question_responses, request_responses, ask_responses, comment_responses]:
        for key, responses_list in responses_dict.items():
            if cleaned_input in key.split(","):
                return random.choice(responses_list)
    
    #etsii sopivaa vastausta
    if cleaned_input in responses and isinstance(responses[cleaned_input], list):
        return random.choice(responses[cleaned_input])
    #jos sopivaa vastausta ei ole
    if cleaned_input not in responses:
        user_response = input("What should I reply to that? ")
        responses[cleaned_input] = [user_response]
        save_responses(responses_file, responses)
        return user_response
    
    return responses.get(cleaned_input, "I'm not sure what to say to that.")

def chat(responses_file):
    responses = load_responses(responses_file)
#chatbot aloittaa tervehtimällä sinua, quit lopettaa ohjelman
    print("Hi, I'm Chatty, your chatbot! Type 'quit' to exit.")
    while True:
        user_input = input("You: ")
        if user_input.lower() == "quit":
            save_responses(responses_file, responses)
            print("Goodbye!")
            break
#botin 'vuorosanat' erottaa sinun inputeista Bot: ja You: aluilla
        response = generate_response(user_input, responses, responses_file)
        print("Bot:", response)

if __name__ == "__main__":
    chatbot_responses_file = "chatbot_responses.json"
    chat(chatbot_responses_file)
