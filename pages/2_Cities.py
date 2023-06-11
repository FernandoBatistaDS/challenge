# IMPORTS
import pandas as pd
import inflection
import streamlit as st
import numpy as np
import random

import plotly.express as px

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

# Top restaurantes por tipo de culinaria em cada cidade
def top_cursines_by_city():
    city_with_most_food =  df_filter[['cuisines', 'city', 'country_name']].groupby(['city', 'country_name']).nunique().reset_index()
    city_with_most_food = city_with_most_food.sort_values('cuisines', ascending=False)
    city_with_most_food = city_with_most_food.head(10)
    fig = px.bar(city_with_most_food, x='city', y='cuisines', color='country_name', labels={'cuisines': 'Quantidade de Tipos Culinários Únicos', 'city': 'Cidade', 'country_name': 'País'}, text_auto=True)
    fig.update_layout(
        title={
            'text': 'TOP 10 Cidades com tipos de culinários distintos',
            'x': 0.5,  # Define o título no centro horizontal da figura
            'xanchor': 'center',  # Alinha o título ao centro
            'yanchor': 'top',  # Alinha o título ao topo
            'font': {
                'family': 'Arial',  # Escolher a família da fonte
                'size': 18  # Definir o tamanho da fonte
            }
        }
    )

    return fig

# Top restaurantes media de avaliação em cada cidade
def top_restaurant_by_city(ratings, condition, label, title, order):
    top_restaurant_by_city = df_filter[['city', 'restaurant_id', 'aggregate_rating', 'country_name']].groupby(['city', 'country_name', 'restaurant_id']).mean()

    top_restaurant_by_city = top_restaurant_by_city.reset_index().sort_values('aggregate_rating', ascending=order)

    if(condition == '>'):
        top_restaurant_by_city = top_restaurant_by_city[top_restaurant_by_city['aggregate_rating'] > ratings]
    else:
        top_restaurant_by_city = top_restaurant_by_city[top_restaurant_by_city['aggregate_rating'] < ratings]

    top_restaurant_by_city = top_restaurant_by_city.groupby(['city', 'country_name']).count().reset_index().sort_values('restaurant_id', ascending=order)
    top_restaurant_by_city = top_restaurant_by_city.head(7)

    fig = px.bar(top_restaurant_by_city, x='city', y='restaurant_id', color='country_name', labels=label, text_auto=True)
    fig.update_layout(
        title={
            'text': title,
            'x': 0.5,  # Define o título no centro horizontal da figura
            'xanchor': 'center',  # Alinha o título ao centro
            'yanchor': 'top',  # Alinha o título ao topo
            'font': {
                'family': 'Arial',  # Escolher a família da fonte
                'size': 12  # Definir o tamanho da fonte
            }
        }
    )

    return fig

# Buscar restaurantes por cidade
def city_data_base_for_charts(cols, label, title, condiction):
    city_with_more_restaurant = df_filter[cols].groupby(cols[:-1]).agg(condiction)
    city_with_more_restaurant = city_with_more_restaurant.reset_index().sort_values('restaurant_id', ascending=False)
    city_with_more_restaurant = city_with_more_restaurant.head(10)

    fig = px.bar(city_with_more_restaurant, x=cols[0], y=cols[2], color=cols[1], labels=label, text_auto=True)
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
        }
    )

    return fig

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

st.markdown("# 🏙️ Visão Cidades")

with st.container():
    st.plotly_chart(city_data_base_for_charts(['city', 'country_name', 'restaurant_id'], {'city': 'Cidade', 'restaurant_id': 'Quantidade de restaurantes', 'country_name': 'País'}, 'TOP 10 Cidades com mais Restaurantes na Base de Dados', 'nunique'), use_container_width=True)

col1, col2 = st.columns(2)
with col1:
    st.plotly_chart(top_restaurant_by_city(4, '>', {'city': 'Cidade', 'restaurant_id': 'Quantidade de restaurantes', 'country_name': 'País'}, 'TOP 7 Cidades com Restaurantes com média de avaliação acima de 4', False), use_container_width=True)

with col2:
    st.plotly_chart(top_restaurant_by_city(2.5, '<', {'city': 'Cidade', 'restaurant_id': 'Quantidade de restaurantes', 'country_name': 'País'}, 'TOP 7 Cidades com Restaurantes com média de avaliação abaixo de 2.5', False), use_container_width=True)

with st.container():
    st.plotly_chart(top_cursines_by_city(), use_container_width=True)

