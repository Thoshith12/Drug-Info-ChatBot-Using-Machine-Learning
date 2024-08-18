from flask import *
import requests

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('loginpage.html')

@app.route('/login')
def login():
    email=request.args.get('email')
    password=request.args.get('password')
    print('creds', email, password)
    f=open('auth.txt', 'r')
    users=f.readlines()
    for u in users:
        vs=u.split(',')
        if vs[2].strip()==email and vs[1]==password:
            f.close()
            return render_template('index.html')
            break 
    return render_template('loginpage.html', msg='invalid uid or pwd')

@app.route('/register')
def register():
    username=request.args.get('username')
    password=request.args.get('password')
    email=request.args.get('email')
    f=open('auth.txt', 'wt')
    f.write(username+','+password+','+email+'\n')
    f.close()
    return render_template('loginpage.html')

@app.route('/aboutus')
def aboutus():
    return render_template('aboutus.html')

def getresults(drug_name,drug_type):
    print('get results ', drug_name, drug_type )
    if drug_type=="drug_info":
        data = get_fda_data2(drug_name, "1")
        #print(data)
        drug_info = []
        for result in data['results']:
            for drug in result['patient']['drug']:
                #print('drug -',drug.get('brand_name'))
                if drug.get('openfda')!=None:
                    if drug.get('openfda')!='N/A':
                        medicinal_product = drug.get('medicinalproduct') or 'N/A'
                        brand_name = drug.get('openfda', {}).get('brand_name', ['N/A'])[0]
                        generic_name = drug.get('openfda', {}).get('generic_name', ['N/A'])[0]
                        manufacturer = drug.get('openfda', {}).get('manufacturer_name', ['N/A'])[0]
                        # drug_info.append( {
                        #     'medicinal_product': medicinal_product,
                        #     'brand_name': brand_name,
                        #     'generic_name': generic_name,
                        #     'manufacturer': manufacturer
                        # })
                        drug_info.append( (
                            # 'Drug info about '+drug_name +' : ',
                            'Medicinal Product: '+medicinal_product,
                            'Brand Name: '+brand_name,
                            'Generic Name: '+generic_name,
                            'Manufacturer: '+ manufacturer
                        ))
                        print(medicinal_product, brand_name, generic_name, manufacturer,'-')
                        break
        
        return drug_info
    if drug_type=="drug_reactions":
        print('...',drug_name, "2")
        data = get_fda_data(drug_name, "2")
        print(data)
        drug_reactions = []
        for result in data['results']:
            print(result)
            drug_reactions.append((result['term']+', People effected are: '+str(result['count'])))
            #for reaction in result['patient']['reaction']:
            #    drug_reactions.append(reaction['reactionmeddrapt'])                
        # return drug_reactions
        if len(drug_reactions) < 10:
            return drug_reactions # interactions 
        else:
            return drug_reactions[:10]
    
    if drug_type=="drug_interactions":
        
        drug_interactions=[]
        try:
            drug_interactions = get_drug_drug_interactions(drug_name)
        except Exception as exp:
            print('json parse issue 2'+str(exp))
        return (drug_name, drug_interactions)        
        #return render_template('results3.html', drug_interactions=drug_interactions)
    
    if drug_type=="drug_absorbability":
        
        drug_absorbability=[]
        try:
            drug_absorbability = get_drug_drug_abso(drug_name)
        except Exception as exp:
            print('json parse issue 2'+str(exp))
        return (drug_name, drug_absorbability)   
    
    if drug_type=="drug_toxicity":
        
        drug_toxicity=[]
        try:
            drug_toxicity = get_drug_drug_toxi(drug_name)
        except Exception as exp:
            print('json parse issue 2'+str(exp))
        if len(drug_toxicity) == 0:
            return 'Not Found' # interactions 
        else:
            return (drug_toxicity)
          
          
    
    if drug_type=="drug_protein_binding":
        
        drug_protein_binding=[]
        try:
            drug_protein_binding = get_drug_drug_protein(drug_name)
        except Exception as exp:
            print('json parse issue 2'+str(exp))
        return (drug_name, drug_protein_binding)  

    if drug_type=="drug_food_interaction":
        
        drug_food_interaction=[]
        try:
            drug_food_interaction = get_drug_drug_food(drug_name)
        except Exception as exp:
            print('json parse issue 2'+str(exp))
        return drug_food_interaction
     
    if drug_type=="drug_prescriptions":
        data = get_fda_data(drug_name, "4")
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
        return prescription_types
    
    if drug_type=="drug_info_all_available_data":
        data = get_fda_data(drug_name, "5")
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
        return (drug_info, reactions, adverse_events)


