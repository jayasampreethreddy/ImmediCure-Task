import pandas as pd
from sentence_transformers import SentenceTransformer, util
import torch  # <-- Add this if missing


# Load the doctor dataset
df = pd.read_csv(r"C:\Users\konde\Music\IMMEDICURE\Immedicure-Task\models\cleaned_doctor_data_fixed.csv")

# Extract unique specialties from the dataset
unique_specialties = df["specialty"].dropna().unique().tolist()

# Load a pretrained sentence transformer model (using a model from sentence-transformers)
model = SentenceTransformer('all-MiniLM-L6-v2')  # You can use other models as needed

# Function to encode text using sentence-transformers
def encode_text(text):
    # Use sentence-transformers to encode the text
    return model.encode(text, convert_to_tensor=True)

# Function to map symptom to specialties
def map_symptom_to_specialty(symptom, top_k=3):
    """Maps a given symptom to the best-matching specialties using sentence-transformers model."""
    
    # Encode the symptom
    symptom_embedding = encode_text(symptom)  # This is a 1D tensor

    # Encode all specialties and stack them into a single tensor
    specialty_embeddings = torch.stack([encode_text(specialty) for specialty in unique_specialties])

    # Calculate cosine similarity using sentence-transformers' util function
    similarity_scores = util.pytorch_cos_sim(symptom_embedding, specialty_embeddings).squeeze(0)

    # Get top K most similar specialties
    top_k_indices = similarity_scores.argsort(descending=True)[:top_k]
    top_specialties = [unique_specialties[idx] for idx in top_k_indices]

    return top_specialties

# Function to search doctors based on specialties
def search_doctors(symptom, location=None, top_k=5):
    """Finds doctors based on AI-mapped specialties and optional location."""
    
    matched_specialties = map_symptom_to_specialty(symptom, top_k=3)
    print(f"🔍 AI Mapped '{symptom}' → {matched_specialties}")

    filtered_doctors = df[df["specialty"].isin(matched_specialties)]

    if location:
        filtered_doctors = filtered_doctors[filtered_doctors["location"].str.contains(location, case=False, na=False)]

    # ✅ Include 'overview' in the result if available
    return filtered_doctors.head(top_k)[["doctor_name", "specialty", "location", "profile_url", "overview"]]


