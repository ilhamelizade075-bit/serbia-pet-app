from flask import Flask, render_template, jsonify, request

app = Flask(__name__)

# Serbiyanın əsas şəhərlərinin siyahısı (server tərəfdən yoxlama üçün)
SERBIAN_CITIES = [
    "Beograd", "Novi Sad", "Niš", "Kragujevac", "Subotica", 
    "Zrenjanin", "Pančevo", "Čačak", "Kruševac", "Kraljevo", 
    "Smederevo", "Leskovac", "Valjevo", "Kopar", "Vranje", 
    "Šabac", "Užice", "Novi Pazar", "Sombor", "Požarevac", 
    "Pirot", "Zaječar", "Kikinda", "Sremska Mitrovica", "Jagodina", "Vrbas"
]

# Serbiyada ev heyvanlarının sığınacağı və övladlığa götürülmə bazası
PETS_DATA = [
    {
        "id": 1, 
        "name": "Luna", 
        "type": "Mačka", 
        "breed": "Britanska kratkodlaka", 
        "city": "Beograd", 
        "age": "1 godina", 
        "gender": "Ženski", 
        "owner": "Azil Beograd",
        "phone": "+381 60 123 4567",
        "description": "Veoma mirna, umiljata i naviknuta na kućne uslove.", 
        "image": "https://images.unsplash.com/photo-1514888286974-6c03e2ca1dba?auto=format&fit=crop&w=500&q=60"
    },
    {
        "id": 2, 
        "name": "Bobi", 
        "type": "Pas", 
        "breed": "Zlatni retriver", 
        "city": "Novi Sad", 
        "age": "2 godine", 
        "gender": "Muški", 
        "owner": "Udruženje Šapice",
        "phone": "+381 63 987 6543",
        "description": "Energičan, voli decu i obožava igru u parku.", 
        "image": "https://images.unsplash.com/photo-1552053831-71594a27632d?auto=format&fit=crop&w=500&q=60"
    },
    {
        "id": 3, 
        "name": "Mila", 
        "type": "Mačka", 
        "breed": "Mešanac", 
        "city": "Niš", 
        "age": "6 meseci", 
        "gender": "Ženski", 
        "owner": "Marija Petrović",
        "phone": "+381 64 555 4433",
        "description": "Razigrano mače, očišćeno od parazita i vakcinisano.", 
        "image": "https://images.unsplash.com/photo-1573865526739-10659fec78a5?auto=format&fit=crop&w=500&q=60"
    },
    {
        "id": 4, 
        "name": "Rex", 
        "type": "Pas", 
        "breed": "Nemački ovčar", 
        "city": "Subotica", 
        "age": "3 godine", 
        "gender": "Muški", 
        "owner": "Nikola Ilić",
        "phone": "+381 61 777 8899",
        "description": "Pametan, poslušan i odličan pas čuvar za dvorište.", 
        "image": "https://images.unsplash.com/photo-1589941013453-ec89f33b5e95?auto=format&fit=crop&w=500&q=60"
    }
]

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/api/pets', methods=['GET'])
def get_pets():
    pet_type = request.args.get('type')
    city = request.args.get('city')
    
    filtered = PETS_DATA
    if pet_type and pet_type != 'All':
        filtered = [p for p in filtered if p['type'].lower() == pet_type.lower()]
    if city and city != 'All':
        filtered = [p for p in filtered if p['city'].lower() == city.lower()]
        
    return jsonify(filtered)

@app.route('/api/pets', methods=['POST'])
def add_pet():
    data = request.json
    new_pet = {
        "id": len(PETS_DATA) + 1,
        "name": data.get("name", "Bez imena"),
        "type": data.get("type", "Pas"),
        "breed": data.get("breed", "Mešanac"),
        "city": data.get("city", "Beograd"),
        "age": data.get("age", "1 godina"),
        "gender": data.get("gender", "Nepoznato"),
        "owner": data.get("owner", "Građanin"),
        "phone": data.get("phone", "+381 60 000 0000"),
        "description": data.get("description", "Nema dodatnog opisa."),
        "image": "https://images.unsplash.com/photo-1543466835-00a7907e9de1?auto=format&fit=crop&w=500&q=60"
    }
    PETS_DATA.append(new_pet)
    return jsonify({"success": True, "pet": new_pet})

if __name__ == '__main__':
    app.run(debug=True, port=5000)