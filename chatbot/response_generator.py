import pandas as pd

# Load the cleaned doctor dataset
doctor_data_path = r"C:\Users\konde\Music\IMMEDICURE\ImmediCure-Task\models\cleaned_doctor_data_fixed.csv"  # Adjust if needed
doctor_df = pd.read_csv(doctor_data_path)

def find_doctors(specialties, top_n=3):
    """
    Find doctors matching the given list of specialties.

    Args:
    specialties (list): List of predicted specialties.
    top_n (int): Number of doctors to return.

    Returns:
    list: List of dictionaries containing doctor details.
    """
    matching_doctors = doctor_df[doctor_df["specialty"].isin(specialties)]

    if matching_doctors.empty:
        return [{"message": "No doctors found for the given symptoms."}]

    # Select top N doctors
    top_doctors = matching_doctors.head(top_n)

    results = []
    for _, row in top_doctors.iterrows():
        results.append({
            "doctor_name": row["doctor_name"],  # Use correct column name
            "specialty": row["specialty"],
            "location": row["location"],
            "profile_url": row.get("profile_url", "N/A")  # Use profile_url
        })

    return results

def generate_response(user_input, specialties):
    """
    Generate a chatbot response with recommended doctors.

    Args:
    user_input (str): The user’s input symptoms.
    specialties (list): Predicted medical specialties.

    Returns:
    str: Formatted response string.
    """
    doctors = find_doctors(specialties)

    if "message" in doctors[0]:
        return doctors[0]["message"]

    response = f"Based on your symptoms: '{user_input}', you may need to consult:\n"
    for doc in doctors:
        response += f"🔹 **{doc['doctor_name']}** - {doc['specialty']} (📍 {doc['location']})\n"
        response += f"   [Doctor Profile]({doc['profile_url']})\n\n"

    return response.strip()
