import streamlit as st
import pandas as pd
import plotly.express as px
import random

# Configuración de página
st.set_page_config(
    page_title="Dashboard de Estudiantes",
    layout="wide"
)

# Paleta de colores
BEIGE = "#F3E6D5"
VINOTINTO = "#800020"
CORAL = "#D45060"
FONDO = "#FAF8F5"

# Estilos del dashboard
st.markdown("""
<style>
    .stApp {
        background-color: #FAF8F5;
    }

    h1, h2, h3 {
        color: #800020;
    }

    [data-testid="stSidebar"] {
        background-color: #F3E6D5;
    }

    div[data-testid="stMetric"] {
        background-color: #F3E6D5;
        padding: 18px;
        border-radius: 12px;
        border-left: 5px solid #800020;
    }

    .descripcion {
        color: #666666;
        font-size: 15px;
        margin-bottom: 20px;
    }
</style>
""", unsafe_allow_html=True)


# Cargar datos
ruta = 'database/Estudiantes_Matriculados_en_Programas_Académicos_-_Institución_Universitaria_Colegio_Mayor_de_Antioquia_20261126.csv'

df = pd.read_csv(ruta)


# Título principal
st.title("Dashboard de Estudiantes Matriculados")

st.markdown(
    '<p class="descripcion">Panel de análisis y caracterización de la población estudiantil.</p>',
    unsafe_allow_html=True
)


# Columnas para filtros y gráficos
columnas = [
    "TIPO INSCRIPCION",
    "PROGRAMA",
    "SEXO BIOLOGICO"
]


# Filtros laterales
st.sidebar.title("Filtros de búsqueda")

df_filtrado = df.copy()

for columna in columnas:

    categorias = ["Todos"] + sorted(
        df[columna].dropna().unique().tolist(),
        key=str
    )

    seleccion = st.sidebar.selectbox(
        columna.replace("_", " ").title(),
        categorias
    )

    if seleccion != "Todos":
        df_filtrado = df_filtrado[
            df_filtrado[columna] == seleccion
        ]


# Indicadores principales
st.subheader("Resumen general")

col1, col2, col3 = st.columns(3)

with col1:
    st.metric("Total de estudiantes", f"{len(df_filtrado):,}")

with col2:
    st.metric("Programas académicos", df_filtrado["PROGRAMA"].nunique())

with col3:
    st.metric("Tipos de inscripción", df_filtrado["TIPO INSCRIPCION"].nunique())


# Textos aleatorios por categoría
descripciones = {
    "inscripcion": [
        "Cada modalidad representa una forma de ingreso a la institución.",
        "Conoce cómo se distribuyen las modalidades de inscripción.",
        "Las inscripciones permiten analizar las formas de acceso académico."
    ],

    "programa": [
        "Descubre cómo se distribuyen los estudiantes entre los programas.",
        "Cada programa representa una oportunidad de formación profesional.",
        "Conoce cuáles son los programas con mayor presencia estudiantil."
    ],

    "sexo": [
        "Observa la composición de la población estudiantil registrada.",
        "Este indicador permite conocer la distribución por sexo biológico.",
        "Explora las frecuencias registradas en esta categoría."
    ]
}

# Mantener los textos durante la sesión
if "descripciones" not in st.session_state:
    st.session_state.descripciones = {
        clave: random.choice(textos)
        for clave, textos in descripciones.items()
    }


# Configuración general de gráficos
configuracion = {
    "plot_bgcolor": FONDO,
    "paper_bgcolor": FONDO,
    "font": dict(
        family="Arial",
        color=VINOTINTO,
        size=12
    ),
    "margin": dict(l=30, r=30, t=50, b=30)
}


# Crear pestañas
tab1, tab2, tab3 = st.tabs([
    "Tipo de inscripción",
    "Programa académico",
    "Sexo biológico"
])


# PESTAÑA 1: TIPO DE INSCRIPCIÓN
with tab1:

    st.subheader("Distribución por tipo de inscripción")

    st.markdown(
        f'<p class="descripcion">{st.session_state.descripciones["inscripcion"]}</p>',
        unsafe_allow_html=True
    )

    datos = (
        df_filtrado["TIPO INSCRIPCION"]
        .fillna("Sin dato")
        .value_counts()
        .reset_index()
    )

    datos.columns = ["Categoría", "Cantidad"]

    fig1 = px.pie(
        datos,
        names="Categoría",
        values="Cantidad",
        hole=0.60,
        color_discrete_sequence=[VINOTINTO, CORAL, BEIGE]
    )

    fig1.update_traces(
        textposition="inside",
        textinfo="percent+label",
        marker=dict(line=dict(color=FONDO, width=3)),
        hovertemplate="<b>%{label}</b><br>Estudiantes: %{value:,}<br>Porcentaje: %{percent}<extra></extra>"
    )

    fig1.update_layout(
        **configuracion,
        height=450,
        showlegend=True,
        legend_title_text="Tipo de inscripción"
    )

    st.plotly_chart(fig1, use_container_width=True)


# PESTAÑA 2: PROGRAMA ACADÉMICO
with tab2:

    st.subheader("Distribución por programa académico")

    st.markdown(
        f'<p class="descripcion">{st.session_state.descripciones["programa"]}</p>',
        unsafe_allow_html=True
    )

    datos = (
        df_filtrado["PROGRAMA"]
        .fillna("Sin dato")
        .value_counts()
        .reset_index()
    )

    datos.columns = ["Programa", "Cantidad"]

    datos = datos.sort_values("Cantidad", ascending=True)

    fig2 = px.bar(
        datos,
        x="Cantidad",
        y="Programa",
        orientation="h",
        color="Cantidad",
        color_continuous_scale=[BEIGE, CORAL, VINOTINTO],
        text="Cantidad"
    )

    fig2.update_traces(
        textposition="outside",
        marker_line_width=0,
        hovertemplate="<b>%{y}</b><br>Estudiantes: %{x:,}<extra></extra>"
    )

    fig2.update_layout(
        **configuracion,
        coloraxis_showscale=False,
        xaxis_title="Cantidad de estudiantes",
        yaxis_title="",
        height=max(450, len(datos) * 30)
    )

    fig2.update_layout(
        margin=dict(l=30, r=65, t=50, b=40)
    )

    st.plotly_chart(fig2, use_container_width=True)


# PESTAÑA 3: SEXO BIOLÓGICO
with tab3:

    st.subheader("Distribución por sexo biológico")

    st.markdown(
        f'<p class="descripcion">{st.session_state.descripciones["sexo"]}</p>',
        unsafe_allow_html=True
    )

    datos = (
        df_filtrado["SEXO BIOLOGICO"]
        .fillna("Sin dato")
        .value_counts()
        .reset_index()
    )

    datos.columns = ["Categoría", "Cantidad"]

    fig3 = px.pie(
        datos,
        names="Categoría",
        values="Cantidad",
        hole=0.60,
        color_discrete_sequence=[VINOTINTO, CORAL, BEIGE]
    )

    fig3.update_traces(
        textposition="inside",
        textinfo="percent+label",
        marker=dict(line=dict(color=FONDO, width=3)),
        hovertemplate="<b>%{label}</b><br>Estudiantes: %{value:,}<br>Porcentaje: %{percent}<extra></extra>"
    )

    fig3.update_layout(
        **configuracion,
        height=450,
        showlegend=True,
        legend_title_text="Sexo biológico"
    )

    st.plotly_chart(fig3, use_container_width=True)


# Tabla oculta
with st.expander("Consultar tabla de datos"):

    st.dataframe(
        df_filtrado,
        use_container_width=True,
        hide_index=True
    )
