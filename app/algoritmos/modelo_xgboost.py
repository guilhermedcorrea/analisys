import xgboost as xgb
import pandas as pd
import streamlit as st
from sklearn.preprocessing import LabelEncoder
import numpy as np

def modelo_xg(construcao,validacao):

    #df_bcu =pd.read_csv(r'C:\GN_Analitycs_WEB\arquivos\base_construcao_usar.csv')
    #construcao = df_bcu['base_construcao_usar'][0]
    #validacao = df_bcu['base_construcao_usar'][0]
    opcao_escolhida = pd.read_csv(r'C:\GN_Analitycs_WEB\arquivos\selecao.csv',delimiter=';')

    df = pd.read_csv(r'C:\GN_Analitycs_WEB\arquivos\base_original_importada.csv',delimiter=';',encoding='latin1')
    qtd_total = len(df)
    flag_resposta_0 = len(df['VENDAS'][df['VENDAS'] == 0])
    flag_resposta_1 = len(df['VENDAS'][df['VENDAS'] == 1])
    retornar_0_em_percentual = flag_resposta_0 / qtd_total
    retornar_1_em_percentual = flag_resposta_1 / qtd_total

    construcao = pd.read_csv(construcao,delimiter=';',encoding='latin1')
    validacao = pd.read_csv(validacao,delimiter=';',encoding='latin1')
    original = pd.read_csv(r'C:\GN_Analitycs_WEB\arquivos\base_aprovada_final_woe_0_02.csv',delimiter=';')

    for col in construcao.columns:
        if construcao[col].dtype == "object":
            le = LabelEncoder()
            construcao.loc[:, col] = le.fit_transform(construcao[col])

    for col in validacao.columns:
        if validacao[col].dtype == "object":
            le = LabelEncoder()
            validacao.loc[:, col] = le.fit_transform(validacao[col])

    for col in original.columns:
        if original[col].dtype == "object":
            le = LabelEncoder()
            original.loc[:, col] = le.fit_transform(original[col])

    X1 = construcao.drop("VENDAS", axis=1)
    y1 = construcao["VENDAS"]

    X2 = validacao.drop("VENDAS", axis=1)
    y2 = validacao["VENDAS"]

    X3 = original.drop("VENDAS", axis=1)
    y3 = original["VENDAS"]

    X_train = X1
    y_train = y1
    X_test = X2
    y_test = y2
    X_origin = X3
    y_origin = y3

    random_state = 42

    # Cria a instância do modelo com o argumento random_state definido
    modelxgb = xgb.XGBClassifier(n_estimators=50, max_depth=3, learning_rate=0.1, subsample=0.7, eta=0.3, random_state=random_state)
    modelxgb.fit(X_train, y_train)

    # Avaliar o modelo
    scorexgb = modelxgb.score(X_train, y_train)
    score2xgb = modelxgb.score(X_test, y_test)
    score3xgb = modelxgb.score(X_origin, y_origin)
    dict_result_xgb = {'construcao': ["{:.2}".format(scorexgb)],
                          'validacao': ["{:.2}".format(score2xgb)],
                          'original': ["{:.2}".format(score3xgb)]}
    df_result_xgb = pd.DataFrame.from_dict(dict_result_xgb)

    y_probs_train = modelxgb.predict_proba(X_train)
    y_probs_test = modelxgb.predict_proba(X_test)
    y_probs_ori = modelxgb.predict_proba(X_origin)

    construcao["probabilidade"] = [p[1] for p in y_probs_train]

    validacao["probabilidade"] = [p[1] for p in y_probs_test]

    original["probabilidade"] = [p[1] for p in y_probs_ori]

    if opcao_escolhida['opcao'][0] =='50%50':
        fator_ajuste = np.array([retornar_0_em_percentual/0.5, retornar_1_em_percentual/0.5])
        y_pred_ajustado = y_probs_ori * fator_ajuste
        y_pred_ajustado /= np.sum(y_pred_ajustado, axis=1, keepdims=True)
        original["y_pred_ajustado"] = [p[1] for p in y_pred_ajustado]
    if opcao_escolhida['opcao'][0] =='70%30':
        fator_ajuste = np.array([retornar_0_em_percentual/0.7, retornar_1_em_percentual/0.3])
        y_pred_ajustado = y_probs_ori * fator_ajuste
        y_pred_ajustado /= np.sum(y_pred_ajustado, axis=1, keepdims=True)
        original["y_pred_ajustado"] = [p[1] for p in y_pred_ajustado]
    if opcao_escolhida['opcao'][0] =='80%20':
        fator_ajuste = np.array([retornar_0_em_percentual/0.8, retornar_1_em_percentual/0.2])
        y_pred_ajustado = y_probs_ori * fator_ajuste
        y_pred_ajustado /= np.sum(y_pred_ajustado, axis=1, keepdims=True)
        original["y_pred_ajustado"] = [p[1] for p in y_pred_ajustado]
    if opcao_escolhida['opcao'][0] =='Sem balanceamento':
        fator_ajuste = np.array([retornar_0_em_percentual/0.99, retornar_1_em_percentual/0.01])
        y_pred_ajustado = y_probs_ori * fator_ajuste
        y_pred_ajustado /= np.sum(y_pred_ajustado, axis=1, keepdims=True)
        original["y_pred_ajustado"] = [p[1] for p in y_pred_ajustado]

    modelxgb.save_model(r"C:\GN_Analitycs_WEB\arquivos\modelo.xgb")

    construcao.to_csv(r'C:\GN_Analitycs_WEB\arquivos\construcao_com_proba_xg_boost.csv', sep=';', index=None)
    validacao.to_csv(r'C:\GN_Analitycs_WEB\arquivos\validacao_com_proba_xg_boost.csv', sep=';', index=None)
    original.to_csv(r'C:\GN_Analitycs_WEB\arquivos\original_com_proba_xg_boost.csv', sep=';', index=None)
    df_result_xgb.to_csv(r'C:\GN_Analitycs_WEB\arquivos\score_xgboost.csv', sep=';', index=False)

    st.title("Modelo 3:")
    st.write("Acuracia do modelo de construção é: {:.2%}".format(scorexgb))
    st.write("Acuracia do modelo de validação é: {:.2%}".format(score2xgb))
    st.write("Acuracia do modelo original é: {:.2%}".format(score3xgb))