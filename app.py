import streamlit as st
import google.generativeai as genai
import os

# ---------------- CONFIGURACION ----------------
st.set_page_config(
    page_title="Mi Analista de Mercados",
    page_icon="📊",
    layout="wide"
)

API_KEY = os.getenv("GOOGLE_API_KEY")
genai.configure(api_key=API_KEY)
modelo = genai.GenerativeModel("gemini-pro")

# ---------------- FUNCIONES ----------------
def analizar(activo):
    consulta = "Eres un analista financiero experto. Analiza: " + activo + ". Estructura en: RESUMEN, PRECIO Y TENDENCIA, FACTORES CLAVE, RIESGOS Y OPORTUNIDADES, PERSPECTIVA. Aclara que NO es recomendacion de inversion. Sé claro y directo."
    return modelo.generate_content(consulta).text

def comparar(a, b):
    consulta = "Compara " + a + " con " + b + ". Incluye: perfil de riesgo, uso principal, ventajas, desventajas y en que escenario conviene cada uno. Aclara que NO es recomendacion de inversion."
    return modelo.generate_content(consulta).text

def noticias(tema):
    consulta = "Dame un resumen claro sobre: " + tema + ". Sé conciso, en espanol, y facil de entender. Aclara que NO es recomendacion de inversion."
    return modelo.generate_content(consulta).text

# ---------------- INTERFAZ ----------------
st.title("Mi Analista de Mercados Financieros")
st.subheader("Tu asistente personal de analisis")
st.divider()

menu = st.sidebar.radio("Menu Principal", [
    "Analizar un activo",
    "Comparar dos activos",
    "Noticias y Perspectivas",
    "Acerca de"
])

if menu == "Analizar un activo":
    st.header("Analisis de Activos")
    activo = st.text_input("Escribe el nombre del activo:", placeholder="Ejemplo: Bitcoin, Oro, NVIDIA")
    
    if st.button("Generar Analisis", type="primary"):
        if activo:
            with st.spinner("Analizando..."):
                resultado = analizar(activo)
                st.success("Analisis listo")
                st.write(resultado)
                st.info("AVISO: Esto es solo informativo. No es recomendacion de inversion.")
        else:
            st.warning("Por favor escribe un activo")

elif menu == "Comparar dos activos":
    st.header("Comparacion Lado a Lado")
    col1, col2 = st.columns(2)
    
    with col1:
        activo1 = st.text_input("Activo 1", placeholder="Bitcoin")
    with col2:
        activo2 = st.text_input("Activo 2", placeholder="Oro")
    
    if st.button("Comparar", type="primary"):
        if activo1 and activo2:
            with st.spinner("Comparando..."):
                resultado = comparar(activo1, activo2)
                st.success("Comparacion lista")
                st.write(resultado)
                st.info("AVISO: Esto es solo informativo. No es recomendacion de inversion.")
        else:
            st.warning("Completa ambos campos")

elif menu == "Noticias y Perspectivas":
    st.header("Noticias y Perspectivas")
    tema = st.text_input("Que tema te interesa?", placeholder="Ejemplo: mercado de criptomonedas hoy")
    
    if st.button("Obtener Informacion", type="primary"):
        if tema:
            with st.spinner("Recopilando informacion..."):
                resultado = noticias(tema)
                st.success("Informacion lista")
                st.write(resultado)
                st.info("AVISO: Esto es solo informativo. No es recomendacion de inversion.")
        else:
            st.warning("Escribe un tema")

elif menu == "Acerca de":
    st.header("Acerca de esta herramienta")
    st.write("""
    Esta es una herramienta de analisis financiero con Inteligencia Artificial.
    Puedes analizar activos, comparar opciones y consultar perspectivas del mercado.
    
    IMPORTANTE: Toda la informacion es solo con fines educativos.
    No constituye recomendacion de inversion.
    """)

st.sidebar.divider()
st.sidebar.write("Consejo: La paciencia vale mas que la prisa.")
