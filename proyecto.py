import streamlit as st
import pandas as pd
import plotly.express as px
df = pd.read_csv("https://raw.githubusercontent.com/Daorsegu/datos-definitivos/refs/heads/main/Data%20definitiva%20proyecto.csv")
df.columns = df.columns.str.strip()
st.title("📶 Análisis del crecimiento de Internet en Colombia por departamento")
# 📅 Resumen por Año (Nuevo)
st.subheader("Resumen por año")
df_resumen = df.groupby("Año").agg(
    Total_Accesos=("Número de accesos a internet", "sum"),
    Penetracion_Promedio=("Penetración", "mean"),
    Departamentos_Registrados=("Departamento", "nunique")
).reset_index()
df_resumen["Total_Accesos"] = df_resumen["Total_Accesos"].apply(lambda x: f"{int(x):,}")
df_resumen["Penetracion_Promedio"] = df_resumen["Penetracion_Promedio"].round(2)
st.dataframe(df_resumen)
# Selección de año
years = sorted(df["Año"].unique())
selected_year = st.selectbox("Selecciona un año:", years)
# Filtrar datos por año
df_year = df[df["Año"] == selected_year]
# 📊 Indicadores Clave
st.subheader("📊 Indicadores Clave")
total_accesos = int(df_year["Número de accesos a internet"].sum())
penetracion_prom = round(df_year["Penetración"].mean(), 2)
depto_max = df_year.loc[df_year["Número de accesos a internet"].idxmax()]
depto_min = df_year.loc[df_year["Número de accesos a internet"].idxmin()]
col1, col2, col3 = st.columns(3)
col1.metric("Accesos totales en Colombia", f"{total_accesos:,}")
col2.metric("Penetración promedio (%)", f"{penetracion_prom} %")
col3.metric("Depto con más accesos", f"{depto_max['Departamento']} ({depto_max['Número de accesos a internet']:,})")
col4, _ = st.columns(2)
col4.metric("Depto con menos accesos", f"{depto_min['Departamento']} ({depto_min['Número de accesos a internet']:,})")
# 📌 Top Departamentos por Accesos
st.subheader(f"🏆 Top departamentos por accesos en {selected_year}")
df_grouped = df_year.groupby("Departamento")["Número de accesos a internet"].sum().reset_index()
df_sorted = df_grouped.sort_values(by="Número de accesos a internet", ascending=False)
top_5_mas = df_sorted.head(5)
top_5_menos = df_sorted.tail(5)
col1, col2 = st.columns(2)
with col1:
    st.markdown("### 🔝 Más accesos")
    st.dataframe(top_5_mas.reset_index(drop=True))
with col2:
    st.markdown("### 🔻 Menos accesos")
    st.dataframe(top_5_menos.reset_index(drop=True))
# Un solo gráfico para top 10
st.subheader(f" Numero de accesos totales por departamento {selected_year}")
top_33 = df_sorted.head(34)
fig_top33 = px.bar(
    top_33,
    x="Número de accesos a internet",
    y="Departamento",
    orientation="h",
    title="Numero de accesos totales por departamento",
    labels={"Número de accesos a internet": "Accesos a Internet"},
    color="Departamento"
)
st.plotly_chart(fig_top33)
# 📈 Evolución en el tiempo
st.subheader("📈 Evolución de accesos por departamentos")
selected_deptos = st.multiselect(
    "Selecciona departamentos:",
    df["Departamento"].unique(),
    default=df["Departamento"].unique()[:5]
)
df_deptos = df[df["Departamento"].isin(selected_deptos)]
fig_line = px.line(
    df_deptos,
    x="Año",
    y="Número de accesos a internet",
    color="Departamento",
    markers=True,
    title="Evolución de los accesos a Internet por Departamento",
    labels={"Número de accesos a internet": "Accesos a Internet", "AÑO": "Año"}
)
st.plotly_chart(fig_line)
st.subheader(f"🧮 Relación entre penetración y accesos en {selected_year}")
fig_scatter = px.scatter(
    df_year,
    x="Penetración",
    y="Número de accesos a internet",
    color="Departamento",
    size="Número de accesos a internet",
    hover_name="Departamento",
    title="Relación entre Penetración y Accesos",
    labels={"Penetración": "Penetración (%)", "Número de accesos a internet": "Accesos"}
)
st.plotly_chart(fig_scatter)
st.subheader(f"◕ Distribución de accesos por departamento en {selected_year}")
fig_pie = px.pie(
    df_sorted.head(10),
    values="Número de accesos a internet",
    names="Departamento",
    title="Participación de los 10 principales departamentos en los accesos",
    hole=0.4  # Para tipo donut
)
st.plotly_chart(fig_pie)