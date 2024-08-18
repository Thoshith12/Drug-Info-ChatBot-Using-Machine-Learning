import json
import requests

# Function to extract drug interaction IDs for a given drug name
def extract_interaction_ids(drug_name, data):
    interaction_ids = []
    for drug in data:
        if drug['name'] == drug_name:
            interaction_ids = drug['drug-interactions'].split()
            break
    return interaction_ids

# Function to get drug names for a list of interaction IDs
def get_interaction_names(interaction_ids):
    interaction_names = []
    for interaction_id in interaction_ids:
        url = f"https://pubchem.ncbi.nlm.nih.gov/rest/pug/compound/cid/{interaction_id}/synonyms/json"
        response = requests.get(url)
        if response.status_code == 200:
            interaction_data = response.json()
            names = interaction_data['InformationList']['Information'][0]['Synonym']
            interaction_names.append(names[0] if names else f"No name found for ID {interaction_id}")
            print(names)
        else:
            interaction_names.append(f"Error: Failed to fetch data for ID {interaction_id}")
    return interaction_names

with open("drugbank.json", "r", encoding="utf-8") as file:
    drugbank_data = json.load(file)


# Drug name to search for
drug_name = "Lepirudin"

# Extract interaction IDs
interaction_ids = extract_interaction_ids(drug_name, drugbank_data)

# Get interaction names
interaction_names = get_interaction_names(interaction_ids)

# Print results
print("Drug Interactions for", drug_name)
for i, name in enumerate(interaction_names, start=1):
    print(f"{i}. {name}")
