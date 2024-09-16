import streamlit as st
import pandas as pd
from functions.text_functions import mkd_text, mkd_paragraph, mkd_text_divider
import time


def alterar_cor_do_fundo():
    
    # Escolher a cor de fundo
    bg_color = st.color_picker('Cor de fundo', '#ffffff',key='bg_color_picker1')

    # Aplicar o estilo de fundo utilizando a cor selecionada
    st.markdown(f"""
        <style>
            .stApp {{
                background-color: {bg_color};
            }}
        </style>
        """, unsafe_allow_html=True)

def alterar_cor_do_texto():
    # Armazenar a cor do texto no session_state
    if "text_color" not in st.session_state:
        st.session_state["text_color"] = '#3B3030'  # Cor padrão
    else:
        # Escolher a cor do texto e armazenar em session_state
        st.session_state["text_color"] = st.color_picker('Cor do Texto', st.session_state["text_color"], key='text_color_picker')
    # Aplicar o estilo de cor de texto utilizando a cor selecionada
    st.markdown(f"""
        <style>
            .stApp {{
                color: {st.session_state["text_color"]}; /* Aplica a cor de texto ao conteúdo */
            }}
            /* Estilizar os widgets de entrada como color picker, botões, etc. */
            .stSlider > div > div > div > input, 
            .stTextInput > div > div > input, 
            .stButton > button, 
            .stColorPicker > div > label {{
                color: {st.session_state["text_color"]}; /* Aplica a cor de texto aos widgets */
            }}
        </style>
        """, unsafe_allow_html=True)




def customizacao():
    # side bar inicia hide
    with st.sidebar:
        # Escolher a cor de fundo com color picker
        with st.expander('Customização do APP'):
            col = st.columns(2)
            with col[0]:
                alterar_cor_do_fundo()
            with col[1]:
                alterar_cor_do_texto()



def sidebar(df, expanded=True, mostrar_dados=True):
    
    with st.sidebar:
        st.title('Rio de Janeiro: A Porta de Entrada pelos Ares')
        # Escolher a cor de fundo com color picker
        
        with st.expander('Filtros', expanded=expanded):    
            mkd_text("", level='h6')
            mkd_text("Região", level='h4')
            continentes = st.radio('Região', df['Continente'].unique(), key='radio_regiao')
            if continentes:
                df = df[df['Continente'] == continentes]


            mkd_text("", level='h6')
            mkd_text("Países", level='h4')
            # Corrigido o filtro dos países pelo continente selecionado
            paises = st.multiselect('Selecione os países', df[df['Continente'] == continentes]['País'].unique(),placeholder='Todos os países da região',help='Selecione os países que deseja visualizar', key='mult')
            if paises:
                df = df[df['País'].isin(paises)]
            
            mkd_paragraph('')
            mkd_paragraph('')
        
            # Determinando os anos disponíveis para os países selecionados
            mkd_text("Período", level='h4')
            anos_disponiveis = sorted(df['Ano'].unique())
            
            ano_inicial, ano_final = st.select_slider(
                'Selecione o período de análise',
                options=anos_disponiveis,  # Certificando que os anos estão ordenados e filtrados
                value=(min(anos_disponiveis), max(anos_disponiveis)),  # Definindo o intervalo padrão de anos
                key='slider_ano'
            )
            df = df[(df['Ano'] >= ano_inicial) & (df['Ano'] <= ano_final) ]
        
            st.divider()
            
                    
            if st.checkbox('Visualizar Dados?', key='mostrardados', help='Mostrar Dados em métricas e tabelas', value=mostrar_dados):
                st.session_state['mostrarcoluna'] = True
                x='''progress_text = "Operação em progresso. Por favor, aguarde."
                my_bar = st.progress(0, text=progress_text)

                for percent_complete in range(100):
                    import time
                    time.sleep(0.01)
                    my_bar.progress(percent_complete + 1, text=progress_text)
                time.sleep(1)
                my_bar.empty()'''
                return df
            else:
                st.session_state['mostrarcoluna'] = False