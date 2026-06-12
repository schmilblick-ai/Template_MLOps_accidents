import requests
# The URL of the login and prediction endpoints
login_url = "http://127.0.0.1:3001/login"
predict_url = "http://127.0.0.1:3001/predict"

# Données de connexion - les APIs BentoML orientées classes attendent une clé égale au nom de l'argument
login_payload = {
    "credentials": {
        "username": "user123",
        "password": "password123"
    }
}

# Send a POST request to the login endpoint
login_response = requests.post(
    login_url,
    headers={"Content-Type": "application/json"},
    json=login_payload
)

# Check if the login was successful
if login_response.status_code == 200:
    token = login_response.json().get("token")
    print("Token JWT obtenu:", token)

  # Data to be sent to the prediction endpoint
    prediction_payload = {
        "input_data": {
            "place": 10,
            "catu": 3,
            "sexe": 1,
            "secu1": 0.0,
            "year_acc": 2021,
            "victim_age": 60,
            "catv": 2,
            "obsm": 1,
            "motor": 1,
            "catr": 3,
            "circ": 2,
            "surf": 1,
            "situ": 1,
            "vma": 50,
            "jour": 7,
            "mois": 12,
            "lum": 5,
            "dep": 77,
            "com": 77317,
            "agg_": 2,
            "int_": 1,
            "atm": 0,
            "col": 6,
            "lat": 48.60,
            "long": 2.89,
            "hour": 17,
            "nb_victim": 2,
            "nb_vehicules": 1
        }
    }
  # Send a POST request to the prediction
    response = requests.post(
        predict_url,
        headers={
            "Content-Type": "application/json",
            "Authorization": f"Bearer {token}"
        },
        json=prediction_payload
    )

    print("Réponse de l'API de prédiction:", response.text)
else:
    print("Erreur lors de la connexion:", login_response.text)
