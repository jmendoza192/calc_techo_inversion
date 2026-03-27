import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

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

    with st.expander("💳 Subgrupo 1: Tarjetas de Crédito", expanded=True):
        linea_tc = st.number_input("Línea Total de Tarjetas (S/)", min_value=0, value=10000, step=500)
        cuota_tc_sbs = int(linea_tc * 0.05)
        st.warning(f"⚠️ Cuota teórica SBS (5%): S/ {cuota_tc_sbs:,}")

    with st.expander("🏦 Subgrupo 2: Otras Cuotas Fijas", expanded=True):
        p_personal = st.number_input("Cuota Préstamo Personal (S/)", min_value=0, value=0)
        p_vehicular = st.number_input("Cuota Préstamo Vehicular (S/)", min_value=0, value=0)
        p_otros = st.number_input("Otros Créditos (S/)", min_value=0, value=0)
        
    with st.expander("🏦 Condiciones del Crédito", expanded=False):
        tea = st.number_input("Tasa Efectiva Anual - TEA (%)", min_value=1.0, max_value=20.0, value=9.5, step=0.1)
        plazo_anios = st.number_input("Plazo del Préstamo (Años)", min_value=5, max_value=30, value=20, step=1)
        
    with st.expander("🎁 Bonos MiVivienda (Tabla 2026)", expanded=True):
        datos_bonos = {
            "Rango 1": {"min": 68800, "max": 98100, "bbp": 27400, "verde": 33700},
            "Rango 2": {"min": 98100, "max": 146900, "bbp": 22800, "verde": 29100},
            "Rango 3": {"min": 146900, "max": 244600, "bbp": 20900, "verde": 27200},
            "Rango 4": {"min": 244600, "max": 362100, "bbp": 7800, "verde": 14100},
            "Rango 5": {"min": 362100, "max": 488800, "bbp": 0, "verde": 0}
        }
        seleccion_rango = st.selectbox("Seleccionar Rango de Valor", list(datos_bonos.keys()), index=3)
        rango_info = datos_bonos[seleccion_rango]
        st.success(f"🏠 Valor Vivienda: S/ {rango_info['min']:,} - S/ {rango_info['max']:,}")
        
        integrador = st.checkbox("¿Aplica Bono Integrador? (+ S/ 3,600)", value=False)
        extra_integrador = 3600 if integrador else 0
        
        monto_bbp = rango_info['bbp'] + extra_integrador if rango_info['bbp'] > 0 else 0
        monto_bbp_verde = rango_info['verde'] + extra_integrador if rango_info['verde'] > 0 else 0

# --- LÓGICA DE CÁLCULO ---
deudas_totales = cuota_tc_sbs + p_personal + p_vehicular + p_otros
pct_endeudamiento = (deudas_totales / ingreso * 100) if ingreso > 0 else 0
capacidad_40 = ingreso * 0.40
cuota_disponible = int(max(0, capacidad_40 - deudas_totales))

tem = (1 + tea/100)**(1/12) - 1
n_meses = plazo_anios * 12
factor = (1 - (1 + tem)**-n_meses) / tem if tem > 0 else 0
prestamo_max = int(cuota_disponible * factor)

cuota_tc_sim = int((linea_tc * 0.5) * 0.05)
cuota_disp_sim = int(max(0, capacidad_40 - (cuota_tc_sim + p_personal + p_vehicular + p_otros)))
prestamo_max_simulado = int(cuota_disp_sim * factor)
incremento_prestamo = prestamo_max_simulado - prestamo_max
inicial_total = ahorros + disponible_afp

esc_verde = int(prestamo_max + inicial_total + monto_bbp_verde)
esc_tradicional = int(prestamo_max + inicial_total + monto_bbp)
esc_directo = int(prestamo_max + inicial_total)

escenarios_data = [
    {"nombre": "ECO-SOSTENIBLE", "monto": esc_verde, "clase": "verde", "color_hex": "#28a745", "desc": f"Bonos: S/ {monto_bbp_verde:,}"},
    {"nombre": "TRADICIONAL", "monto": esc_tradicional, "clase": "azul", "color_hex": "#007bff", "desc": f"Bono: S/ {monto_bbp:,}"},
    {"nombre": "SIN BONOS", "monto": esc_directo, "clase": "gris", "color_hex": "#6c757d", "desc": "Solo Recursos Propios"}
]

# --- CUERPO PRINCIPAL ---
st.title("🎯 Auditoría financiera - Inversión")
st.write(f"Diagnóstico técnico bajo normativa SBS y MiVivienda 2026.")
st.write("---")

# FASE 1: Semáforo y Métricas
st.subheader("1. Salud Crediticia y Diagnóstico")
col_gauge, col_mets = st.columns([1.2, 2])

