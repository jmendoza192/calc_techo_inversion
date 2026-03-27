import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from fpdf import FPDF
from datetime import datetime

# 1. CONFIGURACIÓN DE PÁGINA Y ESTILOS UI
st.set_page_config(page_title="Auditoría Financiera | Jancarlo Inmobiliario", layout="wide")

st.markdown("""
    <style>
    .main { background-color: #0e1117; }
    [data-testid="stMetricValue"] { color: #ffffff !important; font-weight: bold !important; font-size: 2.1rem !important; }
    [data-testid="stMetricLabel"] { color: #a1a1a1 !important; font-size: 1rem !important; }
    div[data-testid="stMetric"] {
        background-color: #1f2630;
        padding: 20px;
        border-radius: 12px;
        border: 1px solid #30363d;
    }
    .resultado-card { 
        padding: 25px; border-radius: 15px; color: white !important; text-align: center; margin-bottom: 20px;
    }
    .verde { background: linear-gradient(135deg, #28a745, #1e7e34); }
    .azul { background: linear-gradient(135deg, #0e2647, #1b3a61); }
    .gris { background: linear-gradient(135deg, #6c757d, #495057); }
    #MainMenu, footer, header {visibility: hidden;}
    </style>
    """, unsafe_allow_html=True)

# --- FUNCIÓN PDF ---
def generar_pdf(datos_informe, escenarios):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_draw_color(14, 38, 71); pdf.set_line_width(0.8); pdf.rect(10, 10, 190, 25)
    pdf.set_y(15); pdf.set_font("Arial", 'B', 16); pdf.set_text_color(14, 38, 71)
    pdf.cell(0, 10, "AUDITORIA FINANCIERA INMOBILIARIA", ln=True, align='C')
    pdf.ln(20)
    pdf.set_fill_color(14, 38, 71); pdf.set_text_color(255, 255, 255); pdf.set_font("Arial", 'B', 12)
    pdf.cell(0, 10, " 1. DIAGNOSTICO FINANCIERO", ln=True, fill=True)
    pdf.ln(2); pdf.set_text_color(30, 30, 30); pdf.set_font("Arial", '', 11)
    for k, v in datos_informe.items():
        pdf.cell(95, 10, f" {k}:", "B"); pdf.cell(0, 10, f"{v}", "B", ln=True, align='R')
    pdf.ln(10); pdf.set_fill_color(215, 179, 93); pdf.cell(0, 10, " 2. TECHOS DE INVERSION", ln=True, fill=True)
    for esc in escenarios:
        pdf.set_font("Arial", 'B', 10); pdf.cell(70, 10, f" {esc['nombre']}", "B")
        pdf.cell(60, 10, f" S/ {esc['monto']:,}", "B", 0, 'C')
        pdf.cell(60, 10, f" {esc['desc']}", "B", 1, 'C')
    return pdf.output(dest='S').encode('latin-1')

# --- PANEL LATERAL ---
with st.sidebar:
    st.title("📊 Datos de Asesoría")
    with st.expander("💰 Ingresos y Capital", expanded=True):
        ingreso = st.number_input("Ingreso Neto Mensual (S/)", min_value=0, value=6000)
        ahorros = st.number_input("Ahorros Líquidos (S/)", min_value=0, value=15000)
        saldo_afp = st.number_input("Saldo Total en AFP (S/)", min_value=0, value=40000)
        disponible_afp = int(saldo_afp * 0.25)
        st.success(f"✅ Disponible para inicial (25% AFP): S/ {disponible_afp:,}")

    with st.expander("💳 Subgrupo 1: Tarjetas", expanded=True):
        linea_tc = st.number_input("Línea Total (S/)", value=10000)
        cuota_tc_sbs = int(linea_tc * 0.05)

    with st.expander("🏦 Subgrupo 2: Otras Cuotas", expanded=True):
        p_personal = st.number_input("Cuota Préstamo Personal (S/)", value=0)
        p_vehicular = st.number_input("Cuota Préstamo Vehicular (S/)", value=0)
        p_otros = st.number_input("Otros Créditos (S/)", value=0)
    
    with st.expander("🏦 Condiciones", expanded=False):
        tea = st.number_input("TEA (%)", value=9.5); plazo = st.number_input("Años", value=20)

    with st.expander("🎁 Bonos MiVivienda (2026)", expanded=True):
        datos_bonos = {"R1": {"b": 27400, "v": 33700}, "R2": {"b": 22800, "v": 29100}, "R3": {"b": 20900, "v": 27200}, "R4": {"b": 7800, "v": 14100}, "R5": {"b": 0, "v": 0}}
        sel = st.selectbox("Rango", ["R1", "R2", "R3", "R4", "R5"], index=3)
        integrador = st.checkbox("¿Bono Integrador? (+3,600)")
        extra = 3600 if integrador else 0
        m_bbp = datos_bonos[sel]['b'] + extra if datos_bonos[sel]['b'] > 0 else 0
        m_verde = datos_bonos[sel]['v'] + extra if datos_bonos[sel]['v'] > 0 else 0

