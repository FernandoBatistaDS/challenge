# IMPORTS
import pandas as pd
import inflection
import streamlit as st
import numpy as np
import plotly as pt
import plotly.express as px

st.set_page_config(
   page_title="Countries",
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

# Function para contar colunas por pais
def number_by_country(df_filter, col, title, label, do):
    count_country = df_filter[col].groupby(col[0]).agg(do)
    count_country = count_country.reset_index().sort_values(col[1], ascending=False)

    fig = px.bar(count_country, x=col[0], y=col[1], labels=label, height=400, text_auto=True)
    fig.update_layout(
        title={
            'text': title,
            'x': 0.5,  # Define o título no centro horizontal da figura
            'xanchor': 'center',  # Alinha o título ao centro
            'yanchor': 'top',  # Alinha o título ao topo
            'font': {
                'family': 'Arial',  # Escolher a família da fonte
                'size': 18  # Definir o tamanho da fonte
            }
        },
        xaxis_tickfont_size=14,
        legend=dict(
            x=0,
            y=1.0,
            bgcolor='rgba(255, 255, 255, 0)',
            bordercolor='rgba(255, 255, 255, 0)'
        ),
        barmode='group',
        bargap=0.15, # gap between bars of adjacent location coordinates.
        bargroupgap=0.1 # gap between bars of the same location coordinate.
    )

    return fig

# Contar cidade por pais
def graphs_number_of_cities_by_country(df_filter, col):
    count_city_by_country = df_filter[col].groupby(col[0]).count()
    count_city_by_country = count_city_by_country.reset_index().sort_values(col[1], ascending=False)

    return px.bar(count_city_by_country, x=col[0], y=col[1])

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
    df["cuisines"] = df["cuisines"].str.split(",").str[0]

    df = df[(df['cuisines'] != 'Mineira') & (df['cuisines'] != 'Drinks Only')]

    # df = df[df['cuisines'].notnull()]

    return df

# @st.cache
def convert_df(df):
    # IMPORTANT: Cache the conversion to prevent computation on every rerun
    return df.to_csv().encode('utf-8')

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

#================================
######   STREAMLIT - CONTAINER
#================================

# st.dataframe(df_filter)

st.markdown("# 🗺️ Visão Países")

with st.container():
    # Chamando a function para fazer o grafico de barras para quantidades de restaurantes por país
    st.plotly_chart(number_by_country(df_filter, ['country_name', 'restaurant_id'], "Quantidade de restaurantes registrados por país", {'country_name':'País', 'restaurant_id': 'Quantidade de Restaurantes'}, 'nunique'), use_container_width=True)

with st.container():
    # Chamando a function para fazer o grafico de barras para quantidades de cidade por país
    st.plotly_chart(number_by_country(df_filter, ['country_name', 'city'], "Quantidade de cidades registradas por país", {'country_name':'País', 'city': 'Quantidade de Cidades'}, 'nunique'), use_container_width=True)

cols1, cols2 = st.columns(2)
with cols1:
    # Media de avaliação feitas por país
    st.plotly_chart(number_by_country(df_filter, ['country_name', 'votes'], "Média de avaliações feitas por país", {'country_name':'País', 'votes': 'Quantidade de avaliações'}, 'mean'), use_container_width=True)

with cols2:
    st.plotly_chart(number_by_country(df_filter, ['country_name', 'average_cost_for_two'], "Média de preço de um prato para duas pessoas por País", {'country_name':'País', 'average_cost_for_two': 'Preço de prato para duas pessoas'}, 'mean'), use_container_width=True)