@app.route('/results', methods=['POST'])
def results():
    drug_name = request.form['drug_name']
    drug_type = request.form['drug_type']
    data=''
    print("inputs ..", drug_name, drug_type)
    print('drug data', drug_name, drug_type)
    if drug_type=="1":
        data = get_fda_data(drug_name, drug_type)
        #print("---data---",data)
        drug_info = []
        for result in data['results']:
            for drug in result['patient']['drug']:
                medicinal_product = drug.get('medicinalproduct') or 'N/A'
                brand_name = drug.get('openfda', {}).get('brand_name', ['N/A'])[0]
                if brand_name=='N/A':
                    continue 
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
        #try:
        drug_interactions = get_drug_drug_interactions(drug_name)
        #except Exception as exp:
        #print('json parse issue 3'+str(exp))
        return render_template('results3.html', drug_name=drug_name, drug_interactions=drug_interactions)        
        #return render_template('results3.html', drug_interactions=drug_interactions)
    
    if drug_type=="6":
        drug_name = request.form['drug_name']
        drug_interactions=[]
        try:
            drug_interactions = get_drug_drug_toxi(drug_name)
        except Exception as exp:
            print('json parse issue 5'+str(exp))
        return render_template('results3tox.html', drug_name=drug_name, drug_interactions=drug_interactions)     
    
    if drug_type=="7":
        drug_name = request.form['drug_name']
        drug_interactions=[]
        try:
            drug_interactions = get_drug_drug_abso(drug_name)
        except Exception as exp:
            print('json parse issue 5'+str(exp))
        return render_template('results3abs.html', drug_name=drug_name, drug_interactions=drug_interactions)     

    if drug_type=="8":
        drug_name = request.form['drug_name']
        drug_interactions=[]
        try:
            drug_interactions = get_drug_drug_food(drug_name)
        except Exception as exp:
            print('json parse issue6'+str(exp))
        return render_template('results3foo.html', drug_name=drug_name, drug_interactions=drug_interactions)     


    if drug_type=="9":
        drug_name = request.form['drug_name']
        drug_interactions=[]
        try:
            drug_interactions = get_drug_drug_protein(drug_name)
        except Exception as exp:
            print('json parse issue 1'+str(exp))
        return render_template('results3pro.html', drug_name=drug_name, drug_interactions=drug_interactions)     


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
    print('drug--',drug_type)
    if drug_type=="1":
        url = 'https://api.fda.gov/drug/event.json?api_key='+api_key+'&search='+drug_name
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
    print('url', url)
    response = requests.get(url)
    data = response.json()
    return data



def get_fda_data2(drug_name, drug_type):
    api_key = 'i5wDk5lmIz9w550MS4naUMmpBfPsnV2lEppwUpXg'
    print("dtype..",drug_type)
    if drug_type=='1': #"drug_info":
        print('..in....')
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
    print('url...', url)
    response = requests.get(url)
    data = response.json()
    print(data)
    print("data received")
    return data



