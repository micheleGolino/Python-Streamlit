import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

def plot_data(column, data, plot_type):
    if data.dtypes[column] == 'object':
        if plot_type == 'bar':
            st.bar_chart(data[column].value_counts())
        elif plot_type == 'pie':
            fig, ax = plt.subplots()
            ax.pie(data[column].value_counts(), labels=data[column].value_counts().index, autopct='%1.1f%%')
            plt.title(f"{column} ({plot_type})")
            st.pyplot(fig)
    else:
        if plot_type == 'bar':
            st.bar_chart(data[column].value_counts(bins=20))
        elif plot_type == 'pie':
            st.write("Il grafico a torta non è appropriato per dati numerici.")

def analyze_dataset(data):
    st.write("## Anteprima del dataset:")
    st.write(data.head())

    for column in data.columns:
        st.write(f"### Analisi per la colonna: {column}")

        st.write("#### Statistica di base:")
        st.write(data[column].describe())

        mode_values = data[column].mode()
        if not mode_values.empty:
            st.write(f"#### Moda: {mode_values[0]}")
        else:
            st.write("#### Moda: Non calcolabile")

        # Verifica il tipo di dati prima di calcolare la mediana
        if pd.api.types.is_numeric_dtype(data[column]):
            try:
                st.write(f"#### Mediana: {data[column].median()}")
            except Exception as e:
                st.write(f"#### Mediana: Non calcolabile. {e}")
        else:
            st.write("#### Mediana: Non applicabile per dati non numerici")

        st.write("#### Grafico a barre:")
        plot_data(column, data, 'bar')

        st.write("#### Grafico a torta:")
        plot_data(column, data, 'pie')

st.title("Analizzatore di Dataset")
st.write("## Benvenuti all'analizzatore di dataset!")
st.write("### Carica un file CSV, XLS o XLSX per iniziare l'analisi.")

uploaded_file = st.file_uploader("Scegli un file", type=['csv', 'xls', 'xlsx'])

if uploaded_file is not None:
    try:
        data = pd.read_csv(uploaded_file)
        analyze_dataset(data)
    except Exception as e:
        st.write(f"Errore durante la lettura del file: {e}")
