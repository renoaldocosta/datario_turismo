import streamlit as st
import pandas as pd
import time
from numerize.numerize import numerize
from functions.text_functions import mkd_text, mkd_paragraph, mkd_text_divider
from functions.sidebarf_functions import sidebar
from functions.sidebarf_functions import customizacao
from functions.report_functions import metricas, cabeçalho
import altair as alt

st.set_page_config(page_icon='🌍', layout='wide', initial_sidebar_state='auto')
#st.button("Rerun")

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
        

@st.cache_data
def load_df():
    df = st.session_state['df']    
    return df


def bar_chart_turistas_mes(df):
    try:
        df_mes = df[['Janeiro', 'Fevereiro', 'Março', 'Abril', 'Maio', 'Junho', 'Julho', 'Agosto', 'Setembro', 'Outubro', 'Novembro', 'Dezembro']].sum().reset_index()

        # Renomear as colunas para 'Mês' e 'Visitantes'
        df_mes.columns = ['Mês', 'Visitantes']

        # Aplicar numerize à coluna 'Visitantes' para formatar grandes números
        df_mes['Visitantes_numerize'] = df_mes['Visitantes'].apply(numerize)
        df_mes['Visitantes_formatado'] = df_mes['Visitantes'].apply(lambda x: f'{x:,.0f}'.replace(',', '.'))

        # Criar gráfico de barras com Altair para visitantes por mês
        grafico = alt.Chart(df_mes).mark_bar().encode(
            x=alt.X('Mês:N', title='Mês', sort=None),
            y=alt.Y('Visitantes:Q', title='Total de Visitantes'),
            color='Visitantes:Q',  # Cor fixa para as barras
            tooltip=[
                alt.Tooltip('Mês:N', title='Mês'),
                alt.Tooltip('Visitantes_formatado:N', title='Total de Visitantes')
            ]
        ).properties(
            width=600,
            height=450,
        )

        # Adicionar os valores sobre as barras com cor preta
        text = grafico.mark_text(
            align='center',
            baseline='middle',
            dy=-10  # Desloca o texto um pouco acima da barra
        ).encode(
            text='Visitantes_numerize:N',  # Exibir o valor formatado da coluna 'Visitantes'
            color=alt.value('black')
        )

        # Combinar o gráfico de barras com os textos
        grafico_final = grafico + text

        # Exibir o gráfico no Streamlit
        st.altair_chart(grafico_final, use_container_width=True)
    except Exception as e:
        st.error(f"Erro: {e}")
        return None

def boxplot_turistas_ano(df):
    # Criar o Box Plot para comparar a variação dos visitantes ao longo dos anos
    box_plot = alt.Chart(df).mark_boxplot(extent='min-max').encode(
        x=alt.X('País:N', title='País'),  # Eixo X com os Países
        y=alt.Y('Total:Q', title='Total de Visitantes'),  # Eixo Y com os visitantes totais
        color='País:N',  # Cor por País
        tooltip=[alt.Tooltip('País:N', title='País'),
                alt.Tooltip('Total:Q', title='Total de Visitantes')]
    ).properties(
        width=600,
        height=450,
    )

    # Exibir o Box Plot no Streamlit
    st.altair_chart(box_plot, use_container_width=True)


def bar_chart_regioes(df):
    df_continente = df.groupby('Continente').sum()
    # Selecionar apenas as colunas dos meses
    meses = ['Janeiro', 'Fevereiro', 'Março', 'Abril', 'Maio', 'Junho', 'Julho', 'Agosto', 'Setembro', 'Outubro', 'Novembro', 'Dezembro']
    # Resetar o índice para o Altair funcionar
    df_continente = df_continente.reset_index()
    # Aplicar numerize à coluna 'Total'
    df_continente['Total_numerize'] = df_continente['Total'].apply(numerize)
    df_continente['Total_formatado'] = df_continente['Total'].apply(lambda x: f'{x:,.0f}'.replace(',', '.'))
    # Criar gráfico com Altair
    # Criar gráfico com Altair
    grafico = alt.Chart(df_continente).mark_bar().encode(
        x=alt.X('Continente:N', title='Região', sort='-y'),
        y=alt.Y('Total:Q', title='Total de Visitantes'),
        color='Continente:N',
        tooltip=[
        alt.Tooltip('Continente:N', title='Região'), 
        alt.Tooltip('Total_formatado:N', title='Total de Visitantes')  # Formatação de milhares
        ]   
    ).properties(
        width=600,
        height=450
    )

    # Adicionar os valores sobre as barras com cor preta
    text = grafico.mark_text(
        align='center',
        baseline='middle',
        dy=-10  # Desloca o texto um pouco acima da barra
    ).encode(
        text='Total_numerize:N',  # Exibir o valor da coluna 'Total'
        color=alt.value('black')
    )

    # Combinar o gráfico de barras com os textos
    grafico_final = grafico + text

    # Exibir o gráfico no Streamlit
    st.altair_chart(grafico_final, use_container_width=True)


