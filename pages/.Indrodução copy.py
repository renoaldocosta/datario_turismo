import streamlit as st
import pandas as pd
import time
from numerize.numerize import numerize
from functions.text_functions import mkd_text, mkd_paragraph

st.set_page_config(page_icon='🌍', layout='wide', initial_sidebar_state='auto')
#st.button("Rerun")


# Cache only the data loading part, not the widget
@st.cache_data
def load_data(file):
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






# Função para converter DataFrame em CSV
@st.cache_data
def convert_to_csv(df):
    return df.to_csv(index=False).encode('utf-8')

import streamlit as st

def alterar_cor_do_fundo():
    
    # Escolher a cor de fundo
    bg_color = st.color_picker('Cor de fundo', '#ffffff',key='bg_color_picker')

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

    
def questao6_sidebar_customizacao():
    # side bar inicia hide
         
    with st.sidebar:
        st.title('Rio de Janeiro: A Porta de Entrada pelos Ares')
        # Escolher a cor de fundo com color picker
        with st.expander('Customização do APP'):
            col = st.columns(2)
            with col[0]:
                alterar_cor_do_fundo()
            with col[1]:
                alterar_cor_do_texto()
        
        
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
        
        
def main(df):
    questao6_sidebar_customizacao()
        
    # converte 'Ano' para string
    df['Ano'] = df['Ano'].astype(str)
    
    # Soma de Janeiro a Dezembro
    df['Total'] = df['Janeiro'] + df['Fevereiro'] + df['Março'] + df['Abril'] + df['Maio'] + df['Junho'] + df['Julho'] + df['Agosto'] + df['Setembro'] + df['Outubro'] + df['Novembro'] + df['Dezembro']
    
    # Ordena as colunas
    df = df[['País', 'Continente','Janeiro', 'Fevereiro', 'Março', 'Abril', 'Maio', 'Junho', 'Julho', 'Agosto', 'Setembro', 'Outubro', 'Novembro', 'Dezembro','Ano', 'Total']]
    
    # Remove as linhas em que total de turistas é igual a 0
    df = df[df['Total'] != 0]
    
    
    # Exemplo de título
    
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
    
    mkd_text("Personalizar Visualização dos Dados", level='h4')
    col1, col2 = st.columns(2)
    with col1:
        mkd_text("", level='h6')
        mkd_text("Região", level='h4')
        continentes = st.radio('Região', df['Continente'].unique())
        if continentes:
            df = df[df['Continente'] == continentes]

    with col2:
        mkd_text("", level='h6')
        mkd_text("Países e Período", level='h4')
        # Corrigido o filtro dos países pelo continente selecionado
        paises = st.multiselect('Selecione os países', df[df['Continente'] == continentes]['País'].unique(),placeholder='Todos os países da região',help='Selecione os países que deseja visualizar')
        if paises:
            df = df[df['País'].isin(paises)]
        
        mkd_paragraph('')
        mkd_paragraph('')
        
        # Determinando os anos disponíveis para os países selecionados
        anos_disponiveis = sorted(df['Ano'].unique())
        
        ano_inicial, ano_final = st.select_slider(
            'Selecione o período de análise',
            options=anos_disponiveis,  # Certificando que os anos estão ordenados e filtrados
            value=(min(anos_disponiveis), max(anos_disponiveis)),  # Definindo o intervalo padrão de anos
        )
    
    
    
    df = df[(df['Ano'] >= ano_inicial) & (df['Ano'] <= ano_final) ]
    
    
    # centralizar checkbox
    
    col3 = st.columns([0.4, 0.2, 0.4])
    with col3[0]:
        st.divider()
    with col3[2]:
        st.divider()
        with col3[1]:
            if st.checkbox('Visualizar Dados?', key='regiao', help='Mostra os dados por região'):
                mostrarcoluna = True
                progress_text = "Operação em progresso. Por favor, aguarde."
                my_bar = st.progress(0, text=progress_text)

                for percent_complete in range(100):
                    import time
                    time.sleep(0.01)
                    my_bar.progress(percent_complete + 1, text=progress_text)
                time.sleep(1)
                my_bar.empty()
    
    
    st.session_state['df'] = df
    
    # ================== Gráfico ==================
    mkd_text("Visualização dos Dados", level='h4')
    chart(df)
    
    # ================== Tabela ==================
    mkd_text("Dados Filtrados", level
                ='h4')
    
    
    
    
    
    try:
        if mostrarcoluna:
            df = df.reset_index(drop=True)
            st.dataframe(df)
            
            
    except Exception as e:
        pass
        
    col4 = st.columns([0.3,0.6,0.3])
    with col4[1]:
        try:
            if mostrarcoluna:
                # Botão para download
                csv = convert_to_csv(df)
                st.download_button(
                    label='Clique para baixar o CSV',
                    data=csv,
                    file_name='dados_filtrados.csv',
                    mime='text/csv',
                    use_container_width=True,
                )
        except:
            pass
    
    
    #st.toast("Dados carregados com sucesso!", icon="success", position="center")
    

