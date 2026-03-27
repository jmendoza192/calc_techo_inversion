import streamlit as st
import pandas as pd
import plotly.express as px

# 1. CONFIGURACIÓN DE PÁGINA Y ESTILOS UI (Jancarlo Inmobiliario Style)
st.set_page_config(page_title="Auditoría 360° | Jancarlo Inmobiliario", layout="wide")

st.markdown("""
    <style>
    /* Fondo general */
    .main { background-color: #f4f7f6; }
    
    /* ESTILO DE MÉTRICAS (Gris Oscuro sobre Blanco) */
    [data-testid="stMetricValue"] {
        color: #1e1e1e !important;
        font-weight: bold !important;
    }
    [data-testid="stMetricLabel"] {
        color: #4a4a4a !important;
        font-size: 1.1rem !important;
    }
    div[data-testid="stMetric"] {
        background-color: #ffffff;
        padding: 20px;
        border-radius: 12px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.05);
        border: 1px solid #e0e0e0;
    }

    /* ESTILO DE TARJETAS DE ESCENARIOS */
    .resultado-card { 
        padding: 25px; 
        border-radius: 15px; 
        color: white !important; 
        text-align: center;
        margin-bottom: 20px;
        min-height: 160px;
        box-shadow: 0 4px 10px rgba(0,0,0,0.15);
    }
    .resultado-card h3 { color: white !important; margin-bottom: 5px; }
    .resultado-card h1 { color: white !important; margin-top: 0px; font-size: 2.2rem; }
    .resultado-card p { color: rgba(255,255,255,0.9) !important; font-size: 0.9rem; }
    
    .verde { background: linear-gradient(135deg, #28a745, #1e7e34); }
    .azul { background: linear-gradient(135deg, #007bff, #0056b3); }
    .gris { background: linear-gradient(135deg, #6c757d, #495057); }
    
    /* Títulos de sección */
    h1, h2, h3 { color: #1e1e1e; font-family: 'Segoe UI', sans-serif; }
    
    /* Ajustes de Sidebar */
    .css-1d391kg { background-color: #ffffff; }
    </style>
    """, unsafe_allow_html=True)

# --- PANEL LATERAL: ENTRADA DE DATOS ---
with st.sidebar:
    st.title("📊 Datos del Cliente")
    st.write("Completa la información para el diagnóstico.")
    
    with st.expander("💰 Ingresos y Ahorros", expanded=True):
        ingreso = st.number_input("Ingreso Neto Mensual (S/)", min_value=0.0, value=6000.0, step=100.0)
        ahorros = st.number_input("Ahorros Líquidos (S/)", min_value=0.0, value=15000.0)
    
    with st.expander("💳 Deudas (Cuotas Mes)", expanded=True):
        p_personal = st.number_input("Préstamos Personales", value=0.0)
        p_vehicular = st.number_input("Préstamo Vehicular", value=0.0)
        tarjetas = st.number_input("Cuotas de Tarjeta", value=0.0, help="Solo cuotas fijas de compras pasadas.")
        otros = st.number_input("Otros Créditos", value=0.0)

# --- LÓGICA DE CÁLCULO FINANCIERO ---
capacidad_40 = ingreso * 0.40
deudas_totales = p_personal + p_vehicular + tarjetas + otros
cuota_disponible = max(0.0, capacidad_40 - deudas_totales)

# Factor financiero MiVivienda (Aprox. TEA 9% - 20 años)
prestamo_max = cuota_disponible * 111.14
inicial_afp = ingreso * 0.25
inicial_total = ahorros + inicial_afp

# Definición de Escenarios (Monto + Identificadores)
esc_verde = prestamo_max + inicial_total + 12800 # BBP + Bono Verde
esc_tradicional = prestamo_max + inicial_total + 7300 # Solo BBP
esc_directo = prestamo_max + inicial_total

escenarios_data = [
    {"nombre": "ECO-SOSTENIBLE", "monto": esc_verde, "clase": "verde", "color_hex": "#28a745", "desc": "Máximo con BBP + Bono Verde"},
    {"nombre": "TRADICIONAL", "monto": esc_tradicional, "clase": "azul", "color_hex": "#007bff", "desc": "Precio con Bono Buen Pagador"},
    {"nombre": "SIN BONOS", "monto": esc_directo, "clase": "gris", "color_hex": "#6c757d", "desc": "Crédito Directo / Recursos Propios"}
]

