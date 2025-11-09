import os
import sys

if 'OPENAI_API_KEY' in os.environ:
    del os.environ['OPENAI_API_KEY']

from ai_helper import interpret_statistics, detect_data_type

print("=" * 60)
print("PRUEBA DE FALLBACK SIN OPENAI - DATOS CUALITATIVOS")
print("=" * 60)

test_data_qualitative = ['Rojo', 'Azul', 'Verde', 'Rojo', 'Azul', 'Rojo']

print(f"\n📊 Datos de prueba: {test_data_qualitative}")

print("\n🔍 Probando detección de tipo de datos sin OpenAI...")
data_type_info = detect_data_type(test_data_qualitative)
print(f"   Tipo: {data_type_info.get('tipo')}")
print(f"   Subtipo: {data_type_info.get('subtipo')}")
print(f"   Razón: {data_type_info.get('razon')}")

stats_data = {
    'tendencia_central': {
        'media': None,
        'mediana': None,
        'moda': 'Rojo'
    },
    'dispersion': {
        'desviacion_estandar': None,
        'varianza': None,
        'rango': None
    },
    'n': len(test_data_qualitative)
}

print("\n💬 Probando interpretación sin OpenAI (datos cualitativos)...")
try:
    interpretation = interpret_statistics(stats_data, 'cualitativo')
    print(f"   ✅ Interpretación generada correctamente:")
    print(f"   {interpretation}")
except Exception as e:
    print(f"   ❌ ERROR: {str(e)}")
    sys.exit(1)

print("\n🔍 Probando interpretación sin OpenAI (datos cuantitativos con None)...")
stats_data_quant_none = {
    'tendencia_central': {
        'media': None,
        'mediana': None,
        'moda': None
    },
    'dispersion': {
        'desviacion_estandar': None,
        'varianza': None,
        'rango': None
    },
    'n': 0
}

try:
    interpretation = interpret_statistics(stats_data_quant_none, 'cuantitativo')
    print(f"   ✅ Interpretación generada correctamente:")
    print(f"   {interpretation}")
except Exception as e:
    print(f"   ❌ ERROR: {str(e)}")
    sys.exit(1)

print("\n🔍 Probando interpretación sin OpenAI (datos cuantitativos válidos)...")
stats_data_quant_valid = {
    'tendencia_central': {
        'media': 25.5,
        'mediana': 24.0,
        'moda': 20.0
    },
    'dispersion': {
        'desviacion_estandar': 5.2,
        'varianza': 27.04,
        'rango': 20.0
    },
    'n': 30
}

try:
    interpretation = interpret_statistics(stats_data_quant_valid, 'cuantitativo')
    print(f"   ✅ Interpretación generada correctamente:")
    print(f"   {interpretation}")
except Exception as e:
    print(f"   ❌ ERROR: {str(e)}")
    sys.exit(1)

print("\n" + "=" * 60)
print("✅ TODAS LAS PRUEBAS DE FALLBACK PASARON EXITOSAMENTE")
print("=" * 60)