def chart(df):
    import streamlit as st
    import streamlit.components.v1 as components
    df['Janeiro'] = pd.to_numeric(df['Janeiro'], errors='coerce')
    soma_janeiro = int(df['Janeiro'].sum())
    
    df['Fevereiro'] = pd.to_numeric(df['Fevereiro'], errors='coerce')
    soma_fevereiro = int(df['Fevereiro'].sum())
    
    df['Março'] = pd.to_numeric(df['Março'], errors='coerce')
    soma_marco = int(df['Março'].sum())
    
    df['Abril'] = pd.to_numeric(df['Abril'], errors='coerce')
    soma_abril = int(df['Abril'].sum())
    
    df['Maio'] = pd.to_numeric(df['Maio'], errors='coerce')
    soma_maio = int(df['Maio'].sum())
    
    df['Junho'] = pd.to_numeric(df['Junho'], errors='coerce')
    soma_junho = int(df['Junho'].sum())
    
    df['Julho'] = pd.to_numeric(df['Julho'], errors='coerce')
    soma_julho = int(df['Julho'].sum())
    
    df['Agosto'] = pd.to_numeric(df['Agosto'], errors='coerce')
    soma_agosto = int(df['Agosto'].sum())
    
    df['Setembro'] = pd.to_numeric(df['Setembro'], errors='coerce')
    soma_setembro = int(df['Setembro'].sum())
    
    df['Outubro'] = pd.to_numeric(df['Outubro'], errors='coerce')
    soma_outubro = int(df['Outubro'].sum())
    
    df['Novembro'] = pd.to_numeric(df['Novembro'], errors='coerce')
    soma_novembro = int(df['Novembro'].sum())
    
    df['Dezembro'] = pd.to_numeric(df['Dezembro'], errors='coerce')
    soma_dezembro = int(df['Dezembro'].sum())
    
    
    col1, col2 = st.columns(2)
    with col1:
        # Sample Data
        months = ['Janeiro', 'Fevereiro', 'Março', 'Abril', 'Maio', 'Junho', 'Julho', 'Agosto', 'Setembro', 'Outubro', 'Novembro', 'Dezembro']
        sales = [soma_janeiro, soma_fevereiro, soma_marco, soma_abril, soma_maio, soma_junho, soma_julho, soma_agosto, soma_setembro, soma_outubro, soma_novembro, soma_dezembro]

        # HTML + JS Code for Chart.js
        chart_code = f"""
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <title>Bar Chart</title>
            <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
        </head>
        <body>
        <canvas id="myChart" width="400" height="400"></canvas>

        <script>
        var ctx = document.getElementById('myChart').getContext('2d');
        var myChart = new Chart(ctx, {{
            type: 'bar',
            data: {{
                labels: {months},
                datasets: [{{
                    label: 'Total de Turistas',
                    data: {sales},
                    backgroundColor: [
                        'rgba(255, 99, 132, 0.2)',
                        'rgba(54, 162, 235, 0.2)',
                        'rgba(255, 206, 86 , 0.2)',
                        'rgba(75 ,192 ,192 ,0.2)',
                        'rgba(153 ,102 ,255 ,0.2)',
                        'rgba(255 ,159 ,64 ,0.2)',
                        'rgba(255 ,99 ,132 ,0.2)',
                        'rgba(54 ,162 ,235 ,0.2)',
                        'rgba(255 ,206 ,86 ,0.2)',
                        'rgba(75 ,192 ,192 ,0.2)',
                        'rgba(153 ,102 ,255 ,0.2)',
                        'rgba(255 ,159 ,64 ,0.2)'
                        
                    ],
                    borderColor: [
                        'rgba(255 ,99 ,132 ,1)',
                        'rgba(54 ,162 ,235 ,1)',
                        'rgba(255 ,206 ,86 ,1)',
                        'rgba(75 ,192 ,192 ,1)',
                        'rgba(153 ,102 ,255 ,1)',
                        'rgba(255 ,159 ,64 ,1)',
                        'rgba(255 ,99 ,132 ,1)',
                        'rgba(54 ,162 ,235 ,1)',
                    ],
                    borderWidth: 1
                }}]
            }},
            options: {{
                scales : {{
                    y : {{
                        beginAtZero : false
                    }}
                }}
            }}
        }});
        </script>
        </body>
        </html>
        """

        # Render the custom component in Streamlit
        components.html(chart_code, height=5000)

