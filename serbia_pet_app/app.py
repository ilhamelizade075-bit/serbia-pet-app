from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

# Serb dilində ilkin elanlar siyahısı
pets_list = [
    {
        'id': 1,
        'name': 'Bella',
        'type': 'Mačka',
        'breed': 'Britanska kratkodlaka',
        'city': 'Beograd',
        'age': '1 godina',
        'phone': '+38160123456',
        'image': 'https://images.unsplash.com/photo-1514888286974-6c03e2ca1dba?auto=format&fit=crop&w=500&q=80'
    },
    {
        'id': 2,
        'name': 'Max',
        'type': 'Pas',
        'breed': 'Zlatni retriver',
        'city': 'Novi Sad',
        'age': '2 godine',
        'phone': '+38162987654',
        'image': 'https://images.unsplash.com/photo-1552053831-71594a27632d?auto=format&fit=crop&w=500&q=80'
    }
]

@app.route('/')
def index():
    return render_template('index.html', pets=pets_list)

# Yeni oglas əlavə etmə route-u
@app.route('/add', methods=['POST'])
def add_pet():
    new_id = len(pets_list) + 1
    name = request.form.get('name')
    pet_type = request.form.get('type')
    breed = request.form.get('breed')
    city = request.form.get('city')
    age = request.form.get('age')
    phone = request.form.get('phone')
    image = request.form.get('image')
    
    if not image:
        image = 'https://images.unsplash.com/photo-1543466835-00a7907e9de1?auto=format&fit=crop&w=500&q=80'

    new_pet = {
        'id': new_id,
        'name': name,
        'type': pet_type,
        'breed': breed,
        'city': city,
        'age': age,
        'phone': phone,
        'image': image
    }
    
    pets_list.append(new_pet)
    return redirect(url_for('index'))

# Oqlası silmə route-u
@app.route('/delete/<int:pet_id>', methods=['POST'])
def delete_pet(pet_id):
    global pets_list
    pets_list = [pet for pet in pets_list if pet['id'] != pet_id]
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
