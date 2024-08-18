from flask import *
import requests

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

def getresults(drug_name,drug_type):
    if drug_type=="1":
        data = get_fda_data(drug_name, drug_type)
        print(data)
        drug_info = []
        for result in data['results']:
            for drug in result['patient']['drug']:
                medicinal_product = drug.get('medicinalproduct') or 'N/A'
                brand_name = drug.get('openfda', {}).get('brand_name', ['N/A'])[0]
                generic_name = drug.get('openfda', {}).get('generic_name', ['N/A'])[0]
                manufacturer = drug.get('openfda', {}).get('manufacturer_name', ['N/A'])[0]
                drug_info.append({
                    'medicinal_product': medicinal_product,
                    'brand_name': brand_name,
                    'generic_name': generic_name,
                    'manufacturer': manufacturer
                })
        
        return render_template('results.html', drug_info=drug_info)
    if drug_type=="2":
        data = get_fda_data(drug_name, drug_type)
        print(data)
        drug_reactions = []
        for result in data['results']:
            print(result)
            drug_reactions.append((result['term'], result['count']))
            #for reaction in result['patient']['reaction']:
            #    drug_reactions.append(reaction['reactionmeddrapt'])                
        return render_template('results2.html', drug_reactions={"drug_reactions":drug_reactions})
    if drug_type=="3":
        drug_name = request.form['drug_name']
        drug_interactions=[]
        try:
            drug_interactions = get_drug_drug_interactions(drug_name)
        except Exception as exp:
            print('json parse issue')
        return render_template('results3.html', drug_name=drug_name, drug_interactions=drug_interactions)        
        #return render_template('results3.html', drug_interactions=drug_interactions)
    if drug_type=="4":
        data = get_fda_data(drug_name, drug_type)
         # Extract prescription type from the API response
        print("prescription types...", data)
        prescription_types = []
        try:
            for result in data['results']:
                drug = result['term']
                prescription_types.append(drug)
                #break
        except Exception as exp:
            pass 
        return render_template('results4.html', prescription_types=prescription_types)
    
    if drug_type=="5":
        data = get_fda_data(drug_name, drug_type)
        # Extract all relevant information from the API response
        drug_info = []
        reactions = []
        adverse_events = []
        for result in data['results']:
            for drug in result['patient']['drug']:
                medicinal_product = drug.get('medicinalproduct') or 'N/A'
                brand_name = drug.get('openfda', {}).get('brand_name', ['N/A'])[0]
                generic_name = drug.get('openfda', {}).get('generic_name', ['N/A'])[0]
                manufacturer = drug.get('openfda', {}).get('manufacturer_name', ['N/A'])[0]
                route_of_administration = drug.get('openfda', {}).get('route', ['N/A'])[0]
                dosage_form = drug.get('openfda', {}).get('dosage_form', ['N/A'])[0]
                drug_info.append({
                    'medicinal_product': medicinal_product,
                    'brand_name': brand_name,
                    'generic_name': generic_name,
                    'manufacturer': manufacturer,
                    'route_of_administration': route_of_administration,
                    'dosage_form': dosage_form
                })
            for reaction in result['patient']['reaction']:
                reactions.append(reaction['reactionmeddrapt'])
            for event in result['patient']['reaction']:
                adverse_events.append(event['reactionmeddrapt'])


