
import pandas as pd
import numpy as np

data= pd.read_csv("https://raw.githubusercontent.com/Daorsegu/Datos_definitivos/refs/heads/main/Data%20definitiva%20proyecto%20(Antes%20de%20limpieza).csv")    
df = pd.DataFrame(data)

print("\nNúmero de filas antes de eliminar faltantes:", len(df))

print("Columnas con valores faltantes")
df=df.dropna(subset=['AÑO'])
df=df.dropna(subset=['TRIMESTRE'])
df=df.dropna(subset=['CÓDIGO DANE'])
df=df.dropna(subset=['DEPARTAMENTO'])
df=df.dropna(subset=['No. ACCESOS FIJOS A INTERNET'])
df=df.dropna(subset=['POBLACIÓN DANE'])
df=df.dropna(subset=['PENETRACIÓN'])
print(df.isnull().sum())
print(df.head(5))

print("\nNúmero de filas despues de eliminar faltantes:", len(df))

print("Reemplazar titulos de columnas")

df.columns = df.columns.str.replace('AÑO', 'Año')
df.columns = df.columns.str.replace('TRIMESTRE', 'Trimestre')
df.columns = df.columns.str.replace('CÓDIGO DANE', 'Código Dane')
df.columns = df.columns.str.replace('DEPARTAMENTO', 'Departamento')
df.columns = df.columns.str.replace('No. ACCESOS FIJOS A INTERNET', 'Número de accesos a internet')
df.columns = df.columns.str.replace('POBLACIÓN DANE', 'Población')
df.columns = df.columns.str.replace('PENETRACIÓN', 'Penetración')
print(df.head(5))

print("Quitar espacios innecesarios")

df['Año'] = df['Año'].astype(str).str.strip()
df['Trimestre'] = df['Trimestre'].astype(str).str.strip()
df['Código Dane'] = df['Código Dane'].astype(str).str.strip()
df['Departamento'] = df['Departamento'].astype(str).str.strip()
df['Número de accesos a internet'] = df['Número de accesos a internet'].astype(str).str.strip()
df['Población'] = df['Población'].astype(str).str.strip()
df['Penetración'] = df['Penetración'].astype(str).str.strip()
print(df.head(5))

print("Columnas a las que le vamos a cambiar el tipo de dato")

df["Penetración"] = pd.to_numeric(df["Penetración"], errors="coerce")
print(df.isnull().sum())
print(df.head(5))
print(df.dtypes)

print(df["Penetración"].head(5))

df['Penetración'] = df['Penetración']*100
df["Penetración"] = df["Penetración"].round(2)
print(df.head(5))

print("Dataset limpio:")
print(df)
df.to_csv('Data definitiva proyecto.csv', index=False)