import streamlit as st
import pandas as pd
import time
from numerize.numerize import numerize
from functions.text_functions import mkd_text, mkd_paragraph, mkd_text_divider
from functions.sidebarf_functions import sidebar
from functions.sidebarf_functions import customizacao
from functions.other_functions import banner

st.set_page_config(page_icon='🌍', layout='wide', initial_sidebar_state='auto')
#st.button("Rerun")


# Cache only the data loading part, not the widget
@st.cache_data
def load_data(file):
    try:
        with st.spinner('Processando...'):
            time.sleep(2)  # Simulating processing time
            df = pd.read_csv(file)
            
            # Progress bar
            progress_text = "Carregando arquivo CSV. Por favor, aguarde."
            my_bar = st.progress(0, text=progress_text)

            for percent_complete in range(100):
                time.sleep(0.01)
                my_bar.progress(percent_complete + 1, text=progress_text)

            time.sleep(1)
            my_bar.empty()
            
        return df
    except Exception as e:
        st.error(f"Erro: {e}")
        return None


# Função para converter DataFrame em CSV
@st.cache_data
def convert_to_csv(df):
    return df.to_csv(index=False).encode('utf-8')


        
        
def upload_PDF():
    import pdfplumber
    uploaded_pdf_file = st.file_uploader("Escolha um arquivo PDF", type="pdf", label_visibility='hidden')
    if uploaded_pdf_file is not None:
        # Ler o arquivo PDF
        with pdfplumber.open(uploaded_pdf_file) as pdf:
            text = ''
            for page in pdf.pages:
                for row in page.extract_text().split('\n'):
                    text += row + '\n\n'
            return text
        
        

def processar_dados(df):
    # converte 'Ano' para string
    df['Ano'] = df['Ano'].astype(str)
    
    # Soma de Janeiro a Dezembro
    df['Total'] = df['Janeiro'] + df['Fevereiro'] + df['Março'] + df['Abril'] + df['Maio'] + df['Junho'] + df['Julho'] + df['Agosto'] + df['Setembro'] + df['Outubro'] + df['Novembro'] + df['Dezembro']
    
    # Ordena as colunas
    df = df[['País', 'Continente','Janeiro', 'Fevereiro', 'Março', 'Abril', 'Maio', 'Junho', 'Julho', 'Agosto', 'Setembro', 'Outubro', 'Novembro', 'Dezembro','Ano', 'Total']]
    
    # Remove as linhas em que total de turistas é igual a 0
    df = df[df['Total'] != 0]
    
    return df

def progress(sleep=1):
    # Progress bar
    progress_text = "Carregando arquivo CSV. Por favor, aguarde."
    my_bar = st.progress(0, text=progress_text)

    for percent_complete in range(100):
        time.sleep(0.01)
        my_bar.progress(percent_complete + 1, text=progress_text)

    time.sleep(sleep)
    my_bar.empty()


def cabeçalho(df):
    # Exemplo de título
    banner()
    mkd_text("Chegada Mensal de Turistas ao Rio de Janeiro por Via Aérea (2006-2019)", level='title')

    
    # Exemplo de header e subheader
    mkd_text("Introdução", level='header')
    st.divider()
    mkd_paragraph("""Conhecer e visualizar os dados sobre a chegada mensal de turistas ao Rio de Janeiro por via aérea, com base nos continentes e países de residência permanente, entre 2006 e 2019, é essencial para entender as dinâmicas do turismo na cidade. Esses dados oferecem uma visão clara sobre o fluxo de turistas de diferentes partes do mundo, permitindo identificar padrões sazonais, picos de demanda e a influência de eventos internacionais. Além disso, essa análise ajuda a avaliar o impacto de políticas públicas, campanhas de marketing e crises globais, como recessões econômicas ou epidemias, no setor de turismo da cidade.""")
    mkd_paragraph('''A visualização desses dados também é crucial para que órgãos governamentais, empresas do setor turístico e pesquisadores possam tomar decisões informadas. Ao identificar tendências de crescimento ou queda de turistas de determinados continentes ou países, é possível ajustar estratégias de infraestrutura, serviços e atendimento ao turista. Além disso, compreender a distribuição geográfica dos visitantes ajuda na criação de campanhas promocionais mais segmentadas, com o objetivo de atrair turistas de mercados estratégicos e melhorar a experiência do visitante, garantindo o crescimento sustentável do turismo na cidade.''')
    
    # Mostrar o DataFrame
    mkd_text("Amostra dos Dados", level='h4')
    
    st.dataframe(df.head())
    
        
    st.divider()
    


def main(first):
    if ('df_carregado' not in st.session_state) or (st.session_state['df_carregado'] == False):
        if 'df' not in st.session_state:
            st.session_state['df'] = None
        
        # File uploader para selecionar CSV
        uploaded_file = st.file_uploader("Escolha um arquivo CSV", type="csv", label_visibility='hidden')

        if uploaded_file is not None:
            df = load_data(uploaded_file)
            df = processar_dados(df)
            st.session_state['df_carregado'] = True

            if df is not None:
                # Salva no session_state para persistência
                st.session_state['df'] = df
                st.write("Arquivo CSV carregado com sucesso.")
            else:
                st.warning("Falha ao carregar o arquivo CSV.")
        
        # Recupera o DataFrame do session_state
        df = st.session_state['df']
        
        # Verifica se o DataFrame foi carregado corretamente antes de processar
        if df is not None:
            concordo = st.checkbox('Entendo que fazendo o upload de um arquivo CSV, eu estou concordando com os termos de uso da plataforma.')
            if 'termo_de_uso' not in st.session_state:
                data_hora_atual = pd.Timestamp.now().strftime('%d/%m/%Y às %H:%M:%S')
                st.session_state['termo_de_uso'] = data_hora_atual
            if concordo:
                mkd_paragraph(f'Termo de uso aceito em {data_hora_atual}.', position='center')
                st.divider()
                cabeçalho(df)
        else:
            st.warning("Nenhum arquivo CSV foi carregado ainda.")
    else:
        df = st.session_state['df']
        df = sidebar(df, expanded=False, mostrar_dados=False)
        customizacao()
        try:
            cabeçalho(df)
        except:
            st.warning('Para visualizar os dados, clique em "Filtros" e então "Visualizar Dados?" no sidebar à esquerda.')
        
        if 'termo_de_uso' in st.session_state:
            termo = st.session_state['termo_de_uso']
            mkd_paragraph(f'Termo de uso aceito em {termo}.', position='center')
    

if __name__ == '__main__':
    first = False
    # Inicializa df vazio no session_state se não existir
    main(True)
        
    
    
    
    
    