import streamlit as st
import streamlit.components.v1 as components

# Função para exibir o gráfico de Bar Racing no Streamlit
def bar_racing_example(df):
    # HTML + JS para renderizar o gráfico com ECharts
    chart_code = """
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="utf-8">
        <script src="https://cdn.jsdelivr.net/npm/echarts@5.0.2/dist/echarts.min.js"></script>
        <style>
            #chart {
                width: 100%;
                height: 500px;
            }
        </style>
    </head>
    <body>
        <div id="chart"></div>

        <script type="text/javascript">
            var chartDom = document.getElementById('chart');
            var myChart = echarts.init(chartDom);

            var data = [];
            for (let i = 0; i < 5; ++i) {
                data.push(Math.round(Math.random() * 200));
            }

            var option = {
                xAxis: {
                    max: 'dataMax'
                },
                yAxis: {
                    type: 'category',
                    data: ['A', 'B', 'C', 'D', 'E'],
                    inverse: true,
                    animationDuration: 300,
                    animationDurationUpdate: 300,
                    max: 2 // only the largest 3 bars will be displayed
                },
                series: [
                    {
                        realtimeSort: true,
                        name: 'X',
                        type: 'bar',
                        data: data,
                        label: {
                            show: true,
                            position: 'right',
                            valueAnimation: true
                        }
                    }
                ],
                legend: {
                    show: true
                },
                animationDuration: 0,
                animationDurationUpdate: 3000,
                animationEasing: 'linear',
                animationEasingUpdate: 'linear'
            };

            myChart.setOption(option);

            function run() {
                var data = option.series[0].data;
                for (var i = 0; i < data.length; ++i) {
                    if (Math.random() > 0.9) {
                        data[i] += Math.round(Math.random() * 2000);
                    } else {
                        data[i] += Math.round(Math.random() * 200);
                    }
                }
                myChart.setOption(option);
            }

            setTimeout(function() {
                run();
            }, 0);

            setInterval(function() {
                run();
            }, 3000);
        </script>
    </body>
    </html>
    """

    # Renderizar o HTML no Streamlit
    components.html(chart_code, height=500)