# --- LÓGICA ---
deudas = cuota_tc_sbs + p_personal + p_vehicular + p_otros
pct_deuda = (deudas / ingreso * 100) if ingreso > 0 else 0
cuota_disp = int(max(0, (ingreso * 0.40) - deudas))
tem = (1 + tea/100)**(1/12) - 1
factor = (1 - (1 + tem)**-(plazo * 12)) / tem if tem > 0 else 0
prestamo = int(cuota_disp * factor)
inicial = ahorros + disponible_afp

escenarios = [
    {"nombre": "ECO-SOSTENIBLE", "monto": prestamo + inicial + m_verde, "clase": "verde", "desc": f"Bono: S/ {m_verde:,}", "color": "#28a745"},
    {"nombre": "MI VIVIENDA TRADICIONAL", "monto": prestamo + inicial + m_bbp, "clase": "azul", "desc": f"Bono: S/ {m_bbp:,}", "color": "#0e2647"},
    {"nombre": "SIN BONOS", "monto": prestamo + inicial, "clase": "gris", "desc": "Solo Rec. Propios", "color": "#6c757d"}
]

# --- UI CUERPO ---
st.title("🎯 Auditoría financiera - Inversión")
st.write("---")
st.subheader("1. Salud Crediticia y Diagnóstico")

col_gauge, col_metrics = st.columns([1.2, 2])
with col_gauge:
    fig = go.Figure(go.Indicator(mode="gauge+number", value=pct_deuda, title={'text': "Carga de Deuda Actual", 'font': {'size': 20, 'color': 'white'}},
        number={'suffix': "%", 'font':{'color':'white'}},
        gauge={'axis': {'range': [None, 50]}, 'bar': {'color': "white"},
               'steps': [{'range': [0, 20], 'color': "#28a745"}, {'range': [20, 35], 'color': "#ffc107"}, {'range': [35, 50], 'color': "#dc3545"}]}))
    fig.update_layout(height=380, paper_bgcolor='rgba(0,0,0,0)', font={'color': "white"})
    st.plotly_chart(fig, use_container_width=True)
    with st.expander("📋 Guía de Evaluación Bancaria"):
        st.markdown("<small>0-20%: Perfil Prime | 21-35%: Riesgo Medio | 36-40%: Límite Crítico</small>", unsafe_allow_html=True)

with col_metrics:
    met_c1, met_c2 = st.columns(2)
    met_c1.metric("Cuota Disponible Real", f"S/ {cuota_disp:,}")
    met_c2.metric("Préstamo Hipotecario", f"S/ {prestamo:,}")
    st.write("")
    st.metric("Inicial Total (Ahorros + AFP)", f"S/ {inicial:,}")
    st.info("💡 **Dato Bancario:** Los bancos suelen limitar el total de tus deudas mensuales al 40% de tus ingresos netos.")

st.write("---")
st.subheader("2. Tu Techo de Inversión por Proyecto")
e1, e2, e3 = st.columns(3)
for i, col in enumerate([e1, e2, e3]):
    with col:
        st.markdown(f'<div class="resultado-card {escenarios[i]["clase"]}"><h3>{escenarios[i]["nombre"]}</h3><h1>S/ {escenarios[i]["monto"]:,}</h1><p>{escenarios[i]["desc"]}</p></div>', unsafe_allow_html=True)

# --- GRÁFICO DE BARRAS POTENCIADO ---
df_grafico = pd.DataFrame(escenarios)
df_grafico['texto_barra'] = df_grafico['monto'].apply(lambda x: f"S/. {x:,.0f}")

fig_bar = px.bar(df_grafico, x='nombre', y='monto', color='nombre', 
                 color_discrete_map={esc['nombre']: esc['color'] for esc in escenarios},
                 text='texto_barra')

fig_bar.update_layout(
    showlegend=False, paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', 
    font=dict(color="white"), xaxis_title=None, yaxis_title="Monto Total (S/)",
    xaxis=dict(tickfont=dict(size=14)), yaxis=dict(tickfont=dict(size=14))
)

fig_bar.update_traces(
    textposition='inside', textfont_size=22, insidetextanchor='middle', marker_line_width=0
)
st.plotly_chart(fig_bar, use_container_width=True)

st.write("---")
st.subheader("🚀 Estrategia y Optimización")
o1, o2 = st.columns(2)
with o1:
    cuota_sim = int(max(0, (ingreso * 0.40) - ((linea_tc*0.5*0.05)+p_personal+p_vehicular+p_otros)))
    inc = int((cuota_sim * factor) - prestamo)
    if inc > 0: st.success(f"📈 **Oportunidad:** Bajando tarjetas al 50%, tu presupuesto sube **S/ {inc:,}**.")
    else: st.info("Deuda saludable.")
with o2: st.warning(f"📜 **Reserva Administrativa (3%):** S/ {int((prestamo+inicial)*0.03):,}")

if st.button("✅ Finalizar Auditoría"):
    st.balloons()
    pdf = generar_pdf({"Ingreso": f"S/ {ingreso:,}", "Deuda": f"{pct_deuda:.2f}%", "Cuota": f"S/ {cuota_disp:,}"}, escenarios)
    st.download_button("📥 Descargar Reporte PDF de Marca", data=pdf, file_name="Reporte_Inversion.pdf")
