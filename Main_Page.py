# IMPORTS
import pandas as pd
import inflection
import numpy as np

import streamlit as st
from streamlit_folium import folium_static


import folium
from folium.plugins import FastMarkerCluster

st.set_page_config(
   page_title="Main Page",
   page_icon="🧊",
   layout="wide",
   initial_sidebar_state="expanded",
)

#================================
######   FUNCTIONS AND VARIABLES
#================================

# Chamando o arquivo CSV
data = pd.read_csv('./dataset/zomato.csv')

# Criando uma variavel para cada ['COUNTRY_CODE'] com o nome do país de origem
COUNTRIES = {
    1: "India",
    14: "Australia",
    30: "Brazil",
    37: "Canada",
    94: "Indonesia",
    148: "New Zeland",
    162: "Philippines",
    166: "Qatar",
    184: "Singapure",
    189: "South Africa",
    191: "Sri Lanka",
    208: "Turkey",
    214: "United Arab Emirates",
    215: "England",
    216: "United States of America"
}

COLORS = {
"3F7E00": "darkgreen",
"5BA829": "green",
"9ACD32": "lightgreen",
"CDD614": "orange",
"FFBA00": "red",
"CBCBC8": "darkred",
"FF7800": "darkred",
}

# Entra codigo e sai o nome da cor
def color_name(color_code):
    return COLORS[color_code]

# função para cadastrar o nome da coluna passando o id do ['country_code']
def country_name(country_id):
    return COUNTRIES[country_id]

# Limpeza dos nomes das colunas que estavam com espaços e letras maiúsculas.
def rename_columns(dataframe):
    df = dataframe.copy()
    df = df.dropna()
    df = df.drop_duplicates()

    title = lambda x: inflection.titleize(x)
    snakecase = lambda x: inflection.underscore(x)
    spaces = lambda x: x.replace(" ", "")
    cols_old = list(df.columns)
    cols_old = list(map(title, cols_old))
    cols_old = list(map(spaces, cols_old))
    cols_new = list(map(snakecase, cols_old))
    df.columns = cols_new

    df['country_name'] = df.apply(lambda x: country_name(x['country_code']), axis=True)
    df['color_name'] = df.apply(lambda x: color_name(x['rating_color']), axis=True)

    df["cuisines"] = df["cuisines"].str.split(",").str[0]

    df = df[(df['cuisines'] != 'Mineira') & (df['cuisines'] != 'Drinks Only')]

    # df = df[df['cuisines'].notnull()]

    return df

# @st.cache
def convert_df(df):
    # IMPORTANT: Cache the conversion to prevent computation on every rerun
    return df.to_csv().encode('utf-8')

def map_restaurant(df):
    callback ="""
        function (row){
            var icon, marker, popup;
            icon = L.AwesomeMarkers.icon({icon: "map-marker", markerColor: row[2]});
            marker = L.marker(new L.LatLng(row[0], row[1]));
            marker.bindPopup("<h4>" + row[3] + "</h4> <br> Type: "+ row[5] + "<br> Aggragate Rating: " + row[4] + "/5.0").openTooltip();
            marker.setIcon(icon)
            return marker;
        }
    """
    restaurant_unique_map = df.drop_duplicates(subset='restaurant_id')
    map = folium.Map(zoom_start=5)
    valores = restaurant_unique_map[['latitude', 'longitude', 'color_name', 'restaurant_name', 'aggregate_rating', 'cuisines']].values.tolist()

    if(len(valores) > 0):
        FastMarkerCluster(data=valores, callback=callback, name=valores[2]).add_to(map)

    folium_static(map, width=1024, height=600)

# CLEAR DATAFRAME
data_copy = rename_columns(data)


#================================
######   STREAMLIT - SIDEBAR
#================================

st.sidebar.markdown("<h1 style='text-align: center;'>Fome Zero</h1>", unsafe_allow_html=True)
st.sidebar.markdown("### Filtros")


# Filtro por país
allCountry = data_copy['country_name'].unique()
np.random.seed(3)
country_selects = st.sidebar.multiselect(
    'Escolha os Paises que Deseja visualizar os Restaurantes',
    allCountry,
    np.random.choice(allCountry, size=6, replace=False)
)

df_filter = data_copy.query('country_name == @country_selects')

# Download CSV filtrado
st.sidebar.markdown("### Dados tratados")
st.sidebar.download_button(
    label="Download",
    data=convert_df(df_filter),
    file_name='large_df.csv',
    mime='text/csv',
)

#================================
######   STREAMLIT - CONTAINER
#================================

# st.dataframe(df_filter)

st.markdown("# Fome Zero!")
st.markdown("## O Melhor lugar para encontrar seu mais novo restaurante favorito!")
st.markdown("### Temos as seguintes marcas dentro da nossa plataforma:")

col1, col2, col3, col4, col5 = st.columns(5)
with col1:
    col1.metric('Restaurantes Cadastrados', len(data_copy['restaurant_id'].unique()))
with col2:
    col2.metric('Países Cadastrados', len(data_copy['country_code'].unique()))
with col3:
    col3.metric('Cidades Cadastrados', len(data_copy['city'].unique()))
with col4:
    col4.metric('Avaliações Feitas na Plataforma', '{:,}'.format(data_copy['votes'].sum()).replace(',', '.'))
with col5:
    col5.metric('Tipos de Culinárias Oferecidas', len(data_copy['cuisines'].unique()))

with st.container():
    map_restaurant(df_filter)
