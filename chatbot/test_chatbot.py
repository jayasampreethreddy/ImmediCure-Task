from intent_classifier import classify_specialty
from response_generator import generate_response
from models.keymapping import map_symptom_to_specialty, search_doctors  # ✅ Import these!

while True:
    user_input = input("User: ")
    if user_input.lower() in ["exit", "quit"]:
        break

    # Step 1: Map user input to a specialty
    specialties = map_symptom_to_specialty(user_input)  # ✅ Use this function
    print(f"Mapped Specialties: {specialties}")  # Debugging

    if not specialties:
        print("\n💬 Chatbot Response: No relevant specialties found for the symptoms.")
        continue

    # Step 2: Search for doctors using mapped specialties
    doctors = search_doctors(specialties)  # ✅ Use this function
    print(f"Recommended Doctors: {doctors}")  # Debugging

    if not doctors:
        print("\n💬 Chatbot Response: No doctors found for the given symptoms.")
    else:
        response = generate_response(doctors)
        print("\n💬 Chatbot Response:", response)
