import pandas as pd
import numpy as np

edades_data = pd.DataFrame({
    'Edad': [18, 19, 20, 18, 21, 19, 20, 22, 19, 18, 20, 21, 19, 18, 20, 
             19, 21, 20, 19, 18, 22, 20, 19, 21, 20, 18, 19, 20, 21, 19]
})
edades_data.to_csv('ejemplos_datos/edades_estudiantes.csv', index=False)

calificaciones_data = pd.DataFrame({
    'Calificacion': [85, 90, 78, 92, 88, 76, 95, 82, 89, 91, 87, 84, 93, 79, 86, 
                     88, 90, 85, 91, 87, 83, 94, 77, 89, 92, 85, 88, 90, 86, 91]
})
calificaciones_data.to_csv('ejemplos_datos/calificaciones.csv', index=False)

colores_data = pd.DataFrame({
    'Color': ['Azul', 'Rojo', 'Verde', 'Azul', 'Amarillo', 'Rojo', 'Azul', 'Verde', 
              'Rojo', 'Azul', 'Amarillo', 'Verde', 'Azul', 'Rojo', 'Verde', 'Azul', 
              'Rojo', 'Amarillo', 'Azul', 'Verde', 'Rojo', 'Azul', 'Verde', 'Azul', 
              'Rojo', 'Verde', 'Azul', 'Amarillo', 'Rojo', 'Verde']
})
colores_data.to_csv('ejemplos_datos/colores_favoritos.csv', index=False)

satisfaccion_data = pd.DataFrame({
    'Nivel': ['Alto', 'Medio', 'Alto', 'Bajo', 'Medio', 'Alto', 'Alto', 'Medio', 
              'Bajo', 'Alto', 'Medio', 'Alto', 'Medio', 'Bajo', 'Alto', 'Medio', 
              'Alto', 'Alto', 'Medio', 'Bajo', 'Alto', 'Medio', 'Alto', 'Medio', 
              'Bajo', 'Alto', 'Medio', 'Alto', 'Alto', 'Medio']
})
satisfaccion_data.to_csv('ejemplos_datos/nivel_satisfaccion.csv', index=False)

alturas_data = pd.DataFrame({
    'Altura_cm': [165, 170, 168, 172, 175, 169, 171, 173, 167, 170, 174, 169, 
                  172, 168, 175, 171, 169, 173, 170, 172, 168, 174, 171, 169, 
                  173, 170, 172, 175, 168, 171]
})
alturas_data.to_excel('ejemplos_datos/alturas.xlsx', index=False)

ingresos_data = pd.DataFrame({
    'Ingreso_Mensual': [1200, 1500, 1350, 1800, 1450, 1600, 1700, 1400, 1550, 1650,
                        1750, 1500, 1600, 1450, 1800, 1550, 1700, 1600, 1500, 1650,
                        1400, 1750, 1550, 1600, 1700, 1450, 1800, 1650, 1500, 1550]
})
ingresos_data.to_excel('ejemplos_datos/ingresos.xlsx', index=False)

print("✅ Archivos de ejemplo creados exitosamente en el directorio 'ejemplos_datos/'")
print(f"   - edades_estudiantes.csv ({len(edades_data)} registros)")
print(f"   - calificaciones.csv ({len(calificaciones_data)} registros)")
print(f"   - colores_favoritos.csv ({len(colores_data)} registros)")
print(f"   - nivel_satisfaccion.csv ({len(satisfaccion_data)} registros)")
print(f"   - alturas.xlsx ({len(alturas_data)} registros)")
print(f"   - ingresos.xlsx ({len(ingresos_data)} registros)")
