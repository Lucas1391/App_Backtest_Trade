#FUNÇÃO PARA BACKTEST INDIVIDUAL
import numpy as np
import pandas as pd
from datetime import datetime
import yfinance as yf
import pandas_ta as ta

#===========================================PROGRAMA AQUI=================================================
#FUNÇÃO QUE CÁLCULA MÉTRICAS
def Metricas(resultado,ativo):
        #alocando resultado da operação
        resultado = resultado.dropna()
        resultado['resultado']=resultado['Price_Sell']-resultado['Price_Buy']
        #Definindo capital inicial
        capital_inicial = 1000.00
        #Calculando quantidade de ações para comprar com capital disponivel
        resultado['qtnd de ações'] = capital_inicial/resultado['Price_Buy']
        #retirando parte inteira da quantidade de ações
        resultado['qtnd de ações'] = resultado['qtnd de ações'].apply(lambda x: int(x))
        #definindo vetor quantidade de operações
        resultado_operações = resultado['qtnd de ações']*resultado['resultado']
        #contruindo metricas estatísticas
        resultado['result'] =  resultado['resultado']*resultado['qtnd de ações']
        resultado['acumulado'] = resultado['result'].cumsum() + capital_inicial
        #coluna losses
        resultado['losses'] = np.where(resultado['resultado'] < 0,resultado['resultado'], np.nan)
        #coluna Gains
        resultado['gains'] = np.where(resultado['resultado'] > 0,resultado['resultado'], np.nan)
        #contagem gains
        gains=resultado['gains'].count()
        #contagem loss
        loss=resultado['losses'].count()
        resultado['duração trade'] = resultado['i_Sell']-resultado['i_Buy'] 
        print(resultado['acumulado'])
        #Número de Trades
        numb_trades=(len(resultado))
        #media gains
        avg_gains=resultado['gains'].mean()
        #media loss
        avg_loss=resultado['losses'].mean()
        #payolf
        payoff=abs(avg_gains/avg_loss)
        #Taxa de Acerto
        tx_acert=gains/numb_trades
        #Expectativa matemática
        porcentagem_operação = 100*(resultado['resultado']/resultado['Price_Sell'])
        exp_mat = porcentagem_operação.mean()
        #Capital Final
        Capital_Final = resultado['acumulado'].iloc[-1]

        #Expectativa matemática total
        exp_mat_total =  100*((Capital_Final - capital_inicial)/capital_inicial)
        Tabela_Resultados = {}
        Tabela_Resultados.update({'Código':ativo,
                            'Nº Trades':numb_trades,
                            'Duração máxima dos Trade':int(resultado['duração trade'].max()),                    
                            'Duração média dos Trade':int(resultado['duração trade'].mean()),
                            'Estimativa trades por mês':numb_trades/60.00,
                            'Tx Acerto':100.00*(tx_acert),
                            'Media Loss':resultado['losses'].mean(),
                            'Media Gain':resultado['gains'].mean(),
                            'Payoff':payoff,
                            'Ex_Mat':exp_mat,
                            'Exp_Mat total':exp_mat_total})
 
        return Tabela_Resultados
