import streamlit as st
from oci_client import OCIClient

CONFIG_PROFILE = "DEFAULT"
CONFIG_PATH = "~/.oci/config"
ENDPOINT = "https://inference.generativeai.us-chicago-1.oci.oraclecloud.com"
COMPARTMENT_ID = "ocid1.compartment.oc1..aaaaaaaalvycmrayvqkw732sqzcpiurdvfagzywqp2ke7wsailtwd2y2e6ka"
MODEL_ID = "ocid1.generativeaimodel.oc1.us-chicago-1.amaaaaaask7dceya2xrydihzvu5pk6vlvfhtbnfapcvwhhugzo7jez4zcnaa"

client = OCIClient(
    config_profile=CONFIG_PROFILE,
    config_path=CONFIG_PATH,
    endpoint=ENDPOINT,
    compartment_id=COMPARTMENT_ID
)

st.set_page_config(page_title="OCI Generative AI Chat", layout="wide")
st.title("🧠 Chat con OCI Generative AI")

user_prompt = st.text_area("Escribe tu pregunta:", height=200)

if st.button("Enviar"):
    if user_prompt.strip():
        with st.spinner("Consultando modelo..."):
            try:
                response = client.ask_question(user_prompt, MODEL_ID)
                result = response.data.messages[0].content[0].text
                st.success("Respuesta:")
                st.write(result)
            except Exception as e:
                st.error(f"Error: {e}")
    else:
        st.warning("Por favor escribe una pregunta.")