@app.route('/results', methods=['POST'])
def results():
    drug_name = request.form['drug_name']
    drug_type = request.form['drug_type']
    data=''
    print('drug data', drug_name, drug_type)
    if drug_type=="1":
        data = get_fda_data(drug_name, drug_type)
        print(data)
        drug_info = []
        for result in data['results']:
            for drug in result['patient']['drug']:
                medicinal_product = drug.get('medicinalproduct') or 'N/A'
                brand_name = drug.get('openfda', {}).get('brand_name', ['N/A'])[0]
                generic_name = drug.get('openfda', {}).get('generic_name', ['N/A'])[0]
                manufacturer = drug.get('openfda', {}).get('manufacturer_name', ['N/A'])[0]
                drug_info.append({
                    'medicinal_product': medicinal_product,
                    'brand_name': brand_name,
                    'generic_name': generic_name,
                    'manufacturer': manufacturer
                })
        
        return render_template('results.html', drug_info=drug_info)
    if drug_type=="2":
        data = get_fda_data(drug_name, drug_type)
        print(data)
        drug_reactions = []
        for result in data['results']:
            print(result)
            drug_reactions.append((result['term'], result['count']))
            #for reaction in result['patient']['reaction']:
            #    drug_reactions.append(reaction['reactionmeddrapt'])                
        return render_template('results2.html', drug_reactions={"drug_reactions":drug_reactions})
    if drug_type=="3":
        drug_name = request.form['drug_name']
        drug_interactions=[]
        try:
            drug_interactions = get_drug_drug_interactions(drug_name)
        except Exception as exp:
            print('json parse issue')
        return render_template('results3.html', drug_name=drug_name, drug_interactions=drug_interactions)        
        #return render_template('results3.html', drug_interactions=drug_interactions)
    if drug_type=="4":
        data = get_fda_data(drug_name, drug_type)
         # Extract prescription type from the API response
        print("prescription types...", data)
        prescription_types = []
        try:
            for result in data['results']:
                drug = result['term']
                prescription_types.append(drug)
                #break
        except Exception as exp:
            pass 
        return render_template('results4.html', prescription_types=prescription_types)
    
    if drug_type=="5":
        data = get_fda_data(drug_name, drug_type)
        # Extract all relevant information from the API response
        drug_info = []
        reactions = []
        adverse_events = []
        for result in data['results']:
            for drug in result['patient']['drug']:
                medicinal_product = drug.get('medicinalproduct') or 'N/A'
                brand_name = drug.get('openfda', {}).get('brand_name', ['N/A'])[0]
                generic_name = drug.get('openfda', {}).get('generic_name', ['N/A'])[0]
                manufacturer = drug.get('openfda', {}).get('manufacturer_name', ['N/A'])[0]
                route_of_administration = drug.get('openfda', {}).get('route', ['N/A'])[0]
                dosage_form = drug.get('openfda', {}).get('dosage_form', ['N/A'])[0]
                drug_info.append({
                    'medicinal_product': medicinal_product,
                    'brand_name': brand_name,
                    'generic_name': generic_name,
                    'manufacturer': manufacturer,
                    'route_of_administration': route_of_administration,
                    'dosage_form': dosage_form
                })
            for reaction in result['patient']['reaction']:
                reactions.append(reaction['reactionmeddrapt'])
            for event in result['patient']['reaction']:
                adverse_events.append(event['reactionmeddrapt'])
    
    return render_template('results5.html', drug_info=drug_info, reactions=reactions, adverse_events=adverse_events)

    return data
def get_fda_data(drug_name, drug_type):
    api_key = 'i5wDk5lmIz9w550MS4naUMmpBfPsnV2lEppwUpXg'
    print(drug_type)
    if drug_type=="1":
        url = f'https://api.fda.gov/drug/event.json?search={drug_name}&api_key={api_key}'
    if drug_type=="2":
        #       https://api.fda.gov/drug/event.json?api_key=" + apiKey + "&search=" + drug.value + "&count=patient.reaction.reactionmeddrapt.exact
        #url = f'https://api.fda.gov/drug/event.json?search=patient.reaction.reactionmeddrapt.exact:{drug_name}&api_key={api_key}' 
        url= "https://api.fda.gov/drug/event.json?api_key=" + api_key + "&search=" + drug_name + "&count=patient.reaction.reactionmeddrapt.exact"

        print('url',url)
    if drug_type=="3":
        url = f'https://api.fda.gov/drug/event.json?search=patient.drug.medicinalproduct:{drug_name}&api_key={api_key}'
    if drug_type=="4":
        #       https://api.fda.gov/drug/label.json?search=" + drug.value + "&count=openfda.product_type.exact"
        #url:  "https://api.fda.gov/drug/label.json?search=" + drug.value + "&count=openfda.product_type.exact",
        url = f'https://api.fda.gov/drug/label.json?count=openfda.product_type.exact&search={drug_name}&api_key={api_key}'
    if drug_type=="5":
        url = f'https://api.fda.gov/drug/event.json?search=patient.drug.medicinalproduct:{drug_name}&api_key={api_key}'
    response = requests.get(url)
    data = response.json()
    return data

import json 
def get_drug_drug_interactions(drug_name):
    interactions = []
    with open('drugbank.json', 'r', encoding='utf-8') as f:
        drugbank_data = json.load(f)
        for drug in drugbank_data['elements']['drugs']:
            if drug['name'] == drug_name:
                interactions.extend(drug.get('drug_interactions', []))
                break
    return interactions

@app.route('/about')
def about():
    return render_template('about.html')


#chat

# import re

