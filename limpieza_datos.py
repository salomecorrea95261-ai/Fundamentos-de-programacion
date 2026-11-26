import pandas as pd
import streamlit as st

st.title("Limpieza de Datos")
ruta = "https://raw.githubusercontent.com/VMjavier/claseAnalisisDatos/refs/heads/main/veterinaria_colombia.csv"

df = pd.read_csv(ruta)
st.write(df)

st.subheader('1.Columnas del dataset')
st.write(df.columns)

st.subheader('2. Valores nulos por columna')
nulos = df.isnull().sum().reset_index()
nulos.columns = ['Columna', 'Valores nulos']
st.write(nulos)

st.subheader('3. dimensiones del dataset')
filas, columnas = df.shape
c1,c2 = st.columns(2)
c1.metric("Filas", filas)
c2.metric("Columnas", columnas)

#Cambiar las columnas a minúsculas y sin espacios
df.columns = df.columns.str.strip().str.lower().str.replace(' ', '_')

#cambiar el nombre de la columna particular
df.rename(columns={'nombre': 'nombre_mascota'}, inplace =True)

st.subheader('4. Columnas del dataset después de la limpieza')
st.write(df.columns)

#Eliminar filas y columnas  completamente nulas
df.dropna(axis=0, how='all', inplace=True) #Fila = 0
df.dropna(axis=1, how='all', inplace=True) #Columna = 1

st.subheader('5. dimensiones del dataset')
filas, columnas = df.shape
c1,c2 = st.columns(2)
c1.metric("Filas", filas)
c2.metric("Columnas", columnas)

#eliminar una columna especifica
df.drop(columns=['nombre_mascota'], inplace=True)

st.subheader('6. Dataset limpieza parcial')
st.write(df)