#===========================================FUNÇÃO BANDAS BOLINGER=================================================
def backtest_BandasBollinger(ativo,stop,desvio,periodo):
        #Definindo ativo e o periodo de backtest
        df = yf.download(ativo,period='5y')
        #Cálculando as métricas necessárias
        df['Std'] = df['Close'].rolling(periodo).std()
        df['M_BB'] = df['Close'].rolling(periodo).mean()
        df['L_BB'] = df['M_BB'] - df['Std'] * desvio
        #Definindo função para compras 
        def podeComprar(indice,dados):
            if (dados['Close'][indice] < dados['L_BB'][indice-1]):
                return True
            return False
        #Definindo função para vender na máxima dos dois ultimos candles
        def podeVender(indice,dados):
            if (dados['L_BB'][indice-1] < dados['Close'][indice]): 
                return True
            return False   
                #Listas de compras
        resultado = []
        #listas de vendas
        resultado_vendas=[]
        #tamanho do Dataframe
        tam = len(df)
        #parametro boleano para não comprar duas veses seguidas
        flag_compra = False
        #marcação do ultima dia compra
        dia_ultima_compra=0
        #laço de repetição para gerar compras e vendas
        #lista de compras 
        for i in range(periodo,tam):
            if (podeComprar(i,df)) and (not flag_compra):
                linha = [df.index[i],i,df['Close'][i]]
                resultado.append(linha)
                flag_compra = True
                dia_ultima_compra=i
            #lista de vendas 
            elif (podeVender(i,df)) and (flag_compra):
                linha1 = [df.index[i],i,df['Close'][i]]
                resultado_vendas.append(linha1)
                flag_compra = False

            elif ((i-dia_ultima_compra)==stop) and (flag_compra):
                linha1 = [df.index[i],i,df['Close'][i]]
                resultado_vendas.append(linha1)
                flag_compra = False  

        #contruindo colunas do data frame   
        COLUNAS = ["Date_Buy",'i_Buy',"Price_Buy"]
        COLUNAS1 = ["Date","Atitude","Preço"]

        #data frame de compras
        resultado = pd.DataFrame(resultado,columns = COLUNAS)
        #data frame de vendas
        resultado_venda = pd.DataFrame(resultado_vendas,columns=COLUNAS1)
        #alocando resultados de vendas em data frame compra
        resultado['Date_Sell'] = resultado_venda['Date']
        resultado['i_Sell'] = resultado_venda['Atitude']
        resultado['Price_Sell'] = resultado_venda['Preço']
        if len(resultado)==1:
            resultado['Price_Sell'] = df['Close'].iloc[-1]
            data_atual = datetime.now().strftime('%Y-%m-%d')
            resultado['Date_Sell'].iloc[-1]= data_atual
            resultado['i_Sell'].iloc[-1] = resultado['i_Buy'].iloc[-1]
        Resposta = {}
        if len(resultado)==0:
            Resposta = Resposta
        else:
            Resposta = Metricas(resultado,ativo)
        return Resposta
#===========================================FUNÇAÕ QUE EXECUTADA EM MULTIPLOS ATIVOS================================================
def Main_1(stop,desvio,periodo,acoes):
    result_ativos = {}  
    for acao in acoes:
        print(acao)
        result_ativos.update({acao:backtest_BandasBollinger(acao,stop,desvio,periodo)})
    Trades = pd.DataFrame(result_ativos.values())
    return Trades

#===========================================FUNÇÃO TIKTOK=================================================
def backtest_Tiktok(ativo,stop):
        #Definindo ativo e o periodo de backtest
        df = yf.download(ativo,period='5y')
        #Cálculando as métricas necessárias
        df['Avg_Low'] = df['Low'].rolling(2).mean()
        df['Avg_High'] = df['High'].rolling(2).mean()
        #Definindo função para compras 
        def podeComprar(indice, dados):
            if (dados['Low'][indice] < dados['Avg_Low'][indice-1]):
                return True
            return False
        #Definindo função para vender em gaps
        def podeVendergap(indice, dados):
            if (dados['Avg_High'] [indice-1] < dados['Open'][indice]):
                return True
            return False

        #Definindo função para vender na máxima dos dois ultimos candles
        def podeVender(indice,dados):
            if (dados['Avg_High'][indice-1] < dados['High'][indice]): 
                return True
            return False   
                #Listas de compras
        resultado = []
        #listas de vendas
        resultado_vendas=[]
        #tamanho do Dataframe
        tam = len(df)
        #parametro boleano para não comprar duas veses seguidas
        flag_compra = False
        #marcação do ultima dia compra
        dia_ultima_compra=0
        #laço de repetição para gerar compras e vendas
        #lista de compras 
        for i in range(2,tam):
            if (podeComprar(i,df)) and (not flag_compra):
                linha = [df.index[i],i,df['Avg_Low'][i-1]]
                resultado.append(linha)
                flag_compra = True
                dia_ultima_compra=i
            #lista de vendas 
            elif (podeVendergap(i,df)) and (flag_compra):
                linha1 = [df.index[i],i,df['Open'][i]]
                resultado_vendas.append(linha1)
                flag_compra = False

            elif (podeVender(i,df)) and (flag_compra):
                linha1 = [df.index[i],i,df['Avg_High'][i-1]]
                resultado_vendas.append(linha1)
                flag_compra = False

            elif ((i-dia_ultima_compra)==stop) and (flag_compra):
                linha1 = [df.index[i],i,df['Close'][i]]
                resultado_vendas.append(linha1)
                flag_compra = False  

        #contruindo colunas do data frame   
        COLUNAS = ["Date_Buy",'i_Buy',"Price_Buy"]
        COLUNAS1 = ["Date","Atitude","Preço"]

        #data frame de compras
        resultado = pd.DataFrame(resultado,columns = COLUNAS)
        #data frame de vendas
        resultado_venda = pd.DataFrame(resultado_vendas,columns=COLUNAS1)
        #alocando resultados de vendas em data frame compra
        resultado['Date_Sell'] = resultado_venda['Date']
        resultado['i_Sell'] = resultado_venda['Atitude']
        resultado['Price_Sell'] = resultado_venda['Preço']
        if len(resultado)==1:
            resultado['Price_Sell'] = df['Close'].iloc[-1]
            data_atual = datetime.now().strftime('%Y-%m-%d')
            resultado['Date_Sell'].iloc[-1]= data_atual
            resultado['i_Sell'].iloc[-1] = resultado['i_Buy'].iloc[-1]
        Resposta = {}
        if len(resultado)==0:
            Resposta = Resposta
        else:
            Resposta = Metricas(resultado,ativo)
        return Resposta

