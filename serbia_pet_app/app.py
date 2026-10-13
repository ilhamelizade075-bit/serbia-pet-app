from flask import Flask, render_template, request, redirect, url_for, session
from authlib.integrations.flask_client import OAuth

app = Flask(__name__)
app.secret_key = 'buraya_istediyin_gizli_bir_soz_yaz'  # Sessiyanı işlətmək üçün vacibdir

# Google OAuth tənzimləmələri
oauth = OAuth(app)
google = oauth.register(
    name='google',
    client_id='BURI_GOOGLE_DAN_ALDIGIN_CLIENT_ID_YAZ',
    client_secret='BURI_GOOGLE_DAN_ALDIGIN_CLIENT_SECRET_YAZ',
    server_metadata_url='https://accounts.google.com/.well-known/openid-configuration',
    client_kwargs={
        'scope': 'openid email profile'
    }
)

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
    }
]

@app.route('/')
def index():
    user = session.get('user')
    return render_template('index.html', pets=pets_list, user=user)

# Google ilə giriş səhifəsinə yönləndirmə
@app.route('/login')
def login():
    redirect_uri = url_for('authorize', _external=True)
    return google.authorize_redirect(redirect_uri)

# Google-dan qayıtdıqdan sonra işləyən hissə
@app.route('/authorize')
def authorize():
    token = google.authorize_access_token()
    user_info = token.get('userinfo')
    session['user'] = user_info['email']  # İstifadəçinin Gmail ünvanını yadda saxlayırıq
    return redirect(url_for('index'))

# Sistemdən çıxış
@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect(url_for('index'))

@app.route('/add', methods=['POST'])
def add_pet():
    # Əgər istifadəçi daxil olmayıbsa, elan əlavə etməyə icazə verməyə bilərik
    if 'user' not in session:
        return redirect(url_for('login'))
        
    new_id = len(pets_list) + 1 if not pets_list else pets_list[-1]['id'] + 1
    # ... qalan elan əlavə etmə kodu ...
    return redirect(url_for('index'))

@app.route('/delete/<int:pet_id>', methods=['POST'])
def delete_pet(pet_id):
    global pets_list
    pets_list = [pet for pet in pets_list if pet['id'] != pet_id]
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
