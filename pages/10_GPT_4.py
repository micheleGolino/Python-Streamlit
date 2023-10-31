import streamlit as st
import openai
import json
import logging

# Configurazione del logging
logging.basicConfig(level=logging.INFO)

# Definizioni delle API e delle credenziali
GPT_4_API_URL = 'https://api.openai.com/v1/chat/completions'
API_KEY = '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'
MODEL = "gpt-3.5-turbo"

# Definizione della funzione per generare i test JUnit
def generate_junit_tests(java_code, language='italian'):
    logging.info(f"Generazione dei test JUnit per il codice Java fornito, lingua: {language}")
    function_call = {
        'function': 'generate_junit_tests',
        'args': [java_code],
        'kwargs': {'language': language}
    }
    try:
        openai.api_key = API_KEY
        response = openai.ChatCompletion.create(
            model=MODEL,
            messages=[{
                "role": "user",
                "content": "Generami dei JUnit tests per il seguente codice Java:",
                "java_code": java_code
            }],
            functions=[function_call]
        )
    except Exception as e:
        logging.error(f"Errore durante la chiamata all'API: {e}")
        return None

    logging.info(f"Risposta ricevuta dall'API")
    return response['choices'][0]['text']

# Funzione per visualizzare l'interfaccia utente
def display_ui():
    st.title("Generatore di Test JUnit")
    java_file = st.file_uploader("Carica il tuo file Java", type=["java"])

    if java_file:
        java_code = java_file.read().decode()
        if st.button("Genera Test JUnit"):
            junit_tests = generate_junit_tests(java_code)
            if junit_tests:
                st.text_area("Test JUnit Generati:", junit_tests, height=400)
            else:
                st.error("Impossibile generare i test JUnit.")

# Esegui la funzione di visualizzazione dell'interfaccia utente
display_ui()