#===========================================FUNÇÃO QUE EXECUTADA BACKTEST EM VÁRIOS ATIVOS ========================================================
def Main_2(stop,acoes):
    result_ativos = {}
    for acao in acoes:
        print(acao)
        result_ativos.update({acao:backtest_Tiktok(acao,stop)})
    Trades = pd.DataFrame(result_ativos.values())
    return Trades
#===========================================FUNÇÃO IFR2========================================================
def backtest_IFR2(ativo,stop):
        #Definindo ativo e o periodo de backtest
        df = yf.download(ativo,period='5y')
        #Cálculando as métricas necessárias
        df['IFR'] = ta.rsi(df['Close'],2)
        #Calculando máxima dos dois ultimos dias
        df['highest_2'] = df['High'].rolling(2).max()
        #Definindo função para compras 
        def podeComprar(indice, dados):
            if (dados['IFR'][indice] < 25.00):
                return True
            return False
        #Definindo função para vender em gaps
        def podeVendergap(indice, dados):
            if (dados['highest_2'][indice-1] < dados['Open'][indice]):
                return True
            return False

        #Definindo função para vender na máxima dos dois ultimos candles
        def podeVender(indice,dados):
            if (dados['highest_2'][indice-1] < dados['High'][indice]): 
                return True
            return False   
                #Listas de compras
        resultado = []
        #listas de vendas
        resultado_vendas=[]
        #tamanho do Dataframe
        tam = len(df)
        #parametro boleano para não comprar duas veses seguidas
        flag_compra = False
        #marcação do ultima dia compra
        dia_ultima_compra=0
        #laço de repetição para gerar compras e vendas
        #lista de compras 
        for i in range(2,tam):
            if (podeComprar(i,df)) and (not flag_compra):
                linha = [df.index[i],i,df['Close'][i]]
                resultado.append(linha)
                flag_compra = True
                dia_ultima_compra=i
            #lista de vendas 
            elif (podeVendergap(i,df)) and (flag_compra):
                linha1 = [df.index[i],i,df['Open'][i]]
                resultado_vendas.append(linha1)
                flag_compra = False

            elif (podeVender(i,df)) and (flag_compra):
                linha1 = [df.index[i],i,df['highest_2'][i-1]]
                resultado_vendas.append(linha1)
                flag_compra = False

            elif ((i-dia_ultima_compra)==stop) and (flag_compra):
                linha1 = [df.index[i],i,df['Close'][i]]
                resultado_vendas.append(linha1)
                flag_compra = False  

        #contruindo colunas do data frame   
        COLUNAS = ["Date_Buy",'i_Buy',"Price_Buy"]
        COLUNAS1 = ["Date","Atitude","Preço"]

        #data frame de compras
        resultado = pd.DataFrame(resultado,columns = COLUNAS)
        #data frame de vendas
        resultado_venda = pd.DataFrame(resultado_vendas,columns=COLUNAS1)
        #alocando resultados de vendas em data frame compra
        resultado['Date_Sell'] = resultado_venda['Date']
        resultado['i_Sell'] = resultado_venda['Atitude']
        resultado['Price_Sell'] = resultado_venda['Preço']
        if len(resultado)==1:
            resultado['Price_Sell'] = df['Close'].iloc[-1]
            data_atual = datetime.now().strftime('%Y-%m-%d')
            resultado['Date_Sell'].iloc[-1]= data_atual
            resultado['i_Sell'].iloc[-1] = resultado['i_Buy'].iloc[-1]
        Resposta = {}
        if len(resultado)==0:
            Resposta = Resposta
        else:
            Resposta = Metricas(resultado,ativo)
        return Resposta

