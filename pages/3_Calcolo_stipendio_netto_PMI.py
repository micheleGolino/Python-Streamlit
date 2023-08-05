import streamlit as st
import requests
import logging

# Imposta il livello di logging
logging.basicConfig(level=logging.INFO)

st.markdown("Calcolo stipendio netto PMI")

def is_valid_param(param):
    return bool(param)

def build_request_string(params):
    base_string = "step=2&car=no&emp=privato&hw=no&toc=ind&tow=no&child_noau=0&child_au=0&childh=0&childcharge=100&family=0&days=365"
    param_string = "&".join([f"{k}={v}" for k, v in params.items()])
    return f"{base_string}&{param_string}"

ral_input = st.text_input("RAL IN EURO")
reg_input = st.selectbox("Seleziona Regione", ('abruzzo', 'basilicata', 'calabria', 'campania', 'emilia-romagna', 'friuli-venezia giulia', 'lazio', 'liguria', 'lombardia', 'marche', 'molise', 'piemonte', 'puglia', 'sardegna', 'sicilia', 'toscana', 'trentino-alto adige', 'umbria', "valle d'aosta", 'veneto'))
com_input = st.text_input("PERCENTUALE TASSE (inserire il punto come divisore, massimo valore 0.9)", "0.9")
monthlypay_input = st.selectbox("Mensilità", ("13", "14"))

if st.button("Effettua calcolo stipendio netto"):
    all_valid_params = True
    params_validate = {
        "ral": ral_input, "reg": reg_input, "com": com_input.replace(",", "."), 
        "monthlypay": monthlypay_input
    }

    try:
        params_validate['com'] = float(params_validate['com'])
        if not (0 <= params_validate['com'] <= 0.9):
            raise ValueError
    except ValueError:
        st.error("Inserire un numero valido per la percentuale delle tasse (massimo 0.9)")
        all_valid_params = False
        logging.error("Percentuale delle tasse non valida")

    for key, value in params_validate.items():
        if not is_valid_param(value):
            st.error(f"Il campo **{key}** non è stato valorizzato")
            all_valid_params = False
            logging.error(f"Campo {key} non valorizzato")

    if all_valid_params:
        build_string_to_request = build_request_string(params_validate)
        endpoint_base = "https://www.pmi.it/servizi/292472/calcolo-stipendio-netto.html?"
        url_endpoint = endpoint_base + build_string_to_request

        response = requests.get(url_endpoint)
        if response.status_code != 200:
            st.error(f"C'è stato un errore nella richiesta, richiamando l'endpoint {url_endpoint}")
            logging.error(f"Errore nella richiesta a {url_endpoint}")
        else:
            st.markdown(f"[Clicca qui per vedere i risultati]({url_endpoint})", unsafe_allow_html=True)

    else:
        st.error("**Compilare tutti i campi richiesti**")
