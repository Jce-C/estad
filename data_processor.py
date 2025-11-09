import pandas as pd
import numpy as np
from typing import Union, List, Dict
import io

def load_data_from_text(text_input: str, delimiter: str = None) -> pd.DataFrame:
    """
    Carga datos desde texto ingresado manualmente
    """
    try:
        if delimiter:
            data = [x.strip() for x in text_input.split(delimiter) if x.strip()]
        else:
            lines = text_input.strip().split('\n')
            data = []
            for line in lines:
                if ',' in line:
                    data.extend([x.strip() for x in line.split(',') if x.strip()])
                elif ';' in line:
                    data.extend([x.strip() for x in line.split(';') if x.strip()])
                elif '\t' in line:
                    data.extend([x.strip() for x in line.split('\t') if x.strip()])
                else:
                    items = line.strip().split()
                    data.extend(items)
        
        try:
            numeric_data = [float(x) for x in data]
            df = pd.DataFrame({'valores': numeric_data})
        except ValueError:
            df = pd.DataFrame({'valores': data})
        
        return df
    except Exception as e:
        raise ValueError(f"Error al procesar los datos: {str(e)}")

def load_data_from_file(file, file_type: str) -> pd.DataFrame:
    """
    Carga datos desde un archivo CSV, TXT o XLSX
    """
    try:
        if file_type == 'csv':
            df = pd.read_csv(file)
        elif file_type == 'txt':
            content = file.read().decode('utf-8')
            df = load_data_from_text(content)
        elif file_type in ['xlsx', 'xls']:
            df = pd.read_excel(file)
        else:
            raise ValueError(f"Tipo de archivo no soportado: {file_type}")
        
        return df
    except Exception as e:
        raise ValueError(f"Error al cargar el archivo: {str(e)}")

def create_frequency_table(data: Union[List, pd.Series], is_quantitative: bool = True, bins: int = None) -> pd.DataFrame:
    """
    Crea una tabla de frecuencias para datos cualitativos o cuantitativos
    """
    if isinstance(data, list):
        data = pd.Series(data)
    
    if is_quantitative:
        try:
            data_numeric = pd.to_numeric(data, errors='coerce').dropna()
            
            if bins is None:
                n = len(data_numeric)
                bins = min(int(1 + 3.322 * np.log10(n)), 20)
            
            freq, bin_edges = np.histogram(data_numeric, bins=bins)
            
            intervals = []
            for i in range(len(bin_edges) - 1):
                intervals.append(f"[{bin_edges[i]:.2f}, {bin_edges[i+1]:.2f})")
            
            freq_table = pd.DataFrame({
                'Intervalo': intervals,
                'Frecuencia Absoluta': freq,
                'Frecuencia Relativa': freq / len(data_numeric),
                'Frecuencia Porcentual': (freq / len(data_numeric)) * 100,
                'Frecuencia Acumulada': np.cumsum(freq),
                'Frecuencia Rel. Acumulada': np.cumsum(freq) / len(data_numeric)
            })
            
            return freq_table
        except:
            is_quantitative = False
    
    if not is_quantitative:
        value_counts = data.value_counts().sort_index()
        
        freq_table = pd.DataFrame({
            'Categoría': value_counts.index,
            'Frecuencia Absoluta': value_counts.values,
            'Frecuencia Relativa': value_counts.values / len(data),
            'Frecuencia Porcentual': (value_counts.values / len(data)) * 100,
            'Frecuencia Acumulada': np.cumsum(value_counts.values),
            'Frecuencia Rel. Acumulada': np.cumsum(value_counts.values) / len(data)
        })
        
        return freq_table

def validate_data(data: pd.DataFrame) -> Dict:
    """
    Valida los datos ingresados y retorna información sobre ellos
    """
    validation = {
        'valid': True,
        'errors': [],
        'warnings': [],
        'info': {}
    }
    
    if data.empty:
        validation['valid'] = False
        validation['errors'].append("El conjunto de datos está vacío")
        return validation
    
    validation['info']['num_rows'] = len(data)
    validation['info']['num_columns'] = len(data.columns)
    validation['info']['columns'] = list(data.columns)
    
    for col in data.columns:
        null_count = data[col].isnull().sum()
        if null_count > 0:
            validation['warnings'].append(f"La columna '{col}' tiene {null_count} valores nulos")
    
    return validation

def clean_data(data: pd.Series, remove_outliers: bool = False) -> pd.Series:
    """
    Limpia los datos eliminando valores nulos y opcionalmente valores atípicos
    """
    cleaned = data.dropna()
    
    if remove_outliers:
        try:
            numeric_data = pd.to_numeric(cleaned, errors='coerce').dropna()
            Q1 = numeric_data.quantile(0.25)
            Q3 = numeric_data.quantile(0.75)
            IQR = Q3 - Q1
            lower_bound = Q1 - 1.5 * IQR
            upper_bound = Q3 + 1.5 * IQR
            cleaned = numeric_data[(numeric_data >= lower_bound) & (numeric_data <= upper_bound)]
        except:
            pass
    
    return cleaned
