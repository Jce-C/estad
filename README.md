# 📊 Aplicación Interactiva para el Análisis Descriptivo de Datos

## Proyecto Final - Estadística I (Ingeniería de Sistemas)

**Docente:** William C. Gutierrez Mejia  
**Tecnologías:** Python, Streamlit, Pandas, NumPy, Plotly, SciPy, OpenAI

---

## 🎯 Objetivo General

Desarrollar una aplicación web que permita analizar conjuntos de datos mediante el cálculo automático de medidas estadísticas y la generación de representaciones gráficas, integrando los conocimientos vistos en el curso de Estadística I.

---

## ✨ Características Principales

### 1. 📥 Ingreso de Datos
- **Ingreso Manual:** Permite escribir datos separados por comas, espacios o saltos de línea
- **Carga de Archivos:** Soporta formatos CSV, TXT y XLSX (Excel)
- **Ejemplos Precargados:** Incluye datos de muestra para demostración inmediata
- **Validación Automática:** Verifica la integridad de los datos ingresados

### 2. 🔍 Detección Automática de Tipo de Datos
- Utiliza inteligencia artificial (OpenAI GPT-5) para identificar automáticamente si los datos son:
  - **Cuantitativos:** Datos numéricos (discretos o continuos)
  - **Cualitativos:** Datos categóricos (nominales u ordinales)
- Modo de respaldo sin IA disponible

### 3. 📋 Generación de Tablas de Frecuencias
- Frecuencia Absoluta
- Frecuencia Relativa
- Frecuencia Porcentual
- Frecuencias Acumuladas
- Intervalos automáticos para datos cuantitativos (Regla de Sturges)

### 4. 📊 Cálculo de Medidas Estadísticas

**Medidas de Tendencia Central:**
- Media aritmética (x̄)
- Mediana
- Moda

**Medidas de Dispersión:**
- Rango
- Varianza (s²)
- Desviación Estándar (s)
- Coeficiente de Variación
- Cuartiles (Q1, Q3)
- Rango Intercuartílico (IQR)

### 5. 📈 Visualizaciones Interactivas

**Para Datos Cuantitativos:**
- Histogramas de distribución
- Diagramas de caja (Box Plot)
- Gráficos de frecuencia por intervalos

**Para Datos Cualitativos:**
- Gráficos de barras
- Gráficos circulares (Pie Chart)
- Gráficos de frecuencia por categorías

### 6. 🤖 Asistente de IA
- Interpretación automática de resultados estadísticos
- Respuestas a preguntas sobre el análisis
- Explicaciones educativas de conceptos estadísticos
- Análisis contextual de los datos

### 7. 💾 Exportación de Resultados
- Descarga de tablas de frecuencias en CSV
- Descarga de estadísticas calculadas en CSV
- Gráficos interactivos exportables

### 8. 🎨 Interfaz Intuitiva
- Diseño moderno y profesional
- Navegación por pestañas
- Indicadores visuales claros
- Completamente en español
- Manual de usuario integrado

---

## 🚀 Instalación y Configuración

### Requisitos Previos
- Python 3.11 o superior

### Dependencias

Las siguientes librerías están instaladas:
```
streamlit
pandas
numpy
matplotlib
seaborn
plotly
scipy
openpyxl
fpdf
openai
```

### Configuración Opcional de OpenAI

Para habilitar las funciones de IA (detección automática de tipos, interpretaciones), configura tu API key:

```bash
export OPENAI_API_KEY="tu-api-key-aqui"
```

**Nota:** La aplicación funciona perfectamente sin OpenAI, utilizando métodos estadísticos tradicionales.

---

## 📖 Cómo Usar la Aplicación

### 1. Iniciar la Aplicación

La aplicación se ejecuta automáticamente en el puerto 5000:
```
http://localhost:5000
```

### 2. Ingresar Datos

**Opción A - Manual:**
1. Ve a la pestaña "Ingreso de Datos"
2. Escribe tus datos en el área de texto
3. Separa los valores por comas, espacios o saltos de línea
4. Haz clic en "Analizar datos manuales"

**Opción B - Archivo:**
1. Haz clic en "Cargar desde Archivo"
2. Selecciona un archivo CSV, TXT o XLSX
3. Si tiene múltiples columnas, elige la que deseas analizar
4. Haz clic en "Analizar datos del archivo"

### 3. Ver Resultados

En la pestaña "Análisis y Resultados" encontrarás:
- Tipo de datos detectado
- Tabla de frecuencias completa
- Todas las medidas estadísticas
- Múltiples visualizaciones interactivas
- Interpretación con IA (si está habilitada)

### 4. Usar el Asistente de IA

En la pestaña "Asistente IA":
- Escribe preguntas sobre tus datos
- Solicita explicaciones de conceptos
- Pide interpretaciones adicionales

---

## 📁 Estructura del Proyecto

