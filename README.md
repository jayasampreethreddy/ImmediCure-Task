# Doctor Recommendation Web App 

## 📌 Project Overview

This project is a Doctor Recommendation Web App that:
- ✅ Takes symptoms as input
- ✅ Uses AI to map symptoms to medical specialties
- ✅ Fetches relevant doctors from a dataset
- ✅ Displays doctor recommendations with profile links

## 📌 Data Sources & Scraping

### 🗂️ Primary Dataset

We obtained doctor details from the CMS (Centers for Medicare & Medicaid Services) API:
- 🔗 CMS Provider Data API

### ✅ Data Fields Scraped:
- doctor_name
- specialty
- location
- profile_url

### 🛠️ Web Scraping Process

We wrote a Python script (datascraper.py) to extract data using requests + pandas:

```python
import requests
import pandas as pd

# API URL
API_URL = "https://data.cms.gov/provider-data/api/1/datastore/query/mj5m-pzi6/0"

# Fetch Data
response = requests.get(API_URL)
data = response.json()

# Convert to DataFrame
df = pd.DataFrame(data["data"])
df.to_csv("cleaned_doctor_data.csv", index=False)

print("✅ Data Scraped & Saved!")
```

🔹 Final Processed Data stored in models/cleaned_doctor_data_fixed.csv.

## 📌 Symptom-to-Specialty Mapping

### 🧠 AI Model Used

We used TF-IDF Vectorization + Cosine Similarity for symptom-specialty mapping.
This method converts text into numerical form and finds the closest specialty.

### 🔍 How It Works

1️⃣ Convert specialties and user input (symptoms) into TF-IDF vectors.
2️⃣ Compute cosine similarity between symptoms & specialties.
3️⃣ Select top 3 matches (if similarity > 0.5).

### 📜 Code for Mapping (keymapping.py)

```python
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import joblib
import pandas as pd

# Load Data
df = pd.read_csv("models/cleaned_doctor_data_fixed.csv")
unique_specialties = df["specialty"].unique()

# Train Vectorizer
vectorizer = TfidfVectorizer()
specialty_vectors = vectorizer.fit_transform(unique_specialties)

# Save Vectorizer
joblib.dump(vectorizer, "models/vectorizer.pkl")

# Function to Map Symptoms → Specialties
def map_symptom_to_specialty(symptom, top_k=3):
    symptom_vector = vectorizer.transform([symptom])
    similarity_scores = cosine_similarity(symptom_vector, specialty_vectors)[0]
    top_k_indices = similarity_scores.argsort()[-top_k:][::-1]
    
    best_matches = [(unique_specialties[idx], similarity_scores[idx]) for idx in top_k_indices]
    best_matches = [match[0] for match in best_matches if match[1] > 0.5]

    return best_matches
```

## 📌 Searching for Doctors

Once we have the specialties, we filter doctors from cleaned_doctor_data_fixed.csv.

### 🔍 Doctor Search Code

```python
def search_doctors(specialties):
    doctors = df[df["specialty"].isin(specialties)][["doctor_name", "specialty", "location", "profile_url"]]
    return doctors
```

## 📌 Web App Implementation

### 💻 Tech Stack

- Backend: Flask
- Frontend: HTML + Bootstrap

### 🛠️ Flask Code (app.py)

```python
from flask import Flask, render_template, request
from models.keymapping import map_symptom_to_specialty, search_doctors

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/search", methods=["POST"])
def search():
    user_input = request.form["symptoms"]
    specialties = map_symptom_to_specialty(user_input)

    if not specialties:
        return render_template("results.html", doctors=None, message="No matching specialties found.")

    doctors = search_doctors(specialties)
    return render_template("results.html", doctors=doctors)

if __name__ == "__main__":
    app.run(debug=True)
```

## 📌 UI Design

### 🎨 Features

- Attractive & Clean UI
- Input box for symptoms
- Displays doctor recommendations

### 🖥️ templates/index.html

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <title>Doctor Finder</title>
    <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css">
</head>
<body class="bg-light">
    <div class="container mt-5">
        <h2 class="text-center">Find the Best Doctors for Your Symptoms</h2>
        <form action="/search" method="POST" class="mt-4">
            <div class="mb-3">
                <label for="symptoms" class="form-label">Enter Your Symptoms:</label>
                <input type="text" class="form-control" id="symptoms" name="symptoms" required>
            </div>
            <button type="submit" class="btn btn-primary w-100">Search</button>
        </form>
    </div>
</body>
</html>
```

## 📌 Deployment

For FREE deployment, we use:

- Backend: Render (Flask)
- Frontend: Render


### 🚀 Steps to Deploy on Render

1️⃣ Push project to GitHub
2️⃣ Go to Render and create a new Flask service
3️⃣ Link GitHub repo & enable auto-deploy
4️⃣ Add requirements.txt:

```
Flask
scikit-learn
pandas
joblib
```

5️⃣ Deploy & test API!

## 📌 Summary of Everything We Did

| Step | Details |
|------|---------|
| 1. Data Collection | Scraped CMS API for doctor data |
| 2. Data Cleaning | Filtered & saved doctor details |
| 3. AI Model | Used TF-IDF + Cosine Similarity |
| 4. Backend | Flask API for symptom mapping & doctor search |
| 5. UI | HTML, Bootstrap for clean design |
| 6. Deployment | Render for backend, Vercel for frontend |

## 🚀 Final Steps

- ✅ Run python app.py to test locally
- ✅ Fix UI if needed
- ✅ Deploy for free on Render/Vercel
- ✅ Make it live & share link! 🎉
