import streamlit as st
import requests

# Lista di Pokémon
pokemon_list = ["pikachu", "charizard", "bulbasaur", "squirtle", "jigglypuff", "chikorita"]

def get_pokemon_abilities(pokemon):
    with st.spinner('Caricamento delle abilità del Pokémon...'):
        response = requests.get(f"https://pokeapi.co/api/v2/pokemon/{pokemon}")
    data = response.json()
    abilities = [ability['ability']['name'] for ability in data['abilities']]
    return abilities

st.title("Pokémon Abilities")

pokemon_list.sort()
pokemon_list = ["-"] + pokemon_list

# Crea una combo box con i nomi dei Pokémon
selected_pokemon = st.selectbox("Seleziona un Pokémon", pokemon_list)

if selected_pokemon != "-":
    # Ottieni le abilità del Pokémon selezionato
    abilities = get_pokemon_abilities(selected_pokemon)

    # Visualizza il Pokémon selezionato e le sue abilità
    st.write(f"Hai selezionato **{selected_pokemon}**. Le sue abilità sono:")
    for ability in abilities:
        st.write(ability)
