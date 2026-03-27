import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from fpdf import FPDF
from datetime import datetime

# 1. CONFIGURACIÓN DE PÁGINA Y ESTILOS UI (WEB BACKUP ORIGINAL)
st.set_page_config(page_title="Auditoría Financiera | Jancarlo Inmobiliario", layout="wide")

st.markdown("""
    <style>
    .main { background-color: #0e1117; }
    [data-testid="stMetricValue"] { color: #ffffff !important; font-weight: bold !important; font-size: 1.9rem !important; }
    [data-testid="stMetricLabel"] { color: #a1a1a1 !important; font-size: 0.9rem !important; }
    div[data-testid="stMetric"] {
        background-color: #1f2630;
        padding: 18px;
        border-radius: 12px;
        border: 1px solid #30363d;
    }
    .resultado-card { 
        padding: 22px; border-radius: 15px; color: white !important; text-align: center; margin-bottom: 20px;
        min-height: 200px;
    }
    .verde { background: linear-gradient(135deg, #28a745, #1e7e34); }
    .azul { background: linear-gradient(135deg, #0e2647, #1b3a61); }
    .gris { background: linear-gradient(135deg, #6c757d, #495057); }
    
    .opt-card {
        padding: 18px; 
        border-radius: 10px; 
        height: 100%;
        display: flex;
        flex-direction: column;
        justify-content: center;
    }
    .opt-blue { background-color: #1e3a8a; border: 1px solid #3b82f6; }
    .opt-green { background-color: #064e3b; border: 1px solid #10b981; }
    
    .opt-header { margin-top:0; font-size: 1.05rem; font-weight: bold; margin-bottom: 5px; }
    .header-blue { color: #60a5fa; }
    .header-green { color: #34d399; }
    
    .opt-text { font-size: 0.85rem; color: #d1d5db; margin-bottom: 8px; line-height: 1.2; }
    .opt-monto { color: white; margin-bottom: 0; font-size: 1.45rem; font-weight: bold; }
    
    #MainMenu, footer, header {visibility: hidden;}
    </style>
    """, unsafe_allow_html=True)

# --- 2. FUNCIÓN DE EXPORTACIÓN PDF PROFESIONAL ---
def generar_pdf(datos_informe, escenarios, seleccion_bono):
    pdf = FPDF()
    pdf.add_page()
    
    # Encabezado y Título con fecha
    pdf.set_draw_color(14, 38, 71); pdf.set_line_width(0.8); pdf.rect(10, 10, 190, 30)
    pdf.set_y(15); pdf.set_font("Arial", 'B', 16); pdf.set_text_color(14, 38, 71)
    pdf.cell(0, 10, "AUDITORIA FINANCIERA INMOBILIARIA", ln=True, align='C')
    
    ahora = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    pdf.set_font("Arial", '', 9); pdf.set_text_color(100, 100, 100)
    pdf.cell(0, 5, f"Fecha y hora de realizacion: {ahora}", ln=True, align='C')
    
    pdf.ln(15)
    
    # Sección 1: Diagnóstico
    pdf.set_fill_color(14, 38, 71); pdf.set_text_color(255, 255, 255); pdf.set_font("Arial", 'B', 12)
    pdf.cell(0, 10, " 1. DIAGNOSTICO FINANCIERO", ln=True, fill=True)
    pdf.ln(2); pdf.set_text_color(30, 30, 30); pdf.set_font("Arial", '', 11)
    for k, v in datos_informe.items():
        pdf.cell(95, 10, f" {k}:", "B"); pdf.cell(0, 10, f"{v}", "B", ln=True, align='R')
    
    pdf.ln(10)
    
    # Sección 2: Techos en Negrita
    pdf.set_fill_color(215, 179, 93); pdf.set_text_color(14, 38, 71); pdf.set_font("Arial", 'B', 12)
    pdf.cell(0, 10, " 2. TECHOS DE INVERSION", ln=True, fill=True)
    pdf.set_font("Arial", 'B', 10)
    for esc in escenarios:
        pdf.cell(70, 10, f" {esc['nombre']}", "B")
        pdf.cell(60, 10, f" S/ {esc['monto']:,}", "B", 0, 'C')
        pdf.cell(60, 10, f" {esc['desc']}", "B", 1, 'C')
    
    pdf.ln(10)
    
    # Notas Referenciales (Bonos MiVivienda Actualizados)
    pdf.set_font("Arial", 'I', 9); pdf.set_text_color(80, 80, 80)
    texto_ref = (
        "IMPORTANTE: Este reporte es estrictamente REFERENCIAL y no constituye una aprobacion de credito. "
        f"Los calculos consideran los Bonos MiVivienda actualizados al 2026 para el rango {seleccion_bono}. "
        "La aprobacion final depende de la evaluacion de riesgos bancaria y la tasacion del inmueble."
    )
    pdf.multi_cell(0, 5, texto_ref)
    
    pdf.ln(20)
    
    # Firma y Redes Sociales
    pdf.set_draw_color(215, 179, 93); pdf.line(120, pdf.get_y(), 200, pdf.get_y()); pdf.ln(2)
    pdf.set_font("Arial", 'B', 11); pdf.set_text_color(14, 38, 71)
    pdf.cell(0, 6, "Realizado por: Ing. Jancarlo Mendoza - Asesoria Inmobiliaria", ln=True, align='R')
    pdf.set_font("Arial", '', 10); pdf.cell(0, 6, "Redes Sociales: @jancarlo.inmobiliario", ln=True, align='R')
    
    return pdf.output(dest='S').encode('latin-1')

