import random
import streamlit as st

def update_clue(guessed_letter, secret_word, clue):
    index = 0
    while index < len(secret_word):
        if guessed_letter == secret_word[index]:
            clue[index] = guessed_letter
        index = index + 1

def generate_secret_word():
    words = ['pizza', 'fairy', 'teeth', 'shirt', 'otter', 'plane']
    return random.choice(words)

# Inizializza lo stato della sessione
if 'guessed_word_correctly' not in st.session_state:
    st.session_state['guessed_word_correctly'] = False
if 'lives' not in st.session_state:
    st.session_state['lives'] = 3
if 'clue' not in st.session_state:
    st.session_state['clue'] = list('?????')
if 'secret_word' not in st.session_state:
    st.session_state['secret_word'] = generate_secret_word()

heart_symbol = u'\u2764'

st.text(f"{st.session_state['clue']}")
st.text(f"Vite rimanenti: {heart_symbol * st.session_state['lives']}")
guess = st.text_input("Digita la parola da indovinare", key='guess_input')

if guess:
    if guess == st.session_state['secret_word']:
        st.session_state['guessed_word_correctly'] = True

    if guess in st.session_state['secret_word']:
        update_clue(guess, st.session_state['secret_word'], st.session_state['clue'])
    else:
        st.warning("Sbagliato. Perdi una vita")
        st.session_state['lives'] = st.session_state['lives'] - 1

    if st.session_state['lives'] <= 0 or st.session_state['guessed_word_correctly']:
        if st.session_state['guessed_word_correctly']:
            st.success(f"Hai vinto! La parola segreta era {st.session_state['secret_word']}")
            st.balloons()
        else:
            st.error(f"Hai perso! La parola segreta era {st.session_state['secret_word']}")
        # Resetta lo stato della sessione per una nuova partita
        st.session_state['guessed_word_correctly'] = False
        st.session_state['lives'] = 3
        st.session_state['clue'] = list('?????')
        st.session_state['secret_word'] = generate_secret_word()