import json 
def get_drug_drug_interactions(drug_name):
    # interactions = []
    # with open('drugbank.json', 'r', encoding='utf-8') as f:
    #     drugbank_data = json.load(f)
    #     for drug in drugbank_data['elements']['drugs']:
    #         if drug['name'] == drug_name:
    #             interactions.extend(drug.get('drug_interactions', []))
    #             break

            
    import json

    # Function to extract drug interaction IDs for a given drug name
    def extract_interaction_ids(drug_name, data):
        interaction_ids = []
        for drug in data:
            try:
                if drug['name'] == drug_name:
                    interaction_ids = drug.get('drug-interactions', '').split()
                    break
            except Exception as exp:
                pass 
        return interaction_ids

    # Function to get drug names for a list of interaction IDs
    def get_interaction_names(interaction_ids, data):
        interaction_names = []
        for interaction_id in interaction_ids:
            try:
                drug = next(drug for drug in data if drug.get('drugbank-id') == interaction_id)
                t=' '
                try: 
                    t=" => toxicity info: [ "+drug['toxicity']+" ] "
                except Exception as exp:
                    print()
                interaction_names.append(drug['name']) # +t)
            except StopIteration:
                interaction_names.append(f"No name found for ID {interaction_id}")
        return interaction_names


    # Drug name to search for
    #drug_name = "Lepirudin"
    global drugbank_data

    drugbank_data=''
    # Load data from drugbank.json
    with open("drugbank.json", "r", encoding="utf-8") as file:

        drugbank_data = json.load(file)

        
    # Extract interaction IDs
    interaction_ids = extract_interaction_ids(drug_name, drugbank_data)

    # Get interaction names
    interaction_names = get_interaction_names(interaction_ids, drugbank_data)

    # Print results
    print("Drug Interactions for", drug_name)
    for i, name in enumerate(interaction_names, start=1):
        print(f"{i}. {name}")
    if len(interaction_names) == 0:
            return 'Not Found' # interactions 
    else:
        if len(interaction_names) < 10:
            return interaction_names # interactions 
        else:
            return interaction_names[:10]

    





import json 
def get_drug_drug_toxi(drug_name):
    # interactions = []
    # with open('drugbank.json', 'r', encoding='utf-8') as f:
    #     drugbank_data = json.load(f)
    #     for drug in drugbank_data['elements']['drugs']:
    #         if drug['name'] == drug_name:
    #             interactions.extend(drug.get('drug_interactions', []))
    #             break

            
    import json

    # Function to extract drug interaction IDs for a given drug name
    def extract_toxic(drug_name, data):
        interaction_ids = []
        for drug in data:
            try:
                if drug['name'] == drug_name:
                    interaction_ids = drug.get('toxicity', '') #.split()
                    break
            except Exception as exp:
                pass 
        return interaction_ids



    # Drug name to search for
    #drug_name = "Lepirudin"
    global drugbank_data

    drugbank_data=''
    # Load data from drugbank.json
    with open("drugbank.json", "r", encoding="utf-8") as file:

        drugbank_data = json.load(file)

        
    # Extract interaction IDs
    interaction_ids = extract_toxic(drug_name, drugbank_data)

    # Get interaction names
    #interaction_names = get_interaction_names(interaction_ids, drugbank_data)

    # Print results
    print("Drug Interactions for", drug_name)
    for i, name in enumerate(interaction_ids, start=1):
        print(f"{i}. {name}")



    return interaction_ids # interactions


import json 
def get_drug_drug_food(drug_name):
    # interactions = []
    # with open('drugbank.json', 'r', encoding='utf-8') as f:
    #     drugbank_data = json.load(f)
    #     for drug in drugbank_data['elements']['drugs']:
    #         if drug['name'] == drug_name:
    #             interactions.extend(drug.get('drug_interactions', []))
    #             break

            
    import json

    # Function to extract drug interaction IDs for a given drug name
    def extract_food(drug_name, data):
        interaction_ids = []
        for drug in data:
            try:
                if drug['name'] == drug_name:
                    interaction_ids = drug.get('food-interactions', '')#.split()
                    break
            except Exception as exp:
                pass
        return interaction_ids


    # Drug name to search for
    #drug_name = "Lepirudin"
    global drugbank_data

    drugbank_data=''
    # Load data from drugbank.json
    with open("drugbank.json", "r", encoding="utf-8") as file:

        drugbank_data = json.load(file)

        
    # Extract interaction IDs
    interaction_ids = extract_food(drug_name, drugbank_data)

    # Get interaction names
    #interaction_names = get_interaction_names(interaction_ids, drugbank_data)

    # Print results
    print("Drug Interactions for", drug_name)
    for i, name in enumerate(interaction_ids, start=1):
        print(f"{i}. {name}")



    return interaction_ids # interactions