def bar_racing_example21(df):
    # HTML + JS para renderizar o gráfico com ECharts
    chart_code = """
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="utf-8">
        <script src="https://cdn.jsdelivr.net/npm/echarts@5.0.2/dist/echarts.min.js"></script>
        <style>
            #chart {
                width: 100%;
                height: 500px;
            }
        </style>
    </head>
    <body>
        <div id="chart"></div>

        <script type="text/javascript">
            var chartDom = document.getElementById('chart');
            var myChart = echarts.init(chartDom);

            var data = [];
            for (let i = 0; i < 5; ++i) {
                data.push(Math.round(Math.random() * 200));
            }

            var option = {
                xAxis: {
                    max: 'dataMax'
                },
                yAxis: {
                    type: 'category',
                    data: ['A', 'B', 'C', 'D', 'E'],
                    inverse: true,
                    animationDuration: 300,
                    animationDurationUpdate: 300,
                    max: 2 // only the largest 3 bars will be displayed
                },
                series: [
                    {
                        realtimeSort: true,
                        name: 'Xxxxx',
                        type: 'bar',
                        data: data,
                        label: {
                            show: true,
                            position: 'right',
                            valueAnimation: true
                        }
                    }
                ],
                legend: {
                    show: true
                },
                animationDuration: 0,
                animationDurationUpdate: 3000,
                animationEasing: 'linear',
                animationEasingUpdate: 'linear'
            };

            myChart.setOption(option);

            function run() {
                var data = option.series[0].data;
                for (var i = 0; i < data.length; ++i) {
                    if (Math.random() > 0.9) {
                        data[i] += Math.round(Math.random() * 2000);
                    } else {
                        data[i] += Math.round(Math.random() * 200);
                    }
                }
                myChart.setOption(option);
            }

            setTimeout(function() {
                run();
            }, 0);

            setInterval(function() {
                run();
            }, 3000);
        </script>
    </body>
    </html>
    """

    # Renderizar o HTML no Streamlit
    components.html(chart_code, height=500)


import pandas as pd
import streamlit.components.v1 as components

