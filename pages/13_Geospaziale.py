import os
import folium
import streamlit as st
import geopandas as gpd
import matplotlib.pyplot as plt
import plotly.express as px

@st.cache_data
def load_data():
    try:
        return gpd.read_file(gpd.datasets.get_path('naturalearth_lowres'))
    except Exception as e:
        st.error(f"Errore nel caricamento dei dati: {e}")
        return None

def create_map(gdf_filtered):
    m = folium.Map(location=[48.8566, 2.3522], zoom_start=2)
    for _, row in gdf_filtered.iterrows():
        folium.Marker(
            location=[row['geometry'].centroid.y, row['geometry'].centroid.x],
            popup=f"{row['name']}, Pop: {row['pop_est']}"
        ).add_to(m)
    return m

def display_map(m):
    tmp_map_file = 'tmp_map.html'
    m.save(tmp_map_file)
    with open(tmp_map_file, 'r', encoding='utf-8') as f:
        st.components.v1.html(f.read(), height=500)
    os.remove(tmp_map_file)

def generate_statistics(gdf_filtered):
    # Funzione per generare statistiche o grafici
    fig, ax = plt.subplots()
    gdf_filtered['pop_est'].hist(ax=ax, bins=15)
    ax.set_title("Distribuzione della Popolazione")
    return fig

def generate_statistics(gdf_filtered):
    # Utilizzo di Plotly per grafici interattivi
    fig = px.histogram(gdf_filtered, x='pop_est')
    return fig

def export_data(gdf_filtered):
    # Funzione per esportare i dati
    csv = gdf_filtered.to_csv(index=False)
    st.download_button(label="Scarica i dati come CSV", data=csv, file_name='data.csv', mime='text/csv')

def generate_advanced_statistics(gdf_filtered):
    # Generazione di statistiche più avanzate
    fig1 = px.bar(gdf_filtered, x='name', y='pop_est', title='Popolazione per Nazione')
    fig2 = px.scatter_geo(gdf_filtered, lat=gdf_filtered.geometry.centroid.y, lon=gdf_filtered.geometry.centroid.x,
                          size='pop_est', hover_name='name', title='Distribuzione Geografica della Popolazione')
    return fig1, fig2

def create_report(gdf_filtered):
    # Funzione per generare un report (esempio di implementazione semplice)
    report = f"Report sulle Nazioni Selezionate\n\nNazioni: {gdf_filtered['name'].tolist()}\nPopolazione Totale: {gdf_filtered['pop_est'].sum()}"
    st.download_button(label="Scarica il Report", data=report, file_name='report.txt', mime='text/plain')


def main():
    st.title("Applicazione di Visualizzazione Dati Geospaziali con Streamlit e Folium")
    gdf = load_data()
    if gdf is None:
        return

    tab1, tab2, tab3, tab4 = st.tabs(["Mappa", "Statistica", "Esporta Dati", "Dashboard e Report"])

    with tab1:
        nations = gdf['name'].unique()
        selected_nations = st.multiselect('Seleziona le nazioni da visualizzare', nations, default=nations)
        pop_range = st.slider("Seleziona l'intervallo di popolazione", int(gdf['pop_est'].min()), int(gdf['pop_est'].max()), (int(gdf['pop_est'].min()), int(gdf['pop_est'].max())))
        gdf_filtered = gdf[(gdf['name'].isin(selected_nations)) & (gdf['pop_est'] >= pop_range[0]) & (gdf['pop_est'] <= pop_range[1])]

        if not gdf_filtered.empty:
            m = create_map(gdf_filtered)
            display_map(m)
        else:
            st.error("Nessun dato da visualizzare con i filtri attuali.")
    
    with tab2:
        if not gdf_filtered.empty:
            fig = generate_statistics(gdf_filtered)
            st.plotly_chart(fig)
        else:
            st.error("Seleziona le nazioni per visualizzare le statistiche.")
    
    with tab3:
        if not gdf_filtered.empty:
            export_data(gdf_filtered)
        else:
            st.error("Nessun dato disponibile per l'esportazione.")

    with tab4:
        st.subheader("Dashboard e Generazione Report")
        if not gdf_filtered.empty:
            fig1, fig2 = generate_advanced_statistics(gdf_filtered)
            st.plotly_chart(fig1)
            st.plotly_chart(fig2)
            create_report(gdf_filtered)
        else:
            st.error("Seleziona i dati da visualizzare nella dashboard e nel report.")

main()
