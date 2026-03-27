import streamlit as st
import pandas as pd
import plotly.express as px

# 1. CONFIGURACIÓN DE PÁGINA Y ESTILOS
st.set_page_config(page_title="Auditoría Financiera | Jancarlo Inmobiliario", layout="wide")

st.markdown("""
    <style>
    .main { background-color: #f4f7f6; }
    [data-testid="stMetricValue"] { color: #1e1e1e !important; font-weight: bold !important; }
    [data-testid="stMetricLabel"] { color: #4a4a4a !important; font-size: 1.1rem !important; }
    div[data-testid="stMetric"] {
        background-color: #ffffff;
        padding: 20px;
        border-radius: 12px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.05);
        border: 1px solid #e0e0e0;
    }
    .resultado-card { 
        padding: 25px; 
        border-radius: 15px; 
        color: white !important; 
        text-align: center;
        margin-bottom: 20px;
        min-height: 160px;
    }
    .resultado-card h3, .resultado-card h1, .resultado-card p { color: white !important; }
    .verde { background: linear-gradient(135deg, #28a745, #1e7e34); }
    .azul { background: linear-gradient(135deg, #007bff, #0056b3); }
    .gris { background: linear-gradient(135deg, #6c757d, #495057); }
    
    #MainMenu, footer, header {visibility: hidden;}
    </style>
    """, unsafe_allow_html=True)

# --- PANEL LATERAL: INPUTS ---
with st.sidebar:
    st.title("📊 Datos de Asesoría")
    
    with st.expander("💰 Ingresos y Capital", expanded=True):
        ingreso = st.number_input("Ingreso Neto Mensual (S/)", min_value=0, value=6000, step=100)
        ahorros = st.number_input("Ahorros Líquidos (S/)", min_value=0, value=15000)
        saldo_afp = st.number_input("Saldo Total en AFP (S/)", min_value=0, value=40000)
        disponible_afp = int(saldo_afp * 0.25)
        st.info(f"✅ Disponible para inicial (25% AFP): S/ {disponible_afp:,}")

    with st.expander("🏦 Condiciones del Crédito", expanded=True):
        tea = st.number_input("Tasa Efectiva Anual - TEA (%)", min_value=1.0, max_value=20.0, value=9.5, step=0.1)
        plazo_anios = st.number_input("Plazo del Préstamo (Años)", min_value=5, max_value=30, value=20, step=1)
        
    with st.expander("🎁 Bonos MiVivienda (Tabla 2026)", expanded=True):
        # Datos de la tabla incluyendo rangos de precio
        datos_bonos = {
            "Rango 1": {"min": 68800, "max": 98100, "bbp": 27400, "verde": 33700},
            "Rango 2": {"min": 98100, "max": 146900, "bbp": 22800, "verde": 29100},
            "Rango 3": {"min": 146900, "max": 244600, "bbp": 20900, "verde": 27200},
            "Rango 4": {"min": 244600, "max": 362100, "bbp": 7800, "verde": 14100},
            "Rango 5": {"min": 362100, "max": 488800, "bbp": 0, "verde": 0}
        }
        
        seleccion_rango = st.selectbox("Seleccionar Rango de Valor", list(datos_bonos.keys()), index=3)
        
        # Mostrar dinámicamente el precio del inmueble según el rango
        rango_info = datos_bonos[seleccion_rango]
        st.success(f"🏠 Valor Vivienda: S/ {rango_info['min']:,} - S/ {rango_info['max']:,}")
        
        integrador = st.checkbox("¿Aplica Bono Integrador? (+ S/ 3,600)", value=False)
        extra_integrador = 3600 if integrador else 0
        
        monto_bbp = rango_info['bbp'] + extra_integrador if rango_info['bbp'] > 0 else 0
        monto_bbp_verde = rango_info['verde'] + extra_integrador if rango_info['verde'] > 0 else 0

    with st.expander("💳 Deudas (Cuotas Mes)", expanded=False):
        deudas_totales = st.number_input("Total Cuotas Mensuales (Préstamos/Tarjetas)", value=0)