def bar_racing_chart2(df):
    # Converter colunas para inteiros, tratando valores não numéricos
    data = {
        'País': df['País'],
        'total_por_ano': df['total_por_ano'].apply(lambda x: int(x) if str(x).isdigit() else 0),
        'Ano': df['Ano'].apply(lambda x: int(x) if str(x).isdigit() else 0)
    }

    df = pd.DataFrame(data)

    # Ordenar por País e Ano para garantir que os dados estão na ordem correta
    df = df.sort_values(by=['País', 'Ano']).reset_index(drop=True)
    
    # Exibir o DataFrame ordenado para verificação
    st.dataframe(df)

    # Preparar os dados para ECharts
    countries = df['País'].unique().tolist()
    anos = df['Ano'].unique().tolist()
    
    # Agrupar os dados por Ano, para que cada ano tenha os valores corretos
    total_por_ano = [df[df['Ano'] == ano]['total_por_ano'].tolist() for ano in anos]

    # HTML + JS para renderizar o gráfico com ECharts
    chart_code = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="utf-8">
        <script src="https://cdn.jsdelivr.net/npm/echarts@5.0.2/dist/echarts.min.js"></script>
        <style>
            #chart {{
                width: 100%;
                height: 500px;
            }}
        </style>
    </head>
    <body>
        <div id="chart"></div>

        <script type="text/javascript">
            var chartDom = document.getElementById('chart');
            var myChart = echarts.init(chartDom);

            var countries = {countries};
            var totalPorAno = {total_por_ano};
            var anos = {anos};
            var idx = 0;

            var option = {{
                title: {{
                    text: 'Corrida de Barras: Total de Viajantes por País',
                    left: 'center'
                }},
                xAxis: {{
                    max: 'dataMax'
                }},
                yAxis: {{
                    type: 'category',
                    data: countries,
                    inverse: true,
                    animationDuration: 300,
                    animationDurationUpdate: 300,
                    max: 10  // Defina o número máximo de barras visíveis
                }},
                series: [
                    {{
                        realtimeSort: true,
                        name: 'Viajantes',
                        type: 'bar',
                        data: totalPorAno[0],  // Mostra os dados do primeiro ano
                        label: {{
                            show: true,
                            position: 'right',
                            valueAnimation: true
                        }}
                    }}
                ],
                legend: {{
                    show: true
                }},
                animationDuration: 0,
                animationDurationUpdate: 3000,
                animationEasing: 'linear',
                animationEasingUpdate: 'linear'
            }};

            myChart.setOption(option);

            // Função para atualizar os dados em intervalos de tempo (animação)
            function updateChart() {{
                idx = (idx + 1) % anos.length;
                var ano = anos[idx];

                myChart.setOption({{
                    series: [{{
                        data: totalPorAno[idx]
                    }}],
                    title: {{
                        text: 'Ano: ' + ano
                    }}
                }});
            }}

            setTimeout(function() {{
                updateChart();
            }}, 0);

            setInterval(function() {{
                updateChart();
            }}, 3000);
        </script>
    </body>
    </html>
    """

    # Renderizar o gráfico no Streamlit
    components.html(chart_code, height=500)











if __name__ == '__main__':
    # cria df vazio
    if 'df' not in st.session_state:
        st.session_state['df'] = None
        df = None
    try:
        if st.session_state['df'] is None:
            # File uploader should be outside of the cached function
            uploaded_file = st.file_uploader("Escolha um arquivo CSV", type="csv", label_visibility='hidden')

            if uploaded_file is not None:
                df = load_data(uploaded_file)
            try:
                if df is None:
                    st.warning("Por favor, faça o upload de um arquivo CSV.")
                else:
                    concordo = st.checkbox('Entendo que fazendo o upload de um arquivo CSV, eu estou concordando com os termos de uso da plataforma.')
                    if concordo:
                        data_hora_atual = pd.Timestamp.now().strftime('%d/%m/%Y às %H:%M:%S')
                        mkd_paragraph(f'Termo de uso aceito em {data_hora_atual}.', position='center')
                        st.divider()
                        main(df)
        
            except Exception as e:
                #st.error(f"Erro: {e}")
                pass
        else:
            try:
                main(st.session_state['df'])
            except:
                pass
    except Exception as e:
        st.error(f"Erro: {e}")
    
    df = pd.read_csv('./paises.csv')
    # Chamar a função para exibir o gráfico no Streamlit
    paises = df['País'].unique().tolist()
    # converte para int se for string e pude ser convertido para int senao 0
    df['Janeiro'] = df['Janeiro'].apply(lambda x: int(x) if str(x).isdigit() else 0)
    df['Fevereiro'] = df['Fevereiro'].apply(lambda x: int(x) if str(x).isdigit() else 0)
    df['Março'] = df['Março'].apply(lambda x: int(x) if str(x).isdigit() else 0)
    df['Abril'] = df['Abril'].apply(lambda x: int(x) if str(x).isdigit() else 0)
    df['Maio'] = df['Maio'].apply(lambda x: int(x) if str(x).isdigit() else 0)
    df['Junho'] = df['Junho'].apply(lambda x: int(x) if str(x).isdigit() else 0)
    df['Julho'] = df['Julho'].apply(lambda x: int(x) if str(x).isdigit() else 0)
    df['Agosto'] = df['Agosto'].apply(lambda x: int(x) if str(x).isdigit() else 0)
    df['Setembro'] = df['Setembro'].apply(lambda x: int(x) if str(x).isdigit() else 0)
    df['Outubro'] = df['Outubro'].apply(lambda x: int(x) if str(x).isdigit() else 0)
    df['Novembro'] = df['Novembro'].apply(lambda x: int(x) if str(x).isdigit() else 0)
    df['Dezembro'] = df['Dezembro'].apply(lambda x: int(x) if str(x).isdigit() else 0)
        
    df['total_por_ano'] = df['Janeiro'] + df['Fevereiro'] + df['Março'] + df['Abril'] + df['Maio'] + df['Junho'] + df['Julho'] + df['Agosto'] + df['Setembro'] + df['Outubro'] + df['Novembro'] + df['Dezembro']
    df = df.sort_values(by='total_por_ano', ascending=False).reset_index(drop=True)
    #bar_racing_chart2(df)
    
    
    