#===========================================FUNÇAÕ QUE EXECUTADA EM MULTIPLOS ATIVOS================================================
def Main_3(stop,acoes):
    result_ativos = {}  
    for acao in acoes:
        print(acao)
        result_ativos.update({acao:backtest_IFR2(acao,stop)})
    Trades = pd.DataFrame(result_ativos.values())
    return Trades
#===========================================FUNÇAÕ MÉDIA 3 MAXIMAS E 3 MÍNIMAS===================================
def Medias3(ativo,stop):
        #Definindo ativo e o periodo de backtest
        df = yf.download(ativo,period='5y')
        #Cálculando as métricas necessárias
        df['Avg_Low'] = df['Low'].rolling(3).mean()
        df['Avg_High'] = df['High'].rolling(3).mean()
        #Definindo função para compras 
        def podeComprar(indice,dados):
            if (dados['Close'][indice] < dados['Avg_Low'][indice-1]):
                return True
            return False
        #Definindo função para vender na máxima dos dois ultimos candles
        def podeVender(indice,dados):
            if (dados['Avg_High'][indice-1] < dados['Close'][indice]): 
                return True
            return False   
                #Listas de compras
        resultado = []
        #listas de vendas
        resultado_vendas=[]
        #tamanho do Dataframe
        tam = len(df)
        #parametro boleano para não comprar duas veses seguidas
        flag_compra = False
        #marcação do ultima dia compra
        dia_ultima_compra=0
        for i in range(3,tam):
            if (podeComprar(i,df)) and (not flag_compra):
                linha = [df.index[i],i,df['Close'][i]]
                resultado.append(linha)
                flag_compra = True
                dia_ultima_compra=i
        #lista de vendas 
            elif (podeVender(i,df)) and (flag_compra):
                linha1 = [df.index[i],i,df['Close'][i]]
                resultado_vendas.append(linha1)
                flag_compra = False  
            elif ((i-dia_ultima_compra)==stop) and (flag_compra):
                linha1 = [df.index[i],i,df['Close'][i]]
                resultado_vendas.append(linha1)
                flag_compra = False  

        #contruindo colunas do data frame   
        COLUNAS = ["Date_Buy",'i_Buy',"Price_Buy"]
        COLUNAS1 = ["Date","Atitude","Preço"]

        #data frame de compras
        resultado = pd.DataFrame(resultado,columns = COLUNAS)
        #data frame de vendas
        resultado_venda = pd.DataFrame(resultado_vendas,columns=COLUNAS1)
        #alocando resultados de vendas em data frame compra
        resultado['Date_Sell'] = resultado_venda['Date']
        resultado['i_Sell'] = resultado_venda['Atitude']
        resultado['Price_Sell'] = resultado_venda['Preço']
        if len(resultado)==1:
            resultado['Price_Sell'] = df['Close'].iloc[-1]
            data_atual = datetime.now().strftime('%Y-%m-%d')
            resultado['Date_Sell'].iloc[-1]= data_atual
            resultado['i_Sell'].iloc[-1] = resultado['i_Buy'].iloc[-1]
        Resposta = {}
        if len(resultado)==0:
            Resposta = Resposta
        else:
            Resposta = Metricas(resultado,ativo)
        return Resposta
#===========================================FUNÇAÕ QUE EXECUTADA EM MULTIPLOS ATIVOS===================================
def Main_4(stop,acoes):
    result_ativos = {}  
    for acao in acoes:
        print(acao)
        result_ativos.update({acao:Medias3(acao,stop)})
    Trades = pd.DataFrame(result_ativos.values())
    return Trades
