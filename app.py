from flask import Flask, render_template, request, g
import sqlite3
import os

app = Flask(__name__)
DATABASE = 'database.db'

# --- Connexion à la base ---
def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
        db.row_factory = sqlite3.Row
    return db

@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()


@app.route('/', methods=['GET', 'POST'])
def index():
    erreur = None
    prenom = None

    if request.method == 'POST':
        prenom = request.form.get('prenom')
        password = request.form.get('password')
        password2 = request.form.get('password2')

        # Vérification des mots de passe
        if password != password2:
            erreur = "Les mots de passe ne correspondent pas."
        elif not prenom or not password:
            erreur = "Tous les champs sont obligatoires."
        else:
            try:
                db = get_db()
                cur = db.cursor()
            
                cur.execute(
                    "INSERT INTO Compte(username, password) VALUES (?, ?)",
                    (prenom, password)
                )
                db.commit()
                erreur = "Compte créé avec succès !"
            except sqlite3.IntegrityError:
                # Gestion de l'unicité du username
                erreur = "Ce nom d'utilisateur existe déjà."

    return render_template('index.html', erreur=erreur, prenom=prenom)
@app.route('/login')
def login():
    """Sert la page principale 'index.html'."""
    return render_template('login.html')
# --- Lancement du serveur ---
if __name__ == '__main__':
    app.run(debug=True)