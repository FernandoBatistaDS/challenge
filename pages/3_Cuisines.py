# IMPORTS
import pandas as pd
import inflection
import streamlit as st
import numpy as np

import plotly.express as px

st.set_page_config(
   page_title="Cuisines",
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

# Quantidade que quer ver
count_restaurant = st.sidebar.slider('Selecione a quantidade de Restaurantes que deseja visualizar', 0, 20, 10)

# Filtro por tipo de culinaria
allCuisines = data_copy['cuisines'].unique()
cuisines_selects = st.sidebar.multiselect(
    'Escolha os Tipos de Culinária',
    allCuisines,
    np.random.choice(allCuisines, size=7, replace=False)
)


df_filter = data_copy.query('country_name == @country_selects & cuisines == @cuisines_selects')

#================================
######   STREAMLIT - CONTAINER
#================================

# st.dataframe(df_filter)

st.markdown("# 🍽️ Visão Tipos de Cusinhas")
st.markdown("## Melhores Restaurantes dos Principais tipos Culinários")
col1, col2, col3, col4, col5 = st.columns(5)


with st.container():
    # top_cuisines = data_copy.pivot_table(index=['cuisines', 'restaurant_id', 'restaurant_name', 'city', 'country_name', 'currency'],
    #                             values=['aggregate_rating', 'average_cost_for_two'],
    #                             aggfunc={'aggregate_rating': 'max', 'average_cost_for_two': 'mean'})
    top_cuisines = data_copy.groupby('cuisines')['aggregate_rating'].idxmax()
    top_cuisines = data_copy.loc[top_cuisines]
    top_cuisines = top_cuisines.sort_values('aggregate_rating', ascending=False)
    top_cuisines = top_cuisines.reset_index()

    with col1:
        textHelp = 'País: ' + top_cuisines['country_name'][0] + '\n\n Cidade: ' + top_cuisines['city'][0] + '\n\n Média Prato para dois: ' + str(top_cuisines['average_cost_for_two'][0]) + ' ('+ top_cuisines['currency'][0] +')'
        col1.metric(label=top_cuisines['cuisines'][0] +': ' + top_cuisines['restaurant_name'][0], value=str(top_cuisines['aggregate_rating'][0]) +'/5.0', help=textHelp)

    with col2:
        textHelp = 'País: ' + top_cuisines['country_name'][1] + '\n\n Cidade: ' + top_cuisines['city'][1] + '\n\n Média Prato para dois: ' + str(top_cuisines['average_cost_for_two'][1]) + ' ('+ top_cuisines['currency'][1] +')'
        col2.metric(label=top_cuisines['cuisines'][1] +': ' + top_cuisines['restaurant_name'][1], value=str(top_cuisines['aggregate_rating'][1]) +'/5.0', help=textHelp)

    with col3:
        textHelp = 'País: ' + top_cuisines['country_name'][2] + '\n\n Cidade: ' + top_cuisines['city'][2] + '\n\n Média Prato para dois: ' + str(top_cuisines['average_cost_for_two'][2]) + ' ('+ top_cuisines['currency'][2] +')'
        col3.metric(label=top_cuisines['cuisines'][2] +': ' + top_cuisines['restaurant_name'][2], value=str(top_cuisines['aggregate_rating'][2]) +'/5.0', help=textHelp)

    with col4:
        textHelp = 'País: ' + top_cuisines['country_name'][3] + '\n\n Cidade: ' + top_cuisines['city'][3] + '\n\n Média Prato para dois: ' + str(top_cuisines['average_cost_for_two'][3]) + ' ('+ top_cuisines['currency'][3] +')'
        col4.metric(label=top_cuisines['cuisines'][3] +': ' + top_cuisines['restaurant_name'][3], value=str(top_cuisines['aggregate_rating'][3]) +'/5.0', help=textHelp)

    with col5:
        textHelp = 'País: ' + top_cuisines['country_name'][4] + '\n\n Cidade: ' + top_cuisines['city'][4] + '\n\n Média Prato para dois: ' + str(top_cuisines['average_cost_for_two'][4]) + ' ('+ top_cuisines['currency'][4] +')'
        col5.metric(label=top_cuisines['cuisines'][4] +': ' + top_cuisines['restaurant_name'][4], value=str(top_cuisines['aggregate_rating'][4]) +'/5.0', help=textHelp)

with st.container():
    st.markdown("## Top "+ str(count_restaurant) +" Restaurantes")
    st.dataframe(df_filter[['restaurant_id', 'restaurant_name', 'country_name', 'city', 'cuisines', 'average_cost_for_two', 'aggregate_rating', 'votes']].sort_values('aggregate_rating', ascending=False).head(count_restaurant), use_container_width=True)

with st.container():
    col1, col2 = st.columns(2)
    with col1:
        df = data_copy.query('country_name == @country_selects')
        dt_top_cuisines = df[['aggregate_rating', 'cuisines']].groupby('cuisines').mean().reset_index().sort_values('aggregate_rating', ascending=False).head(count_restaurant)
        fig = px.bar(dt_top_cuisines, x='cuisines', y='aggregate_rating', text_auto=True, title="Top "+ str(count_restaurant) +" Melhores Tipos de Culinárias", labels={'cuisines': 'Tipo de culinária', 'aggregate_rating': 'Média de avaliação'})
        st.plotly_chart(fig, use_container_width=True)
    with col2:
        df = data_copy.query('country_name == @country_selects')
        dt_top_cuisines = df[['aggregate_rating', 'cuisines']].groupby('cuisines').mean().reset_index().sort_values('aggregate_rating', ascending=True)
        dt_top_cuisines = dt_top_cuisines[dt_top_cuisines['aggregate_rating'] != 0]
        dt_top_cuisines = dt_top_cuisines.head(count_restaurant)
        fig = px.bar(dt_top_cuisines, x='cuisines', y='aggregate_rating', text_auto=True, title="Top "+ str(count_restaurant) +" Piores Tipos de Culinárias", labels={'cuisines': 'Tipo de culinária', 'aggregate_rating': 'Média de avaliação'})
        st.plotly_chart(fig, use_container_width=True)
