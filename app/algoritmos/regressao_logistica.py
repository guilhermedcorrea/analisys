import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import accuracy_score
import os
import streamlit as st
import numpy as np

def regressao_logistica(construcao,validacao):

    opcao_escolhida = pd.read_csv(r'C:\GN_Analitycs_WEB\arquivos\selecao.csv',delimiter=';')

    df = pd.read_csv(r'C:\GN_Analitycs_WEB\arquivos\base_original_importada.csv',delimiter=';',encoding='latin1')
    qtd_total = len(df)
    flag_resposta_0 = len(df['VENDAS'][df['VENDAS'] == 0])
    flag_resposta_1 = len(df['VENDAS'][df['VENDAS'] == 1])
    retornar_0_em_percentual = flag_resposta_0 / qtd_total
    retornar_1_em_percentual = flag_resposta_1 / qtd_total
    construcao = pd.read_csv(construcao,
                     delimiter=';')
    validacao = pd.read_csv(validacao,delimiter=';')

    base_original = pd.read_csv(r'C:\GN_Analitycs_WEB\arquivos\base_aprovada_final_woe_0_02.csv',delimiter=';')

    for col in construcao.columns:
        if construcao[col].dtype == "object":
            le = LabelEncoder()
            construcao.loc[:, col] = le.fit_transform(construcao[col])

    for col in validacao.columns:
        if validacao[col].dtype == "object":
            le = LabelEncoder()
            validacao.loc[:, col] = le.fit_transform(validacao[col])

    for col in base_original.columns:
        if base_original[col].dtype == "object":
            le = LabelEncoder()
            # base_original.loc[:, col] = le.fit_transform(base_original[col]) (comentado para parte melhorada)
            base_original.loc[:, col] = le.fit_transform(pd.to_numeric(base_original[col], errors='coerce'))

    train = construcao
    test = validacao
    original = base_original


    X_train = train.drop("VENDAS", axis=1)
    y_train = train["VENDAS"]

    X_test = test.drop("VENDAS", axis=1)
    y_test = test["VENDAS"]

    X_test2 = original.drop("VENDAS", axis=1)
    y_test2 = original["VENDAS"]

    model = LogisticRegression(random_state=42)
    model.fit(X_train, y_train)

    y_pred = model.predict(X_train)
    y_pred_test = model.predict(X_test)
    y_pred_original = model.predict(X_test2)

    y_probs_train = model.predict_proba(X_train)
    y_probs_test = model.predict_proba(X_test)
    y_probs_original = model.predict_proba(X_test2)

    accuracy = accuracy_score(y_train, y_pred)
    accuracy_test = accuracy_score(y_test, y_pred_test)
    accuracy_orig = accuracy_score(y_test2, y_pred_original)

    train["probabilidade"] = [p[1] for p in y_probs_train]

    test["probabilidade"] = [p[1] for p in y_probs_test]

    original["probabilidade"] = [p[1] for p in y_probs_original]

    if opcao_escolhida['opcao'][0] =='50%50':
        fator_ajuste = np.array([retornar_0_em_percentual/0.5, retornar_1_em_percentual/0.5])
        y_pred_ajustado = y_probs_original * fator_ajuste
        y_pred_ajustado /= np.sum(y_pred_ajustado, axis=1, keepdims=True)
        original["y_pred_ajustado"] = [p[1] for p in y_pred_ajustado]
    if opcao_escolhida['opcao'][0] =='70%30':
        fator_ajuste = np.array([retornar_0_em_percentual/0.7, retornar_1_em_percentual/0.3])
        y_pred_ajustado = y_probs_original * fator_ajuste
        y_pred_ajustado /= np.sum(y_pred_ajustado, axis=1, keepdims=True)
        original["y_pred_ajustado"] = [p[1] for p in y_pred_ajustado]
    if opcao_escolhida['opcao'][0] =='80%20':
        fator_ajuste = np.array([retornar_0_em_percentual/0.8, retornar_1_em_percentual/0.2])
        y_pred_ajustado = y_probs_original * fator_ajuste
        y_pred_ajustado /= np.sum(y_pred_ajustado, axis=1, keepdims=True)
        original["y_pred_ajustado"] = [p[1] for p in y_pred_ajustado]

    if opcao_escolhida['opcao'][0] =='Sem balanceamento':
        fator_ajuste = np.array([retornar_0_em_percentual / 0.99, retornar_1_em_percentual / 0.01])
        y_pred_ajustado = y_probs_original * fator_ajuste
        y_pred_ajustado /= np.sum(y_pred_ajustado, axis=1, keepdims=True)
        original["y_pred_ajustado"] = [p[1] for p in y_pred_ajustado]


    train.to_csv(r'C:\GN_Analitycs_WEB\arquivos\construcao_regressao.csv',sep=';',encoding='latin1',index=None)
    test.to_csv(r'C:\GN_Analitycs_WEB\arquivos\validacao_regressao.csv',sep=';',encoding='latin1',index=None)
    original.to_csv(r'C:\GN_Analitycs_WEB\arquivos\original_regressao.csv',sep=';',encoding='latin1',index=None)

    st.title("Modelo 1:")
    st.write("Acuracia do modelo de construção é: {:.2f}%".format(accuracy * 100))
    st.write("Acuracia do modelo de validação é: {:.2f}%".format(accuracy_test * 100))
    st.write("Acuracia do modelo original é: {:.2f}%".format(accuracy_orig * 100))