
import streamlit as st
from google import genai
import os

# ---------------- CONFIGURACION ----------------

st.set_page_config(
    page_title="Mi Analista de Mercados",
    page_icon="📊",
    layout="wide"
)

# Obtener API KEY de Streamlit o variable de entorno
try:
    API_KEY = st.secrets.get("GOOGLE_API_KEY", "")
except Exception:
    API_KEY = ""

if not API_KEY:
    API_KEY = os.getenv("GOOGLE_API_KEY", "") or os.getenv(
        "GOOGLE_GENERATIVEAI_API_KEY", ""
    )

# Modelo de Gemini
MODELO = "gemini-3.5-flash-lite"

# Conectar con Gemini
if API_KEY:
    client = genai.Client(api_key=API_KEY)
else:
    client = None


# ---------------- FUNCION GENERAL ----------------

def consultar_gemini(consulta):

    if client is None:
        return (
            "ERROR: No se encontro la API KEY de Google. "
            "Configura GOOGLE_API_KEY en Streamlit Secrets."
        )

    try:
        respuesta = client.models.generate_content(
            model=MODELO,
            contents=consulta
        )

        if respuesta.text:
            return respuesta.text

        return "Gemini no devolvio contenido. Intenta nuevamente."

    except Exception as e:
        return f"Error al consultar Gemini: {str(e)}"


# ---------------- FUNCIONES ----------------

def analizar(activo):

    consulta = f"""
    Eres un analista financiero experto.

    Analiza el siguiente activo: {activo}

    Estructura tu respuesta en:

    1. RESUMEN
    2. PRECIO Y TENDENCIA
    3. FACTORES CLAVE
    4. RIESGOS Y OPORTUNIDADES
    5. PERSPECTIVA

    IMPORTANTE:
    - No inventes precios actuales.
    - Si no tienes datos actualizados, indicalo.
    - Diferencia hechos de estimaciones.
    - Responde en español.
    - Aclara que NO es recomendacion de inversion.
    """

    return consultar_gemini(consulta)


def comparar(a, b):

    consulta = f"""
    Compara los activos {a} y {b}.

    Incluye:

    1. Perfil de riesgo.
    2. Uso principal.
    3. Ventajas.
    4. Desventajas.
    5. Diferencias.
    6. En que escenarios conviene cada uno.

    Responde en español.
    Aclara que NO es recomendacion de inversion.
    """

    return consultar_gemini(consulta)


def noticias(tema):

    consulta = f"""
    Explica el siguiente tema financiero: {tema}.

    Presenta:
    1. Contexto.
    2. Factores importantes.
    3. Posibles consecuencias para los mercados.
    4. Riesgos.
    5. Perspectivas.

    IMPORTANTE:
    No inventes noticias ni acontecimientos recientes.
    Si no tienes acceso a informacion actualizada,
    aclara esa limitacion.

    Responde en español.
    """

    return consultar_gemini(consulta)


# ---------------- INTERFAZ ----------------

st.title("📊 Mi Analista de Mercados Financieros")

st.subheader("Tu asistente personal de analisis financiero")

st.divider()

if client is None:
    st.warning(
        "Falta configurar la API KEY de Google en Streamlit Secrets."
    )

menu = st.sidebar.radio(
    "Menu Principal",
    [
        "Analizar un activo",
        "Comparar dos activos",
        "Noticias y Perspectivas",
        "Acerca de"
    ]
)


# ---------------- ANALIZAR ACTIVO ----------------

if menu == "Analizar un activo":

    st.header("Analisis de Activos")

    activo = st.text_input(
        "Escribe el nombre del activo:",
        placeholder="Ejemplo: Bitcoin, Oro, NVIDIA"
    )

    if st.button("Generar Analisis", type="primary"):

        if activo.strip():

            with st.spinner("Analizando activo..."):

                resultado = analizar(activo.strip())

                st.markdown("### Resultado del analisis")
                st.write(resultado)

                st.info(
                    "AVISO: Informacion educativa. "
                    "No constituye recomendacion de inversion."
                )

        else:
            st.warning("Por favor escribe un activo.")


# ---------------- COMPARAR ACTIVOS ----------------

elif menu == "Comparar dos activos":

    st.header("Comparacion Lado a Lado")

    col1, col2 = st.columns(2)

    with col1:
        activo1 = st.text_input(
            "Activo 1",
            placeholder="Bitcoin"
        )

    with col2:
        activo2 = st.text_input(
            "Activo 2",
            placeholder="Oro"
        )

    if st.button("Comparar", type="primary"):

        if activo1.strip() and activo2.strip():

            with st.spinner("Comparando activos..."):

                resultado = comparar(
                    activo1.strip(),
                    activo2.strip()
                )

                st.markdown("### Resultado de la comparacion")
                st.write(resultado)

                st.info(
                    "AVISO: Informacion educativa. "
                    "No constituye recomendacion de inversion."
                )

        else:
            st.warning("Completa ambos campos.")


# ---------------- NOTICIAS ----------------

elif menu == "Noticias y Perspectivas":

    st.header("Noticias y Perspectivas")

    tema = st.text_input(
        "Que tema te interesa?",
        placeholder="Ejemplo: mercado de criptomonedas"
    )

    if st.button("Obtener Informacion", type="primary"):

        if tema.strip():

            with st.spinner("Procesando consulta..."):

                resultado = noticias(tema.strip())

                st.markdown("### Resultado")
                st.write(resultado)

                st.info(
                    "La informacion generada puede no reflejar "
                    "noticias en tiempo real."
                )

        else:
            st.warning("Escribe un tema.")


# ---------------- ACERCA DE ----------------

elif menu == "Acerca de":

    st.header("Acerca de esta herramienta")

    st.write("""
    Esta es una herramienta de analisis financiero
    desarrollada con Python, Streamlit e Inteligencia
    Artificial de Google Gemini.

    FUNCIONES:

    - Analisis de activos financieros.
    - Comparacion de activos.
    - Analisis de perspectivas de mercado.
    - Consultas financieras mediante inteligencia artificial.

    IMPORTANTE:

    Toda la informacion es de caracter educativo.
    No constituye recomendacion de inversion.
    """)


# ---------------- PIE DE PAGINA ----------------

st.sidebar.divider()

st.sidebar.write(
    "Consejo: La paciencia vale mas que la prisa."
)

st.sidebar.caption(
    "Desarrollado con Python, Streamlit y Google Gemini."
)
