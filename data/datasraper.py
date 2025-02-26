#!/usr/bin/env python
# coding: utf-8

# In[8]:


import requests
import csv
import time
import random

# API URL for Medicare provider data
api_url = "https://data.cms.gov/provider-data/api/1/datastore/query/mj5m-pzi6/0"

# List of specialties to fetch (Add more if needed)
specialties = ["Family Practice", "Cardiology", "Neurology", "Dermatology", "Pediatrics", "Orthopedic Surgery"]

# Function to scrape ALL Medicare doctors
def scrape_all_medicare_doctors(specialties=specialties, num_results_per_request=1000, max_doctors=50000):
    all_doctors = []
    headers = {
        'User-Agent': 'Mozilla/5.0',
        'Accept': 'application/json',
        'Content-Type': 'application/json'
    }

    for specialty in specialties:
        offset = 0  # Start from the first record
        specialty_count = 0  # Track doctors per specialty
        
        while True:
            params = {
                "filter[pri_spec]": specialty,
                "limit": num_results_per_request,  # Fetch max allowed per request
                "offset": offset,
                "sort[npi]": "ASC"
            }

            try:
                print(f"🔍 Fetching {num_results_per_request} {specialty} doctors (Offset: {offset})...")
                time.sleep(random.uniform(2, 3))  # Slow down requests to prevent rate limiting

                response = requests.get(api_url, headers=headers, params=params)
                response.raise_for_status()
                data = response.json()

                if "results" in data and data["results"]:
                    doctors = data["results"]
                    
                    for doctor in doctors:
                        try:
                            # ✅ Fixed Name Extraction
                            name = f"{doctor.get('provider_first_name', '')} {doctor.get('provider_middle_name', '')} {doctor.get('provider_last_name', '')}".strip()

                            address = f"{doctor.get('adr_ln_1', '')}, {doctor.get('city', '')}, {doctor.get('state', '')} {doctor.get('zip', '')}"
                            specialty = doctor.get('pri_spec', 'N/A')

                            npi = doctor.get('npi', '')
                            profile_link = f"https://www.medicare.gov/care-compare/details/clinicians/{npi}" if npi else "N/A"

                            overview = f"Gender: {doctor.get('gndr', 'N/A')}, Credentials: {doctor.get('cred', 'N/A')}"

                            doctor_info = {
                                'name': name,
                                'location': address,
                                'specialty': specialty,
                                'overview': overview,
                                'profile_link': profile_link
                            }

                            all_doctors.append(doctor_info)
                            specialty_count += 1
                            print(f"✅ Found: {name} ({specialty})")

                            if len(all_doctors) >= max_doctors:
                                print("✅ Reached max doctor limit. Stopping...")
                                return all_doctors

                        except Exception as e:
                            print(f"⚠️ Error processing doctor data: {e}")
                            continue

                    # Move to next set of results
                    offset += num_results_per_request
                else:
                    print(f"✅ No more {specialty} doctors found. Moving to next specialty...")
                    break  # Stop if no more data

            except Exception as e:
                print(f"❌ Error fetching data: {e}")
                break  # Stop on error

        print(f"✅ Total {specialty_count} {specialty} doctors extracted.")

    return all_doctors

# Save data to CSV
def save_to_csv(doctors, filename="all_medicare_doctors.csv"):
    if not doctors:
        print("⚠️ No doctor data to save")
        return

    fieldnames = doctors[0].keys()

    with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(doctors)

    print(f"📂 Successfully saved {len(doctors)} doctors to {filename}")

# Run the scraper for ALL doctors
doctors = scrape_all_medicare_doctors(max_doctors=50000)  # Adjust max limit as needed

# Save results to CSV
if doctors:
    save_to_csv(doctors)
else:
    print("❌ No doctors were scraped.")


# In[ ]:




