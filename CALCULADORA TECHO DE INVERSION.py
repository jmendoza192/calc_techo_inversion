import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from fpdf import FPDF
import base64

# 1. CONFIGURACIÓN DE PÁGINA Y ESTILOS
st.set_page_config(page_title="Auditoría Financiera | Jancarlo Inmobiliario", layout="wide")

st.markdown("""
    <style>
    .main { background-color: #f4f7f6; }
    [data-testid="stMetricValue"] { color: #1e1e1e !important; font-weight: bold !important; }
    div[data-testid="stMetric"] {
        background-color: #ffffff;
        padding: 20px;
        border-radius: 12px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.05);
        border: 1px solid #e0e0e0;
    }
    .resultado-card { 
        padding: 25px; border-radius: 15px; color: white !important; text-align: center; margin-bottom: 20px;
    }
    .verde { background: linear-gradient(135deg, #28a745, #1e7e34); }
    .azul { background: linear-gradient(135deg, #007bff, #0056b3); }
    .gris { background: linear-gradient(135deg, #6c757d, #495057); }
    </style>
    """, unsafe_allow_html=True)

# --- PANEL LATERAL: INPUTS ---
with st.sidebar:
    st.title("📊 Datos de Asesoría")
    with st.expander("💰 Ingresos y Capital", expanded=True):
        ingreso = st.number_input("Ingreso Neto Mensual (S/)", min_value=0, value=6000)
        ahorros = st.number_input("Ahorros Líquidos (S/)", min_value=0, value=15000)
        saldo_afp = st.number_input("Saldo Total en AFP (S/)", min_value=0, value=40000)
        disponible_afp = int(saldo_afp * 0.25)

    with st.expander("💳 Deudas Actuales", expanded=True):
        linea_tc = st.number_input("Línea Total de Tarjetas (S/)", min_value=0, value=10000)
        cuota_tc_sbs = int(linea_tc * 0.05)
        p_personal = st.number_input("Cuota Préstamo Personal (S/)", min_value=0, value=0)
        
    with st.expander("🎁 Bonos MiVivienda 2026", expanded=True):
        datos_bonos = {
            "Rango 1": {"min": 68800, "max": 98100, "bbp": 27400, "verde": 33700},
            "Rango 2": {"min": 98100, "max": 146900, "bbp": 22800, "verde": 29100},
            "Rango 3": {"min": 146900, "max": 244600, "bbp": 20900, "verde": 27200},
            "Rango 4": {"min": 244600, "max": 362100, "bbp": 7800, "verde": 14100},
            "Rango 5": {"min": 362100, "max": 488800, "bbp": 0, "verde": 0}
        }
        sel_rango = st.selectbox("Rango de Valor", list(datos_bonos.keys()), index=3)
        rango_info = datos_bonos[sel_rango]
        integrador = st.checkbox("Bono Integrador (+ S/ 3,600)", value=False)
        extra = 3600 if integrador else 0
        monto_bbp = rango_info['bbp'] + extra if rango_info['bbp'] > 0 else 0
        monto_bbp_verde = rango_info['verde'] + extra if rango_info['verde'] > 0 else 0

# --- LÓGICA DE CÁLCULO ---
deudas_totales = cuota_tc_sbs + p_personal
pct_endeudamiento = (deudas_totales / ingreso * 100) if ingreso > 0 else 0
cuota_disponible = int(max(0, (ingreso * 0.40) - deudas_totales))

# Cálculo de préstamo (TEA 9.5% a 20 años aprox factor 110)
prestamo_max = int(cuota_disponible * 110.3) 
inicial_total = ahorros + disponible_afp
esc_verde = prestamo_max + inicial_total + monto_bbp_verde
esc_tradicional = prestamo_max + inicial_total + monto_bbp

# --- FUNCIÓN GENERAR PDF ---
def create_pdf():
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", 'B', 16)
    pdf.cell(200, 10, "Reporte de Auditoria Financiera - Jancarlo Inmobiliario", ln=True, align='C')
    pdf.ln(10)
    pdf.set_font("Arial", '', 12)
    pdf.cell(200, 10, f"Ingreso Mensual: S/ {ingreso:,}", ln=True)
    pdf.cell(200, 10, f"Carga de Deuda SBS: {pct_endeudamiento:.1f}%", ln=True)
    pdf.cell(200, 10, f"Cuota Disponible: S/ {cuota_disponible:,}", ln=True)
    pdf.ln(5)
    pdf.set_font("Arial", 'B', 14)
    pdf.cell(200, 10, "Escenarios de Inversion:", ln=True)
    pdf.set_font("Arial", '', 12)
    pdf.cell(200, 10, f"- Eco-Sostenible: S/ {esc_verde:,}", ln=True)
    pdf.cell(200, 10, f"- MiVivienda Tradicional: S/ {esc_tradicional:,}", ln=True)
    return pdf.output(dest='S').encode('latin-1')

# --- CUERPO PRINCIPAL ---
st.title("🎯 Auditoría financiera - Inversión")
st.write("---")

col_gauge, col_mets = st.columns([1.2, 2])
with col_gauge:
    fig = go.Figure(go.Indicator(
        mode="gauge+number", value=pct_endeudamiento, number={'suffix': "%"},
        gauge={'axis': {'range': [None, 50]}, 'steps': [
            {'range': [0, 20], 'color': "#28a745"},
            {'range': [20, 35], 'color': "#ffc107"},
            {'range': [35, 50], 'color': "#dc3545"}]}))
    st.plotly_chart(fig, use_container_width=True)
    
    with st.expander("📋 Guia de Evaluacion Bancaria"):
        st.markdown(f'<p style="color:white"><b>0-20%: Perfil Prime</b></p>', unsafe_allow_html=True)
        st.markdown(f'<p style="color:white"><b>21-35%: Riesgo Medio</b></p>', unsafe_allow_html=True)
        st.markdown(f'<p style="color:white"><b>36-40%: Limite Critico</b></p>', unsafe_allow_html=True)

with col_mets:
    st.metric("Préstamo Hipotecario Estimado", f"S/ {prestamo_max:,}")
    st.metric("Inicial Total (Ahorros + AFP)", f"S/ {inicial_total:,}")

st.write("---")
st.subheader("2. Tu Techo de Inversión")
c1, c2 = st.columns(2)
c1.markdown(f'<div class="resultado-card verde"><h3>ECO-SOSTENIBLE</h3><h1>S/ {esc_verde:,}</h1></div>', unsafe_allow_html=True)
c2.markdown(f'<div class="resultado-card azul"><h3>MIVIVIENDA TRADICIONAL</h3><h1>S/ {esc_tradicional:,}</h1></div>', unsafe_allow_html=True)

if st.button("✅ Finalizar Auditoría"):
    st.balloons()
    pdf_data = create_pdf()
    st.download_button(label="📥 Descargar Reporte PDF", data=pdf_data, file_name="Auditoria_Inmobiliaria.pdf", mime="application/pdf")
