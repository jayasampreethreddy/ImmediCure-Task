import pandas as pd
from sentence_transformers import SentenceTransformer, util
import torch
BASE_DIR = os.path.dirname(os.path.abspath(__file__))  # Directory of keymapping.py
CSV_PATH = os.path.join(BASE_DIR, r"cleaned_doctor_data_fixed.csv")
# Load the doctor dataset
df = pd.read_csv(CSV_PATH)

# Extract unique specialties from the dataset
unique_specialties = df["specialty"].dropna().unique().tolist()

# Load a pretrained sentence transformer model
model = SentenceTransformer('all-MiniLM-L6-v2')

# Function to encode text using sentence-transformers
def encode_text(text):
    return model.encode(text, convert_to_tensor=True)

# Function to map symptom to specialties
def map_symptom_to_specialty(symptom, top_k=3):
    """Maps a given symptom to the best-matching specialties using sentence-transformers model."""
    
    # Encode the symptom
    symptom_embedding = encode_text(symptom)

    # Encode all specialties and stack them into a single tensor
    specialty_embeddings = torch.stack([encode_text(specialty) for specialty in unique_specialties])

    # Calculate cosine similarity
    similarity_scores = util.pytorch_cos_sim(symptom_embedding, specialty_embeddings).squeeze(0)

    # Get top K most similar specialties
    top_k_indices = similarity_scores.argsort(descending=True)[:top_k]
    top_specialties = [unique_specialties[idx] for idx in top_k_indices]

    return top_specialties

# Function to search doctors based on specialties
def search_doctors(symptom, location=None, top_k=20):
    """Finds doctors based on AI-mapped specialties and optional location."""

    matched_specialties = map_symptom_to_specialty(symptom, top_k=20)
    print(f"🔍 AI Mapped '{symptom}' → {matched_specialties}")

    filtered_doctors = df[df["specialty"].isin(matched_specialties)]

    if location:
        filtered_doctors = filtered_doctors[filtered_doctors["location"].str.contains(location, case=False, na=False)]

    # Shuffle results to remove alphabetical order
    filtered_doctors = filtered_doctors.sample(frac=1, random_state=42)

    return filtered_doctors.head(top_k)[["doctor_name", "specialty", "location", "profile_url", "overview"]]

