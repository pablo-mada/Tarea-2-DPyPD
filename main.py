import pandas as pd
import joblib
from fastapi import FastAPI
from pydantic import BaseModel

# 1. Cargar el modelo guardado
model = joblib.load('maternal_health_risk_model_v2.joblib')

# 2. Inicializar la aplicación FastAPI
app = FastAPI()

# 3. Definir la clase Pydantic con el orden correcto de las variables
class MaternalHealthData(BaseModel):
    Age: int
    SystolicBP: int
    DiastolicBP: int
    BS: float       
    BodyTemp: float 
    HeartRate: int

# 4. Definir el endpoint de predicción
@app.post("/predict")
def predict_risk(data: MaternalHealthData):
    # Convertir el objeto Pydantic a un DataFrame de pandas
    df = pd.DataFrame([data.dict()])
    
    # Asegurarse de que el orden de las columnas sea el EXACTO
    df = df[['Age', 'SystolicBP', 'DiastolicBP', 'BS', 'BodyTemp', 'HeartRate']]
    
    # Realizar la predicción
    prediction = model.predict(df)[0]
    
    # Asignar un texto a la predicción para que sea más legible
    risk_mapping = {
        0: "High Risk",
        1: "Low Risk",
        2: "Mid Risk"
    }
    predicted_risk = risk_mapping.get(prediction, "Unknown")
    
    return {"risk_level_predicted": predicted_risk}

