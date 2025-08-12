#client.py
import requests
import json
from typing import Dict, Any


# URL de la API local 

API_URL = "https://maternal-health-risk-api.onrender.com/predict"
#API_URL = "http://127.0.0.1:8000/predict"


# 1. Definir función predicción con al menos tres payloads distintos para enviar a la API

def make_prediction(payload: Dict[str, Any], test_name: str):
    """
    Realiza una predicción individual con manejo de errores
    
    Args:
        payload: Datos a enviar a la API
        test_name: Nombre descriptivo del test
    """
    print(f"\n{'='*50}")
    print(f"🧪 {test_name}")
    print(f"{'='*50}")
    print("📤 Enviando datos:")
    print(json.dumps(payload, indent=2))
    
    try:
        # Enviar la petición POST con timeout
        response = requests.post(API_URL, json=payload, timeout=30)
        
        # Mostrar información de la respuesta
        print(f"\n📊 Status Code: {response.status_code}")
        
        if response.status_code == 200:
            # Predicción exitosa
            result = response.json()
            print("✅ Predicción exitosa!")
            print("📋 Resultado:")
            print(json.dumps(result, indent=2))
            
        else:
            # Error en la respuesta
            print("❌ Error en la predicción")
            try:
                error_detail = response.json()
                print("💬 Detalle del error:")
                print(json.dumps(error_detail, indent=2))
            except json.JSONDecodeError:
                print(f"💬 Respuesta del servidor: {response.text}")
        
        return response
    # Manejo de errores
    except requests.exceptions.Timeout:
        print("⏰ Error: Tiempo de espera agotado")
    except requests.exceptions.ConnectionError:
        print("🔌 Error: No se pudo conectar con la API")
    except requests.exceptions.RequestException as e:
        print(f"🚫 Error en la petición: {e}")
    except json.JSONDecodeError:
        print("📄 Error: Respuesta no válida del servidor")
    except Exception as e:
        print(f"💥 Error inesperado: {e}")
    
    return None


# 2. Función principal que ejecuta todos los tests

def main():
    print("🏥 CLIENTE DE PRUEBAS - API DE RIESGO DE SALUD MATERNA")
    print("=" * 60)
    
    # Casos de prueba válidos
    valid_payloads = [
        {
            "payload": {
                "Age": 25,
                "SystolicBP": 120,
                "DiastolicBP": 80,
                "BS": 7.5,
                "BodyTemp": 36.8,
                "HeartRate": 75
            },
            "test_name": "CASO 1: Perfil de Bajo Riesgo (Valores Normales)"
        },
        {
            "payload": {
                "Age": 45,
                "SystolicBP": 160,
                "DiastolicBP": 100,
                "BS": 15.0,
                "BodyTemp": 38.5,
                "HeartRate": 110
            },
            "test_name": "CASO 2: Perfil de Alto Riesgo (Múltiples Factores)"
        },
        {
            "payload": {
                "Age": 22,
                "SystolicBP": 85,
                "DiastolicBP": 60,
                "BS": 6.9,
                "BodyTemp": 37.3,
                "HeartRate": 76
            },
            "test_name": "CASO 3: Perfil de Riesgo Intermedio (Valores Limítrofes)"
        }
    ]
    
    # Casos de prueba con errores, para probar validaciones
    invalid_payloads = [
        {
            "payload": {
                "Age": -5,  # Edad negativa
                "SystolicBP": 120,
                "DiastolicBP": 80,
                "BS": 7.5,
                "BodyTemp": 36.8,
                "HeartRate": 75
            },
            "test_name": "CASO 4: Error - Edad Negativa (Prueba de Validación)"
        },
        {
            "payload": {
                "Age": 30,
                "SystolicBP": 90,
                "DiastolicBP": 110,  # Diastólica mayor que sistólica
                "BS": 7.5,
                "BodyTemp": 36.8,
                "HeartRate": 75
            },
            "test_name": "CASO 5: Error - Presión Diastólica > Sistólica (Prueba de Validación)"
        }
    ]
    
    # Ejecutar casos válidos
    print(f"\n{'🟢 EJECUTANDO CASOS VÁLIDOS':^60}")
    for test_case in valid_payloads:
        make_prediction(test_case["payload"], test_case["test_name"])
    
    # Ejecutar casos con errores
    print(f"\n{'🔴 EJECUTANDO CASOS DE ERROR (PRUEBAS DE VALIDACIÓN)':^60}")
    for test_case in invalid_payloads:
        make_prediction(test_case["payload"], test_case["test_name"])
    
    print(f"\n{'='*60}")
    print("🏁 PRUEBAS COMPLETADAS")
    print("📋 Revisa los resultados arriba para verificar el comportamiento de la API")
    print("=" * 60)

if __name__ == "__main__":
    main()