# --- 3. PANEL LATERAL (INPUTS) ---
with st.sidebar:
    st.title("📊 Datos de Asesoría")
    
    with st.expander("💰 Ingresos y Capital", expanded=True):
        ingreso = st.number_input("Ingreso Neto Mensual (S/)", min_value=0, value=6000)
        ahorros = st.number_input("Ahorros Líquidos (S/)", min_value=0, value=15000)
        saldo_afp = st.number_input("Saldo Total en AFP (S/)", min_value=0, value=40000)
        disponible_afp = int(saldo_afp * 0.25)
        st.caption(f"✅ Disponible para inicial (25% AFP): S/ {disponible_afp:,}")

    with st.expander("💳 Subgrupo 1: Tarjetas", expanded=True):
        linea_tc = st.number_input("Línea de crédito total (S/.)", value=10000)
        cuota_tc_sbs = int(linea_tc * 0.05)
        st.caption(f"Carga financiera estimada (5% SBS): S/ {cuota_tc_sbs:,}")

    with st.expander("🏦 Subgrupo 2: Otras Cuotas", expanded=True):
        p_personal = st.number_input("Cuota Préstamo Personal (S/)", value=0)
        p_vehicular = st.number_input("Cuota Préstamo Vehicular (S/)", value=0)
        p_otros = st.number_input("Otros Créditos (S/)", value=0)
    
    with st.expander("🏦 Condiciones", expanded=False):
        tea = st.number_input("TEA (%)", value=9.5); plazo = st.number_input("Años", value=20)

    with st.expander("🎁 Bonos MiVivienda (2026)", expanded=True):
        datos_bonos = {
            "R1": {"b": 27400, "v": 33700, "rango": "S/ 68,000 - S/ 102,800"},
            "R2": {"b": 22800, "v": 29100, "rango": "S/ 102,801 - S/ 154,300"},
            "R3": {"b": 20900, "v": 27200, "rango": "S/ 154,301 - S/ 257,000"},
            "R4": {"b": 7800, "v": 14100, "rango": "S/ 257,001 - S/ 355,100"},
            "R5": {"b": 0, "v": 0, "rango": "Más de S/ 355,100 (Sin Bono)"}
        }
        sel = st.selectbox("Seleccione Rango de Vivienda", list(datos_bonos.keys()), index=3)
        st.caption(f"🏷️ Precio Vivienda: {datos_bonos[sel]['rango']}")
        
        integrador = st.checkbox("¿Bono Integrador? (+3,600)")
        extra = 3600 if integrador else 0
        m_bbp = datos_bonos[sel]['b'] + extra if datos_bonos[sel]['b'] > 0 else 0
        m_verde = datos_bonos[sel]['v'] + extra if datos_bonos[sel]['v'] > 0 else 0

# --- 4. LÓGICA FINANCIERA ---
deudas = cuota_tc_sbs + p_personal + p_vehicular + p_otros
pct_deuda = (deudas / ingreso * 100) if ingreso > 0 else 0
cuota_disp = int(max(0, (ingreso * 0.40) - deudas))
tem = (1 + tea/100)**(1/12) - 1
factor = (1 - (1 + tem)**-(plazo * 12)) / tem if tem > 0 else 0
prestamo = int(cuota_disp * factor)
inicial = ahorros + disponible_afp

escenarios = [
    {"nombre": "ECO-SOSTENIBLE", "monto": prestamo + inicial + m_verde, "clase": "verde", "desc": f"Bono: S/ {m_verde:,}"},
    {"nombre": "TRADICIONAL", "monto": prestamo + inicial + m_bbp, "clase": "azul", "desc": f"Bono: S/ {m_bbp:,}"},
    {"nombre": "SIN BONOS", "monto": prestamo + inicial, "clase": "gris", "desc": "Solo Rec. Propios"}
]

# --- 5. INTERFAZ WEB (SECCIÓN 1: DIAGNÓSTICO) ---
st.title("🎯 Auditoría financiera - Inversión")
st.write("---")
st.subheader("1. Salud Crediticia y Diagnóstico")

col_gauge, col_metrics = st.columns([1.2, 2])
with col_gauge:
    fig = go.Figure(go.Indicator(mode="gauge+number", value=pct_deuda, title={'text': "Carga de Deuda Actual"},
        number={'suffix': "%", 'font':{'color':'white'}},
        gauge={'axis': {'range': [None, 50]}, 'bar': {'color': "white"},
               'steps': [{'range': [0, 20], 'color': "#28a745"}, {'range': [20, 35], 'color': "#ffc107"}, {'range': [35, 50], 'color': "#dc3545"}]}))
    fig.update_layout(height=350, paper_bgcolor='rgba(0,0,0,0)', font={'color': "white"})
    st.plotly_chart(fig, use_container_width=True)

with col_metrics:
    met_c1, met_c2 = st.columns(2)
    met_c1.metric("Cuota Disponible Real", f"S/ {cuota_disp:,}")
    met_c2.metric("Préstamo Hipotecario", f"S/ {prestamo:,}")
    st.write("")
    st.metric("Inicial Total (Ahorros + AFP)", f"S/ {inicial:,}")
    st.info("💡 **Dato Bancario:** Los bancos limitan tus deudas mensuales al 40% de tus ingresos netos.")

# --- SECCIÓN 2: TECHOS DE INVERSIÓN ---
st.write("---")
st.subheader("2. Tu Techo de Inversión por Proyecto")
e1, e2, e3 = st.columns(3)

for i, col in enumerate([e1, e2, e3]):
    esc = escenarios[i]
    porcentaje_inicial = (inicial / esc['monto']) * 100 if esc['monto'] > 0 else 0
    with col:
        st.markdown(f"""
            <div class="resultado-card {esc['clase']}">
                <h3 style="font-size: 1.1rem;">{esc['nombre']}</h3>
                <h1 style="font-size: 1.9rem;">S/ {esc['monto']:,}</h1>
                <p style="font-size: 0.9rem;">{esc['desc']}</p>
                <hr style="border: 0.5px solid rgba(255,255,255,0.3)">
                <p style="font-size: 0.9rem;"><b>Inicial Real: {porcentaje_inicial:.2f}%</b></p>
            </div>
        """, unsafe_allow_html=True)

# --- 6. SECCIÓN 3: VALIDACIÓN DE POLÍTICAS ---
st.write("")
st.subheader("🚀 Validación de Políticas e Inicial Mínima")
v1, v2, v3 = st.columns(3)

porcentaje_ref = (inicial / escenarios[1]['monto']) if escenarios[1]['monto'] > 0 else 0

