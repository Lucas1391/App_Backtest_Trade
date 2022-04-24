import streamlit as st
#Instalando Pacotes
import numpy as np
import pandas as pd
import yfinance as yf
import pandas_ta as ta
from PIL import Image
from Backtest import Main_1,Main_2,Main_3,Main_4,Main_5,Main_6
import requests
import streamlit_authenticator as stauth

#===========================================PROGRAMA AQUI=================================================
#Carregando Logomarca
#Abrindo logomarca no Streamlit
#st.image(image,width=200)
#Iniciando APP

st.title("APP BACKTEST TRADE")
#Função para Carregar Ativos do SP&500
def Ativos_SP500():
    tickers = pd.read_html('https://en.wikipedia.org/wiki/List_of_S%26P_500_companies')[0]
    ativos = tickers['Symbol'].to_list()
    acoes = []
    for ativo in ativos:
        ativo = ativo.replace(".","-")
        acoes.append(ativo)
    return acoes
#Função para Carregar Ativos do SP&500
def Ativos_B3():
    tickers = pd.read_excel(r"C:\Users\Lucas\Documents\DADOS.xlsx")
    ativos = tickers['Código'].to_list()
    acoes = []
    for ativo in ativos:
        ativo = ativo + ".SA"
        acoes.append(ativo)
    return acoes
def Resultado(dados):
    DataFrame = st.dataframe(dados)
    dados = dados.to_csv()
    Mensagem = st.write("Clique no Botão abaixo e faça o Download do arquivo")
    Botao = st.download_button( label="Resultado do Backtest",file_name='Resultado.csv', data = dados)
    return DataFrame,Mensagem,Botao