#===============================================BACKTEST TUTLE 20 -10-==================================================
def Tutle_20_10(ativo,stop):
        #Definindo ativo e o periodo de backtest
        df = yf.download(ativo,period='5y')
        df['data'] = df.index
        #Cálculando as métricas necessárias
        df['Avg_Low'] = df['Low'].rolling(10).min()
        df['Avg_High'] = df['High'].rolling(20).max()
        #Definindo função para compras 
        def podeComprar(indice,dados):
            if (dados['Avg_High'] [indice-1] < dados['Close'][indice]):
                return True
            return False
        #Definindo função para vender na máxima dos dois ultimos candles
        def podeVender(indice,dados):
            if (dados['Close'][indice] < dados['Avg_Low'][indice-1]): 
                return True
            return False   
        #Listas de compras
        resultado = []
        #listas de vendas
        resultado_vendas=[]
        #tamanho do Dataframe
        tam = len(df)
        #parametro boleano para não comprar duas veses seguidas
        flag_compra = False
        #marcação do ultima dia compra
        dia_ultima_compra=0
        #laço de repetição para gerar compras e vendas
        #lista de compras 
        for i in range(20,tam):
            if (podeComprar(i,df)) and (not flag_compra):
                linha = [df.index[i],i,df['Close'][i]]
                resultado.append(linha)
                flag_compra = True
                dia_ultima_compra=i
        #lista de vendas 
            elif (podeVender(i,df)) and (flag_compra):
                linha1 = [df.index[i],i,df['Close'][i]]
                resultado_vendas.append(linha1)
                flag_compra = False  
            elif ((i-dia_ultima_compra)==stop) and (flag_compra):
                linha1 = [df.index[i],i,df['Close'][i]]
                resultado_vendas.append(linha1)
                flag_compra = False  
        #contruindo colunas do data frame   
        COLUNAS = ["Date_Buy",'i_Buy',"Price_Buy"]
        COLUNAS1 = ["Date","Atitude","Preço"]

        #data frame de compras
        resultado = pd.DataFrame(resultado,columns = COLUNAS)
        #data frame de vendas
        resultado_venda = pd.DataFrame(resultado_vendas,columns=COLUNAS1)
        #alocando resultados de vendas em data frame compra
        resultado['Date_Sell'] = resultado_venda['Date']
        resultado['i_Sell'] = resultado_venda['Atitude']
        resultado['Price_Sell'] = resultado_venda['Preço']
        if len(resultado)==1:
            resultado['Price_Sell'] = df['Close'].iloc[-1]
            data_atual = datetime.now().strftime('%Y-%m-%d')
            resultado['Date_Sell'].iloc[-1]= data_atual
            resultado['i_Sell'].iloc[-1] = resultado['i_Buy'].iloc[-1]
        print(resultado)
        Resposta = {}
        if len(resultado)==0:
            Resposta = Resposta
        else:
            Resposta = Metricas(resultado,ativo)
        return Resposta
#===========================================FUNÇAÕ QUE EXECUTADA EM MULTIPLOS ATIVOS===================================
def Main_5(stop,acoes):
    result_ativos = {}  
    for acao in acoes:
        print(acao)
        result_ativos.update({acao:Tutle_20_10(acao,stop)})
    Trades = pd.DataFrame(result_ativos.values())
    return Trades

