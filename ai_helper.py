import json
import os
from openai import OpenAI

# the newest OpenAI model is "gpt-5" which was released August 7, 2025.
# do not change this unless explicitly requested by the user
OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")

def get_openai_client():
    """
    Crea y retorna el cliente de OpenAI
    """
    if not OPENAI_API_KEY:
        return None
    return OpenAI(api_key=OPENAI_API_KEY)

def detect_data_type(data_sample: list, column_name: str = "datos") -> dict:
    """
    Utiliza IA para detectar si los datos son cualitativos o cuantitativos
    """
    client = get_openai_client()
    
    if not client:
        return _fallback_detect_data_type(data_sample)
    
    try:
        sample_str = str(data_sample[:20])
        
        prompt = f"""Analiza la siguiente muestra de datos y determina si son cualitativos o cuantitativos.

Muestra de datos: {sample_str}

Responde en formato JSON con:
- "tipo": "cuantitativo" o "cualitativo"
- "razon": breve explicación
- "subtipo": "discreto" o "continuo" si es cuantitativo, "nominal" u "ordinal" si es cualitativo
"""
        
        response = client.chat.completions.create(
            model="gpt-5",
            messages=[
                {"role": "system", "content": "Eres un experto en estadística que clasifica tipos de datos."},
                {"role": "user", "content": prompt}
            ],
            response_format={"type": "json_object"}
        )
        
        result = json.loads(response.choices[0].message.content)
        return result
    except Exception as e:
        return _fallback_detect_data_type(data_sample)

def _fallback_detect_data_type(data_sample: list) -> dict:
    """
    Método de respaldo para detectar tipo de datos sin IA
    """
    try:
        numeric_count = sum(1 for x in data_sample if isinstance(x, (int, float)) or (isinstance(x, str) and x.replace('.', '', 1).replace('-', '', 1).isdigit()))
        
        if numeric_count / len(data_sample) > 0.8:
            return {
                "tipo": "cuantitativo",
                "razon": "La mayoría de los valores son numéricos",
                "subtipo": "continuo"
            }
        else:
            return {
                "tipo": "cualitativo",
                "razon": "La mayoría de los valores son categorías o texto",
                "subtipo": "nominal"
            }
    except:
        return {
            "tipo": "cualitativo",
            "razon": "No se pudo determinar con certeza",
            "subtipo": "nominal"
        }

def interpret_statistics(stats_data: dict, data_type: str) -> str:
    """
    Genera una interpretación de las estadísticas usando IA
    """
    client = get_openai_client()
    
    if not client:
        return _fallback_interpretation(stats_data, data_type)
    
    try:
        prompt = f"""Como experto en estadística, interpreta los siguientes resultados de un análisis descriptivo de datos {data_type}:

Estadísticas: {json.dumps(stats_data, indent=2)}

Proporciona una interpretación clara y concisa en español que incluya:
1. Qué nos dicen las medidas de tendencia central sobre los datos
2. Qué indican las medidas de dispersión sobre la variabilidad
3. Observaciones importantes o patrones relevantes
4. Recomendaciones o conclusiones

Responde en un párrafo claro y educativo."""

        response = client.chat.completions.create(
            model="gpt-5",
            messages=[
                {"role": "system", "content": "Eres un profesor de estadística que explica resultados de forma clara y educativa."},
                {"role": "user", "content": prompt}
            ],
            max_completion_tokens=500
        )
        
        return response.choices[0].message.content
    except Exception as e:
        return _fallback_interpretation(stats_data, data_type)

def _fallback_interpretation(stats_data: dict, data_type: str) -> str:
    """
    Interpretación básica sin IA
    """
    if data_type == "cuantitativo":
        media = stats_data.get('tendencia_central', {}).get('media')
        desv_est = stats_data.get('dispersion', {}).get('desviacion_estandar')
        
        if media is not None and desv_est is not None:
            return f"""Los datos muestran una distribución con un valor promedio de {media:.2f} 
y una desviación estándar de {desv_est:.2f}, 
lo que indica la variabilidad presente en los datos."""
        else:
            return "Los datos cuantitativos han sido analizados. Consulta las tablas de frecuencias y estadísticas para ver los resultados."
    else:
        return "Los datos cualitativos han sido analizados. Consulta la tabla de frecuencias para ver la distribución de categorías."

def answer_question(question: str, data_context: dict) -> str:
    """
    Responde preguntas del usuario sobre el análisis de datos
    """
    client = get_openai_client()
    
    if not client:
        return "Lo siento, necesito una API key de OpenAI para responder preguntas. Por favor, configura tu OPENAI_API_KEY."
    
    try:
        context_str = json.dumps(data_context, indent=2, ensure_ascii=False)
        
        prompt = f"""Contexto del análisis de datos:
{context_str}

Pregunta del usuario: {question}

Responde de forma clara, concisa y educativa en español."""

        response = client.chat.completions.create(
            model="gpt-5",
            messages=[
                {"role": "system", "content": "Eres un asistente experto en estadística que ayuda a estudiantes a entender sus análisis de datos."},
                {"role": "user", "content": prompt}
            ],
            max_completion_tokens=500
        )
        
        return response.choices[0].message.content
    except Exception as e:
        return f"Error al procesar la pregunta: {str(e)}"
