import pandas as pd  

# Load the dataset
df = pd.read_excel(r"ImmediCure-Task\data\scraped_placidway_data (1).xlsx")

# Display basic info
print(df.info())
print(df.head())

# Remove exact duplicate rows based on name and specialties
df.drop_duplicates(subset=["name", "specialties"], keep="first", inplace=True)

print(f"After removing duplicates: {df.shape}")

# Convert specialties column to lowercase for consistency
df["specialties"] = df["specialties"].str.lower().str.strip()

# Extract unique specialties
all_specialties = set()
for specialties in df["specialties"].dropna():
    for specialty in specialties.split(","):  # Split multi-specialty doctors
        all_specialties.add(specialty.strip())

print("Extracted Specialties:", all_specialties)

# Fill missing overviews with a placeholder
df["overview"].fillna("Information not available.", inplace=True)

# Fill missing locations with "Unknown"
df["location"].fillna("Unknown", inplace=True)

print("Missing values handled!")

# Standardize location format (capitalize + strip spaces)
df["location"] = df["location"].str.title().str.strip()

print(df["location"].unique())

# Save cleaned dataset
df.to_csv("cleaned_placidway_doctors.csv", index=False)

print(" Data Cleaning Completed! Cleaned file saved.")
