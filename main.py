import pandas as pd
import joblib
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field, field_validator
from typing import Dict, Any



# 1. Cargar el modelo guardado
try:
    model = joblib.load('maternal_health_risk_model_v2.joblib')
except Exception as e:
    print(f"Error cargando modelo: {e}")
    model = None


# 2. Inicializar la aplicación FastAPI
app = FastAPI(
    title="Maternal Health Risk Prediction API",
    description="API para predecir el nivel de riesgo en salud materna",
    version="1.0.0"
)

# 3. Definir la clase Pydantic con sus respectivos validadores
class MaternalHealthData(BaseModel):
    Age: int = Field(ge=13, le=60, description="Edad entre 13-60 años")
    SystolicBP: int = Field(ge=70, le=250, description="Presión sistólica 70-250 mmHg")
    DiastolicBP: int = Field(ge=40, le=150, description="Presión diastólica 40-150 mmHg")
    BS: float = Field(ge=3.0, le=25.0, description="Glucosa 3.0-25.0 mmol/L")
    BodyTemp: float = Field(ge=35.0, le=42.0, description="Temperatura 35.0-42.0°C")
    HeartRate: int = Field(ge=40, le=200, description="Ritmo cardíaco 40-200 bpm")

    @field_validator('DiastolicBP')
    @classmethod
    def diastolic_must_be_less_than_systolic(cls, v, info):
        if 'SystolicBP' in info.data and v >= info.data['SystolicBP']:
            raise ValueError('La presión diastólica debe ser menor que la sistólica')
        return v

    class Config:
        schema_extra = {
            "example": {
                "Age": 25,
                "SystolicBP": 120,
                "DiastolicBP": 80,
                "BS": 7.5,
                "BodyTemp": 36.8,
                "HeartRate": 75
            }
        }


# 4. Definir el endpoint de predicción
@app.post("/predict")
def predict_risk(data: MaternalHealthData) -> Dict[str, Any]:
    """
    Predice el nivel de riesgo de salud materna
    
    Args:
       Datos de salud materna validados
    
    Returns:
    Dict con la predicción y información adicional
    
    Raises:
        HTTPException: Si hay errores en la predicción o el modelo no está cargado
    """
    # Verificar que el modelo esté cargado
    if model is None:
        raise HTTPException(
            status_code=503, 
            detail="El modelo no está disponible. Contacte al administrador."
        )
    
    try:
        # Convertir el objeto Pydantic a un DataFrame de pandas
        input_data = data.dict()
        df = pd.DataFrame([input_data])
        
        # Asegurarse de que el orden de las columnas sea el correcto
        column_order = ['Age', 'SystolicBP', 'DiastolicBP', 'BS', 'BodyTemp', 'HeartRate']
        df = df[column_order]
        
        # Realizar la predicción
        prediction = model.predict(df)[0]
        
        # Mapeo de predicciones
        risk_mapping = {
            0: "High Risk",
            1: "Low Risk",
            2: "Mid Risk"
        }
        
        predicted_risk = risk_mapping.get(prediction, "Unknown")
        
        
        return {"risk_level_predicted": predicted_risk}


    except ValueError as e:
        raise HTTPException(
            status_code=422, 
            detail=f"Error en los datos de entrada: {str(e)}"
        )
    except Exception as e:
        raise HTTPException(
            status_code=500, 
            detail=f"Error interno del servidor durante la predicción: {str(e)}"
        )


