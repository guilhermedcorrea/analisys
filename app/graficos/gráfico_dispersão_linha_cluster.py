import streamlit as st
import altair as alt
import pandas as pd

def grafico_clus():
    data = pd.read_csv(r'C:\GN_Analitycs_WEB\arquivos\resultado_cluster.csv',delimiter=';')

    data['%Vendas'] = data['%Vendas'].str.rstrip('%')
    data['%Vendas_graph'] = data['%Vendas'].shift(1).fillna(0).astype(float)

    for i in range(2, data.shape[0]):
        data.at[i, '%Vendas_graph'] = data.at[i - 1, '%Vendas_graph'] + float(data.at[i-1, '%Vendas'])

    data['%Qtde'] = data['%Qtde'].str.rstrip('%')
    data['%Qtde_graph'] = data['%Qtde'].shift(1).fillna(0).astype(float)

    for i in range(2, data.shape[0]):
        data.at[i, '%Qtde_graph'] = data.at[i - 1, '%Qtde_graph'] + float(data.at[i-1, '%Qtde'])

    data['%Qtde_graph'] = data['%Qtde_graph'].round()

    data = data[['%Vendas_graph', '%Qtde_graph']]
    print(data)

    # Define o gráfico para %vendas
    vendas_chart = alt.Chart(data).mark_line(point=True).encode(
        x=alt.X('%Qtde_graph:Q', axis=alt.Axis(tickCount=10)),  # alterado
        y='%Vendas_graph:Q',
        color=alt.value('blue')
    )

    # Adiciona os rótulos suaves para %vendas
    vendas_text = vendas_chart.mark_text(
        align='left',
        baseline='middle',
        dx=7
    ).encode(
        text=alt.Text('%Vendas_graph:Q', format='.1f')
    )

    # Define o gráfico para %qtde
    qtde_chart = alt.Chart(data).mark_line(point=True).encode(
        x=alt.X('%Qtde_graph:Q', axis=alt.Axis(tickCount=10)),  # alterado
        y='%Qtde_graph:Q',
        color=alt.value('red')
    )

    # Adiciona os rótulos suaves para %qtde
    qtde_text = qtde_chart.mark_text(
        align='left',
        baseline='middle',
        dx=7
    ).encode(
        text=alt.Text('%Qtde_graph:Q', format='.1f')
    )

    # Combina os dois gráficos e os rótulos
    final_chart = (vendas_chart + vendas_text+ qtde_chart + qtde_text).properties(
        width=300,
        height=300
    )

    # Exibe o gráfico no Streamlit
    st.altair_chart(final_chart, use_container_width=True)