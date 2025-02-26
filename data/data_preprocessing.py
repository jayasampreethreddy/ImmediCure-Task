#!/usr/bin/env python
# coding: utf-8

# In[5]:


import pandas as pd

# Load Medicare Data
medicare_df = pd.read_csv(r"C:\Users\konde\Music\IMMEDICURE\ImmediCure-Task\data\all_medicare_doctors.csv")

# Load Placidway Data
placidway_df = pd.read_csv(r"C:\Users\konde\Music\IMMEDICURE\ImmediCure-Task\data\cleaned_placidway_doctors.csv")  # Change filename as needed

print(f"✅ Medicare dataset: {medicare_df.shape[0]} rows")
print(f"✅ Placidway dataset: {placidway_df.shape[0]} rows")


# In[6]:


# Rename columns for consistency
medicare_df.rename(columns={
    "name": "doctor_name",
    "specialty": "specialty",
    "location": "location",
    "overview": "overview",
    "profile_link": "profile_url"
}, inplace=True)

placidway_df.rename(columns={
    "Doctor Name": "doctor_name",
    "Specialty": "specialty",
    "Location": "location",
    "Overview": "overview",
    "Profile URL": "profile_url"
}, inplace=True)

print("✅ Column names standardized!")


# In[7]:


# Concatenate both datasets
merged_df = pd.concat([medicare_df, placidway_df], ignore_index=True)

print(f"✅ Merged dataset: {merged_df.shape[0]} rows")


# In[8]:


# Convert doctor names to lowercase for consistency
merged_df["doctor_name"] = merged_df["doctor_name"].str.lower().str.strip()

# Remove exact duplicates
merged_df.drop_duplicates(subset=["doctor_name", "location", "specialty"], keep="first", inplace=True)

print(f"✅ After duplicate removal: {merged_df.shape[0]} rows")


# In[9]:


# Group by doctor name and aggregate specialties
merged_df = merged_df.groupby(["doctor_name", "location"]).agg({
    "specialty": lambda x: ", ".join(set(x.dropna())),  # Merge unique specialties
    "overview": lambda x: " | ".join(set(x.dropna())),  # Merge unique overviews
    "profile_url": "first"  # Keep one profile link
}).reset_index()

print(f"✅ After merging specialties: {merged_df.shape[0]} unique doctor-location pairs")


# In[10]:


# Fill missing values
merged_df.fillna("N/A", inplace=True)

# Remove doctors with no name
merged_df = merged_df[merged_df["doctor_name"] != "N/A"]

print(f"✅ After cleaning missing values: {merged_df.shape[0]} doctors")


# In[11]:


merged_df.to_csv("cleaned_doctor_data.csv", index=False)
print("✅ Final cleaned dataset saved as 'cleaned_doctor_data.csv'")


# In[ ]:




