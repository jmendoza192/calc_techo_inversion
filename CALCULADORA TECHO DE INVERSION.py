import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from fpdf import FPDF
from datetime import datetime

# 1. CONFIGURACIÓN DE PÁGINA Y ESTILOS UI (Restauración Visual)
st.set_page_config(page_title="Auditoría Financiera | Jancarlo Inmobiliario", layout="wide")

st.markdown("""
    <style>
    .main { background-color: #0e1117; } /* Fondo oscuro original */
    [data-testid="stMetricValue"] { color: #ffffff !important; font-weight: bold !important; font-size: 2.2rem !important; }
    [data-testid="stMetricLabel"] { color: #a1a1a1 !important; font-size: 1.1rem !important; }
    div[data-testid="stMetric"] {
        background-color: #1f2630;
        padding: 25px;
        border-radius: 15px;
        border: 1px solid #30363d;
    }
    .resultado-card { 
        padding: 30px; 
        border-radius: 15px; 
        color: white !important; 
        text-align: center;
        margin-bottom: 20px;
    }
    .verde { background-color: #28a745; }
    .azul { background-color: #0e2647; }
    .gris { background-color: #6c757d; }
    
    #MainMenu, footer, header {visibility: hidden;}
    </style>
    """, unsafe_allow_html=True)

# --- FUNCIÓN PDF (Ajustada a tus colores de marca) ---
def generar_pdf(datos_informe, escenarios):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_draw_color(14, 38, 71) # Azul #0e2647
    pdf.set_line_width(0.8)
    pdf.rect(10, 10, 190, 25)
    pdf.set_y(15)
    pdf.set_font("Arial", 'B', 16)
    pdf.set_text_color(14, 38, 71)
    pdf.cell(0, 10, "AUDITORIA FINANCIERA INMOBILIARIA", ln=True, align='C')
    pdf.ln(20)
    
    # Tabla de datos
    pdf.set_font("Arial", 'B', 12)
    pdf.set_fill_color(14, 38, 71)
    pdf.set_text_color(255, 255, 255)
    pdf.cell(0, 10, " 1. RESUMEN FINANCIERO", ln=True, fill=True)
    pdf.ln(2)
    pdf.set_text_color(30, 30, 30)
    pdf.set_font("Arial", '', 11)
    for k, v in datos_informe.items():
        pdf.cell(95, 10, f" {k}:", "B")
        pdf.cell(0, 10, f"{v}", "B", ln=True, align='R')
    
    pdf.ln(10)
    pdf.set_font("Arial", 'B', 12)
    pdf.set_fill_color(215, 179, 93) # Dorado #d7b35d
    pdf.cell(0, 10, " 2. ESCENARIOS DE INVERSION", ln=True, fill=True)
    pdf.ln(2)
    for esc in escenarios:
        pdf.set_font("Arial", 'B', 10)
        pdf.cell(70, 10, f" {esc['nombre']}", "B")
        pdf.cell(60, 10, f" S/ {esc['monto']:,}", "B", 0, 'C')
        pdf.cell(60, 10, f" {esc['desc']}", "B", 1, 'C')
    
    pdf.ln(10)
    pdf.set_font("Arial", '', 9)
    pdf.write(5, "Este documento es una ")
    pdf.set_font("Arial", 'B', 9)
    pdf.write(5, "proyeccion tecnica referencial")
    pdf.set_font("Arial", '', 9)
    pdf.write(5, " basada en politicas bancarias generales.\nDatos de Bonos MiVivienda actualizados a 2026.")
    
    return pdf.output(dest='S').encode('latin-1')

# --- SIDEBAR (Entradas de datos) ---
with st.sidebar:
    st.title("📊 Datos de Asesoría")
    with st.expander("💰 Ingresos y Capital", expanded=True):
        ingreso = st.number_input("Ingreso Neto Mensual (S/)", min_value=0, value=6000)
        ahorros = st.number_input("Ahorros Líquidos (S/)", min_value=0, value=15000)
        saldo_afp = st.number_input("Saldo Total en AFP (S/)", min_value=0, value=40000)
        disponible_afp = int(saldo_afp * 0.25)
        st.info(f"AFP Disponible: S/ {disponible_afp:,}")

    with st.expander("💳 Subgrupo 1: Tarjetas", expanded=True):
        linea_tc = st.number_input("Línea Total (S/)", value=10000)
        cuota_tc = int(linea_tc * 0.05)

    with st.expander("🏦 Subgrupo 2: Cuotas Fijas", expanded=True):
        p_personal = st.number_input("Préstamo Personal (S/)", value=0)
        p_vehicular = st.number_input("Préstamo Vehicular (S/)", value=0)
        p_otros = st.number_input("Otros (S/)", value=0)

    with st.expander("🎁 Bonos MiVivienda (2026)", expanded=True):
        datos_bonos = {
            "Rango 1": {"bbp": 27400, "verde": 33700},
            "Rango 2": {"bbp": 22800, "verde": 29100},
            "Rango 3": {"bbp": 20900, "verde": 27200},
            "Rango 4": {"bbp": 7800, "verde": 14100},
            "Rango 5": {"bbp": 0, "verde": 0}
        }
        sel_rango = st.selectbox("Rango de Valor", list(datos_bonos.keys()), index=3)
        integrador = st.checkbox("Bono Integrador (+3,600)")
        m_bbp = datos_bonos[sel_rango]['bbp'] + (3600 if integrador else 0)
        m_verde = datos_bonos[sel_rango]['verde'] + (3600 if integrador else 0)

# --- CÁLCULOS ---
deudas = cuota_tc + p_personal + p_vehicular + p_otros
pct_deuda = (deudas / ingreso * 100) if ingreso > 0 else 0
cuota_disponible = int(max(0, (ingreso * 0.40) - deudas))
prestamo_est = int(cuota_disponible * 110.3)
inicial_total = ahorros + disponible_afp

# --- UI CUERPO (Restauración de Columnas) ---
st.title("🎯 Auditoría financiera - Inversión")
st.write("Diagnóstico técnico bajo normativa SBS y MiVivienda 2026.")
st.write("---")

st.subheader("1. Salud Crediticia y Diagnóstico")
col_gauge, col_mets = st.columns([1.2, 2])

with col_gauge:
    fig = go.Figure(go.Indicator(
        mode="gauge+number", value=pct_deuda,
        number={'suffix': "%", 'font':{'color':'white'}},
        gauge={'axis': {'range': [None, 50]},
               'bar': {'color': "#ffffff"},
               'steps': [
                   {'range': [0, 20], 'color': "#28a745"},
                   {'range': [20, 35], 'color': "#ffc107"},
                   {'range': [35, 50], 'color': "#dc3545"}]}))
    fig.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', height=300)
    st.plotly_chart(fig, use_container_width=True)

with col_mets:
    c1, c2 = st.columns(2)
    c1.metric("Cuota Disponible Real", f"S/ {cuota_disponible:,}")
    c2.metric("Préstamo Hipotecario", f"S/ {prestamo_est:,}")
    st.write("---")
    st.metric("Inicial Total (Ahorros + AFP)", f"S/ {inicial_total:,}")

st.write("---")
st.subheader("2. Tu Techo de Inversión por Proyecto")
e1, e2, e3 = st.columns(3)
escenarios = [
    {"nombre": "ECO-SOSTENIBLE", "monto": prestamo_est + inicial_total + m_verde, "clase": "verde", "desc": f"Bono: S/ {m_verde:,}"},
    {"nombre": "TRADICIONAL", "monto": prestamo_est + inicial_total + m_bbp, "clase": "azul", "desc": f"Bono: S/ {m_bbp:,}"},
    {"nombre": "SIN BONOS", "monto": prestamo_est + inicial_total, "clase": "gris", "desc": "Solo Rec. Propios"}
]

for i, col in enumerate([e1, e2, e3]):
    with col:
        st.markdown(f'<div class="resultado-card {escenarios[i]["clase"]}"><h3>{escenarios[i]["nombre"]}</h3><h1>S/ {escenarios[i]["monto"]:,}</h1><p>{escenarios[i]["desc"]}</p></div>', unsafe_allow_html=True)

# --- BOTÓN FINAL ---
st.write("---")
if st.button("✅ Finalizar Auditoría"):
    st.balloons()
    datos_pdf = {
        "Ingreso Mensual": f"S/ {ingreso:,}",
        "Deuda Actual": f"{pct_deuda:.2f}%",
        "Cuota Disponible": f"S/ {cuota_disponible:,}",
        "Capacidad de Credito": f"S/ {prestamo_est:,}"
    }
    pdf_output = generar_pdf(datos_pdf, escenarios)
    st.download_button("📥 Descargar Reporte PDF de Marca", data=pdf_output, file_name="Auditoria_Inmobiliaria.pdf", mime="application/pdf")