def scatter_plot(df):
    # Aplicar numerize à coluna 'Total' para formatar grandes números
        df['Total_numerize'] = df['Total'].apply(numerize)

        # Criar uma coluna com o total formatado para exibir no tooltip
        df['Total_formatado'] = df['Total'].apply(lambda x: f'{x:,.0f}'.replace(',', '.'))

        # Transformar o DataFrame para derreter as colunas de meses
        df_long = df.melt(id_vars=['País', 'Ano', 'Total', 'Total_numerize', 'Total_formatado'], 
                        value_vars=['Janeiro', 'Fevereiro', 'Março'],
                        var_name='Mês', value_name='Visitantes')

        # Criar scatter plot (gráfico de dispersão) agrupado por Ano e País
        scatter_plot = alt.Chart(df_long).mark_circle(size=80).encode(
            x=alt.X('Total:Q', title='Total de Visitantes Anual', scale=alt.Scale(zero=False)),
            y=alt.Y('Visitantes:Q', title='Visitantes Mensais', scale=alt.Scale(zero=False)),
            color=alt.Color('País:N', legend=alt.Legend(title="País")),  # Cor por País
            shape='Mês:N',  # Diferenciar os pontos por Mês
            tooltip=[alt.Tooltip('País:N', title='País'),
                    alt.Tooltip('Ano:O', title='Ano'),
                    alt.Tooltip('Mês:N', title='Mês'),
                    alt.Tooltip('Total_formatado:N', title='Total de Visitantes Anual'),
                    alt.Tooltip('Visitantes:Q', title='Visitantes Mensais')]
        ).properties(
            width=600,
            height=450,
        )

        # Exibir o scatter plot no Streamlit
        st.altair_chart(scatter_plot, use_container_width=True)


def line_chart(df):
    df['Total_numerize'] = df['Total'].apply(numerize)

    # Criar uma coluna com o total formatado para exibir no tooltip
    df['Total_formatado'] = df['Total'].apply(lambda x: f'{x:,.0f}'.replace(',', '.'))

    # Transformar o DataFrame para derreter as colunas de meses
    df_long = df.melt(id_vars=['País', 'Ano', 'Total', 'Total_numerize', 'Total_formatado'], 
                    value_vars=['Janeiro', 'Fevereiro', 'Março', 'Abril', 'Maio', 'Junho', 'Julho', 'Agosto', 'Setembro', 'Outubro', 'Novembro', 'Dezembro'],
                    var_name='Mês', value_name='Visitantes')

    # Gráfico de linhas para mostrar a variação ao longo dos anos
    line_chart = alt.Chart(df_long).mark_line(point=True).encode(
        x=alt.X('Ano:O', title='Ano', scale=alt.Scale(zero=False)),  # Ano no eixo X
        y=alt.Y('Visitantes:Q', title='Visitantes por Mês', scale=alt.Scale(zero=False)),  # Visitantes no eixo Y
        color=alt.Color('País:N', legend=alt.Legend(title="País")),  # Cor por País
        strokeDash='Mês:N',  # Traçado da linha por Mês (diferente por mês)
        tooltip=[alt.Tooltip('País:N', title='País'),
                alt.Tooltip('Ano:O', title='Ano'),
                alt.Tooltip('Mês:N', title='Mês'),
                alt.Tooltip('Visitantes:Q', title='Visitantes')]
    ).properties(
        width=600,
        height=450
    )

    # Exibir o gráfico de linhas no Streamlit
    st.altair_chart(line_chart, use_container_width=True)


def save_csv(df_csv):
    with st.expander('Dados Brutos'):
        df_csv = df_csv.reset_index(drop=True)
        st.dataframe(df_csv)
        col4 = st.columns([0.3,0.6,0.3])
        with col4[1]:
            try:
                # Botão para download
                csv = convert_to_csv(df_csv)
                st.download_button(
                    label='Clique para baixar o CSV',
                    data=csv,
                    file_name='dados_filtrados.csv',
                    mime='text/csv',
                    use_container_width=True,
                )
            except:
                pass

from functions.other_functions import banner

def main():
    altura_entre_graficos = 'h7'
    
    banner()
    df = load_df()
    
    df= sidebar(df)
    try:
        df_csv = df.copy()
    except:
        pass
    customizacao()
    cabeçalho()
    
    
    if st.session_state['mostrarcoluna'] == True:
        progress_text = "Operação em progresso. Por favor, aguarde."
        my_bar = st.progress(0, text=progress_text)
        
        for percent_complete in range(100):
            import time
            time.sleep(0.01)
            my_bar.progress(percent_complete + 1, text=progress_text)
        time.sleep(1)
        my_bar.empty()
        
        
        
        metricas(df)
        
        mkd_text('', level='subheader', position='center')
        mkd_text_divider('Visualizações', level='subheader', position='center')
        
        continente = df['Continente'].unique()
        ano_menor = df['Ano'].min()
        ano_maior = df['Ano'].max()
        
        tab1, tab2 = st.tabs(['Análise Tipo 1 - Básico', 'Análise Tipo 2 - Insights'])
        with tab1:
            mkd_text(f'Número de Turistas por Mês ({continente[0]} | {ano_menor} ~ {ano_maior})', level='h5', position='center')
            paises = str(df['País'].unique()).replace("' '",", ").replace("['","").replace("']","")
            mkd_paragraph(f'<strong>Países: </strong>{paises}', position='center')
            bar_chart_turistas_mes(df)
            mkd_text('', level=altura_entre_graficos)
            
            mkd_text(f'Variação de Visitantes Mensais ao Longo dos Anos por País <br>({continente[0]} | {ano_menor} ~ {ano_maior})', level='h5', position='center')
            line_chart(df)
            mkd_text('', level=altura_entre_graficos)
        with tab2:
            mkd_text(f'Número de Turistas por Região ao longo dos Anos <br>({continente[0]} | {ano_menor} ~ {ano_maior})', level='h5', position='center')
            boxplot_turistas_ano(df)
            mkd_text('', level=altura_entre_graficos)
            
            mkd_text(f'Relação entre Total de Visitantes Anual e Visitantes Mensais por País <br>({continente[0]} | {ano_menor} ~ {ano_maior})', level='h5', position='center')
            scatter_plot(df)
            mkd_text('', level=altura_entre_graficos)
        
        
        
        
        
        
        
        save_csv(df_csv)
        
        

    
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
    main()
    
    
    
    
    