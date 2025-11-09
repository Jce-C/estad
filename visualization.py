import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
import numpy as np
from typing import Union, List

def create_histogram(data: Union[List, pd.Series], title: str = "Histograma", bins: int = None) -> go.Figure:
    """
    Crea un histograma interactivo
    """
    if isinstance(data, list):
        data = pd.Series(data)
    
    try:
        data_numeric = pd.to_numeric(data, errors='coerce').dropna()
    except:
        data_numeric = data
    
    if bins is None:
        n = len(data_numeric)
        bins = min(int(1 + 3.322 * np.log10(n)), 20)
    
    fig = go.Figure(data=[go.Histogram(
        x=data_numeric,
        nbinsx=bins,
        marker_color='#1f77b4',
        opacity=0.75,
        name='Frecuencia'
    )])
    
    fig.update_layout(
        title=title,
        xaxis_title="Valores",
        yaxis_title="Frecuencia",
        showlegend=False,
        template="plotly_white",
        hovermode='x'
    )
    
    return fig

def create_bar_chart(data: Union[List, pd.Series], title: str = "Gráfico de Barras") -> go.Figure:
    """
    Crea un gráfico de barras para datos cualitativos
    """
    if isinstance(data, list):
        data = pd.Series(data)
    
    value_counts = data.value_counts().sort_values(ascending=False)
    
    fig = go.Figure(data=[go.Bar(
        x=value_counts.index.astype(str),
        y=value_counts.values,
        marker_color='#2ca02c',
        text=value_counts.values,
        textposition='auto'
    )])
    
    fig.update_layout(
        title=title,
        xaxis_title="Categorías",
        yaxis_title="Frecuencia",
        showlegend=False,
        template="plotly_white"
    )
    
    return fig

def create_pie_chart(data: Union[List, pd.Series], title: str = "Gráfico Circular") -> go.Figure:
    """
    Crea un gráfico circular (pie chart)
    """
    if isinstance(data, list):
        data = pd.Series(data)
    
    value_counts = data.value_counts()
    
    fig = go.Figure(data=[go.Pie(
        labels=value_counts.index.astype(str),
        values=value_counts.values,
        hole=0.3,
        textinfo='label+percent',
        textposition='auto'
    )])
    
    fig.update_layout(
        title=title,
        showlegend=True,
        template="plotly_white"
    )
    
    return fig

def create_box_plot(data: Union[List, pd.Series], title: str = "Diagrama de Caja") -> go.Figure:
    """
    Crea un diagrama de caja (box plot)
    """
    if isinstance(data, list):
        data = pd.Series(data)
    
    try:
        data_numeric = pd.to_numeric(data, errors='coerce').dropna()
    except:
        data_numeric = data
    
    fig = go.Figure(data=[go.Box(
        y=data_numeric,
        name='Datos',
        marker_color='#ff7f0e',
        boxmean='sd'
    )])
    
    fig.update_layout(
        title=title,
        yaxis_title="Valores",
        showlegend=False,
        template="plotly_white"
    )
    
    return fig

def create_frequency_bar_chart(freq_table: pd.DataFrame, is_quantitative: bool = True) -> go.Figure:
    """
    Crea un gráfico de barras desde una tabla de frecuencias
    """
    if is_quantitative:
        x_data = freq_table['Intervalo']
        title = "Distribución de Frecuencias (Intervalos)"
    else:
        x_data = freq_table['Categoría'].astype(str)
        title = "Distribución de Frecuencias (Categorías)"
    
    fig = go.Figure()
    
    fig.add_trace(go.Bar(
        x=x_data,
        y=freq_table['Frecuencia Absoluta'],
        name='Frecuencia Absoluta',
        marker_color='#1f77b4',
        text=freq_table['Frecuencia Absoluta'],
        textposition='auto'
    ))
    
    fig.update_layout(
        title=title,
        xaxis_title="Clases" if is_quantitative else "Categorías",
        yaxis_title="Frecuencia",
        template="plotly_white",
        showlegend=True
    )
    
    return fig

def create_multiple_visualizations(data: Union[List, pd.Series], data_type: str, freq_table: pd.DataFrame = None):
    """
    Crea múltiples visualizaciones según el tipo de datos
    """
    visualizations = {}
    
    is_quantitative = (data_type == "cuantitativo")
    
    if is_quantitative:
        visualizations['histogram'] = create_histogram(data, "Histograma de Distribución")
        visualizations['box_plot'] = create_box_plot(data, "Diagrama de Caja")
    else:
        visualizations['bar_chart'] = create_bar_chart(data, "Distribución de Categorías")
        visualizations['pie_chart'] = create_pie_chart(data, "Distribución Porcentual")
    
    if freq_table is not None:
        visualizations['freq_chart'] = create_frequency_bar_chart(freq_table, is_quantitative)
    
    return visualizations
