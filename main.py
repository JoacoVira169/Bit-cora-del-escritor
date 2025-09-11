# Importar
from flask import Flask, render_template,request, redirect
# Conectando a la biblioteca de bases de datos
from flask_sqlalchemy import SQLAlchemy
import speech


app = Flask(__name__)
# Conectando SQLite
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///diary.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# Creando una base de datos
db = SQLAlchemy(app)
# Creación de una tabla

class Card(db.Model):
    # Creación de columnas
    # id
    id = db.Column(db.Integer, primary_key=True)
    # Título
    title = db.Column(db.String(100), nullable=False)
    # Descripción
    subtitle = db.Column(db.String(300), nullable=False)
    # Texto
    text = db.Column(db.Text, nullable=False)

    # Salida del objeto y del id
    def __repr__(self):
        return f'<Card {self.id}>'
    

#Asignación #2. Crear la tabla Usuario
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    login = db.Column(db.String(100), nullable=False)
    password = db.Column(db.String(100), nullable=False)



# Ejecutar la página de contenidos
@app.route('/', methods=['GET','POST'])
def login():
        error = ''
        if request.method == 'POST':
            form_login = request.form['email']
            form_password = request.form['password']
            
            #Asignación #4. Aplicar la autorización
            
            usersdb = User.query.all()
            for user in usersdb:
                if form_login == user.login and form_password == user.password:
                    return redirect('/index')
                
            else:
                error = 'La contraseña o nombre de usuario son incorrectos.'
                return render_template('login.html', error=error)

            
        else:
            return render_template('login.html')



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
    # Visualización de las entradas de la base de datos
    cards = Card.query.order_by(Card.id).all()
    return render_template('index.html', cards=cards)

# Ejecutar la página con la entrada
@app.route('/card/<int:id>')
def card(id):
    card = Card.query.get(id)

    return render_template('card.html', card=card)

# Ejecutar la página de creación de entradas
@app.route('/create')
def create():
    return render_template('create_card.html')

# El formulario de inscripción
@app.route('/form_create', methods=['GET','POST'])
def form_create():
    if request.method == 'POST':
        title =  request.form['title']
        subtitle =  request.form['subtitle']
        text =  request.form['text']
        

        # Creación de un objeto que se enviará a la base de datos
        card = Card(title=title, subtitle=subtitle, text=text)

        db.session.add(card)
        db.session.commit()
        return redirect('/index')
    else:
        return render_template('create_card.html')
    
@app.route('/delete/<int:id>', methods=['POST'])
def delete(id):
    card = Card.query.get_or_404(id)
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
    
    




# ...existing code...
if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)
# ...existing code...