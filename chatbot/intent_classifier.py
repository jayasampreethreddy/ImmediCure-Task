from sentence_transformers import SentenceTransformer, util
import pandas as pd

# Load dataset with unique specialties
specialties = pd.read_csv("data/cleaned_doctor_data.csv")["specialty"].unique().tolist()

# Load sentence embedding model
model = SentenceTransformer("all-MiniLM-L6-v2")

def classify_specialty(user_input):
    """ Maps symptoms or keywords to the most relevant medical specialties. """
    user_embedding = model.encode(user_input, convert_to_tensor=True)
    specialty_embeddings = model.encode(specialties, convert_to_tensor=True)

    similarities = util.pytorch_cos_sim(user_embedding, specialty_embeddings)[0]
    top_indices = similarities.argsort(descending=True)[:3]

    best_matches = [specialties[i] for i in top_indices if similarities[i] > 0.5]  # Keep if similarity > 0.5
    return best_matches if best_matches else ["General Medicine"]
