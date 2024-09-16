import streamlit as st
from numerize.numerize import numerize
import functions.text_functions as my
from functions.text_functions import mkd_text, mkd_paragraph,mkd_text_divider

@st.cache_data
def load_df():
    df = st.session_state['df']    
    return df


def metricas(df):
    
    
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        total_turistas = df['Total'].sum()
        st.metric('Total de Turistas', numerize(int(total_turistas)))
    with col2:
        media_turistas = df['Total'].mean()
        st.metric(f"Média de Turistas por Mês", numerize(float(media_turistas/12)))
    with col3:
        total_paises = len(df['País'].unique())
        st.metric('Total de Países', numerize(int(total_paises)))
    with col4:
        ano_inicio = df['Ano'].min()
        ano_fim = df['Ano'].max()
        st.metric('Período', f'{ano_inicio} - {ano_fim}')
    
def cabeçalho():
    my.mkd_text('Métricas e Visualizações', level='header', position='center')
    my.mkd_paragraph('Nesta página, você pode visualizar as métricas do dataset e os gráficos de sua escolha.', position='center')
    my.mkd_text_divider('Métricas', level='subheader', position='center')



    