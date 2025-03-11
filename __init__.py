from flask import Flask
from flask import render_template, jsonify, request
from flask_jwt_extended import create_access_token, get_jwt_identity, jwt_required, JWTManager
from datetime import timedelta

app = Flask(__name__)

# Configuration du module JWT
app.config["JWT_SECRET_KEY"] = "Ma_clé_secrete"  # Clé secrète
app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(hours=1)  # Expiration du jeton après 1 heure
jwt = JWTManager(app)

@app.route('/')
def hello_world():
    return render_template('accueil.html')

# Route pour vérifier l'utilisateur et retourner un Jeton JWT si ok.
@app.route("/login", methods=["POST"])
def login():
    username = request.json.get("username", None)
    password = request.json.get("password", None)
    if username != "test" or password != "test":
        return jsonify({"msg": "Mauvais utilisateur ou mot de passe"}), 401

    access_token = create_access_token(identity=username)
    return jsonify(access_token=access_token)

# Route protégée par un jeton valide
@app.route("/protected", methods=["GET"])
@jwt_required()
def protected():
    current_user = get_jwt_identity()
    return jsonify(logged_in_as=current_user), 200

if __name__ == "__main__":
    app.run(debug=True)
