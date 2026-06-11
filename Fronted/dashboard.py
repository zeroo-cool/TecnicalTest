# dashboard.py
import streamlit as st
import requests
import pandas as pd
import plotly.express as px

# 1. Configuración de la interfaz de la página
st.set_page_config(
    page_title="Control de Facturación y Gestión de Cartera Vencida",
    page_icon="📊",
    layout="wide"
)

st.title("📊 Control de Facturación y Gestión de Cartera Vencida")
st.markdown("---")

# URL base de tu API de FastAPI (Uvicorn)
API_BASE_URL = "http://127.0.0.1:8000"

# 2. Consumo de Endpoints con manejo de errores de conexión
@st.cache_data(ttl=60)  # Cachea los datos por 60 segundos para optimizar rendimiento
def cargar_datos_api(endpoint: str):
    try:
        respuesta = requests.get(f"{API_BASE_URL}{endpoint}")
        if respuesta.status_code == 200:
            return respuesta.json()
        else:
            st.error(f"Error {respuesta.status_code} al consultar el endpoint {endpoint}")
            return None
    except requests.exceptions.ConnectionError:
        st.error(f"❌ No se pudo conectar con la API en {API_BASE_URL}. Asegúrate de que Uvicorn esté corriendo.")
        return None

# Realizar las peticiones HTTP a la API
datos_tendencia = cargar_datos_api("/Ventas/TendenciaHistorica")
datos_deudores = cargar_datos_api("/Ventas/MontoDeudores")
datos_totales = cargar_datos_api("/Ventas/TotalesByMes")

# Verificar que los datos críticos existan antes de renderizar
if datos_tendencia is None or datos_deudores is None:
    st.warning("⚠️ Esperando la conexión con los servicios de FastAPI para pintar los gráficos...")
    st.stop()

# ==========================================
# SECCIÓN 1: SUBSECTION DE ENCABEZADO Y KPIS
# ==========================================
# Extraemos el monto global pendiente de cobro desde nuestra API unificada
monto_pendiente_global = datos_deudores.get("monto_total_pendiente", 0.0)

col_kpi1, col_kpi2 = st.columns(2)
with col_kpi1:
    st.metric(
        label="💰 MONTO TOTAL PENDIENTE DE COBRO", 
        value=f"$ {monto_pendiente_global:,.2f}",
        delta="Cuentas por Cobrar Activas",
        delta_color="inverse"
    )
with col_kpi2:
    total_clientes_deuda = len(datos_deudores.get("top_deudores", []))
    st.metric(
        label="👥 CLIENTES EN CARTERA VENCIDA / PENDIENTE", 
        value=total_clientes_deuda,
        delta="Requieren Gestión de Cobro"
    )

st.markdown("---")

# ==========================================
# SECCIÓN 2: TENDENCIA HISTÓRICA DE VENTAS
# ==========================================
st.subheader("📈 1. Tendencia Histórica de Ventas")

df_tendencia = pd.DataFrame(datos_tendencia)

if not df_tendencia.empty:
    # Crear un gráfico de líneas limpio, ordenado cronológicamente
    fig_linea = px.line(
        df_tendencia,
        x="Mes",
        y="TotalMensual",
        title="Evolución de Facturación Mensual Global ($)",
        labels={"Mes": "Periodo Cronológico (Año-Mes)", "TotalMensual": "Total Facturado ($)"},
        markers=True,
        template="plotly_dark" 
    )
    # Personalización de la línea
    fig_linea.update_traces(line_color="#00D2C4", line_width=3)
    st.plotly_chart(fig_linea, use_container_width=True)
else:
    st.info("No se encontraron registros de tendencias mensuales.")

st.markdown("---")

# ==========================================
# SECCIÓN 3: MONTO PENDIENTE DE COBRO Y DEUDORES
# ==========================================
st.subheader("🗂️ 2. Análisis de Cobranza y Gestión de Deudores")

df_deudores = pd.DataFrame(datos_deudores.get("top_deudores", []))

col_tabla, col_grafico = st.columns([2, 3])

with col_tabla:
    st.markdown("#### Lista de Deudores Principales")
    if not df_deudores.empty:
        # Formatear la tabla para mostrar la moneda de forma profesional
        df_tabla_formato = df_deudores.copy()
        df_tabla_formato["Total"] = df_tabla_formato["Total"].map("$ {:,.2f}".format)
        st.dataframe(df_tabla_formato, use_container_width=True, hide_index=True)
    else:
        st.success("No existen saldos pendientes registrados.")

with col_grafico:
    st.markdown("#### Concentración del Monto Pendiente")
    if not df_deudores.empty:
        # Gráfico de barras horizontales para identificar rápidamente deudores críticos
        fig_barras = px.bar(
            df_deudores,
            x="Total",
            y="NombreCliente",
            orientation="h",
            title="Ranking de Deudas por Cliente",
            labels={"Total": "Monto Adeudado ($)", "NombreCliente": "Razón Social / Cliente"},
            color="Total",
            color_continuous_scale=px.colors.sequential.Reds,
            template="plotly_dark"
        )
        # Ordenar para que el deudor que más debe quede arriba
        fig_barras.update_layout(yaxis={"categoryorder": "total ascending"}, showlegend=False)
        st.plotly_chart(fig_barras, use_container_width=True)