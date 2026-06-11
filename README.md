# 📊 Proyecto: Ingesta, Limpieza, Análisis y Visualización de Ventas

## 📌 Descripción General

Este proyecto implementa una solución integral de procesamiento de datos (**Data Pipeline End-to-End**) para la gestión y análisis de información de ventas.

La arquitectura contempla:

* Extracción de datos desde archivos CSV provenientes de sistemas legados.
* Perfilamiento y validación de calidad de datos.
* Limpieza y transformación utilizando Python y Pandas.
* Implementación de un proceso ETL para carga en SQL Server.
* Diseño de un modelo dimensional tipo Star Schema.
* Exposición de métricas mediante una API REST desarrollada con FastAPI.
* Construcción de dashboards interactivos con Streamlit y Plotly.
* Análisis de ventas, clientes y cuentas por cobrar.

---

## 🏗️ Arquitectura de la Solución

```text
CSV
 │
 ▼
Perfilamiento de Datos
(Errores.py)
 │
 ▼
Limpieza y Transformación
(Perfilamiento.py)
 │
 ▼
Proceso ETL
(insersion.py)
 │
 ▼
SQL Server
(Star Schema)
 │
 ▼
FastAPI
(API REST)
 │
 ▼
Streamlit
(Dashboard Analítico)
```

---

## 🛠️ Fase 1. Diagnóstico y Perfilamiento de Datos

**Archivo:** `Errores.py`

Objetivos:

* Validar la estructura del archivo fuente.
* Detectar valores nulos.
* Identificar formatos de fecha inválidos.
* Detectar inconsistencias numéricas.
* Identificar registros duplicados.
* Generar métricas de calidad de datos previas al proceso ETL.

---

## 🧹 Fase 2. Limpieza y Transformación de Datos

**Archivo:** `Perfilamiento.py`

Procesos aplicados:

* Eliminación de registros duplicados.
* Estandarización de fechas.
* Conversión de importes monetarios.
* Recuperación de valores faltantes.
* Normalización de nombres de clientes.
* Generación de un dataset listo para análisis.

---

## 🗄️ Fase 3. ETL y Modelo Dimensional

**Archivo:** `insersion.py`

Objetivos:

* Extraer información desde el dataset procesado.
* Transformar datos para análisis empresarial.
* Construir dimensiones y tabla de hechos.
* Cargar información hacia SQL Server.

### Modelo Dimensional

#### Dimensión Clientes

* cliente_id
* nombre_cliente

#### Dimensión Tiempo

* fecha_id
* año
* mes_numero
* mes
* trimestre

#### Tabla de Hechos

* invoice_id
* fecha_id
* cliente_id
* item_description
* qty
* unit_price
* total
* status

#### Diagrama ER

<img width="1024" height="188" alt="image" src="https://github.com/user-attachments/assets/f5588f33-6809-4738-8953-ac248a66a8e7" />




---

## 🌐 Fase 4. API REST con FastAPI

**Archivo:** `main.py`

La API expone indicadores de negocio mediante endpoints REST.

### Endpoints Disponibles

| Endpoint                   | Método | Descripción                 |
| -------------------------- | ------ | --------------------------- |
| /Ventas/TendenciaHistorica | GET    | Tendencia mensual de ventas |
| /Ventas/TotalesByMes       | GET    | Ventas por cliente y mes    |
| /Ventas/TopCincoClientes   | GET    | Ranking de clientes         |
| /Ventas/MontoDeudores      | GET    | Cartera vencida y deudores  |

### Tecnologías Utilizadas

* FastAPI
* SQLAlchemy
* Pydantic
* SQL Server
* Stored Procedures

---

## 📊 Fase 5. Dashboard Analítico

**Archivo:** `dashboard.py`

Dashboard interactivo construido con Streamlit y Plotly.

### Indicadores Implementados

#### 📈 Tendencia Histórica de Ventas

Visualización cronológica de la facturación mensual.

#### 💰 Monto Total Pendiente de Cobro

Indicador global de cuentas por cobrar.

#### 👥 Clientes con Adeudos

Cantidad de clientes con saldo pendiente.

#### 🏆 Ranking de Deudores

Visualización gráfica de los principales deudores.

### Características Técnicas

* Caché inteligente con `st.cache_data`.
* Consumo de API REST.
* Manejo de errores de conexión.
* Visualizaciones interactivas.
* Diseño responsive.

---

## 🔌 Configuración de Base de Datos

**Archivo:** `database.py`

Tecnologías utilizadas:

* SQL Server Express
* SQLAlchemy
* pyodbc
* ODBC Driver 17 for SQL Server

---

## ⚙️ Instalación del Entorno

### Crear entorno virtual para arraque la API (Ejecutar en el mismo directorio del archivo main.py)

```bash
python -m venv venv
```

### Activar entorno

Windows

```bash
venv\Scripts\activate
```

Linux / Mac

```bash
source venv/bin/activate
```

### Instalar dependencias

```bash
pip install pandas numpy sqlalchemy pyodbc fastapi uvicorn pydantic streamlit requests plotly python-multipart
```
---

## 📦 Dependencias del Proyecto

```text
pandas
numpy
sqlalchemy
pyodbc
fastapi
uvicorn
pydantic
streamlit
requests
plotly
python-multipart
```

---

## 🚀 Ejecución del Proyecto

### 1. Diagnóstico de Datos

```bash
python Errores.py
```

### 2. Limpieza de Datos

```bash
python Perfilamiento.py
```

### 3. Ejecución del ETL

```bash
python insersion.py
```

### 4. Levantar API

```bash
uvicorn main:app --reload
```

### 5. Ejecutar Dashboard

```bash
streamlit run dashboard.py
```

---

## 📖 Accesos del Sistema

### Swagger

```text
http://127.0.0.1:8000/docs
```

### Dashboard Streamlit

```text
http://localhost:8501
```

---

## 🎯 Resultados del Proyecto

* Automatización del procesamiento de datos.
* Reducción de errores manuales.
* Centralización de métricas empresariales.
* Exposición de información mediante servicios REST.
* Visualización ejecutiva para apoyo en la toma de decisiones.

---

## 👨‍💻 Autor

Ernesto Bardales Hernández, Solucion de prueba técnica
