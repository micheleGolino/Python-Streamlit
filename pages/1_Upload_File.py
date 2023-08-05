import streamlit as st
from collections import Counter
import matplotlib.pyplot as plt
import re

def process_text(text):
    # Rimuove i caratteri non alfanumerici e li converte in minuscolo
    words = re.sub(r'\W+', ' ', text).lower().split()
    # Conta le parole
    word_counts = Counter(words)
    # Prende le 10 parole più comuni
    most_common_words = word_counts.most_common(10)
    return most_common_words

uploaded_file = st.file_uploader("Carica un file di testo", type="txt")

if uploaded_file is not None:
    text = uploaded_file.read().decode()
    most_common_words = process_text(text)

    # Crea un diagramma a torta
    words, counts = zip(*most_common_words)
    plt.pie(counts, labels=words, autopct='%1.1f%%')
    plt.title('Le 10 parole più comuni nel testo')
    st.pyplot(plt)
