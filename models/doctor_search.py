#!/usr/bin/env python
# coding: utf-8

# In[13]:


import pandas as pd

# Load the cleaned dataset
df = pd.read_csv(r"C:\Users\konde\Music\IMMEDICURE\ImmediCure-Task\data\cleaned_doctor_data.csv")

# Display the first few rows


# Extract all unique specialties
all_specialties = sorted(df["specialty"].dropna().unique())

print("✅ Found Specialties:", all_specialties)


# In[17]:


def clean_location(location):
    """Fixes inconsistent location formatting"""
    if pd.isna(location):
        return "Unknown Location"
    
    # Remove extra spaces & commas
    cleaned_location = ", ".join([part.strip() for part in location.split(",") if part.strip()])
    
    return cleaned_location

# Apply to all locations
df["location"] = df["location"].apply(clean_location)

# Display fixed locations
print(df["location"].unique()[:10])


# In[18]:


# Group by doctor and combine all unique locations
df = df.groupby("doctor_name").agg({
    "specialty": "first",
    "location": lambda x: ", ".join(set(x.dropna())),  # Merge locations correctly
    "overview": "first",
    "profile_url": "first"
}).reset_index()

print(f"✅ After merging locations: {df.shape[0]} unique doctors")


# In[19]:


df.to_csv("cleaned_doctor_data_fixed.csv", index=False)
print("✅ Final cleaned dataset saved as 'cleaned_doctor_data_fixed.csv'")

doctors_df = pd.read_csv(r"C:\Users\konde\Music\IMMEDICURE\ImmediCure-Task\models\cleaned_doctor_data_fixed.csv")


def search_doctors(specialties):
    """ Returns doctors matching given specialties. """
    filtered_doctors = doctors_df[doctors_df["specialty"].isin(specialties)]
    return filtered_doctors.to_dict(orient="records")

