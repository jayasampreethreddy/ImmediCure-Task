from chatbot.intent_classifier import classify_specialty
from models.doctor_search import search_doctors

def chatbot_response(user_input):
    """ Main chatbot function: Maps symptoms to specializations and recommends doctors. """
    specializations = classify_specialty(user_input)

    if not specializations:
        return "I'm sorry, I couldn't find a relevant specialty. Please try again."

    doctors = search_doctors(specializations)

    if not doctors:
        return f"I found the relevant specialties {specializations}, but no doctors are available."

    response = f"Based on your input, here are some recommended doctors:\n"
    for doc in doctors[:5]:  # Show top 5 doctors
        response += f"👨‍⚕️ {doc['name']} | {doc['specialty']} | 📍 {doc['location']}\n"

    return response
