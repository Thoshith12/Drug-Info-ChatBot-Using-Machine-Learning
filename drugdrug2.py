import json

# Function to extract drug interaction IDs for a given drug name
def extract_interaction_ids(drug_name, data):
    interaction_ids = []
    for drug in data:
        if drug['name'] == drug_name:
            interaction_ids = drug.get('drug-interactions', '').split()
            break
    return interaction_ids

# Function to get drug names for a list of interaction IDs
def get_interaction_names(interaction_ids, data):
    interaction_names = []
    for interaction_id in interaction_ids:
        try:
            drug = next(drug for drug in data if drug.get('drugbank-id') == interaction_id)
            interaction_names.append(drug['name'])
        except StopIteration:
            interaction_names.append(f"No name found for ID {interaction_id}")
    return interaction_names

# Load data from drugbank.json
with open("drugbank.json", "r", encoding="utf-8") as file:
    drugbank_data = json.load(file)

# Drug name to search for
drug_name = "Lepirudin"

# Extract interaction IDs
interaction_ids = extract_interaction_ids(drug_name, drugbank_data)

# Get interaction names
interaction_names = get_interaction_names(interaction_ids, drugbank_data)

# Print results
print("Drug Interactions for", drug_name)
for i, name in enumerate(interaction_names, start=1):
    print(f"{i}. {name}")