# --- CUERPO PRINCIPAL ---
st.title("🎯 Auditoría Inmobiliaria 360°")
st.write("Análisis dinámico de capacidad de compra y salud crediticia.")
st.write("---")

# FASE 1: Salud Crediticia
st.subheader("1. Indicadores de Calificación")
c_met1, c_met2, c_met3 = st.columns(3)
c_met1.metric("Cuota Mensual Máx.", f"S/ {cuota_disponible:,.2f}")
c_met2.metric("Préstamo Hipotecario", f"S/ {prestamo_max:,.2f}")
c_met3.metric("Inicial (Ahorros + AFP)", f"S/ {inicial_total:,.2f}")

# FASE 2: Techo de Inversión (Tarjetas)
st.write("---")
st.subheader("2. Tu Techo de Inversión según Proyecto")
col1, col2, col3 = st.columns(3)
cols = [col1, col2, col3]

for i, esc in enumerate(escenarios_data):
    with cols[i]:
        st.markdown(f"""
            <div class="resultado-card {esc['clase']}">
                <h3>{esc['nombre']}</h3>
                <h1>S/ {esc['monto']:,.0f}</h1>
                <p>{esc['desc']}</p>
            </div>
            """, unsafe_allow_html=True)

# FASE 3: Gráfico Sincronizado
st.write("---")
st.subheader("3. Comparativa Visual de Inversión")

df_grafico = pd.DataFrame(escenarios_data)
fig = px.bar(
    df_grafico, x='nombre', y='monto', color='nombre',
    color_discrete_map={d['nombre']: d['color_hex'] for d in escenarios_data},
    text_auto=',.0f'
)
fig.update_layout(showlegend=False, plot_bgcolor='rgba(0,0,0,0)', xaxis_title=None, yaxis_title="Monto (S/)")
fig.update_traces(textposition='outside', textfont_size=14)
st.plotly_chart(fig, use_container_width=True)

# FASE 4: Rutas de Optimización (Cierre de Asesoría)
st.write("---")
st.subheader("🚀 Rutas de Optimización para tu Compra")
st.info("Como asesor, estas son las estrategias que podemos ejecutar para mejorar tus números:")

opt1, opt2 = st.columns(2)
with opt1:
    with st.expander("📉 Plan de Liberación de Capacidad", expanded=False):
        st.write(f"Si liquidamos tus deudas de **S/ {deudas_totales:,.2f}**, tu techo de inversión podría subir drásticamente.")
        st.write("- **Meta:** Eliminar cuotas de tarjeta de corto plazo.")
        st.write("- **Impacto:** Subir el préstamo bancario en aprox. S/ 25,000.")
    
    with st.expander("📍 Estrategia Magdalena vs. San Isidro", expanded=False):
        st.write("Comparamos el precio por m² para maximizar el área de tu futuro departamento.")
        st.write("- **Magdalena:** Ideal para primera vivienda (m² competitivo).")
        st.write("- **San Isidro:** Alta plusvalía y perfil de inversión.")

with opt2:
    with st.expander("🏦 Perfilamiento para Tasa Preferencial", expanded=False):
        st.write("No todos los bancos evalúan igual. Te ayudamos a elegir la entidad con la menor TEA.")
        st.write("- **Acción:** Revisión de Score Sentinel/Infocorp.")
        st.write("- **Acción:** Preparación de sustento de ingresos (Ingenieros/Independientes).")
    
    with st.expander("📜 Gestión de Gastos de Cierre", expanded=False):
        st.write("Calculamos el 3% adicional para que tu inicial sea real y sin sorpresas.")
        st.write("- **Detalle:** Alcabala, Gastos Notariales y Registrales.")

# Botón final decorativo
if st.button("✅ Finalizar Auditoría y Generar PDF"):
    st.balloons()
    st.success("Auditoría completada satisfactoriamente para Jancarlo Inmobiliario.")
