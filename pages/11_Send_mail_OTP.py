import random
import smtplib
import streamlit as st

def generate_otp_number():
    return ''.join(random.choices('0123456789', k=6))

def generate_message(otp):
    return f"{otp} is your OTP"

def send_otp_email(email, msg):
    with smtplib.SMTP('smtp.gmail.com', 587) as s:
        s.starttls()
        s.login("mikele.golino@gmail.com", "gkwydzpcqybwharz")
        s.sendmail('&&&&&&&&&&&', email, msg)

def init_session_state():
    st.session_state.setdefault('otp', None)
    st.session_state.setdefault('simulated', None)
    st.session_state.setdefault('emailsended', None)

init_session_state()
with st.spinner("Caricamento..."):
    email_id = st.text_input("Inserisci la tua mail")
    st.session_state['simulated'] = st.checkbox("Simula invio")

    if st.button("Invia codice OTP"):
        st.session_state['otp'] = generate_otp_number()
        msg = generate_message(st.session_state['otp'])
        
        if not st.session_state['simulated']:
            send_otp_email(email_id, msg)
            st.toast(f"Email inviata correttamente all'indirizzo {email_id}", icon="✅")
        else:
            st.write(f"Il codice OTP generato è {st.session_state['otp']}")
            st.toast(f"Email inviata correttamente all'indirizzo blabla", icon="✅")
        
        st.session_state['emailsended'] = True

    otp_code = st.text_input("Inserisci il tuo codice OTP")

    if not st.session_state['emailsended']:
        st.error("Cliccare prima sul bottone Invia codice OTP")
    elif st.button("Verifica OTP"):
        if st.session_state['simulated']:
            st.write(f"Sto confrontando {otp_code} con {st.session_state['otp']}")
        
        if otp_code == st.session_state['otp']:
            st.success("OTP Verificato con successo", icon="✅")
            init_session_state()
        else:
            st.error("Verifica dell'OTP fallita")
