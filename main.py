# Importar
from flask import Flask, render_template, request, redirect, session, abort, url_for, g
# Conectando a la biblioteca de bases de datos
from flask_sqlalchemy import SQLAlchemy
import speech
import os

app = Flask(__name__)
# Asegura SECRET_KEY (usar variable de entorno en producción)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'dev-change-me-to-a-secure-key')
# Conectando SQLite
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///diary.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# Creando una base de datos
db = SQLAlchemy(app)
# Creación de una tabla

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    login = db.Column(db.String(100), nullable=False, unique=True)
    password = db.Column(db.String(200), nullable=False)

    # relación: un usuario tiene muchas cards
    cards = db.relationship(
        'Card',
        backref='user',
        lazy=True,
        cascade='all, delete-orphan'
    )

    def __repr__(self):
        return f'<User {self.id} {self.login}>'

class Card(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    subtitle = db.Column(db.String(300), nullable=False)
    text = db.Column(db.Text, nullable=False)

    # llave foránea al usuario
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        return f'<Card {self.id} user={self.user_id}>'

# Ejecutar la página de contenidos
@app.route('/', methods=['GET','POST'])
def login():
    error = None
    if request.method == 'POST':
        form_login = request.form.get('email')
        form_password = request.form.get('password')
        user = User.query.filter_by(login=form_login, password=form_password).first()
        if user:
            # Guardar id del usuario en la sesión (paso 2)
            session['user_id'] = user.id
            print("DEBUG session after login:", dict(session))
            return redirect('/index')
        error = 'Usuario o contraseña incorrectos.'
    return render_template('login.html', error=error)

@app.route('/reg', methods=['GET','POST'])
def reg():
    if request.method == 'POST':
        login= request.form['email']
        password = request.form['password']
        
        #Asignación #3. Hacer que los datos del usuario se registren en la base de datos.
        user = User(login=login, password=password)
        db.session.add(user)
        db.session.commit()
        return redirect('/')
    
    else:    
        return render_template('registration.html')


# Ejecutar la página de contenidos
@app.route('/index')
def index():
    if not session.get('user_id'):
        return redirect('/')
    user_id = session['user_id']
    print("DEBUG: session user_id =", user_id)
    cards = Card.query.filter_by(user_id=user_id).order_by(Card.id).all()
    print("DEBUG: cards returned ids:", [c.id for c in cards])
    # pasar current_user_id para depuración en la plantilla
    return render_template('index.html', cards=cards, current_user_id=user_id)



# Ejecutar la página con la entrada
@app.route('/card/<int:id>')
def card(id):
    # requerir login y sólo devolver la card si pertenece al user actual
    if not session.get('user_id'):
        return redirect('/')
    card = Card.query.filter_by(id=id, user_id=session['user_id']).first()
    if not card:
        abort(404)
    return render_template('card.html', card=card)

# Ejecutar la página de creación de entradas
@app.route('/create')
def create():
    # Validar sesión antes de mostrar el formulario
    if not session.get('user_id'):
        return redirect('/')  # redirige al login si no está autenticado
    return render_template('create_card.html')

# El formulario de inscripción
@app.route('/form_create', methods=['GET','POST'])
def form_create():
    if request.method == 'POST':
        if not session.get('user_id'):
            return redirect('/')  # evita crear sin autenticación
        title = request.form.get('title', '')
        subtitle = request.form.get('subtitle', '')
        text = request.form.get('text', '')
        card = Card(title=title, subtitle=subtitle, text=text, user_id=session['user_id'])
        db.session.add(card)
        db.session.commit()
        return redirect('/index')
    # para GET muestra el formulario (también protegido por /create)
    return redirect('/create')

@app.route('/delete/<int:id>', methods=['POST'])
def delete(id):
    # validar sesión y propiedad antes de borrar
    if not session.get('user_id'):
        return redirect('/')
    card = Card.query.filter_by(id=id, user_id=session['user_id']).first()
    if not card:
        abort(404)
    db.session.delete(card)
    db.session.commit()
    return redirect('/index')


@app.route('/voice', methods=['GET', 'POST'])
def voice():
    if request.method == 'POST':
        # Recuperar lo que ya estaba escrito
        title = request.form.get('title', '')
        subtitle = request.form.get('subtitle', '')
        previous_text = request.form.get('text', '')

        try:
            # Reconocer voz
            rec_word = speech.speech_es()  # tu función de STT
            rec_word = rec_word.lower()    # opcional

            # Anexar en vez de reemplazar
            sep = '\n' if previous_text and not previous_text.endswith('\n') else ''
            combined_text = f"{previous_text}{sep}{rec_word}"

            # Devolver la misma plantilla, conservando todo
            return render_template(
                'create_card.html',
                title=title,
                subtitle=subtitle,
                text=combined_text
            )
        except Exception as e:
            # Mantener lo escrito y mostrar error
            return render_template(
                'create_card.html',
                title=title,
                subtitle=subtitle,
                text=f"{previous_text}\n[Error al reconocer la voz: {e}]"
            )
    # Si alguien entra por GET a /voice, solo mostramos la plantilla vacía/actual
    return render_template('create_card.html')
    
@app.after_request
def add_no_cache_headers(response):
    response.headers["Cache-Control"] = "no-store, no-cache, must-revalidate, private"
    response.headers["Pragma"] = "no-cache"
    return response

@app.route('/logout')
def logout():
    session.pop('user_id', None)
    return redirect('/')

@app.route('/cards_list')
def cards_list():
    if not session.get('user_id'):
        return redirect('/')
    cards = Card.query.filter_by(user_id=session['user_id']).all()
    return render_template('cards_list.html', cards=cards)

@app.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit(id):
    if not session.get('user_id'):
        return redirect('/')
    card = Card.query.filter_by(id=id, user_id=session['user_id']).first()
    if not card:
        abort(404)
    
    if request.method == 'POST':
        card.title = request.form.get('title', '')
        card.subtitle = request.form.get('subtitle', '')
        card.text = request.form.get('text', '')
        db.session.commit()
        return redirect(url_for('card', id=card.id))
    
    return render_template('edit_card.html', card=card)

@app.route('/config', methods=['GET', 'POST'])
def config():
    # 1) Protección: solo usuarios logueados pueden acceder
    if not session.get('user_id'):
        return redirect(url_for('login' if 'login' in globals() else 'index'))

    # 2) Leemos los ajustes actuales desde la sesión (si existen)
    current = session.get('settings', {})

    # 3) Si el formulario se envía (POST) guardamos los valores recibidos
    if request.method == 'POST':
        theme = request.form.get('theme', 'light')                 # valor select tema
        notifications = bool(request.form.get('notifications'))    # checkbox -> True/False
        display_name = request.form.get('display_name', '').strip()# texto del usuario

        # 4) Guardado temporal en session (no en BD): práctico para prototipo
        session['settings'] = {
            'theme': theme,
            'notifications': notifications,
            'display_name': display_name
        }
        return redirect(url_for('index'))  # redirige tras guardar (Post/Redirect/Get)

    # 5) GET: preparar valores por defecto para la plantilla
    settings = {
        'theme': current.get('theme', 'light'),
        'notifications': current.get('notifications', True),
        'display_name': current.get('display_name', '')
    }
    return render_template('config.html', settings=settings)

@app.context_processor
def inject_settings():
    # Devuelve un dict 'settings' accesible en todas las plantillas
    return {
        'settings': session.get('settings', {
            'theme': 'light',
            'notifications': True,
            'display_name': ''
        })
    }

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)