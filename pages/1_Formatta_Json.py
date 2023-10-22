import streamlit as st
import json
import pyperclip
import logging

def is_valid_json(json_string):
    try:
        json.loads(json_string)
        return True
    except ValueError:
        return False

def format_json(json_string):
    parsed = json.loads(json_string)
    formatted = json.dumps(parsed, indent=4)
    logging.info(f"Json formattato: {formatted}")
    return formatted

# Assumendo che questa sia la pagina pages/6_Formatta_Json
def json_formatter_page():
    st.title("Formattatore JSON")
    
    user_input = st.text_area("Inserisci la tua stringa JSON qui:")
    
    if st.button("Formatta stringa"):
        if user_input and is_valid_json(user_input):
            formatted_json = format_json(user_input)
            st.text_area("Il tuo JSON formattato:", value=formatted_json, height=300)
        elif not user_input:
            st.error("La casella di testo è vuota. Inserisci una stringa JSON.")
        elif not is_valid_json(user_input):
            st.error("La stringa fornita non è un JSON valido.")
    
    if st.button("Copia testo formattato"):
        formatted_json_area = st.empty()
        if user_input and is_valid_json(user_input):
            formatted_json = format_json(user_input)
            formatted_json_area.text_area("Il tuo JSON formattato:", value=formatted_json, height=300)
            pyperclip.copy(formatted_json)
            st.write("Testo copiato correttamente")
        elif not user_input:
            st.error("La casella di testo è vuota. Inserisci una stringa JSON.")
        elif not is_valid_json(user_input):
            st.error("La stringa fornita non è un JSON valido.")

# Aggiungere la seguente riga nel tuo main o nel punto in cui vuoi includere questa pagina nel tuo progetto
json_formatter_page()
