import numpy as np
import pandas as pd
from scipy import stats
from typing import Union, List, Dict

def calculate_central_tendency(data: Union[List, pd.Series]) -> Dict:
    """
    Calcula las medidas de tendencia central: media, mediana y moda
    """
    if isinstance(data, list):
        data = pd.Series(data)
    
    try:
        data_numeric = pd.to_numeric(data, errors='coerce').dropna()
    except:
        data_numeric = data
    
    result = {}
    
    if len(data_numeric) > 0:
        result['media'] = float(np.mean(data_numeric))
        result['mediana'] = float(np.median(data_numeric))
        
        mode_result = stats.mode(data_numeric, keepdims=True)
        if len(mode_result.mode) > 0:
            result['moda'] = float(mode_result.mode[0])
            result['frecuencia_moda'] = int(mode_result.count[0])
        else:
            result['moda'] = None
            result['frecuencia_moda'] = 0
    else:
        result = {
            'media': None,
            'mediana': None,
            'moda': None,
            'frecuencia_moda': 0
        }
    
    return result

def calculate_dispersion(data: Union[List, pd.Series]) -> Dict:
    """
    Calcula las medidas de dispersión: rango, desviación estándar y varianza
    """
    if isinstance(data, list):
        data = pd.Series(data)
    
    try:
        data_numeric = pd.to_numeric(data, errors='coerce').dropna()
    except:
        data_numeric = data
    
    result = {}
    
    if len(data_numeric) > 0:
        result['rango'] = float(np.max(data_numeric) - np.min(data_numeric))
        result['varianza'] = float(np.var(data_numeric, ddof=1))
        result['desviacion_estandar'] = float(np.std(data_numeric, ddof=1))
        result['minimo'] = float(np.min(data_numeric))
        result['maximo'] = float(np.max(data_numeric))
        result['q1'] = float(np.percentile(data_numeric, 25))
        result['q3'] = float(np.percentile(data_numeric, 75))
        result['rango_intercuartil'] = result['q3'] - result['q1']
        result['coeficiente_variacion'] = (result['desviacion_estandar'] / calculate_central_tendency(data_numeric)['media'] * 100) if calculate_central_tendency(data_numeric)['media'] != 0 else None
    else:
        result = {
            'rango': None,
            'varianza': None,
            'desviacion_estandar': None,
            'minimo': None,
            'maximo': None,
            'q1': None,
            'q3': None,
            'rango_intercuartil': None,
            'coeficiente_variacion': None
        }
    
    return result

def calculate_all_statistics(data: Union[List, pd.Series]) -> Dict:
    """
    Calcula todas las estadísticas descriptivas
    """
    central = calculate_central_tendency(data)
    dispersion = calculate_dispersion(data)
    
    return {
        'tendencia_central': central,
        'dispersion': dispersion,
        'n': len(data)
    }
