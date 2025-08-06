import requests
import json

# URL de la API local 
API_URL = "https://maternal-health-risk-api.onrender.com/"

# 1. Definir al menos tres payloads distintos para enviar a la API

# Los datos corresponden:
 
#Age - Age in years when a woman is pregnant (int64)
#SystolicBP - Upper value of Blood Pressure in mmHg (int64)
#DiastolicBP - Lower value of Blood Pressure in mmHg (int64)
#BS - Blood glucose levels is in terms of a molar concentration, mmol/L (float64)
#BodyTemp - Body temperature in Celsius (float64)
#HeartRate - Resting heart rate in beats per minute (int64)
#RiskLevel - Predicted Risk Intensity Level during pregnancy ['high risk', 'mid risk', 'low risk']


payloads = [
    {
      "Age": 25,         # Baja edad
      "SystolicBP": 120,   # Presión normal
      "DiastolicBP": 80,   # Presión normal
      "BS": 7.5,           # Glucosa normal
      "BodyTemp": 36.8,    # Temperatura normal
      "HeartRate": 75      # Ritmo cardíaco normal
    },
    {
      "Age": 45,         # Alta edad
      "SystolicBP": 145,   # Presión alta
      "DiastolicBP": 95,   # Presión alta
      "BS": 10.0,          # Glucosa alta
      "BodyTemp": 38.6,   # Fiebre
      "HeartRate": 105     # Ritmo cardíaco alto
    },
    {
      "Age": 32,         # Edad intermedia
      "SystolicBP": 130,   # Presión limítrofe
      "DiastolicBP": 85,   # Presión limítrofe
      "BS": 8.2,           # Glucosa limítrofe
      "BodyTemp": 37.2,    # Temperatura limítrofe
      "HeartRate": 88      # Ritmo cardíaco limítrofe
    }
]

# 2. Iterar sobre los payloads y enviar las peticiones
for i, payload in enumerate(payloads):
    print(f"\n--- Petición {i + 1} ---")
    print("Enviando datos:")
    print(json.dumps(payload, indent=2))
    
    # Enviar la petición POST
    try:
        response = requests.post(API_URL, json=payload)
        response.raise_for_status()  # Lanza una excepción si el status es 4xx o 5xx
        
        # 3. Mostrar los resultados obtenidos
        print(f"\nRespuesta del servidor (Status Code: {response.status_code}):")
        print(json.dumps(response.json(), indent=2))
        
    except requests.exceptions.RequestException as e:
        print(f"\nError en la petición: {e}")