#===========================================MEDIA MOVEL DE 9============================================
def Media9(ativo,stop):
        #Definindo ativo e o periodo de backtest
        #Definindo ativo e o periodo de backtest
        df = yf.download(ativo,period='5y')
        df['data'] = df.index
        df['avg_exp 9'] = df['Close'].ewm(span = 9,min_periods = 9).mean()
        #Definindo função para compras 
        def podeComprar(indice, dados):
            if (dados['avg_exp 9'][indice-1] < dados['Close'][indice]):
                return True
            return False
        #Definindo função para vender
        def podeVender(indice, dados):
            if (dados['Close'][indice] < dados['avg_exp 9'][indice-1]):
                return True
            return False
         #Listas de compras
        resultado = []
        #listas de vendas
        resultado_vendas=[]
        #tamanho do Dataframe
        tam = len(df)
        #parametro boleano para não comprar duas veses seguidas
        flag_compra = False
        #marcação do ultima dia compra
        dia_ultima_compra=0
        #laço de repetição para gerar compras e vendas
        #lista de compras 
        for i in range(9,tam):
            if (podeComprar(i,df)) and (not flag_compra):
                linha = [df.index[i],i,df['Close'][i]]
                resultado.append(linha)
                flag_compra = True
                dia_ultima_compra=i
        #lista de vendas 
            elif (podeVender(i,df)) and (flag_compra):
                linha1 = [df.index[i],i,df['Close'][i]]
                resultado_vendas.append(linha1)
                flag_compra = False  
            elif ((i-dia_ultima_compra)==stop) and (flag_compra):
                linha1 = [df.index[i],i,df['Close'][i]]
                resultado_vendas.append(linha1)
                flag_compra = False  
        #contruindo colunas do data frame   
        COLUNAS = ["Date_Buy",'i_Buy',"Price_Buy"]
        COLUNAS1 = ["Date","Atitude","Preço"]

        #data frame de compras
        resultado = pd.DataFrame(resultado,columns = COLUNAS)
        #data frame de vendas
        resultado_venda = pd.DataFrame(resultado_vendas,columns=COLUNAS1)
        #alocando resultados de vendas em data frame compra
        resultado['Date_Sell'] = resultado_venda['Date']
        resultado['i_Sell'] = resultado_venda['Atitude']
        resultado['Price_Sell'] = resultado_venda['Preço']
        if len(resultado)==1:
            resultado['Price_Sell'] = df['Close'].iloc[-1]
            data_atual = datetime.now().strftime('%Y-%m-%d')
            resultado['Date_Sell'].iloc[-1]= data_atual
            resultado['i_Sell'].iloc[-1] = resultado['i_Buy'].iloc[-1]
        print(resultado)
        Resposta = {}
        if len(resultado)==0:
            Resposta = Resposta
        else:
            Resposta = Metricas(resultado,ativo)
        return Resposta

#===========================================FUNÇÃO EXECUTADA BACKTEST EM VÁRIOS ATIVOS============================================
def Main_6(stop,acoes):
    result_ativos = {}  
    for acao in acoes:
        print(acao)
        result_ativos.update({acao:Media9(acao,stop)})
    Trades = pd.DataFrame(result_ativos.values())
    return Trades

#============================================FUNÇÃO STOP ATR=================================================================
def Stop_Atr(ativo,stop,periodo,desvio):
        #Definindo ativo e o periodo de backtest
        #Definindo ativo e o periodo de backtest
        df = yf.download(ativo,period='5y')
        df['data'] = df.index
        high_low = df['High'] - df['Low']
        high_close = np.abs(df['High'] - df['Close'].shift())
        low_close = np.abs(df['Low'] - df['Close'].shift())
        ranges = pd.concat([high_low, high_close, low_close], axis=1)
        true_range = np.max(ranges, axis=1)
        df['Atr'] = true_range.rolling(periodo).sum()/periodo
        df['STOP ATR'] = df['Close']-desvio*df['Atr']
        #Definindo função para compras 
        #Definindo função para compras 
        def podeComprar(indice,dados):
            if (dados['STOP ATR'][indice-1] < dados['Close'][indice]):
                return True
            return False
        #Definindo função para vender
        def podeVender(indice,dados):
            if (dados['Close'][indice] < dados['STOP ATR'][indice-1]):
                return True
            return False
         #Listas de compras
        resultado = []
        #listas de vendas
        resultado_vendas=[]
        #tamanho do Dataframe
        tam = len(df)
        #parametro boleano para não comprar duas veses seguidas
        flag_compra = False
        #marcação do ultima dia compra
        dia_ultima_compra=0
        #laço de repetição para gerar compras e vendas
        #lista de compras 
        for i in range(period,tam):
            if (podeComprar(i,df)) and (not flag_compra):
                linha = [df.index[i],i,df['Close'][i]]
                resultado.append(linha)
                flag_compra = True
                dia_ultima_compra=i
        #lista de vendas 
            elif (podeVender(i,df)) and (flag_compra):
                linha1 = [df.index[i],i,df['Close'][i]]
                resultado_vendas.append(linha1)
                flag_compra = False  
            elif ((i-dia_ultima_compra)==stop) and (flag_compra):
                linha1 = [df.index[i],i,df['Close'][i]]
                resultado_vendas.append(linha1)
                flag_compra = False  
        #contruindo colunas do data frame   
        COLUNAS = ["Date_Buy",'i_Buy',"Price_Buy"]
        COLUNAS1 = ["Date","Atitude","Preço"]

        #data frame de compras
        resultado = pd.DataFrame(resultado,columns = COLUNAS)
        #data frame de vendas
        resultado_venda = pd.DataFrame(resultado_vendas,columns=COLUNAS1)
        #alocando resultados de vendas em data frame compra
        resultado['Date_Sell'] = resultado_venda['Date']
        resultado['i_Sell'] = resultado_venda['Atitude']
        resultado['Price_Sell'] = resultado_venda['Preço']
        if len(resultado)==1:
            resultado['Price_Sell'] = df['Close'].iloc[-1]
            data_atual = datetime.now().strftime('%Y-%m-%d')
            resultado['Date_Sell'].iloc[-1]= data_atual
            resultado['i_Sell'].iloc[-1] = resultado['i_Buy'].iloc[-1]
        print(resultado)
        Resposta = {}
        if len(resultado)==0:
            Resposta = Resposta
        else:
            Resposta = Metricas(resultado,ativo)
        return Resposta