with col_gauge:
    # GRÁFICO DEL SEMÁFORO
    fig_gauge = go.Figure(go.Indicator(
        mode = "gauge+number",
        value = pct_endeudamiento,
        number = {'suffix': "%", 'font': {'size': 26}},
        title = {'text': "Carga de Deuda Actual", 'font': {'size': 18}},
        gauge = {
            'axis': {'range': [None, 50], 'tickwidth': 1},
            'bar': {'color': "#1e1e1e"},
            'steps': [
                {'range': [0, 20], 'color': "#28a745"},
                {'range': [20, 35], 'color': "#ffc107"},
                {'range': [35, 50], 'color': "#dc3545"}],
            'threshold': {
                'line': {'color': "red", 'width': 4},
                'thickness': 0.75,
                'value': 40}
        }))
    fig_gauge.update_layout(height=280, margin=dict(l=30, r=30, t=50, b=10))
    st.plotly_chart(fig_gauge, use_container_width=True)
    
    # GUÍA TÉCNICA (DEBAJO DEL SEMÁFORO)
    st.markdown("""
    <div style="background-color: #ffffff; padding: 18px; border-radius: 12px; border: 1px solid #e0e0e0; box-shadow: 0 2px 4px rgba(0,0,0,0.05);">
        <p style="font-size: 1rem; font-weight: bold; margin-bottom: 12px; color: #1e1e1e; border-bottom: 2px solid #f0f0f0; padding-bottom: 5px;">📊 Escala de Evaluación Bancaria</p>
        <table style="width: 100%; font-size: 0.9rem; border-collapse: collapse;">
            <tr style="border-bottom: 1px solid #f5f5f5;">
                <td style="color: #28a745; font-weight: bold; padding: 8px 0; width: 35%;">0% - 20%</td>
                <td style="color: #444; padding: 8px 0;"><b>Perfil Prime:</b> Calificación rápida y acceso a mejores tasas.</td>
            </tr>
            <tr style="border-bottom: 1px solid #f5f5f5;">
                <td style="color: #ffb100; font-weight: bold; padding: 8px 0;">21% - 35%</td>
                <td style="color: #444; padding: 8px 0;"><b>Riesgo Medio:</b> Aprobación condicionada a sustento de ingresos.</td>
            </tr>
            <tr>
                <td style="color: #dc3545; font-weight: bold; padding: 8px 0;">36% - 40%</td>
                <td style="color: #444; padding: 8px 0;"><b>Límite Crítico:</b> Requiere liquidar deudas para calificar.</td>
            </tr>
        </table>
    </div>
    """, unsafe_allow_html=True)

with col_mets:
    st.write("")
    m1, m2 = st.columns(2)
    m1.metric("Cuota Disponible Bruta", f"S/ {cuota_disponible:,}")
    m2.metric("Préstamo Hipotecario Est.", f"S/ {prestamo_max:,}")
    st.write("---")
    st.metric("Inicial Total (Ahorros + AFP)", f"S/ {inicial_total:,}")
    st.write("---")
    st.info("💡 **Dato Bancario:** El banco evalúa tu capacidad basándose en que el total de tus cuotas (incluyendo la nueva hipoteca) no supere el 40% de tu sueldo neto.")

# FASE 2: Escenarios
st.write("---")
st.subheader("2. Tu Techo de Inversión por Proyecto")
c1, c2, c3 = st.columns(3)
cols = [c1, c2, c3]
for i, esc in enumerate(escenarios_data):
    with cols[i]:
        st.markdown(f'<div class="resultado-card {esc["clase"]}"><h3>{esc["nombre"]}</h3><h1>S/ {esc["monto"]:,}</h1><p>{esc["desc"]}</p></div>', unsafe_allow_html=True)

# FASE 3: Gráfico
st.write("---")
df_grafico = pd.DataFrame(escenarios_data)
fig_bar = px.bar(df_grafico, x='nombre', y='monto', color='nombre',
             color_discrete_map={"ECO-SOSTENIBLE": "#28a745", "TRADICIONAL": "#007bff", "SIN BONOS": "#6c757d"},
             text_auto=True)
fig_bar.update_layout(showlegend=False, plot_bgcolor='rgba(0,0,0,0)', yaxis_title="S/ Totales", xaxis_title=None)
fig_bar.update_traces(texttemplate='S/ %{y:,.0f}', textposition='outside')
st.plotly_chart(fig_bar, use_container_width=True)

# FASE 4: Estrategia de Mejora
st.write("---")
st.subheader("🚀 Estrategia de Poder de Compra")
if incremento_prestamo > 0:
    st.success(f"📈 **Oportunidad Detectada:** Si reduces tu línea de tarjeta a la mitad (S/ {int(linea_tc*0.5):,}), tu presupuesto de compra sube en **S/ {incremento_prestamo:,}**.")
else:
    st.info("Tu nivel de deuda es saludable para el proceso hipotecario.")

# FASE 5: Optimización Final
st.write("---")
o1, o2 = st.columns(2)
with o1:
    with st.expander("📉 Análisis de Deudas", expanded=True):
        st.write(f"Carga mensual actual: **S/ {deudas_totales:,}**.")
with o2:
    with st.expander("📜 Reserva para Gastos Administrativos", expanded=True):
        st.write(f"Reserva estimada (3%): **S/ {int(esc_tradicional * 0.03):,}**")

if st.button("✅ Finalizar"):
    st.balloons()