import json 
def get_drug_drug_protein(drug_name):
    # interactions = []
    # with open('drugbank.json', 'r', encoding='utf-8') as f:
    #     drugbank_data = json.load(f)
    #     for drug in drugbank_data['elements']['drugs']:
    #         if drug['name'] == drug_name:
    #             interactions.extend(drug.get('drug_interactions', []))
    #             break

            
    import json

    # Function to extract drug interaction IDs for a given drug name
    def extract_protein(drug_name, data):
        interaction_ids = []
        for drug in data:
            try:
                if drug['name'] == drug_name:
                    interaction_ids = drug.get('protein-binding', '') #.split()
                    break
            except Exception as exp:
                pass 
        if len(interaction_ids) == 0:
            return 'Not Found' # interactions 
        else:
            return (interaction_ids)


    # Drug name to search for
    #drug_name = "Lepirudin"
    global drugbank_data

    drugbank_data=''
    # Load data from drugbank.json
    with open("drugbank.json", "r", encoding="utf-8") as file:

        drugbank_data = json.load(file)

        
    # Extract interaction IDs
    interaction_ids = extract_protein(drug_name, drugbank_data)

    # Get interaction names
    #interaction_names = get_interaction_names(interaction_ids, drugbank_data)

    # Print results
    print("Drug Interactions for", drug_name)
    for i, name in enumerate(interaction_ids, start=1):
        print(f"{i}. {name}")



    return interaction_ids # interactions







import json 
def get_drug_drug_abso(drug_name):
    # interactions = []
    # with open('drugbank.json', 'r', encoding='utf-8') as f:
    #     drugbank_data = json.load(f)
    #     for drug in drugbank_data['elements']['drugs']:
    #         if drug['name'] == drug_name:
    #             interactions.extend(drug.get('drug_interactions', []))
    #             break

            
    import json

    # Function to extract drug interaction IDs for a given drug name
    def extract_abso(drug_name, data):
        interaction_ids = []
        for drug in data:
            try:
                if drug['name'] == drug_name:
                    interaction_ids = drug.get('absorption', '')#.split()
                    break
            except Exception as exp:
                pass 
        if len(interaction_ids) == 0:
            return 'Not Found' # interactions 
        else:
            return (interaction_ids)

    # Function to get drug names for a list of interaction IDs
    def get_interaction_names(interaction_ids, data):
        interaction_names = []
        for interaction_id in interaction_ids:
            try:
                drug = next(drug for drug in data if drug.get('drugbank-id') == interaction_id)
                t=' '
                try: 
                    t=" => toxicity info: [ "+drug['toxicity']+" ] "
                except Exception as exp:
                    print()
                interaction_names.append(drug['name']) # +t)
            except StopIteration:
                interaction_names.append(f"No name found for ID {interaction_id}")
        return interaction_names


    # Drug name to search for
    #drug_name = "Lepirudin"
    global drugbank_data

    drugbank_data=''
    # Load data from drugbank.json
    with open("drugbank.json", "r", encoding="utf-8") as file:

        drugbank_data = json.load(file)

        
    # Extract interaction IDs
    interaction_ids = extract_abso(drug_name, drugbank_data)

    # Get interaction names
    #interaction_names = get_interaction_names(interaction_ids, drugbank_data)

    # Print results
    print("Drug Interactions for", drug_name)
    for i, name in enumerate(interaction_ids, start=1):
        print(f"{i}. {name}")



    return interaction_ids # interactions


@app.route('/about')
def about():
    return render_template('about.html')


#chat


import re

@app.route('/rasa', methods=['POST'])
def rasa():
    data = request.get_json()
    message = data['message']
    # rasa has problems
    fword = message.split()[0]
    lword = message.split()[-1]
    #result=getresults(lword, fword)
    # print('input msg is ',message)
    rasa_url = 'http://localhost:5005/model/parse'  # Replace with your Rasa server URL
    payload = {'text': message}
    response = requests.post(rasa_url, json=payload)
    print('response ', response)
    rasa_data = response.json()
    print('response data ', rasa_data)
    intent = rasa_data.get('intent', {}).get('name')
    entities = rasa_data.get('entities', [])
    print('enti',entities)
    #intent_ranking = rasa_data.get('intent_ranking', [])
    print('from rasa parsing,....................')
    print( 'intent:', intent)
    result=''
    #try:
        #print( 'entities:', entities[0]['value']) 
    result=getresults(lword, intent)
    #except Exception as exp:
    #    print('exp 1 ', exp)
    #    pass 
    # #print( 'intent_ranking:', intent_ranking)
    # #return jsonify({'message':'intent '+intent+' entity '+entities[0]['value']})
    print(result)
    return jsonify({'message':result, 'intent':intent, 'entity':lword})    



@app.route('/chat')
def chat():
    return render_template('chat.html')

if __name__ == '__main__':
    app.run(debug=True)