#===========================================FUNÇÃO EXECUTADA BACKTEST EM VÁRIOS ATIVOS============================================
def Main_7(stop,acoes,periodo,desvio):
    result_ativos = {}  
    for acao in acoes:
        print(acao)
        result_ativos.update({acao:Stop_Atr(acao,stop,periodo,desvio)})
    Trades = pd.DataFrame(result_ativos.values())
    return Trades
#======================================================Open True Range==============================================================
def OpenTrueRange(ativo,periodo,desvio):
    #dados
  def OpenTrueRange(ativo,periodo,desvio):
    #dados
    df = yf.download(ativo,period='5y')
    #Cálculo do indicador Open-Atr
    high_low = df['High'] - df['Low']
    high_close = np.abs(df['High'] - df['Close'].shift())
    low_close = np.abs(df['Low'] - df['Close'].shift())
    ranges = pd.concat([high_low, high_close, low_close], axis=1)
    true_range = np.max(ranges, axis=1)
    df['atr'] = (true_range.rolling(periodo).sum())/periodo
    df['open-atr'] = df['Open'] -desvio*df['atr']
    df['Price_Buy'] = np.where(df['Low'] <  df['open-atr'],df['open-atr'],np.NaN)
    df['Price_Sell'] = df['Close']
    df['i_Buy'] =  df.index
    df['i_Sell'] =  df.index
    return df

#==========================================================FUNÇÃO EXECUTA BACKTEST EM VÁRIOS ATIVOS====================================
def Main_8(desvio,periodo,acoes):
    result_ativos = {}  
    for acao in acoes:
        print(acao)
        result_ativos.update({acao:OpenTrueRange(ativo,periodo,desvio)})
    Trades = pd.DataFrame(result_ativos.values())
    return Trades
#=====================================================Gambit============================================================================
def Gambit(ativo,periodo,desvio):
    #dados
    df = yf.download(ativo,period='5y')
    df['data'] = df.index
    df['lowest'] = df['low'].rolling(periodo).min()
    df['lowest'] = df['lowest'].shift(1)
    desvio = 1 - desvio
    df['lowest- Queda'] = df['lowest']*desvio   
    Price_Buy = np.where(df['Low'] < df['lowest- Queda'],df['lowest- Queda'],np.NaN)
    Price_Sell = df['Close']
    colunas = ["Price_Buy","Price_Sell",'i_Buy',"i_Sell"]
    resultado = pd.DataFrame(columns = colunas)
    resultado["Price_Buy"] = Price_Buy 
    resultado["Price_Sell"] = Price_Sell
    resultado['i_Buy'] = df['data']
    resultado['i_Sell'] = df['data'] 
    return resultado
#======================================================FUNÇÃO EXECUTA EM VÁRIOS ATIVOS====================================================
def Main_9(desvio,periodo,acoes):
    result_ativos = {}  
    for acao in acoes:
        print(acao)
        result_ativos.update({acao:Gambit(ativo,periodo,desvio)})
    Trades = pd.DataFrame(result_ativos.values())
    return Trades

