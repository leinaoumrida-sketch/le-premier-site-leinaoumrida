
from flask import Flask, render_template, request, redirect, abort, jsonify
from datetime import datetime
from zoneinfo import ZoneInfo
from html import escape

app = Flask(__name__)


# ---------------------------------------------------------------
# PAGE D'ACCUEIL
# ---------------------------------------------------------------

@app.get("/")
def accueil():
    return render_template("accueil.html")


# ---------------------------------------------------------------
# PAGE DE PRESENTATION
# ---------------------------------------------------------------

@app.get("/presentation")
def presentation():
    return render_template(
        "presentation.html",
        prenom="Léina",
        nom="Oumrida"
    )


# ---------------------------------------------------------------
# PAGE LOISIRS
# ---------------------------------------------------------------

@app.get("/loisirs")
def loisirs():
    return """
    <!DOCTYPE html>
    <html lang="fr">
    <head>
        <meta charset="utf-8">
        <title>Mes loisirs</title>
        <link rel="stylesheet" href="/static/style.css">
    </head>
    <body>
        <nav>
            <a href="/">Accueil</a>
            <a href="/presentation">Présentation</a>
            <a href="/loisirs">Loisirs</a>
            <a href="/formulaire">Formulaire</a>
        </nav>

        <h1>Mes loisirs</h1>
        <ul>
            <li>La danse</li>
            <li>Le sport</li>
            <li>La cuisine</li>
        </ul>
    </body>
    </html>
    """


# ---------------------------------------------------------------
# EXERCICE 7 : INFORMATION DANS L'URL
# ---------------------------------------------------------------

@app.get("/bonjour/<prenom>")
def bonjour(prenom):
    return f"<h1>Bonjour {escape(prenom)} !</h1>"


@app.get("/calcul")
def calcul():
    a = int(request.args.get("a", 0))
    b = int(request.args.get("b", 0))

    return f"{a} + {b} = {a + b}"


# ---------------------------------------------------------------
# EXERCICE 8 : FORMULAIRES
# ---------------------------------------------------------------

@app.get("/formulaire")
def formulaire():
    return render_template("formulaire.html")


@app.route("/salut", methods=["GET", "POST"])
def salut():

    if request.method == "POST":
        prenom = request.form.get("prenom", "inconnu")
        ville = request.form.get("ville", "nulle part")
    else:
        prenom = request.args.get("prenom", "inconnu")
        ville = request.args.get("ville", "nulle part")

    return f"Bonjour {escape(prenom)}, qui vient de {escape(ville)} ! (reçu en {request.method})"


# ---------------------------------------------------------------
# LANCEMENT DU SITE
# ---------------------------------------------------------------

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)


# ---------------------------------------------------------------
# EXERCICE 9 : LES CODES DE STATUT HTTP
# ---------------------------------------------------------------

# 3xx : redirection vers la page d'accueil
@app.get("/home")
def home():
    return redirect("/")


# 4xx : accès interdit
@app.get("/secret")
def secret():
    abort(403)


# Page d'erreur 404 personnalisée
@app.errorhandler(404)
def page_introuvable(erreur):
    return render_template("404.html"), 404




@app.get("/moi")
def moi():
    return render_template(
        "moi.html",
        ip=request.headers.get("X-Real-IP", request.remote_addr),
        navigateur=request.headers.get("User-Agent"),
        langues=request.headers.get("Accept-Language"),
        entetes=request.headers,
    )


@app.get("/api/heure")
def api_heure():
    maintenant = datetime.now(ZoneInfo("Europe/Paris"))

    return jsonify({
        "heure": maintenant.strftime("%H:%M:%S"),
        "date": maintenant.strftime("%d/%m/%Y"),
        "message": "Bonjour depuis mon API !",
    })