# --- LÓGICA DE CÁLCULO ---
capacidad_40 = ingreso * 0.40
cuota_disponible = int(max(0, capacidad_40 - deudas_totales))

# Cálculo Financiero de Préstamo
tem = (1 + tea/100)**(1/12) - 1
n_meses = plazo_anios * 12
if tem > 0:
    factor = (1 - (1 + tem)**-n_meses) / tem
    prestamo_max = int(cuota_disponible * factor)
else:
    prestamo_max = 0

inicial_total = ahorros + disponible_afp

# Escenarios Finales (Sin Decimales)
esc_verde = int(prestamo_max + inicial_total + monto_bbp_verde)
esc_tradicional = int(prestamo_max + inicial_total + monto_bbp)
esc_directo = int(prestamo_max + inicial_total)

escenarios_data = [
    {"nombre": "ECO-SOSTENIBLE", "monto": esc_verde, "clase": "verde", "color_hex": "#28a745", "desc": f"Bonos Incluidos: S/ {monto_bbp_verde:,}"},
    {"nombre": "TRADICIONAL", "monto": esc_tradicional, "clase": "azul", "color_hex": "#007bff", "desc": f"Bono Incluido: S/ {monto_bbp:,}"},
    {"nombre": "SIN BONOS", "monto": esc_directo, "clase": "gris", "color_hex": "#6c757d", "desc": "Solo Recursos Propios"}
]

# --- CUERPO PRINCIPAL ---
st.title("🎯 Auditoría financiera - Inversión")
st.write(f"Proyección financiera estimada a una TEA de {tea}%")
st.write("---")

# FASE 1: Salud Crediticia
st.subheader("1. Indicadores de Calificación")
c_met1, c_met2, c_met3 = st.columns(3)
c_met1.metric("Cuota Mensual Máx.", f"S/ {cuota_disponible:,}")
c_met2.metric("Préstamo Hipotecario", f"S/ {prestamo_max:,}")
c_met3.metric("Inicial (Ahorros + AFP)", f"S/ {inicial_total:,}")

# FASE 2: Escenarios
st.write("---")
st.subheader("2. Tu Techo de Inversión por Proyecto")
col1, col2, col3 = st.columns(3)
cols = [col1, col2, col3]

for i, esc in enumerate(escenarios_data):
    with cols[i]:
        st.markdown(f"""
            <div class="resultado-card {esc['clase']}">
                <h3>{esc['nombre']}</h3>
                <h1>S/ {esc['monto']:,}</h1>
                <p>{esc['desc']}</p>
            </div>
            """, unsafe_allow_html=True)

# FASE 3: Gráfico
st.write("---")
st.subheader("3. Visualización Comparativa de Inversión")
df_grafico = pd.DataFrame(escenarios_data)
fig = px.bar(
    df_grafico, x='nombre', y='monto', color='nombre',
    color_discrete_map={d['nombre']: d['color_hex'] for d in escenarios_data},
    text_auto=True
)
fig.update_layout(showlegend=False, plot_bgcolor='rgba(0,0,0,0)', xaxis_title=None, yaxis_title="Monto (S/) Totales")
fig.update_traces(textposition='outside', textfont_size=14, texttemplate='S/ %{y:,.0f}')
st.plotly_chart(fig, use_container_width=True)

# FASE 4: Rutas de Optimización
st.write("---")
st.subheader("🚀 Rutas de Optimización para tu Compra")

opt1, opt2 = st.columns(2)
with opt1:
    with st.expander("📉 Plan de Liberación de Capacidad", expanded=True):
        st.write(f"Si liquidamos tus deudas de S/ {deudas_totales:,}, tu préstamo bancario podría subir significativamente.")

with opt2:
    with st.expander("📜 Gestión de Gastos de Cierre", expanded=True):
        st.write(f"Gasto estimado de cierre (3%): S/ {int(esc_tradicional * 0.03):,}")

st.write("---")
if st.button("✅ Finalizar Auditoría"):
    st.balloons()
    st.success("Cálculo completado.")
