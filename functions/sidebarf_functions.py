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

        with st.expander('Filtros', expanded=expanded):    
            mkd_text("", level='h6')
            mkd_text("Região", level='h4')

            # Verifica se o continente já foi selecionado no session_state
            continente_anterior = st.session_state.get('continente', None)
            continente_selecionado = st.session_state.get('continente', df['Continente'].unique()[0])

            # Seleção de Continente com persistência
            continentes = st.radio('Região', df['Continente'].unique(), key='radio_regiao',
                                   index=list(df['Continente'].unique()).index(continente_selecionado))

            # Atualizar o session_state com o continente selecionado
            st.session_state['continente'] = continentes

            # Verificar se o continente mudou
            continente_mudou = continente_anterior != continentes

            # Filtrar o dataframe pelo continente selecionado
            df_continente = df[df['Continente'] == continentes]

            mkd_text("", level='h6')
            mkd_text("Países", level='h4')

            # Seleção de País com persistência, filtrado pelo continente
            paises_disponiveis = df_continente['País'].unique()

            # Se o continente mudou, resetar a seleção de países
            if continente_mudou:
                st.session_state['paises'] = []

            # Garantir que os países selecionados ainda estão disponíveis
            paises_selecionados = [p for p in st.session_state.get('paises', []) if p in paises_disponiveis]

            paises = st.multiselect(
                'Selecione os países',
                paises_disponiveis,
                placeholder='Todos os países da região',
                help='Selecione os países que deseja visualizar', 
                key='mult', 
                default=paises_selecionados
            )

            # Atualizar o session_state com os países selecionados
            st.session_state['paises'] = paises

            # Filtrar o dataframe pelos países selecionados
            if paises:
                df_paises = df_continente[df_continente['País'].isin(paises)]
            else:
                df_paises = df_continente

            mkd_paragraph('')
            mkd_paragraph('')

            # Filtro de Período com persistência
            mkd_text("Período", level='h4')

            # Obter os anos disponíveis após os filtros
            anos_disponiveis = sorted(df_paises['Ano'].unique())

            # Se o continente ou os países mudaram, resetar a seleção de anos
            if continente_mudou or 'paises' in st.session_state and st.session_state['paises'] != paises_selecionados:
                st.session_state['anos'] = (min(anos_disponiveis), max(anos_disponiveis))

            # Garantir que os anos selecionados estão disponíveis
            anos_selecionados = st.session_state.get('anos', (min(anos_disponiveis), max(anos_disponiveis)))
            ano_inicio, ano_fim = anos_selecionados

            # Ajustar anos selecionados se não estiverem nos anos disponíveis
            if ano_inicio not in anos_disponiveis:
                ano_inicio = min(anos_disponiveis)
            if ano_fim not in anos_disponiveis:
                ano_fim = max(anos_disponiveis)

            # Slider de seleção de anos
            ano_inicial, ano_final = st.select_slider(
                'Selecione o período de análise',
                options=anos_disponiveis,
                value=(ano_inicio, ano_fim),
                key='slider_ano'
            )

            # Atualizar o session_state com os anos selecionados
            st.session_state['anos'] = (ano_inicial, ano_final)

            # Filtrar o dataframe pelos anos selecionados
            df_final = df_paises[(df_paises['Ano'] >= ano_inicial) & (df_paises['Ano'] <= ano_final)]

            st.divider()
            
            # Exibir dados com barra de progresso se solicitado
            if st.checkbox('Visualizar Dados?', key='mostrardados', help='Mostrar Dados em métricas e tabelas', value=mostrar_dados):
                st.session_state['mostrarcoluna'] = True
                
                progress_text = "Operação em progresso. Por favor, aguarde."
                my_bar = st.progress(0, text=progress_text)

                for percent_complete in range(100):
                    import time
                    time.sleep(0.01)
                    my_bar.progress(percent_complete + 1, text=progress_text)
                
                time.sleep(1)
                my_bar.empty()
                
                return df_final  # Retorna o DataFrame filtrado
            else:
                st.session_state['mostrarcoluna'] = False
