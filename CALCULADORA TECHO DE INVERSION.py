import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from fpdf import FPDF
from datetime import datetime

# 1. CONFIGURACIÓN DE PÁGINA Y ESTILOS UI (Versión Oscura Original)
st.set_page_config(page_title="Auditoría Financiera | Jancarlo Inmobiliario", layout="wide")

st.markdown("""
    <style>
    .main { background-color: #0e1117; }
    [data-testid="stMetricValue"] { color: #ffffff !important; font-weight: bold !important; }
    [data-testid="stMetricLabel"] { color: #a1a1a1 !important; font-size: 1.1rem !important; }
    div[data-testid="stMetric"] {
        background-color: #1f2630;
        padding: 20px;
        border-radius: 12px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.1);
        border: 1px solid #30363d;
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
    .azul { background: linear-gradient(135deg, #0e2647, #1b3a61); } /* Azul Marca */
    .gris { background: linear-gradient(135deg, #6c757d, #495057); }
    
    #MainMenu, footer, header {visibility: hidden;}
    </style>
    """, unsafe_allow_html=True)

# --- FUNCIÓN GENERAR PDF DE MARCA ---
def generar_pdf(datos_informe, escenarios):
    pdf = FPDF()
    pdf.add_page()
    # Recuadro de Título
    pdf.set_draw_color(14, 38, 71)
    pdf.set_line_width(0.8)
    pdf.rect(10, 10, 190, 25)
    pdf.set_y(15)
    pdf.set_font("Arial", 'B', 16)
    pdf.set_text_color(14, 38, 71)
    pdf.cell(0, 10, "AUDITORIA FINANCIERA INMOBILIARIA", ln=True, align='C')
    pdf.set_font("Arial", '', 9)
    pdf.cell(0, 5, f"REPORTE TECNICO - {datetime.now().strftime('%d/%m/%Y')}", ln=True, align='C')
    
    pdf.ln(15)
    pdf.set_fill_color(14, 38, 71)
    pdf.set_text_color(255, 255, 255)
    pdf.set_font("Arial", 'B', 12)
    pdf.cell(0, 10, " 1. DIAGNOSTICO FINANCIERO", ln=True, fill=True)
    
    pdf.ln(2)
    pdf.set_text_color(30, 30, 30)
    pdf.set_font("Arial", '', 11)
    pdf.cell(95, 10, " Ingreso Neto Mensual:", "B"); pdf.cell(0, 10, f"S/ {datos_informe['ingreso']:,}", "B", ln=True, align='R')
    pdf.cell(95, 10, " Carga de Deuda SBS:", "B"); pdf.cell(0, 10, f"{datos_informe['deuda_pct']:.2f}%", "B", ln=True, align='R')
    pdf.cell(95, 10, " Cuota Disponible:", "B"); pdf.cell(0, 10, f"S/ {datos_informe['cuota_disp']:,}", "B", ln=True, align='R')
    
    pdf.ln(10)
    pdf.set_fill_color(215, 179, 93) # Dorado Marca
    pdf.cell(0, 10, " 2. TECHOS DE INVERSION", ln=True, fill=True)
    pdf.ln(4)
    for esc in escenarios:
        pdf.set_font("Arial", 'B', 10)
        pdf.cell(70, 10, f" {esc['nombre']}", "B")
        pdf.cell(60, 10, f" S/ {esc['monto']:,}", "B", 0, 'C')
        pdf.cell(60, 10, f" {esc['desc']}", "B", 1, 'C')
    
    pdf.ln(10)
    pdf.set_font("Arial", '', 9)
    pdf.write(5, "Este documento es una ")
    pdf.set_font("Arial", 'B', 9); pdf.write(5, "proyeccion tecnica referencial"); pdf.set_font("Arial", '', 9)
    pdf.write(5, " basada en politicas bancarias generales.\nBonos actualizados a 2026.")
    return pdf.output(dest='S').encode('latin-1')

# --- PANEL LATERAL: INPUTS ---
with st.sidebar:
    st.title("📊 Datos de Asesoría")
    with st.expander("💰 Ingresos y Capital", expanded=True):
        ingreso = st.number_input("Ingreso Neto Mensual (S/)", min_value=0, value=6000, step=100)
        ahorros = st.number_input("Ahorros Líquidos (S/)", min_value=0, value=15000)
        saldo_afp = st.number_input("Saldo Total en AFP (S/)", min_value=0, value=40000)
        disponible_afp = int(saldo_afp * 0.25)
        st.info(f"AFP Disponible: S/ {disponible_afp:,}")

    with st.expander("💳 Subgrupo 1: Tarjetas", expanded=True):
        linea_tc = st.number_input("Línea Total (S/)", min_value=0, value=10000)
        cuota_tc_sbs = int(linea_tc * 0.05)

    with st.expander("🏦 Subgrupo 2: Cuotas Fijas", expanded=True):
        p_personal = st.number_input("Préstamo Personal (S/)", value=0)
        p_vehicular = st.number_input("Préstamo Vehicular (S/)", value=0)
        p_otros = st.number_input("Otros Créditos (S/)", value=0)
        
    with st.expander("🏦 Condiciones Crédito", expanded=False):
        tea = st.number_input("TEA (%)", value=9.5); plazo = st.number_input("Plazo (Años)", value=20)
        
    with st.expander("🎁 Bonos MiVivienda (2026)", expanded=True):
        datos_bonos = {
            "Rango 1": {"bbp": 27400, "verde": 33700},
            "Rango 2": {"bbp": 22800, "verde": 29100},
            "Rango 3": {"bbp": 20900, "verde": 27200},
            "Rango 4": {"bbp": 7800, "verde": 14100},
            "Rango 5": {"bbp": 0, "verde": 0}
        }
        sel_rango = st.selectbox("Rango", list(datos_bonos.keys()), index=3)
        integrador = st.checkbox("¿Aplica Bono Integrador? (+3,600)")
        extra = 3600 if integrador else 0
        m_bbp = datos_bonos[sel_rango]['bbp'] + extra if datos_bonos[sel_rango]['bbp'] > 0 else 0
        m_verde = datos_bonos[sel_rango]['verde'] + extra if datos_bonos[sel_rango]['verde'] > 0 else 0

