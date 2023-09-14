import streamlit as st
import logging
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from pyVinted import Vinted

def build_url(vinted_item, price_from=None, price_to=None, selected_status=None, selected_sort=None):
    url = f"https://www.vinted.it/catalog?search_text={vinted_item}&currency=EUR"
    if price_from:
        url += f"&price_from={price_from}"
    if price_to:
        url += f"&price_to={price_to}"
    selected_status_values = [status_options[key] for key in selected_status]
    if selected_status_values:
        for status_value in selected_status_values:
            url += f"&{status_value}"
    selected_sort_values = priority_order[selected_sort]
    if selected_sort_values:
        url += f"&order={selected_sort_values}"
    logging.info(f"Url da cercare come richiesta {url}")
    return url

def replace_domain(url):
    return url.replace("https://www.vinted.fr/", "https://www.vinted.it/")

def display_item(index, item, email_content, check_search_perfect, vinted_item):
    title_contains_item = vinted_item.lower() in item.title.lower()
    item_displayed = False
    
    if check_search_perfect and not title_contains_item:
        return email_content, item_displayed
    
    st.markdown("---")
    st.text(f"Articolo numero {index+1}")
    
    fields = [
        ("Titolo", item.title),
        ("Id", item.id),
        ("Photo Url", replace_domain(item.photo)),
        ("Marca", item.brand_title),
        ("Prezzo", item.price),
        ("Url", replace_domain(item.url)),
        ("Valuta", item.currency)
    ]
    
    for field_name, field_value in fields:
        logging.info(f"{field_name}: {field_value}")
        if field_name == "Photo Url":
            st.image(field_value, caption="Foto dell'articolo", use_column_width=False)
        elif field_name == "Url":
            st.markdown(f"{field_name}: [Clicca qui]({field_value})")
        else:
            st.text(f"{field_name}: {field_value}")
        
        email_content += f"{field_name}: {field_value}\n"
    
    email_content += "---\n"
    item_displayed = True
    return email_content, item_displayed

logging.basicConfig(level=logging.INFO)
vinted = Vinted()
status_options = {
    "Nuovo con cartellino": "status_ids[]=6",
    "Nuovo senza cartellino": "status_ids[]=1",
    "Ottime": "status_ids[]=2",
    "Buone": "status_ids[]=3",
    "Discrete": "status_ids[]=4"
}
priority_order = {
    "Rilevanza": "relevance",
    "Prezzo: dal più alto al più basso": "price_high_to_low",
    "Prezzo: dal più basso al più alto": "price_low_to_high",
    "Dal più recente": "newest_first"
}
items = None
email_content = ""
email_sender = "michelegolino94@gmail.com"
email_receiver = "michelegolino94@gmail.com"
password_email = "Roklas12a1b2c3d4e52023!"
subject = "Risultati della ricerca Vinted"

msg = MIMEMultipart()
msg["From"] = email_sender
msg["To"] = email_receiver
msg["Subject"] = subject

st.markdown("### Articoli Vinted ###")
st.markdown("Gli articoli contrassegnati con l'asterisco (*) sono obbligatori")

error_message = st.empty()
vinted_item = st.text_input("Inserisci l'oggetto da cercare *")
item_price_from = st.text_input("Prezzo a partire da")
item_price_to = st.text_input("Prezzo massimo")
selected_status = st.multiselect("Seleziona lo stato degli articoli", list(status_options.keys()), None, placeholder="Seleziona gli stati")
selected_sort = st.selectbox("Ordina per", list(priority_order.keys()), index=0, placeholder="Seleziona l'ordine di visualizzazione (default: Per Rilevanza)")
number_of_page = st.text_input("Inserisci il numero della pagina (Opzionale, default 1)", "1")
number_of_items = st.text_input("Inserisci il numero di elementi per pagina (Opzionale, default 30)", "30")
check_search_perfect = st.checkbox("Ricerca precisa del testo nel titolo dell'articolo su Vinted", False)

show_email_button = False  # Variabile per controllare se mostrare il pulsante email

if st.button("Clicca qui per effettuare la ricerca"):
    if not vinted_item.strip():
        error_message.error("Inserire obbligatoriamente il nome dell'oggetto da cercare")
    else:
        vinted_url = build_url(vinted_item, item_price_from, item_price_to, selected_status, selected_sort)
        items = vinted.items.search(vinted_url, int(number_of_items), int(number_of_page))
        
        if not items:
            st.error("Nessun risultato trovato.")

if items:
    for index, item in enumerate(items):
        email_content, item_displayed = display_item(index, item, email_content, check_search_perfect, vinted_item)
        if item_displayed:
            show_email_button = True  # Imposta la variabile a True se almeno un elemento è mostrato
    
    msg.attach(MIMEText(email_content, "plain"))
    
    if show_email_button and st.button("Invia risultati via email"):
        try:
            server = smtplib.SMTP("smtp.gmail.com", 587)
            server.starttls()
            server.login(email_sender, password_email)
            server.sendmail(email_sender, email_receiver, msg.as_string())
            server.quit()
            st.success("Email inviata con successo.")
        except Exception as e:
            st.error(f"Si è verificato un errore: {e}")