# def generate_response(message):
#     # Define regex patterns to match intents and extract drug names
#     drug_name_pattern = r'drug name is (\w+)'
#     drug_info_patterns = {
#         'Drug Info': r'(information|info) about (\w+)',
#         'Drug Reactions': r'side(-|\s)?effects of (\w+)',
#         'Drug-Drug Interactions': r'drug(-|\s)?interactions of (\w+)',
#         'Prescription-Type': r'prescription(-|\s)?type of (\w+)',
#         'All available data': r'all (information|data) about (\w+)'
#     }
#     drug_name=''
#     sub_intent=''
#     # Search for drug name
#     drug_name_match = re.search(drug_name_pattern, message, re.IGNORECASE)
#     if drug_name_match:
#         drug_name = drug_name_match.group(1)
#         #return f"Drug name identified: {drug_name}"

#     # Search for drug info intents
#     for intent, pattern in drug_info_patterns.items():
#         match = re.search(pattern, message, re.IGNORECASE)
#         if match:
#             drug_name = match.group(2)
#             sub_intent = intent
#             return f"Intent identified: {sub_intent} for drug {drug_name}"

#     # If no matching intent is found
#     return drug_name, sub_intent


import re


def identifydrug(message):
    drug_name_pattern = r'drug name is (\w+)'
    drug_name=''
    

    drug_name_match = re.search(drug_name_pattern, message, re.IGNORECASE)
    if drug_name_match:
        drug_name = drug_name_match.group(1)
        #return f"Drug name identified: {drug_name}"

    return drug_name

def identifydrugtype(message):
    drug_info_patterns = {
        'Drug Info': r'\b(?:{})(?:s)?\b'.format('|'.join(['drug', 'information', 'info'])),
        'Drug Reactions': r'\b(?:{})(?:s)?\b'.format('|'.join(['side-effects', 'reactions', 'adverse'])),
        'Drug-Drug Interactions': r'\b(?:{})(?:s)?\b'.format('|'.join(['interactions', 'combine'])),
        'Prescription-Type': r'\b(?:{})(?:s)?\b'.format('|'.join(['prescription', 'type', 'medication'])),
        'All available data': r'\b(?:{})(?:s)?\b'.format('|'.join(['all', 'available', 'data']))
    }
    sub_intent=''
    return ""

def generate_response(message):
    drug_name_pattern = r'drug name is (\w+)'
    drug_info_patterns = {
        'Drug Info': r'\b(?:{})(?:s)?\b'.format('|'.join(['drug', 'information', 'info'])),
        'Drug Reactions': r'\b(?:{})(?:s)?\b'.format('|'.join(['side-effects', 'reactions', 'adverse'])),
        'Drug-Drug Interactions': r'\b(?:{})(?:s)?\b'.format('|'.join(['interactions', 'combine'])),
        'Prescription-Type': r'\b(?:{})(?:s)?\b'.format('|'.join(['prescription', 'type', 'medication'])),
        'All available data': r'\b(?:{})(?:s)?\b'.format('|'.join(['all', 'available', 'data']))
    }

    drug_name=''
    sub_intent=''

    drug_name_match = re.search(drug_name_pattern, message, re.IGNORECASE)
    if drug_name_match:
        drug_name = drug_name_match.group(1)
        return f"Drug name identified: {drug_name}"

    for intent, pattern in drug_info_patterns.items():
        match = re.search(pattern, message, re.IGNORECASE)
        if match:
            drug_name = re.sub(pattern, '', message, flags=re.IGNORECASE).strip()
            sub_intent = intent
            return f"Intent identified: {sub_intent} for drug {drug_name}"

    return drug_name, sub_intent



# Define keywords for each intent
intents = {
    'Drug Info': ['drug', 'information', 'info'],
    'Drug Reactions': ['side-effects', 'reactions', 'adverse'],
    'Drug-Drug Interactions': ['interactions', 'combine'],
    'Prescription-Type': ['prescription', 'type', 'medication'],
    'All available data': ['all', 'available', 'data']
}

# Function to identify intent from message
def identify_intent(message):
    message = message.lower()
    for intent, keywords in intents.items():
        for keyword in keywords:
            if keyword in message:
                return intent
    return "Intent not recognized"



@app.route('/chat')
def chat():
    return render_template('chat.html')

@app.route('/message', methods=['POST'])
def message():
    data = request.get_json()
    message = data['message']
    # Implement your logic to generate a response based on the message received
    # Example usage
    user_message = message # "What are the side-effects of ibuprofen?"
    intent = identify_intent(user_message)
    print("Intent:", intent)

    response = generate_response(message)
    return jsonify({'message': response})

def generate_response(message):
    # Implement your logic to generate a response
    return "You said: " + message

if __name__ == '__main__':
    app.run(debug=True)
