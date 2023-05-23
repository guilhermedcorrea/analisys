def particiona(arquivo,particionamento):

    import pandas as pd
    from sklearn.model_selection import train_test_split

    df = pd.read_csv(arquivo,delimiter=';',encoding='latin1')

    if particionamento =='30%':
        particionamento_1 = 0.7
        particionamento_2 = 0.7
        opcao = 'validação'

    if particionamento =='70%':
        particionamento_1 = 0.3
        particionamento_2 = 0.3
        opcao = 'construção'

    df_vendas_1 = df[df['VENDAS'] == 1]
    df_vendas_0 = df[df['VENDAS'] == 0]

    train_vendas_1, test_vendas_1 = train_test_split(df_vendas_1, test_size=particionamento_1)
    train_vendas_0, test_vendas_0 = train_test_split(df_vendas_0, test_size=particionamento_2)

    modelo_de_treino = pd.concat([train_vendas_1, train_vendas_0])

    modelo_de_teste = pd.concat([test_vendas_1, test_vendas_0])

    ones = modelo_de_treino[modelo_de_treino['VENDAS'] == 1]
    zeros = modelo_de_treino[modelo_de_treino['VENDAS'] == 0].iloc[:len(ones) * 4, :]

    if opcao =='construção':
        modelo_de_treino.to_csv(r'C:\GN_Analitycs_WEB\arquivos\modelo_construção.csv',sep=';',index=None)
        base_balanceada_80_20_construcao = pd.concat([ones, zeros])
        base_balanceada_80_20_construcao.to_csv(r'C:\GN_Analitycs_WEB\arquivos\base_balanceada_80_20_construcao.csv', sep=';',index=None)


    else:
        modelo_de_treino.to_csv(r'C:\GN_Analitycs_WEB\arquivos\modelo_validação.csv',sep=';',index=None)
        base_balanceada_80_20_validação = pd.concat([ones, zeros])
        base_balanceada_80_20_validação.to_csv(r'C:\GN_Analitycs_WEB\arquivos\base_balanceada_80_20_validação.csv', sep=';',index=None)


    ones = modelo_de_treino[modelo_de_treino['VENDAS'] == 1]
    zeros = modelo_de_treino[modelo_de_treino['VENDAS'] == 0].iloc[:len(ones) * 1, :]

    if opcao == 'construção':
        modelo_de_treino.to_csv(r'C:\GN_Analitycs_WEB\arquivos\modelo_construção.csv',sep=';',index=None)
        base_balanceada_80_20_construcao = pd.concat([ones, zeros])
        base_balanceada_80_20_construcao.to_csv(r'C:\GN_Analitycs_WEB\arquivos\base_balanceada_50_50_construcao.csv', sep=';',index=None)


    else:
        modelo_de_treino.to_csv(r'C:\GN_Analitycs_WEB\arquivos\modelo_validação.csv',sep=';',index=None)
        base_balanceada_80_20_validação = pd.concat([ones, zeros])
        base_balanceada_80_20_validação.to_csv(r'C:\GN_Analitycs_WEB\arquivos\base_balanceada_50_50_validação.csv', sep=';',index=None)


    ones = modelo_de_treino[modelo_de_treino['VENDAS'] == 1]
    zeros = modelo_de_treino.loc[modelo_de_treino['VENDAS'] == 0].iloc[:int(len(ones) * 2.33), :]


    if opcao == 'construção':
        modelo_de_treino.to_csv(r'C:\GN_Analitycs_WEB\arquivos\modelo_construção.csv',sep=';',index=None)
        base_balanceada_80_20_construcao = pd.concat([ones, zeros])
        base_balanceada_80_20_construcao.to_csv(r'C:\GN_Analitycs_WEB\arquivos\base_balanceada_70_30_construcao.csv', sep=';',index=None)


    else:
        modelo_de_treino.to_csv(r'C:\GN_Analitycs_WEB\arquivos\modelo_validação.csv',sep=';',index=None)
        base_balanceada_80_20_validação = pd.concat([ones, zeros])
        base_balanceada_80_20_validação.to_csv(r'C:\GN_Analitycs_WEB\arquivos\base_balanceada_70_30_validação.csv', sep=';',index=None)