```
.
├── app.py                      # Aplicación principal Streamlit
├── stats_utils.py              # Funciones de cálculos estadísticos
├── data_processor.py           # Procesamiento y carga de datos
├── visualization.py            # Generación de gráficos
├── ai_helper.py                # Integración con OpenAI
├── create_examples.py          # Script para crear archivos de ejemplo
├── test_calculations.py        # Pruebas de verificación
├── ejemplos_datos/             # Directorio con archivos de ejemplo
│   ├── edades_estudiantes.csv
│   ├── calificaciones.csv
│   ├── colores_favoritos.csv
│   ├── nivel_satisfaccion.csv
│   ├── alturas.xlsx
│   └── ingresos.xlsx
└── README.md                   # Este archivo
```

---

## 🧪 Ejemplos de Uso

### Ejemplo 1: Análisis de Edades (Cuantitativo)

**Entrada:**
```
18, 19, 20, 18, 21, 19, 20, 22, 19, 18
```

**Resultados Esperados:**
- Tipo: Cuantitativo
- Media: 19.4
- Mediana: 19.0
- Moda: 18
- Desviación Estándar: ~1.35
- Visualización: Histograma + Diagrama de Caja

### Ejemplo 2: Análisis de Colores Favoritos (Cualitativo)

**Entrada:**
```
Azul, Rojo, Verde, Azul, Amarillo, Rojo, Azul
```

**Resultados Esperados:**
- Tipo: Cualitativo
- Tabla de frecuencias por categoría
- Moda: Azul
- Visualización: Gráfico de Barras + Gráfico Circular

---

## 🔧 Configuración Avanzada

### Eliminar Valores Atípicos
En la barra lateral, activa "Eliminar valores atípicos" para aplicar el método IQR y filtrar outliers automáticamente.

### Ajustar Número de Intervalos
Para datos cuantitativos, puedes ajustar el número de intervalos en la tabla de frecuencias usando el control deslizante (5-20 intervalos).

---

## 📊 Fórmulas Utilizadas

### Media Aritmética
```
x̄ = Σx / n
```

### Desviación Estándar Muestral
```
s = √[Σ(x - x̄)² / (n-1)]
```

### Varianza Muestral
```
s² = Σ(x - x̄)² / (n-1)
```

### Número de Intervalos (Regla de Sturges)
```
k = 1 + 3.322 * log₁₀(n)
```

---

## ✅ Criterios de Evaluación Cumplidos

| Criterio | Cumplimiento | Detalles |
|----------|--------------|----------|
| **Diseño del Programa** (25%) | ✅ | Estructura modular, validación de datos, manejo de errores |
| **Cálculos Estadísticos** (25%) | ✅ | Todas las fórmulas correctamente implementadas y verificadas |
| **Visualización de Resultados** (20%) | ✅ | Múltiples gráficos interactivos, tablas claras y exportables |
| **Interfaz y Usabilidad** (10%) | ✅ | Interfaz web intuitiva, navegación clara, ejemplos incluidos |
| **Informe y Documentación** (20%) | ✅ | README completo, código comentado, manual de usuario integrado |

---

## 🎓 Entregables

1. ✅ **Código Fuente con Comentarios:** Todos los archivos Python están documentados
2. ✅ **Manual de Usuario:** Incluido en la pestaña "Manual de Usuario" de la aplicación
3. ✅ **Informe Técnico:** Este README sirve como informe técnico con:
   - Descripción del problema
   - Metodología aplicada (módulos, librerías, algoritmos)
   - Resultados de ejemplo
   - Conclusiones

---

## 🏆 Conclusiones

Esta aplicación cumple con todos los requisitos del proyecto final de Estadística I:

1. **Funcionalidad Completa:** Ingreso manual y por archivos, detección automática de tipos, cálculos precisos, visualizaciones profesionales.

2. **Innovación:** Integración de IA para mejorar la experiencia del usuario y facilitar la interpretación de resultados.

3. **Usabilidad:** Interfaz web moderna y accesible que no requiere conocimientos técnicos.

4. **Extensibilidad:** Arquitectura modular que facilita agregar nuevas funcionalidades.

5. **Educación:** Manual integrado y asistente de IA que ayudan al aprendizaje de conceptos estadísticos.

La aplicación demuestra competencia en:
- Desarrollo de software (Python, Streamlit)
- Estadística descriptiva (cálculos y visualizaciones)
- Integración de tecnologías modernas (IA, gráficos interactivos)
- Diseño de interfaces de usuario
- Documentación técnica

---

## 📞 Soporte

Para preguntas o problemas:
1. Consulta el Manual de Usuario dentro de la aplicación
2. Revisa los ejemplos incluidos
3. Usa el Asistente de IA para aclaraciones

---

## 📄 Licencia

Proyecto académico desarrollado para el curso de Estadística I - Ingeniería de Sistemas

**Desarrollado con ❤️ usando Python y Streamlit**
