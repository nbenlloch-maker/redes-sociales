import streamlit as st
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

# Configuración de la página
st.set_page_config(page_title="Content Generator 🤖", page_icon="🤖")
st.title("Content generator")

# --- SECCIÓN DE AUTENTICACIÓN ---
with st.sidebar:
    st.header("Configuración")
    groq_api_key = st.text_input("Introduce tu Groq API Key:", type="password")
    st.info("Obtén tu llave en [console.groq.com](https://console.groq.com/keys)")

## Función de generación (ahora recibe la API Key)
def llm_generate(api_key, prompt):
    id_model = "llama-3.3-70b-versatile"
    
    # Inicializamos el modelo localmente con la llave proporcionada
    llm = ChatGroq(
        model=id_model,
        temperature=0.7,
        groq_api_key=api_key,
        max_retries=2,
    )

    template = ChatPromptTemplate.from_messages([
        ("system", "You are a digital marketing expert specialized in SEO and persuasive copywriting."),
        ("human", "{prompt}"),
    ])

    chain = template | llm | StrOutputParser()
    return chain.invoke({"prompt": prompt})

# --- FORMULARIO DE ENTRADA ---
topic = st.text_input("Topic:", placeholder="e.g., nutrition, mental health...")
col1, col2 = st.columns(2)

with col1:
    platform = st.selectbox("Platform:", ['Instagram', 'Facebook', 'LinkedIn', 'Blog', 'E-mail'])
    tone = st.selectbox("Message tone:", ['Normal', 'Informative', 'Inspiring', 'Urgent', 'Informal'])
with col2:
    length = st.selectbox("Text length:", ['Short', 'Medium', 'Long'])
    audience = st.selectbox("Target audience:", ['All', 'Young adults', 'Families', 'Seniors', 'Teenagers'])

cta = st.checkbox("Include CTA")
hashtags = st.checkbox("Return Hashtags")
keywords = st.text_area("Keywords (SEO):", placeholder="Example: wellness, preventive healthcare...")

# --- LÓGICA DE GENERACIÓN ---
if st.button("Generate Content"):
    if not groq_api_key:
        st.warning("Por favor, introduce tu API Key de Groq en la barra lateral.")
    elif not topic:
        st.error("El campo 'Topic' es obligatorio.")
    else:
        with st.spinner("Generando contenido..."):
            prompt = f"""
            Write an SEO-optimized text on the topic '{topic}'.
            Return only the final text in your response and don't put it inside quotes.
            - Platform: {platform}.
            - Tone: {tone}.
            - Target audience: {audience}.
            - Length: {length}.
            - {"Include a clear Call to Action." if cta else "Do not include a Call to Action."}
            - {"Include relevant hashtags." if hashtags else "Do not include hashtags."}
            {"- Keywords: " + keywords if keywords else ""}
            """
            try:
                res = llm_generate(groq_api_key, prompt)
                st.subheader("Resultado:")
                st.markdown(res)
            except Exception as e:
                st.error(f"Error de autenticación o de API: {e}")