# Laboratorio Práctico: OCI Generative AI + Python + Streamlit

Este laboratorio te guía paso a paso para construir una aplicación visual que se conecta al servicio de **OCI Generative AI**, utilizando **Python **, **Streamlit**, y el **SDK oficial de Oracle Cloud**.

## 🔹 Requisitos

- Cuenta activa en Oracle Cloud Infrastructure (OCI)
- Permisos para crear recursos en un Compartment
- Llave API configurada para el OCI CLI SDK
- Acceso a un modelo de Generative AI (por ejemplo, `cohere.command-r`)

---

## 📚 Parte 1: Crear la VM en OCI

### 1. Iniciar una VM
- Ve a [Oracle Cloud Console](https://cloud.oracle.com/)
- Navega a: Compute → Instances → Create Instance
- Nombre: `oci-genai-lab`
- Imagen: Oracle Linux 8
- Shape: VM.Standard3.Flex

### 2. Acceder por SSH
Desde tu terminal:
```bash
ssh -i oci.pem opc@<public_ip>
```

---

## 📅 Parte 2: Preparar el entorno en la VM

### 1. Instalar dependencias
```bash
sudo dnf update -y
sudo dnf install python39 python39-pip git unzip -y
sudo alternatives --install /usr/bin/python python /usr/bin/python3.9 1
python --version
sudo pip3 install --upgrade pip
```

### 2. Instalar el SDK de OCI
```bash
pip install oci streamlit requests python-dotenv
```

---

## 🎓 Parte 3: Configurar OCI CLI/API

### 1. Crear archivo de configuración
```bash
mkdir -p ~/.oci
nano ~/.oci/config
```
Ejemplo de contenido:
```
[DEFAULT]
user=ocid1.user.oc1..aaaa...xxxx
fingerprint=xx:xx:xx:xx:xx:xx:xx:xx:xx
key_file=/home/opc/.oci/oci_api_key.pem
tenancy=ocid1.tenancy.oc1..aaaa...xxxx
region=us-chicago-1
```

Sube tu `oci_api_key.pem` al mismo directorio.

---

## 📂 Parte 4: Estructura del proyecto

```bash
oci_genai_demo/
├── app.py
├── oci_client.py
├── test_sdk.py
└── README.md
```

### `oci_client.py`
Contiene la lógica para conectarse al LLM de OCI y enviar prompts:
```python
import oci

class OCIClient:
    def __init__(self, config_profile="DEFAULT", config_path="~/.oci/config", endpoint=None, compartment_id=None):
        self.config = oci.config.from_file(config_path, config_profile)
        self.endpoint = endpoint
        self.compartment_id = compartment_id
        self.client = oci.generative_ai_inference.GenerativeAiInferenceClient(
            config=self.config,
            service_endpoint=self.endpoint,
            retry_strategy=oci.retry.NoneRetryStrategy(),
            timeout=(10, 240)
        )

    def ask_question(self, prompt_text, model_id, temperature=1, max_tokens=600, top_p=0.75):
        content = oci.generative_ai_inference.models.TextContent(text=prompt_text)
        message = oci.generative_ai_inference.models.Message(role="USER", content=[content])

        chat_request = oci.generative_ai_inference.models.GenericChatRequest(
            api_format=oci.generative_ai_inference.models.BaseChatRequest.API_FORMAT_GENERIC,
            messages=[message],
            max_tokens=max_tokens,
            temperature=temperature,
            frequency_penalty=0,
            presence_penalty=0,
            top_p=top_p
        )

        chat_detail = oci.generative_ai_inference.models.ChatDetails(
            serving_mode=oci.generative_ai_inference.models.OnDemandServingMode(model_id=model_id),
            compartment_id=self.compartment_id,
            chat_request=chat_request
        )

        response = self.client.chat(chat_detail)
        return response
```

### `app.py`
Interfaz visual con Streamlit:
```python
import streamlit as st
from oci_client import OCIClient

CONFIG_PROFILE = "DEFAULT"
CONFIG_PATH = "~/.oci/config"
ENDPOINT = "https://inference.generativeai.us-chicago-1.oci.oraclecloud.com"
COMPARTMENT_ID = "<tu_compartment_ocid>"
MODEL_ID = "<tu_model_ocid>"

client = OCIClient(
    config_profile=CONFIG_PROFILE,
    config_path=CONFIG_PATH,
    endpoint=ENDPOINT,
    compartment_id=COMPARTMENT_ID
)

st.set_page_config(page_title="OCI Generative AI Chat", layout="wide")
st.title("🧐 Chat con OCI Generative AI")

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
```

---

## 🔄 Parte 5: Ejecutar la app

```bash
cd oci_genai_demo
streamlit run app.py
```
Abre el navegador en `http://<tu_ip>:8501`

Si estás en una instancia OCI, abre el puerto:
```bash
sudo firewall-cmd --permanent --add-port=8501/tcp
sudo firewall-cmd --reload
```

---

## 📊 Parte 6: Resultado Final

- Interfaz simple para enviar preguntas
- Conectado a un modelo real en OCI
- Ejecutado desde una VM Oracle Linux 8
- Modular y escalable para usar otros modelos o endpoints

---

## 🌟 Mejora sugerida

- Historial de preguntas
- Controles para temperatura y tokens
- Soporte para imagenes (multimodal) si se libera SDK visual

---

## 🔗 Repositorio sugerido (estructura GitHub)

```bash
git clone https://github.com/tu_usuario/oci-genai-lab.git
cd oci-genai-lab
```

---

## 📅 Créditos

Desarrollado por: [Tu Nombre]  
Basado en la documentación oficial de Oracle Generative AI  
Actualizado: Abril 2025