with v1:
    if porcentaje_ref >= 0.075:
        st.success(f"✅ **Fondo Mivivienda:** Su inicial de S/ {inicial:,} cumple con el 7.5% mínimo legal.")
    else:
        st.error(f"⚠️ **Fondo Mivivienda:** Su inicial ({porcentaje_ref*100:.1f}%) es menor al 7.5% legal.")

with v2:
    if porcentaje_ref >= 0.10:
        st.success("🏦 **Perfil Bancario:** Su inicial supera el 10%, facilitando la aprobación comercial.")
    else:
        st.warning(f"🏦 **Perfil Bancario:** Inicial de {porcentaje_ref*100:.1f}%. El banco podría pedir llegar al 10%.")

with v3:
    reserva = int((prestamo + inicial) * 0.03)
    st.warning(f"📜 **Reserva Administrativa (3%):** Necesitarás **S/ {reserva:,}** para gastos de notaría y registros.")

# --- 7. SECCIÓN 4: ESTRATEGIAS DE OPTIMIZACIÓN ---
st.write("---")
st.subheader("💡 Estrategias de Optimización")
opt_col1, opt_col2, opt_col3 = st.columns(3)

with opt_col1:
    cuota_sim_deuda = int(max(0, (ingreso * 0.40) - ((linea_tc*0.5*0.05)+p_personal+p_vehicular+p_otros)))
    inc_deuda = int((cuota_sim_deuda * factor) - prestamo)
    monto_opt1 = inc_deuda if inc_deuda > 0 else 0
    st.markdown(f"""
        <div class="opt-card opt-blue">
            <div class="opt-header header-blue">📈 Proyección por Deuda</div>
            <div class="opt-text">Bajando tus tarjetas al 50%, tu techo de inversión sube:</div>
            <div class="opt-monto">+ S/ {monto_opt1:,}</div>
        </div>
    """, unsafe_allow_html=True)

with opt_col2:
    ingreso_proy = ingreso + 500
    cuota_proy = int(max(0, (ingreso_proy * 0.40) - deudas))
    prestamo_proy = int(cuota_proy * factor)
    inc_ingreso = prestamo_proy - prestamo
    st.markdown(f"""
        <div class="opt-card opt-blue">
            <div class="opt-header header-blue">🚀 Proyección por Ingresos</div>
            <div class="opt-text">Si tus ingresos aumentan en <b>S/ 500</b>, tu techo de inversión sube:</div>
            <div class="opt-monto">+ S/ {inc_ingreso:,}</div>
        </div>
    """, unsafe_allow_html=True)

with opt_col3:
    ahorro_extra = 5000
    nuevo_techo = escenarios[1]['monto'] + ahorro_extra
    nueva_inicial_pct = ((inicial + ahorro_extra) / nuevo_techo) * 100 if nuevo_techo > 0 else 0
    st.markdown(f"""
        <div class="opt-card opt-green">
            <div class="opt-header header-green">💰 Ahorro Estratégico</div>
            <div class="opt-text">Si ahorras <b>S/ 5,000</b> extra, tu inicial sube a:</div>
            <div class="opt-monto">{nueva_inicial_pct:.2f}%</div>
            <div style="font-size: 0.75rem; color: #a7f3d0; margin-top: 5px; line-height: 1.1;">
                * Hace más viable el crédito y permite negociar una mejor tasa bancaria.
            </div>
        </div>
    """, unsafe_allow_html=True)

# --- 8. BOTÓN FINAL (PDF REFORZADO) ---
st.write("")
if st.button("✅ Finalizar Auditoría"):
    st.balloons()
    datos_pdf = {
        "Ingreso Mensual Neto": f"S/ {ingreso:,}",
        "Carga de Deuda (SBS)": f"{pct_deuda:.2f}%",
        "Cuota Disponible Hipotecaria": f"S/ {cuota_disp:,}",
        "Capital Disponible (Inicial)": f"S/ {inicial:,}",
        "TEA Proyectada": f"{tea}%"
    }
    pdf_bytes = generar_pdf(datos_pdf, escenarios, sel)
    st.download_button("📥 Descargar Reporte PDF Profesional", data=pdf_bytes, file_name=f"Auditoria_{datetime.now().strftime('%Y%m%d')}.pdf", mime="application/pdf")
