#!/usr/bin/env python
# coding: utf-8

# In[1]:



# In[2]:


import pandas as pd

# Load the cleaned doctor dataset
df = pd.read_csv(r"C:\Users\konde\Music\IMMEDICURE\ImmediCure-Task\models\cleaned_doctor_data_fixed.csv")

# Extract unique specialties from dataset
unique_specialties = df["specialty"].dropna().unique().tolist()

print(f"✅ Found {len(unique_specialties)} unique specialties!")


# In[6]:


from sentence_transformers import SentenceTransformer, util
import pandas as pd

# Load cleaned doctor dataset
df = pd.read_csv(r"C:\Users\konde\Music\IMMEDICURE\ImmediCure-Task\models\cleaned_doctor_data_fixed.csv")

# Extract unique specialties from dataset
unique_specialties = df["specialty"].dropna().unique().tolist()
print(f"✅ Found {len(unique_specialties)} unique specialties!")

# Load a good AI model for medical text
model = SentenceTransformer("BAAI/bge-small-en")

# Encode all specialties from the dataset
specialty_embeddings = model.encode(unique_specialties, convert_to_tensor=True)

def map_symptom_to_specialty(symptom, top_k=3):
    """Maps a given symptom to the best-matching specialties from the dataset."""
    symptom_embedding = model.encode(symptom, convert_to_tensor=True)
    similarity_scores = util.pytorch_cos_sim(symptom_embedding, specialty_embeddings).squeeze(0)

    # Get top-K matches
    top_k_indices = similarity_scores.argsort(descending=True)[:top_k]
    best_matches = [(unique_specialties[idx], similarity_scores[idx].item()) for idx in top_k_indices]

    # Apply confidence threshold (remove low-scoring matches)
    best_matches = [match[0] for match in best_matches if match[1] > 0.5]  

    return best_matches



# In[7]:


print(map_symptom_to_specialty("chest pain"))   # Expected: Cardiology
print(map_symptom_to_specialty("skin rash"))    # Expected: Dermatology
print(map_symptom_to_specialty("anxiety"))      # Expected: Psychiatry
print(map_symptom_to_specialty("blurry vision")) # Expected: Ophthalmology


# In[12]:


import pandas as pd

# Load cleaned doctor dataset
df = pd.read_csv(r"C:\Users\konde\Music\IMMEDICURE\ImmediCure-Task\models\cleaned_doctor_data_fixed.csv")

def search_doctors(symptom, location=None, top_k=5):
    """Finds doctors based on AI-mapped specialties and optional location."""
    
    # Step 1: AI Maps symptom to specialties
    matched_specialties = map_symptom_to_specialty(symptom, top_k=3)
    print(f"🔍 AI Mapped '{symptom}' → {matched_specialties}")

    # Step 2: Filter doctors by matched specialties
    filtered_doctors = df[df["specialty"].isin(matched_specialties)]

    # Step 3: Filter by location (if provided)
    if location:
        filtered_doctors = filtered_doctors[filtered_doctors["location"].str.contains(location, case=False, na=False)]

    # Step 4: Return top K results
    return filtered_doctors.head(top_k)[["doctor_name", "specialty", "location", "profile_url"]]

# Test the search function



# In[13]:


print(search_doctors("chest pain", location="New York"))  # Example with location
print(search_doctors("skin rash"))  # Example without location


# In[ ]:




