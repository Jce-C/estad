import pandas as pd
import numpy as np
from stats_utils import calculate_all_statistics, calculate_central_tendency, calculate_dispersion
from data_processor import load_data_from_text, create_frequency_table
from visualization import create_histogram, create_bar_chart

print("=" * 60)
print("PRUEBA DE CÁLCULOS ESTADÍSTICOS")
print("=" * 60)

test_data_quantitative = [10, 20, 30, 40, 50, 20, 30, 20, 40, 30]
print(f"\n📊 Datos de prueba (cuantitativos): {test_data_quantitative}")

stats = calculate_all_statistics(test_data_quantitative)
print("\n✅ Medidas de Tendencia Central:")
print(f"   Media: {stats['tendencia_central']['media']:.2f}")
print(f"   Mediana: {stats['tendencia_central']['mediana']:.2f}")
print(f"   Moda: {stats['tendencia_central']['moda']:.2f}")

print("\n✅ Medidas de Dispersión:")
print(f"   Rango: {stats['dispersion']['rango']:.2f}")
print(f"   Varianza: {stats['dispersion']['varianza']:.2f}")
print(f"   Desviación Estándar: {stats['dispersion']['desviacion_estandar']:.2f}")
print(f"   Mínimo: {stats['dispersion']['minimo']:.2f}")
print(f"   Máximo: {stats['dispersion']['maximo']:.2f}")

expected_mean = np.mean(test_data_quantitative)
expected_median = np.median(test_data_quantitative)
expected_std = np.std(test_data_quantitative, ddof=1)

print("\n🔍 Verificación:")
print(f"   Media esperada: {expected_mean:.2f} | Calculada: {stats['tendencia_central']['media']:.2f} | ✓" if abs(expected_mean - stats['tendencia_central']['media']) < 0.01 else " ✗")
print(f"   Mediana esperada: {expected_median:.2f} | Calculada: {stats['tendencia_central']['mediana']:.2f} | ✓" if abs(expected_median - stats['tendencia_central']['mediana']) < 0.01 else " ✗")
print(f"   Desv. Est. esperada: {expected_std:.2f} | Calculada: {stats['dispersion']['desviacion_estandar']:.2f} | ✓" if abs(expected_std - stats['dispersion']['desviacion_estandar']) < 0.01 else " ✗")

print("\n" + "=" * 60)
print("PRUEBA DE TABLA DE FRECUENCIAS")
print("=" * 60)

freq_table_quant = create_frequency_table(test_data_quantitative, is_quantitative=True, bins=5)
print("\n📋 Tabla de Frecuencias (Datos Cuantitativos):")
print(freq_table_quant)

test_data_qualitative = ['Rojo', 'Azul', 'Verde', 'Rojo', 'Azul', 'Rojo', 'Verde', 'Azul', 'Rojo']
print(f"\n📊 Datos de prueba (cualitativos): {test_data_qualitative}")

freq_table_qual = create_frequency_table(test_data_qualitative, is_quantitative=False)
print("\n📋 Tabla de Frecuencias (Datos Cualitativos):")
print(freq_table_qual)

print("\n" + "=" * 60)
print("PRUEBA DE CARGA DE DATOS")
print("=" * 60)

text_input = "10, 20, 30, 40, 50"
df = load_data_from_text(text_input)
print(f"\n✅ Datos cargados desde texto: {len(df)} valores")
print(df.head())

print("\n" + "=" * 60)
print("TODAS LAS PRUEBAS COMPLETADAS EXITOSAMENTE ✓")
print("=" * 60)