# --- LÓGICA DE CÁLCULO ---
deudas = cuota_tc_sbs + p_personal + p_vehicular + p_otros
pct_deuda = (deudas / ingreso * 100) if ingreso > 0 else 0
cuota_disponible = int(max(0, (ingreso * 0.40) - deudas))
tem = (1 + tea/100)**(1/12) - 1
factor = (1 - (1 + tem)**-(plazo * 12)) / tem if tem > 0 else 0
prestamo_max = int(cuota_disponible * factor)
inicial_total = ahorros + disponible_afp

# Incremento potencial
cuota_sim = int(max(0, (ingreso * 0.40) - ((linea_tc*0.5*0.05) + p_personal + p_vehicular + p_otros)))
incremento = int((cuota_sim * factor) - prestamo_max)

escenarios_data = [
    {"nombre": "ECO-SOSTENIBLE", "monto": prestamo_max + inicial_total + m_verde, "clase": "verde", "desc": f"Bono: S/ {m_verde:,}"},
    {"nombre": "TRADICIONAL", "monto": prestamo_max + inicial_total + m_bbp, "clase": "azul", "desc": f"Bono: S/ {m_bbp:,}"},
    {"nombre": "SIN BONOS", "monto": prestamo_max + inicial_total, "clase": "gris", "desc": "Solo Recursos Propios"}
]

# --- CUERPO PRINCIPAL ---
st.title("🎯 Auditoría financiera - Inversión")
st.write("---")

# FASE 1: Semáforo y Métricas
st.subheader("1. Salud Crediticia y Diagnóstico")
col_gauge, col_mets = st.columns([1.2, 2])
with col_gauge:
    fig = go.Figure(go.Indicator(mode="gauge+number", value=pct_deuda, number={'suffix': "%", 'font': {'color': 'white'}},
        gauge={'axis': {'range': [None, 50]}, 'bar': {'color': "white"},
               'steps': [{'range': [0, 20], 'color': "#28a745"}, {'range': [20, 35], 'color': "#ffc107"}, {'range': [35, 50], 'color': "#dc3545"}]}))
    fig.update_layout(height=280, paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')
    st.plotly_chart(fig, use_container_width=True)

with col_mets:
    m1, m2 = st.columns(2)
    m1.metric("Cuota Disponible Real", f"S/ {cuota_disponible:,}")
    m2.metric("Préstamo Hipotecario", f"S/ {prestamo_max:,}")
    st.write("---")
    st.metric("Inicial Total (Ahorros + AFP)", f"S/ {inicial_total:,}")

# FASE 2: Escenarios
st.write("---")
st.subheader("2. Tu Techo de Inversión por Proyecto")
c1, c2, c3 = st.columns(3)
cols = [c1, c2, c3]
for i, esc in enumerate(escenarios_data):
    with cols[i]:
        st.markdown(f'<div class="resultado-card {esc["clase"]}"><h3>{esc["nombre"]}</h3><h1>S/ {esc["monto"]:,}</h1><p>{esc["desc"]}</p></div>', unsafe_allow_html=True)

# FASE 3: Gráfico de Barras
st.write("---")
fig_bar = px.bar(pd.DataFrame(escenarios_data), x='nombre', y='monto', color='nombre', 
                 color_discrete_map={"ECO-SOSTENIBLE": "#28a745", "TRADICIONAL": "#0e2647", "SIN BONOS": "#6c757d"}, text_auto=True)
fig_bar.update_layout(showlegend=False, paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', font=dict(color="white"))
st.plotly_chart(fig_bar, use_container_width=True)

# FASE 4: Estrategia y Gastos
st.write("---")
st.subheader("🚀 Estrategia y Optimización")
o1, o2 = st.columns(2)
with o1:
    if incremento > 0:
        st.success(f"📈 **Oportunidad:** Al bajar tu tarjeta a la mitad, tu presupuesto sube **S/ {incremento:,}**.")
    else:
        st.info("Tu nivel de deuda es saludable.")
with o2:
    gasto_est = int((prestamo_max + inicial_total) * 0.03)
    st.warning(f"📜 **Reserva Administrativa (3%):** S/ {gasto_est:,}")

# FASE 5: Finalización
st.write("---")
if st.button("✅ Finalizar Auditoría"):
    st.balloons()
    pdf_bytes = generar_pdf({'ingreso': ingreso, 'deuda_pct': pct_deuda, 'cuota_disp': cuota_disponible}, escenarios_data)
    st.download_button("📥 Descargar Reporte PDF de Marca", data=pdf_bytes, file_name="Reporte_Jancarlo_Inmobiliario.pdf")
