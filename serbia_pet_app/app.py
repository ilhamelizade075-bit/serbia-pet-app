import os
from flask import Flask, render_template, request, redirect, url_for, session
from authlib.integrations.flask_client import OAuth
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.secret_key = 'SALAM'

# Şəkillərin yüklənəcəyi qovluq və icazə verilən uzantılar
UPLOAD_FOLDER = 'static/uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'webp'}

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Əgər uploads qovluğu yoxdursa, yaradırıq
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# Google OAuth tənzimləmələri
oauth = OAuth(app)
google = oauth.register(
    name='google',
    client_id='152148942306-s631n8mfff2lppno2t3g74ett93m8nrh.apps.googleusercontent.com',
    client_secret='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',
    server_metadata_url='https://accounts.google.com/.well-known/openid-configuration',
    client_kwargs={
        'scope': 'openid email profile'
    }
)

# İlkin olaraq elanlar siyahısı tamamilə BOŞdur
pets_list = []

@app.route('/')
def index():
    user = session.get('user')
    return render_template('index.html', pets=pets_list, user=user)

@app.route('/login')
def login():
    redirect_uri = url_for('authorize', _external=True)
    return google.authorize_redirect(redirect_uri)

@app.route('/authorize')
def authorize():
    token = google.authorize_access_token()
    user_info = token.get('userinfo')
    session['user'] = user_info['email']
    return redirect(url_for('index'))

@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect(url_for('index'))

@app.route('/add', methods=['POST'])
def add_pet():
    # İstəsəniz buraya giriş şərti də qoya bilərsiniz
    new_id = len(pets_list) + 1 if not pets_list else pets_list[-1]['id'] + 1
    
    name = request.form.get('name')
    pet_type = request.form.get('type')
    breed = request.form.get('breed')
    city = request.form.get('city')
    age = request.form.get('age')
    phone = request.form.get('phone')
    
    # Şəkil faylını qəbul etmək
    file = request.files.get('image')
    image_url = 'https://images.unsplash.com/photo-1543466835-00a7907e9de1?auto=format&fit=crop&w=500&q=80'
    
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        image_url = url_for('static', filename=f'uploads/{filename}')

    new_pet = {
        'id': new_id,
        'name': name,
        'type': pet_type,
        'breed': breed,
        'city': city,
        'age': age,
        'phone': phone,
        'image': image_url
    }
    
    pets_list.append(new_pet)
    return redirect(url_for('index'))

@app.route('/delete/<int:pet_id>', methods=['POST'])
def delete_pet(pet_id):
    global pets_list
    pets_list = [pet for pet in pets_list if pet['id'] != pet_id]
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
