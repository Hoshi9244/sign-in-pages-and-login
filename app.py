from flask import Flask, render_template, request, g
import sqlite3
import os

app = Flask(__name__)
DATABASE = 'database.db'

def get_db():
    """
    connection a la base de donnée
    """
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
        db.row_factory = sqlite3.Row
    return db

@app.teardown_appcontext
def close_connection(exception):
    """
    ferme la connection
    """
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()


@app.route('/', methods=['GET', 'POST'])
def index():
    # on initialise les variable
    erreur = None
    prenom = None
    password = None

    if request.method == 'POST':
        # on demande le username et password
        prenom = request.form.get('prenom')
        password = request.form.get('password')
        password2 = request.form.get('password2')

        # Vérification des password
        if password != password2:
            erreur = "Les mots de passe ne correspondent pas."
        elif not prenom or not password:
            erreur = "Tous les champs sont obligatoires."
        else:
            try:
                db = get_db()
                cur = db.cursor()

                cur.execute( #on ecrit le username et password dans la base de donnée
                    "INSERT INTO Compte(username, password) VALUES (?, ?)",
                    (prenom, password)
                )

                db.commit() #sauvegarde

                return render_template(
                    #on est drole donc on marque notre username et password
                    'index.html',
                    succes="Compte créé avec succès !",
                    prenom=prenom,
                    password=password
                )

            except sqlite3.IntegrityError:
                erreur = "Ce nom d'utilisateur existe déjà."

    return render_template('index.html', erreur=erreur)

@app.route('/login', methods=['GET', 'POST'])
def login():
    erreur = None
    prenom = None
    password = None

    if request.method == 'POST':
        prenom = request.form.get('prenom')
        password = request.form.get('password')

        if not prenom or not password:
            erreur = "Tous les champs sont obligatoires."
        else:
            db = get_db()
            cur = db.cursor()

            cur.execute(
                "SELECT * FROM Compte WHERE username = ? AND password = ?",
                (prenom, password)
            )
            compte = cur.fetchone()

            if compte:
                return render_template(
                    # on ecrit le prenom et le password
                    'login.html',
                    succes="Connexion réussie !",
                    prenom=prenom,
                    password=password
                )

            erreur = "Nom d'utilisateur ou mot de passe incorrect."

    return render_template('login.html', erreur=erreur)

if __name__ == '__main__':
    app.run(debug=True)