import pandas as pd  

df = pd.read_excel(r"ImmediCure-Task\data\scraped_placidway_data (1).xlsx")  

df.drop_duplicates(subset=["name", "specialties"], inplace=True)  

unique_specialties = df["specialties"].explode().unique()  

df.to_csv("cleaned_placidway_doctors.csv", index=False)  
print("Data Cleaned!")
