import streamlit as st
import pandas as pd
import altair as alt

def grafico_2():

    data = pd.read_csv(r'C:\GN_Analitycs_WEB\arquivos\resultado_cluster.csv',delimiter=';')
    data['Index'] = data['Index'].str.rstrip('%').astype(int)

    data = data[['Index', 'Clusters']]
    data['Index'] = data['Index'] / 100
    data = data.drop(data[data['Clusters'] == 'Total'].index)

    print(data)

    chart = alt.Chart(data).mark_bar().encode(
        x=alt.X('Clusters', sort=['Grupo1', 'Grupo2', 'Grupo3', 'Grupo4']),
        y='Index',
        color=alt.value('blue')
    ).properties(
        width=700,
        height=500,
        title=''
    )

    # Adicionar os rótulos com os percentuais
    text = chart.mark_text(
        align='center',
        baseline='bottom',
        dy=-5  # ajuste para posicionar o rótulo acima da barra
    ).encode(
        text=alt.Text('Index:Q', format='.0%')
    )

    # Mostrar o gráfico no Streamlit
    st.altair_chart(chart + text, use_container_width=True)