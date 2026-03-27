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
    .azul { background: linear-gradient(135deg, #0e2647, #1b3a61); } /* Color Marca */
    .gris { background: linear-gradient(135deg, #6c757d, #495057); }
    </style>
    """, unsafe_allow_html=True)

# --- FUNCIÓN GENERAR PDF CON DISEÑO DE MARCA ---
def generar_pdf(datos_informe, escenarios):
    pdf = FPDF()
    pdf.add_page()
    
    # 1. RECUADRO DE TÍTULO (Grande y Elegante)
    pdf.set_draw_color(14, 38, 71) # Azul Marca #0e2647
    pdf.set_line_width(0.8)
    pdf.rect(10, 10, 190, 25) # x, y, ancho, alto
    
    pdf.set_y(15)
    pdf.set_font("Arial", 'B', 16)
    pdf.set_text_color(14, 38, 71)
    pdf.cell(0, 10, "AUDITORIA FINANCIERA INMOBILIARIA", ln=True, align='C')
    pdf.set_font("Arial", '', 9)
    pdf.cell(0, 5, f"REPORTE TECNICO GENERADO EL {datetime.now().strftime('%d/%m/%Y %H:%M')}", ln=True, align='C')
    
    pdf.ln(15)
    
    # 2. RESUMEN PERFIL (Celdas con borde Azul Marca)
    pdf.set_font("Arial", 'B', 12)
    pdf.set_fill_color(14, 38, 71)
    pdf.set_text_color(255, 255, 255)
    pdf.cell(0, 10, " 1. DIAGNOSTICO DE SALUD CREDITICIA", ln=True, fill=True)
    
    pdf.ln(2)
    pdf.set_text_color(30, 30, 30)
    pdf.set_font("Arial", '', 11)
    
    # Filas de datos
    pdf.cell(95, 10, f" Ingreso Neto Mensual:", "B")
    pdf.cell(0, 10, f"S/ {datos_informe['ingreso']:,}", "B", ln=True, align='R')
    pdf.cell(95, 10, f" Carga de Deuda SBS:", "B")
    pdf.cell(0, 10, f"{datos_informe['deuda_pct']:.2f}%", "B", ln=True, align='R')
    pdf.cell(95, 10, f" Capacidad de Cuota Hipotecaria:", "B")
    pdf.cell(0, 10, f"S/ {datos_informe['cuota_disp']:,}", "B", ln=True, align='R')
    
    pdf.ln(10)
    
    # 3. TABLA DE ESCENARIOS (Estilo Moderno)
    pdf.set_font("Arial", 'B', 12)
    pdf.set_fill_color(14, 38, 71)
    pdf.set_text_color(255, 255, 255)
    pdf.cell(0, 10, " 2. TECHOS DE INVERSION Y BONOS", ln=True, fill=True)
    
    pdf.ln(4)
    pdf.set_font("Arial", 'B', 10)
    pdf.set_fill_color(215, 179, 93) # Amarillo Marca #d7b35d
    pdf.cell(70, 10, " ESCENARIO", 0, 0, 'L', True)
    pdf.cell(60, 10, " INVERSION TOTAL", 0, 0, 'C', True)
    pdf.cell(60, 10, " DETALLE BONOS", 0, 1, 'C', True)
    
    pdf.set_text_color(30, 30, 30)
    pdf.set_font("Arial", '', 10)
    for esc in escenarios:
        pdf.cell(70, 10, f" {esc['nombre']}", "B")
        pdf.cell(60, 10, f"S/ {esc['monto']:,}", "B", 0, 'C')
        pdf.cell(60, 10, f"{esc['desc']}", "B", 1, 'C')
    
    pdf.ln(10)
    
    # 4. NOTA LEGAL Y ESTRATEGIA
    pdf.set_font("Arial", 'B', 10)
    pdf.set_text_color(14, 38, 71)
    pdf.cell(0, 8, "NOTAS ESTRATEGICAS:", ln=True)
    pdf.set_font("Arial", '', 9)
    pdf.set_text_color(50, 50, 50)
    
    # Texto solicitado con "Referencial" resaltado (FPDF requiere separar para negritas)
    pdf.write(5, "Este documento es una ")
    pdf.set_font("Arial", 'B', 9)
    pdf.write(5, "proyeccion tecnica referencial")
    pdf.set_font("Arial", '', 9)
    pdf.write(5, " basada en politicas bancarias generales para creditos hipotecarios.\n")
    pdf.ln(2)
    pdf.write(5, "Informacion de Bonos MiVivienda y Bono Verde actualizada al año 2026.\n")
    
    # 5. PIE DE PÁGINA MINIMALISTA (Barra Amarilla)
    pdf.set_y(-25)
    pdf.set_fill_color(215, 179, 93) # Amarillo Marca
    pdf.rect(10, 275, 190, 1, 'F') # Línea decorativa
    pdf.set_font("Arial", 'I', 8)
    pdf.set_text_color(100, 100, 100)
    pdf.cell(0, 10, "Jancarlo Inmobiliario - Consultoria en Inversion y Real Estate", 0, 0, 'C')

    return pdf.output(dest='S').encode('latin-1')

# --- LÓGICA DE DATOS (Basada en tu versión preferida) ---
with st.sidebar:
    st.title("📊 Datos de Asesoría")
    with st.expander("💰 Ingresos y Capital", expanded=True):
        ingreso = st.number_input("Ingreso Neto Mensual (S/)", min_value=0, value=6000, step=100)
        ahorros = st.number_input("Ahorros Líquidos (S/)", min_value=0, value=15000)
        saldo_afp = st.number_input("Saldo Total en AFP (S/)", min_value=0, value=40000)
        disponible_afp = int(saldo_afp * 0.25)

    with st.expander("💳 Subgrupo 1: Tarjetas de Crédito", expanded=True):
        linea_tc = st.number_input("Línea Total de Tarjetas (S/)", min_value=0, value=10000)
        cuota_tc_sbs = int(linea_tc * 0.05)

    with st.expander("🏦 Subgrupo 2: Otras Cuotas Fijas", expanded=True):
        p_personal = st.number_input("Cuota Préstamo Personal (S/)", min_value=0, value=0)
        p_vehicular = st.number_input("Cuota Préstamo Vehicular (S/)", min_value=0, value=0)
        p_otros = st.number_input("Otros Créditos (S/)", min_value=0, value=0)

    with st.expander("🎁 Bonos MiVivienda (2026)", expanded=True):
        datos_bonos = {
            "Rango 1": {"min": 68800, "max": 98100, "bbp": 27400, "verde": 33700},
            "Rango 2": {"min": 98100, "max": 146900, "bbp": 22800, "verde": 29100},
            "Rango 3": {"min": 146900, "max": 244600, "bbp": 20900, "verde": 27200},
            "Rango 4": {"min": 244600, "max": 362100, "bbp": 7800, "verde": 14100},
            "Rango 5": {"min": 362100, "max": 488800, "bbp": 0, "verde": 0}
        }
        sel_rango = st.selectbox("Rango", list(datos_bonos.keys()), index=3)
        integrador = st.checkbox("Bono Integrador (+3,600)", value=False)
        monto_bbp = datos_bonos[sel_rango]['bbp'] + (3600 if integrador else 0)
        monto_bbp_verde = datos_bonos[sel_rango]['verde'] + (3600 if integrador else 0)

# --- CÁLCULOS ---
deudas = cuota_tc_sbs + p_personal + p_vehicular + p_otros
pct_deuda = (deudas / ingreso * 100) if ingreso > 0 else 0
cuota_disp = int(max(0, (ingreso * 0.40) - deudas))
prestamo = int(cuota_disp * 110.3) # Estimado rápido
inicial = ahorros + disponible_afp

escenarios_pdf = [
    {"nombre": "ECO-SOSTENIBLE", "monto": prestamo + inicial + monto_bbp_verde, "desc": f"Bonos: S/ {monto_bbp_verde:,}"},
    {"nombre": "MIVIVIENDA TRADICIONAL", "monto": prestamo + inicial + monto_bbp, "desc": f"Bono: S/ {monto_bbp:,}"},
    {"nombre": "SIN BONOS", "monto": prestamo + inicial, "desc": "Solo Fondos Propios"}
]

# --- UI PRINCIPAL (Manteniendo tu estructura) ---
st.title("🎯 Auditoría financiera - Inversión")
st.write("---")

col1, col2 = st.columns([1.2, 2])
with col1:
    fig = go.Figure(go.Indicator(mode="gauge+number", value=pct_deuda, number={'suffix': "%"}))
    st.plotly_chart(fig, use_container_width=True)

with col2:
    st.metric("Préstamo Hipotecario Estimado", f"S/ {prestamo:,}")
    st.metric("Inicial Total", f"S/ {inicial:,}")

st.write("---")
if st.button("✅ Finalizar Auditoría"):
    st.balloons()
    
    datos_pdf = {
        'ingreso': ingreso,
        'deuda_pct': pct_deuda,
        'cuota_disp': cuota_disp,
        'prestamo_max': prestamo
    }
    
    pdf_bytes = generar_pdf(datos_pdf, escenarios_pdf)
    
    st.download_button(
        label="📥 Descargar Reporte Oficial (PDF)",
        data=pdf_bytes,
        file_name=f"Reporte_Inversion_{datetime.now().strftime('%Y%m%d')}.pdf",
        mime="application/pdf"
    )
