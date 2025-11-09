import streamlit as st
import streamlit.components.v1 as components
import pandas as pd
import numpy as np
from io import BytesIO
import base64
from streamlit_float import *

from stats_utils import calculate_all_statistics, calculate_central_tendency, calculate_dispersion
from data_processor import load_data_from_text, load_data_from_file, create_frequency_table, validate_data, clean_data
from visualization import create_multiple_visualizations, create_histogram, create_bar_chart, create_pie_chart, create_box_plot
from ai_helper import detect_data_type, interpret_statistics, answer_question

st.set_page_config(
    page_title="Análisis Estadístico Descriptivo",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

if 'chat_messages' not in st.session_state:
    st.session_state['chat_messages'] = []
if 'chat_open' not in st.session_state:
    st.session_state['chat_open'] = False

st.markdown("""
<style>
    /* Mover la barra lateral a la derecha */
    [data-testid="stSidebar"] {
        right: 0 !important;
        left: auto !important;
        border-right: none !important;
        border-left: 1px solid #f0f2f6 !important;
    }

    /* Ajustar la posición del botón para colapsar la barra lateral si es visible */
    [data-testid="stSidebarCollapseButton"] {
        right: 20px !important;
        left: auto !important;
    }
    
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 0.5rem;
    }
    .sub-header {
        font-size: 1.2rem;
        color: #666;
        text-align: center;
        margin-bottom: 2rem;
    }
    .stat-card {
        background-color: #f0f2f6;
        border-radius: 10px;
        padding: 1rem;
        margin: 0.5rem 0;
    }
    .metric-value {
        font-size: 1.8rem;
        font-weight: bold;
        color: #1f77b4;
    }
    .metric-label {
        font-size: 0.9rem;
        color: #666;
        margin-bottom: 0.3rem;
    }
    
    .chat-window {
        position: fixed;
        bottom: 90px;
        left: 20px;
        width: 380px;
        max-height: 500px;
        background: white;
        border-radius: 15px;
        box-shadow: 0 8px 24px rgba(0,0,0,0.2);
        z-index: 9998;
        display: none;
        flex-direction: column;
    }
    
    .chat-window.open {
        display: flex;
    }
    
    .chat-header {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 15px;
        border-radius: 15px 15px 0 0;
        font-weight: bold;
        display: flex;
        justify-content: space-between;
        align-items: center;
    }
    
    .chat-bubble-btn {
        position: fixed;
        bottom: 20px;
        left: 20px;
        z-index: 9999;
        width: 60px;
        height: 60px;
        border-radius: 50%;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        border: none;
        cursor: pointer;
        display: flex;
        align-items: center;
        justify-content: center;
        box-shadow: 0 4px 12px rgba(0,0,0,0.15);
        transition: transform 0.3s;
    }
    
    .chat-bubble-btn:hover {
        transform: scale(1.1);
    }
    
    .chat-icon {
        font-size: 30px;
        color: white;
    }
    
    .results-anchor {
        scroll-margin-top: 100px;
    }
</style>
""", unsafe_allow_html=True)

def get_example_data():
    """Retorna ejemplos de datos para demostración"""
    examples = {
        "Edades de estudiantes (cuantitativo)": "18, 19, 20, 18, 21, 19, 20, 22, 19, 18, 20, 21, 19, 18, 20, 19, 21, 20, 19, 18, 22, 20, 19, 21, 20",
        "Calificaciones (cuantitativo)": "85, 90, 78, 92, 88, 76, 95, 82, 89, 91, 87, 84, 93, 79, 86, 88, 90, 85, 91, 87",
        "Colores favoritos (cualitativo)": "Azul, Rojo, Verde, Azul, Amarillo, Rojo, Azul, Verde, Rojo, Azul, Amarillo, Verde, Azul, Rojo, Verde, Azul, Rojo, Amarillo, Azul, Verde",
        "Nivel de satisfacción (cualitativo ordinal)": "Alto, Medio, Alto, Bajo, Medio, Alto, Alto, Medio, Bajo, Alto, Medio, Alto, Medio, Bajo, Alto, Medio, Alto, Alto, Medio, Bajo"
    }
    return examples

def export_to_csv(df, filename="resultados.csv"):
    """Exporta un DataFrame a CSV"""
    return df.to_csv(index=False).encode('utf-8')

def render_go_to_results_button():
    """Renderiza un botón flotante para ir a resultados cuando hay datos"""
    if 'data' in st.session_state:
        components.html("""
        <script>
        function scrollToResults() {
            const resultsSection = window.parent.document.getElementById('results-section');
            if (resultsSection) {
                resultsSection.scrollIntoView({ behavior: 'smooth', block: 'start' });
            }
        }
        </script>
        <button onclick="scrollToResults()" style="
            position: fixed;
            bottom: 20px;
            right: 20px;
            z-index: 99999;
            background: #1f77b4;
            color: white;
            padding: 12px 24px;
            border-radius: 25px;
            box-shadow: 0 4px 12px rgba(31, 119, 180, 0.4);
            cursor: pointer;
            font-weight: bold;
            border: none;
            transition: all 0.3s;
            font-size: 14px;
        " onmouseover="this.style.background='#1565c0'; this.style.transform='translateY(-2px)'; this.style.boxShadow='0 6px 20px rgba(31, 119, 180, 0.6)'" 
           onmouseout="this.style.background='#1f77b4'; this.style.transform='translateY(0)'; this.style.boxShadow='0 4px 12px rgba(31, 119, 180, 0.4)'">
            📊 Ver Análisis
        </button>
        """, height=0)

def render_floating_chat_button():
    """Renderiza el botón flotante de chat - siempre visible en pantalla usando método simple"""
    chat_button_container = st.container()
    with chat_button_container:
        col1, col2, col3 = st.columns([1, 20, 1])
        with col1:
            if st.button("💬" if not st.session_state.get('chat_open', False) else "✕", 
                         key="chat_toggle_btn", 
                         help="Asistente IA"):
                st.session_state['chat_open'] = not st.session_state.get('chat_open', False)
                st.rerun()
    
    chat_button_container.float("position: fixed; bottom: 20px; left: 20px; width: 60px; z-index: 99999; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); border-radius: 50%; box-shadow: 0 4px 16px rgba(102, 126, 234, 0.4);")

def render_floating_chat_window():
    """Renderiza la ventana flotante de chat cuando está abierta"""
    if not st.session_state.get('chat_open', False):
        return
    
    st.markdown("---")
    st.markdown("### 💬 Asistente IA")
    st.caption("Pregúntame sobre cómo usar la aplicación o sobre tus datos")
    
    for msg in st.session_state.get('chat_messages', []):
        with st.chat_message(msg['role']):
            st.write(msg['content'])
    
    if prompt := st.chat_input("Escribe tu pregunta aquí..."):
        st.session_state['chat_messages'].append({'role': 'user', 'content': prompt})
        
        if 'data' in st.session_state:
            context = {
                'tipo_datos': st.session_state.get('data_type_info', {}),
                'estadisticas': st.session_state.get('statistics', {}),
                'n_valores': len(st.session_state['data'])
            }
            response = answer_question(prompt, context)
        else:
            response = "Puedo ayudarte con lo siguiente:\n- Cómo usar la aplicación\n- Entender conceptos estadísticos\n- Interpretar resultados\n\nPrimero ingresa algunos datos para un análisis más específico."
        
        st.session_state['chat_messages'].append({'role': 'assistant', 'content': response})
        st.rerun()
    
    if st.session_state.get('chat_messages'):
        if st.button("🗑️ Limpiar conversación", use_container_width=True):
            st.session_state['chat_messages'] = []
            st.rerun()

def main():
    float_init()
    
    st.markdown('<div class="main-header">📊 Aplicación de Análisis Estadístico Descriptivo</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-header">Proyecto Final - Estadística I | Ingeniería de Sistemas</div>', unsafe_allow_html=True)
    
    with st.sidebar:
        st.header("ℹ️ Información del Proyecto")
        st.markdown("""
        **Equipo:** Análisis Estadístico Pro
        
        **Descripción:**
        Esta aplicación permite analizar conjuntos de datos mediante:
        - ✅ Ingreso manual o desde archivos
        - ✅ Detección automática de tipo de datos
        - ✅ Cálculo de estadísticas descriptivas
        - ✅ Generación de tablas de frecuencia
        - ✅ Visualizaciones interactivas
        - ✅ Asistente de IA para interpretación
        
        **Docente:** William C. Gutierrez Mejia
        
        **Desarrollado con:** Python, Streamlit, OpenAI
        """)
        
        st.divider()
        
        st.header("🔧 Configuración")
        show_ai_features = st.checkbox("Activar funciones de IA", value=True, help="Requiere OPENAI_API_KEY configurada")
        remove_outliers = st.checkbox("Eliminar valores atípicos", value=False, help="Aplica método IQR para eliminar outliers")
    
    tabs = st.tabs(["🏠 Inicio", "📖 Manual de Usuario"])
    
    with tabs[0]:
        if 'data' in st.session_state:
            st.success("✅ Datos cargados. Desplázate hacia abajo para ver el análisis completo o haz clic en el botón que aparece abajo.")
        
        st.header("Ingreso de Datos")
        
        col1, col2 = st.columns([1, 1])
        
        with col1:
            st.subheader("📝 Ingreso Manual")
            
            manual_input = st.text_area(
                "Ingresa los datos separados por comas, espacios o saltos de línea:",
                value="",
                height=200,
                help="Ejemplo: 10, 20, 30, 40 o una lista de categorías",
                key="manual_input_area"
            )
            
            if st.button("📊 Analizar datos manuales", type="primary", use_container_width=True):
                if manual_input.strip():
                    try:
                        df = load_data_from_text(manual_input)
                        st.session_state['data'] = df
                        st.session_state['data_source'] = "Manual"
                        st.success(f"✅ Datos cargados correctamente: {len(df)} valores")
                        st.rerun()
                    except Exception as e:
                        st.error(f"❌ Error al procesar los datos: {str(e)}")
                else:
                    st.warning("⚠️ Por favor, ingresa algunos datos")
            
            st.divider()
            
            st.subheader("📚 Ejemplos de Datos")
            examples = get_example_data()
            selected_example = st.selectbox(
                "Selecciona un ejemplo para cargar:",
                ["Selecciona..."] + list(examples.keys()),
                key="example_selector"
            )
            
            if selected_example and selected_example != "Selecciona...":
                if st.button("📥 Cargar ejemplo", use_container_width=True):
                    try:
                        df = load_data_from_text(examples[selected_example])
                        st.session_state['data'] = df
                        st.session_state['data_source'] = f"Ejemplo: {selected_example}"
                        st.success(f"✅ Ejemplo cargado: {len(df)} valores")
                        st.rerun()
                    except Exception as e:
                        st.error(f"❌ Error al cargar el ejemplo: {str(e)}")
        
        with col2:
            st.subheader("📁 Cargar desde Archivo")
            
            uploaded_file = st.file_uploader(
                "Sube un archivo CSV, TXT o XLSX:",
                type=['csv', 'txt', 'xlsx', 'xls'],
                help="El archivo debe contener datos en columnas"
            )
            
            if uploaded_file is not None:
                file_type = uploaded_file.name.split('.')[-1].lower()
                
                try:
                    df = load_data_from_file(uploaded_file, file_type)
                    st.success(f"✅ Archivo cargado: {uploaded_file.name}")
                    
                    st.write("**Vista previa del archivo:**")
                    st.dataframe(df.head(10), use_container_width=True)
                    
                    if len(df.columns) > 1:
                        selected_column = st.selectbox(
                            "Selecciona la columna a analizar:",
                            df.columns
                        )
                    else:
                        selected_column = df.columns[0]
                    
                    if st.button("📊 Analizar datos del archivo", type="primary", use_container_width=True):
                        analysis_df = pd.DataFrame({'valores': df[selected_column]})
                        st.session_state['data'] = analysis_df
                        st.session_state['data_source'] = f"Archivo: {uploaded_file.name} (columna: {selected_column})"
                        st.success(f"✅ Datos listos para analizar: {len(analysis_df)} valores")
                        st.rerun()
                        
                except Exception as e:
                    st.error(f"❌ Error al cargar el archivo: {str(e)}")
        
        st.divider()
        
        if 'data' in st.session_state:
            st.markdown('<div id="results-section" class="results-anchor"></div>', unsafe_allow_html=True)
            st.header("📊 Análisis de Datos")
            
            df = st.session_state['data']
            data_series = clean_data(df['valores'], remove_outliers=remove_outliers)
            
            if len(data_series) == 0:
                st.error("❌ No hay datos válidos para analizar después de la limpieza")
                return
            
            st.success(f"📂 Fuente: {st.session_state.get('data_source', 'Desconocida')}")
            st.info(f"📈 Total de valores: {len(data_series)}")
            
            if remove_outliers and len(data_series) < len(df):
                st.warning(f"⚠️ Se eliminaron {len(df) - len(data_series)} valores atípicos")
            
            with st.spinner("🔍 Detectando tipo de datos..."):
                if show_ai_features:
                    data_type_info = detect_data_type(data_series.tolist())
                    data_type = data_type_info.get('tipo', 'cualitativo')
                    st.session_state['data_type_info'] = data_type_info
                else:
                    try:
                        pd.to_numeric(data_series, errors='raise')
                        data_type = 'cuantitativo'
                        data_type_info = {'tipo': 'cuantitativo', 'razon': 'Datos numéricos', 'subtipo': 'continuo'}
                    except:
                        data_type = 'cualitativo'
                        data_type_info = {'tipo': 'cualitativo', 'razon': 'Datos categóricos', 'subtipo': 'nominal'}
                    st.session_state['data_type_info'] = data_type_info
            
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Tipo de Datos", data_type.capitalize())
            with col2:
                st.metric("Subtipo", data_type_info.get('subtipo', 'N/A').capitalize())
            with col3:
                st.metric("Cantidad", len(data_series))
            
            if show_ai_features:
                st.info(f"💡 **Razón:** {data_type_info.get('razon', 'N/A')}")
            
            st.divider()
            
            st.subheader("📋 Tabla de Frecuencias")
            is_quantitative = (data_type == 'cuantitativo')
            
            if is_quantitative:
                num_bins = st.slider("Número de intervalos:", min_value=5, max_value=20, value=10)
            else:
                num_bins = None
            
            freq_table = create_frequency_table(data_series, is_quantitative, bins=num_bins)
            st.dataframe(freq_table, use_container_width=True)
            
            csv_freq = export_to_csv(freq_table)
            st.download_button(
                label="📥 Descargar Tabla de Frecuencias (CSV)",
                data=csv_freq,
                file_name="tabla_frecuencias.csv",
                mime="text/csv"
            )
            
            st.divider()
            
            if is_quantitative:
                st.subheader("📊 Medidas Estadísticas")
                
                stats = calculate_all_statistics(data_series)
                st.session_state['statistics'] = stats
                
                col1, col2 = st.columns(2)
                
                with col1:
                    st.markdown("### 📍 Medidas de Tendencia Central")
                    central = stats['tendencia_central']
                    
                    metrics_col1, metrics_col2, metrics_col3 = st.columns(3)
                    with metrics_col1:
                        if central['media'] is not None:
                            st.metric("Media (x̄)", f"{central['media']:.4f}")
                    with metrics_col2:
                        if central['mediana'] is not None:
                            st.metric("Mediana", f"{central['mediana']:.4f}")
                    with metrics_col3:
                        if central['moda'] is not None:
                            st.metric("Moda", f"{central['moda']:.4f}")
                            st.caption(f"Frecuencia: {central['frecuencia_moda']}")
                
                with col2:
                    st.markdown("### 📏 Medidas de Dispersión")
                    dispersion = stats['dispersion']
                    
                    metrics_col1, metrics_col2 = st.columns(2)
                    with metrics_col1:
                        if dispersion['rango'] is not None:
                            st.metric("Rango", f"{dispersion['rango']:.4f}")
                        if dispersion['varianza'] is not None:
                            st.metric("Varianza (s²)", f"{dispersion['varianza']:.4f}")
                        if dispersion['desviacion_estandar'] is not None:
                            st.metric("Desv. Estándar (s)", f"{dispersion['desviacion_estandar']:.4f}")
                    
                    with metrics_col2:
                        if dispersion['minimo'] is not None:
                            st.metric("Mínimo", f"{dispersion['minimo']:.4f}")
                        if dispersion['maximo'] is not None:
                            st.metric("Máximo", f"{dispersion['maximo']:.4f}")
                        if dispersion['coeficiente_variacion'] is not None:
                            st.metric("Coef. Variación", f"{dispersion['coeficiente_variacion']:.2f}%")
                
                st.markdown("### 📦 Información Adicional")
                col1, col2, col3, col4 = st.columns(4)
                with col1:
                    st.metric("Q1 (25%)", f"{dispersion['q1']:.4f}")
                with col2:
                    st.metric("Q3 (75%)", f"{dispersion['q3']:.4f}")
                with col3:
                    st.metric("IQR", f"{dispersion['rango_intercuartil']:.4f}")
                with col4:
                    st.metric("N", stats['n'])
                
                stats_summary = pd.DataFrame({
                    'Estadística': ['Media', 'Mediana', 'Moda', 'Desv. Estándar', 'Varianza', 'Rango', 'Mínimo', 'Máximo'],
                    'Valor': [
                        central['media'],
                        central['mediana'],
                        central['moda'],
                        dispersion['desviacion_estandar'],
                        dispersion['varianza'],
                        dispersion['rango'],
                        dispersion['minimo'],
                        dispersion['maximo']
                    ]
                })
                
                csv_stats = export_to_csv(stats_summary)
                st.download_button(
                    label="📥 Descargar Estadísticas (CSV)",
                    data=csv_stats,
                    file_name="estadisticas.csv",
                    mime="text/csv"
                )
            
            st.divider()
            
            st.subheader("📈 Visualizaciones")
            
            visualizations = create_multiple_visualizations(data_series, data_type, freq_table)
            
            if is_quantitative:
                viz_col1, viz_col2 = st.columns(2)
                
                with viz_col1:
                    if 'histogram' in visualizations:
                        st.plotly_chart(visualizations['histogram'], use_container_width=True)
                    if 'freq_chart' in visualizations:
                        st.plotly_chart(visualizations['freq_chart'], use_container_width=True)
                
                with viz_col2:
                    if 'box_plot' in visualizations:
                        st.plotly_chart(visualizations['box_plot'], use_container_width=True)
            else:
                viz_col1, viz_col2 = st.columns(2)
                
                with viz_col1:
                    if 'bar_chart' in visualizations:
                        st.plotly_chart(visualizations['bar_chart'], use_container_width=True)
                
                with viz_col2:
                    if 'pie_chart' in visualizations:
                        st.plotly_chart(visualizations['pie_chart'], use_container_width=True)
                
                if 'freq_chart' in visualizations:
                    st.plotly_chart(visualizations['freq_chart'], use_container_width=True)
            
            if show_ai_features and is_quantitative:
                st.divider()
                st.subheader("🤖 Interpretación con IA")
                
                with st.spinner("Generando interpretación..."):
                    interpretation = interpret_statistics(stats, data_type)
                    st.info(interpretation)
                    st.session_state['interpretation'] = interpretation
        else:
            st.info("👆 Por favor, ingresa datos en la sección superior para comenzar el análisis")
            
            st.markdown("### 📚 Ejemplo de salida esperada")
            st.markdown("""
            Una vez que ingreses datos, verás:
            1. **Información del conjunto de datos** - tipo, cantidad de valores
            2. **Tabla de frecuencias** - distribución de los datos
            3. **Medidas de tendencia central** - media, mediana, moda
            4. **Medidas de dispersión** - rango, desviación estándar, varianza
            5. **Visualizaciones** - gráficos interactivos
            6. **Interpretación con IA** - análisis automático de resultados
            """)
        
    
    with tabs[1]:
        st.header("📖 Manual de Usuario")
        
        st.markdown("""
        ## 🎯 Objetivo
        
        Esta aplicación permite analizar conjuntos de datos mediante el cálculo automático de medidas 
        estadísticas y la generación de representaciones gráficas.
        
        ## 🚀 Cómo usar la aplicación
        
        ### 1️⃣ Ingreso de Datos
        
        **Opción A: Ingreso Manual**
        - Escribe o pega tus datos separados por comas, espacios o saltos de línea
        - Haz clic en "Analizar datos manuales"
        
        **Opción B: Usar Ejemplos**
        - Selecciona uno de los ejemplos precargados
        - Haz clic en "Cargar ejemplo"
        
        **Opción C: Cargar Archivo**
        - Formatos soportados: CSV, TXT, XLSX (Excel)
        - Arrastra y suelta tu archivo o haz clic para buscarlo
        - Si el archivo tiene varias columnas, selecciona la que deseas analizar
        - Haz clic en "Analizar datos del archivo"
        
        ### 2️⃣ Análisis de Datos
        
        Una vez cargados los datos, automáticamente verás:
        
        **Detección automática del tipo:**
        - **Cuantitativo**: Datos numéricos (edades, alturas, calificaciones)
        - **Cualitativo**: Datos categóricos (colores, géneros, niveles)
        
        **Tabla de Frecuencias:**
        - Frecuencia absoluta: cantidad de veces que aparece cada valor
        - Frecuencia relativa: proporción del total
        - Frecuencia porcentual: porcentaje del total
        - Frecuencias acumuladas
        
        **Para datos cuantitativos:**
        - Media (promedio)
        - Mediana (valor central)
        - Moda (valor más frecuente)
        - Desviación estándar (dispersión)
        - Varianza
        - Rango (diferencia entre máximo y mínimo)
        
        **Gráficos interactivos:**
        - Histogramas
        - Diagramas de caja
        - Gráficos de barras
        - Gráficos circulares
        
        ### 3️⃣ Asistente de IA (Burbuja Flotante)
        
        - Haz clic en el botón morado en la esquina inferior izquierda
        - Pregunta sobre tus resultados
        - Solicita interpretaciones
        - Pide ayuda sobre cómo usar la aplicación
        
        ### 4️⃣ Exportar Resultados
        
        - Descarga las tablas de frecuencias en formato CSV
        - Descarga las estadísticas calculadas
        
        ## 💡 Consejos
        
        - Usa datos limpios sin valores faltantes para mejores resultados
        - Para datos cuantitativos, todos los valores deben ser numéricos
        - Puedes activar/desactivar la eliminación de valores atípicos en la barra lateral
        - Las funciones de IA requieren una API key de OpenAI configurada
        
        ## 📊 Ejemplo de uso
        
        **Entrada (edades):**
        ```
        18, 19, 20, 18, 21, 19, 20, 22, 19, 18
        ```
        
        **Salida esperada:**
        - Tipo: Cuantitativo
        - Media: 19.4
        - Mediana: 19.0
        - Moda: 18
        - Desviación estándar: ~1.35
        - Gráficos: Histograma y diagrama de caja
        
        ## ⚙️ Configuración
        
        En la barra lateral (derecha) puedes:
        - Activar/desactivar funciones de IA
        - Eliminar valores atípicos automáticamente
        
        ## 📧 Información del Proyecto
        
        **Curso:** Estadística I - Ingeniería de Sistemas
        **Docente:** William C. Gutierrez Mejia
        **Tecnologías:** Python, Streamlit, Pandas, NumPy, Plotly, OpenAI
        
        ## ❓ Solución de problemas
        
        - **Error al cargar archivo**: Verifica que el formato sea CSV, TXT o XLSX
        - **No se calculan estadísticas**: Asegúrate de que los datos sean numéricos para análisis cuantitativo
        - **IA no responde**: Verifica que la API key de OpenAI esté configurada correctamente
        """)
        
        st.divider()
        
        st.markdown("### 🎓 Conceptos Estadísticos")
        
        with st.expander("📍 Medidas de Tendencia Central"):
            st.markdown("""
            - **Media**: Promedio aritmético de todos los valores
            - **Mediana**: Valor que divide el conjunto de datos en dos partes iguales
            - **Moda**: Valor que aparece con mayor frecuencia
            """)
        
        with st.expander("📏 Medidas de Dispersión"):
            st.markdown("""
            - **Rango**: Diferencia entre el valor máximo y mínimo
            - **Varianza**: Promedio de las desviaciones cuadradas respecto a la media
            - **Desviación Estándar**: Raíz cuadrada de la varianza, indica dispersión promedio
            - **Coeficiente de Variación**: Desviación estándar relativa a la media (en %)
            """)
        
        with st.expander("📊 Tipos de Gráficos"):
            st.markdown("""
            - **Histograma**: Muestra la distribución de datos cuantitativos en intervalos
            - **Diagrama de Caja**: Visualiza cuartiles, mediana y valores atípicos
            - **Gráfico de Barras**: Compara frecuencias de categorías
            - **Gráfico Circular**: Muestra proporciones en forma de pastel
            """)
    
    render_go_to_results_button()
    render_floating_chat_button()
    render_floating_chat_window()


if __name__ == "__main__":
    main()