st.text("I-Este App realiza backtest em ações do indice Bovespa,Brasil Amplo e SP&500")
st.text("II-O Dados são obtidos pela API do yahoo finance;")
st.text("III-Todos as operações são do tipo Swing Trade com parametros abertos;")
st.text("IV- Os backtest são realizados para um periodo dos últimos cinco anos")
names = ['Lucas Campos','Leandro Giron']
passwords = ['lucassomatoria7@gmail.com','leandro.giron@gmail.com']
usuario = st.text_input("Insira seu nome de usuário : ")
senha = st.text_input("Insira sua senha : ")
if senha:
    if usuario in names and senha in passwords:
        st.text("Seja bem Vindo ao App Backtest Trade!")
    else:
        st.write("Digite o login Novamente!")

    ACOES = [" ","AÇÕES B3","AÇÕES SP&500"]
    INDICE = st.sidebar.selectbox("Escolha a classe de ações desejada :",ACOES)
    if INDICE =='AÇÕES SP&500':
        acoes = Ativos_SP500()
    else:
        acoes = Ativos_B3()
    ESTRATEGIA = ['','BANDAS DE BOLLINGER','TIKTOK','IFR2','3MAX3MIN','TUTLE 20-10','MÉDIA 9.1','STOP ATR']
    SETUP = st.sidebar.selectbox('Escolha a estratégia desejado :',ESTRATEGIA)
    #Indicadores disponíveis
    if SETUP:
        if SETUP == ESTRATEGIA[1]:
            st.header("O Setup Bandas de Bollinger possui as seguintes regras;")
            st.text("I) Se fechamento do dia e menor do que a banda inferior compra-se o fechamento do dia")
            st.text("II) Se o fechamento do dia for superior a banda inferior vende-se o fechamento do dia")
            st.text("III) Caso queira pode-se incluir stop no tempo")
            st.text("IV-O cálculo das Bandas de Bollinger e dado pela seguinte fórmula :")
            st.text("Cálculo da Banda Superior com desvio padrão sigma para n periodos")
            st.latex(r'''BandaSuperior = \frac{\sum_{1}^{n}Close_{i}}{n} + n\sigma''')
            st.text("Cálculo da Banda Inferior com desvio padrão sigma para n periodos")
            st.latex(r'''BandaInferior = \frac{\sum_{1}^{n}Close_{i}}{n} - n\sigma''')
            stop = st.slider("Escolha o valor do stop no tempo.Caso não deseje deixe o valor zero")
            desvio = st.slider("Esolha o valor do desvio")
            periodo = st.slider("Digite o valor do periodo")
            if (periodo != 0):
                st.write("Robo Trabalhando!")
                dados = Main_1(stop,desvio,periodo,acoes)
                Resultado(dados)
                
        elif SETUP == ESTRATEGIA[2]:
            st.header("O Setup TikTtok possui as seguintes regras;")
            st.text("I) Se o preço tocar na média das ultimas 2 mínimas compra-se neste valor")
            st.text("II) Se o preço tocar a média das ultimas três máximas vende-se neste preço")
            st.text("III) Caso queira pode-se incluir stop no tempo")
            st.text("O cálculo da média móvel aritmética é dado por ;")
            st.latex(r'''\frac{\sum_{1}^{n}Close_{i}}{n}''')
            stop = st.slider("Digite o stop no tempo.Caso não deseje digite o valor zero")
            if (stop!=0)or(stop==0):
                st.write("Robo Trabalhando!")
                dados = Main_2(stop,acoes)
                Resultado(dados)

        elif SETUP==ESTRATEGIA[3]:
            st.header("O Setup do IFR2 possui as seguintes regras;")
            st.text("I) Se o valor do IFR de periodos for menor do que 25 compra-se o fechamento do dia")
            st.text("II)Alvo encontra-se na máxima dos dois ultimos dias")
            st.text("III)Caso queira pode-se incluir stop no tempo")
            st.text("A formula do IFR é dada por:")
            st.latex(r'''
            RSI = \frac{100}{1+\frac{U}{D}}
            ''')
            st.text("U = média das cotações dos últimos N dias em que a cotação subiu")
            st.text("D = média das cotações dos últimos N dias em que a cotação desceu")
            stop = st.slider("Digite o stop no tempo.Caso não deseje digite o valor zero")
            #Condição de executação para entradas do usuário
            if (stop!=0)or(stop==0):
                st.write("Robo Trabalhando!")
                dados = Main_3(stop,acoes)
                Resultado(dados)

        elif SETUP == ESTRATEGIA[4]:
            st.header("O Setup 3 Máximas 3 Mínimas possui as seguintes regras;")
            st.text("I- Se o fechamento do dia for menor do que a média das três minimas compra-se o fechamento do dia")
            st.text("II - Se o fechamento do dia for maior do que a média das três máximas vende-se o fechamento do dia")
            st.text("III - Caso queira pode-se incluir stop no tempo")
            st.text("O cálculo da média móvel aritmética é dado por ;")
            st.latex(r'''\frac{\sum_{1}^{n}High_{i}}{n}''')
            stop = st.slider("Digite o stop no tempo.Caso não deseje digite o valor zero")
            if (stop!=0)or(stop==0):
                st.write("Robo Trabalhando!")
                dados = Main_4(stop,acoes)
                Resultado(dados)

        elif SETUP == ESTRATEGIA[5]:
            st.header("O Setup Tutle 20-10 possui as seguintes regras;")
            st.text("I)Se o fechamento do dia for maior do que as 20 máximas compra-se o fechamento do dia")
            st.text("II)Se o fechamento do dia for menor do que as 10 mínimas vende-se o fechamento do dia")
            st.text("III)Caso queira pode-se incluir stop no tempo")
            stop = st.slider("Digite o stop no tempo.Caso não deseje digite o valor zero")
            st.text("O cálculo da maior máxima é dado por;")
            st.latex(r'''Max\left \{ Hight_{1},Hight_{2},...,Hight_{n}\right \}''')
            st.text("O cálculo da menor mínima é dado por;")
            st.latex(r'''Min\left \{ Low_{1},Low_{2},...,Low_{n}\right \}''')
            if (stop!=0)or(stop==0):
                st.write("Robo Trabalhando!")
                dados = Main_5(stop,acoes)
                Resultado(dados)

        elif SETUP == ESTRATEGIA[6]:
            st.header("O Setup 9.1 possui as seguintes regras;")
            st.text("I-Se o fechamento do dia for menor do que a média exponencial de 9 compra-se o fechamento do dia")
            st.text("II-Se o fechamento do dia for maior do que a média exponencial de 9  vende-se o fechamento do dia")
            st.text("III-Caso queira pode-se incluir stop no tempo")
            st.text("O cálculo da média móvel exponencial é dado por ;")
            st.latex(r'''MME = \left [ Close_{n}-MME_{n-1} \right ]*MME_{n-1}''')
            stop = st.slider("Digite o stop no tempo.Caso não deseje digite o valor zero")
            if (stop!=0)or(stop==0):
                st.write("Robo Trabalhando!")
                dados = Main_6(stop,acoes)
                Resultado(dados)

        elif SETUP == ESTRATEGIA[7]:
            st.header("O Setup Stop Atr possui as seguintes regras;")
            st.text("I-Se o fechamento do dia for maior do que o Stop Atr de N periodos com D desvio compra-se o fechamento do dia")
            st.text("II-Se o fechamento do dia for menor do que o Stop Atr de N periodos com D desvio vende-se o fechamento do dia")
            st.text("III-Caso queira pode-se incluir stop no tempo")
            st.text("O cálculo do Stop Atr é dado por ;")
            st.latex(r'''STOPATR = Close_1-d*Atr_n''')
            st.text("O atr e a média de n periodo do true range ;")
            st.latex(r'''Atr_n = \frac{\sum_{2}^{n}max\left \{ abs(High_{n-1}-Close_n,Low_{n-1}-Close_n,High_n-Low_n) \right \}}{n}''')
            stop = st.slider("Escolha o valor do stop no tempo.Caso não deseje deixe o valor zero")
            desvio = st.slider("Esolha o valor do desvio")
            periodo = st.slider("Digite o valor do periodo")
            if (periodo != 0):
                st.write("Robo Trabalhando!")
                dados = Main_1(stop,desvio,periodo,acoes)
                Resultado(dados)
                
