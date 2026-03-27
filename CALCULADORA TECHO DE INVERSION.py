import streamlit as st
import pandas as pd

# 1. CONFIGURACIÓN Y ESTILO PERSONALIZADO (CSS)
st.set_page_config(page_title="Auditoría 360° | Jancarlo Inmobiliario", layout="wide")

st.markdown("""
    <style>
    .main { background-color: #f8f9fa; }
    .stMetric { background-color: #ffffff; padding: 15px; border-radius: 10px; box-shadow: 0 4px 6px rgba(0,0,0,0.1); }
    .resultado-card { 
        padding: 20px; 
        border-radius: 15px; 
        color: white; 
        text-align: center;
        margin-bottom: 20px;
    }
    .verde { background: linear-gradient(135deg, #28a745, #218838); }
    .azul { background: linear-gradient(135deg, #007bff, #0056b3); }
    .gris { background: linear-gradient(135deg, #6c757d, #495057); }
    h1, h2, h3 { color: #1e1e1e; font-family: 'Helvetica Neue', sans-serif; }
    </style>
    """, unsafe_allow_html=True)

# --- SIDEBAR: ENTRADA DE DATOS ---
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/602/602182.png", width=100) # Puedes cambiar por tu logo
    st.title("Inputs de Asesoría")
    
    with st.expander("💰 Ingresos y Ahorros", expanded=True):
        ingreso = st.number_input("Ingreso Neto Mensual (S/)", min_value=0.0, value=5000.0, step=100.0)
        ahorros = st.number_input("Ahorros Disponibles (S/)", min_value=0.0, value=20000.0)
    
    with st.expander("💳 Deudas Actuales", expanded=True):
        p_personal = st.number_input("Préstamos Personales (S/)", min_value=0.0)
        p_vehicular = st.number_input("Préstamo Vehicular (S/)", min_value=0.0)
        tarjetas = st.number_input("Cuotas Fijas Tarjeta (S/)", min_value=0.0)
        otros = st.number_input("Otras Cuotas (S/)", min_value=0.0)

# --- LÓGICA FINANCIERA ---
capacidad_40 = ingreso * 0.40
deudas_totales = p_personal + p_vehicular + tarjetas + otros
cuota_disponible = max(0.0, capacidad_40 - deudas_totales)
prestamo_max = cuota_disponible * 111.14
inicial_afp = ingreso * 0.25
inicial_total = ahorros + inicial_afp

# Escenarios
esc_verde = prestamo_max + inicial_total + 12800
esc_tradicional = prestamo_max + inicial_total + 7300
esc_directo = prestamo_max + inicial_total

# --- CUERPO PRINCIPAL ---
st.title("🎯 Auditoría Inmobiliaria 360°")
st.info(f"Análisis estratégico para compra de primer inmueble.")

# Métricas de Salud Crediticia
col_a, col_b, col_c = st.columns(3)
col_a.metric("Cuota Disponible", f"S/ {cuota_disponible:,.2f}")
col_b.metric("Préstamo Bancario", f"S/ {prestamo_max:,.2f}")
col_c.metric("Inicial (Ahorros + AFP)", f"S/ {inicial_total:,.2f}")

st.write("---")
st.subheader("🏢 Comparativa de Inversión Máxima")

# Tarjetas Visuales de Escenarios
c1, c2, c3 = st.columns(3)

with c1:
    st.markdown(f"""<div class="resultado-card verde">
        <h3>ECO-SOSTENIBLE</h3>
        <h1>S/ {esc_verde:,.0f}</h1>
        <small>BBP + Bono Verde Incluidos</small>
    </div>""", unsafe_allow_html=True)
    st.caption("✅ Mayor rentabilidad y menor tasa.")

with c2:
    st.markdown(f"""<div class="resultado-card azul">
        <h3>TRADICIONAL</h3>
        <h1>S/ {esc_tradicional:,.0f}</h1>
        <small>Solo Bono Buen Pagador</small>
    </div>""", unsafe_allow_html=True)
    st.caption("📍 Proyectos estándar en Lima.")

with c3:
    st.markdown(f"""<div class="resultado-card gris">
        <h3>SIN BONOS</h3>
        <h1>S/ {esc_directo:,.0f}</h1>
        <small>Inversión Directa / MiVivienda</small>
    </div>""", unsafe_allow_html=True)
    st.caption("📉 Sin subsidios del Estado.")

# Gráfico de Barras Comparativo
df_chart = pd.DataFrame({
    'Escenario': ['Eco', 'Tradicional', 'Sin Bonos'],
    'Monto (S/)': [esc_verde, esc_tradicional, esc_directo]
})
st.bar_chart(df_chart.set_index('Escenario'))

# Recomendaciones Dinámicas
st.warning("💡 **Tip de Asesoría:** Si el cliente desea llegar al escenario 'Tradicional' pero no le alcanza, recomiéndale consolidar la deuda de tarjetas de S/ {:.0f} para liberar capacidad.".format(tarjetas))

# Botón de impresión (Simulado)
if st.button("Generar Reporte para Cliente"):
    st.balloons()
    st.success("Reporte listo para captura de pantalla.")