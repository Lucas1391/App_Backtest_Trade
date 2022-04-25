import streamlit as st
#Instalando Pacotes
import numpy as np
import pandas as pd
import yfinance as yf
import pandas_ta as ta
from PIL import Image
from Backtest import Main_1,Main_2,Main_3,Main_4,Main_5,Main_6
import requests

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
    ativos = ['ALPA4', 'ABEV3', 'AMER3', 'ASAI3', 'AZUL4', 'B3SA3', 'BIDI11', 'BPAN4', 'BBSE3', 'BRML3', 'BBDC3', 'BBDC4', 'BRAP4', 'BBAS3', 'BRKM5', 'BRFS3', 'BPAC11', 'CRFB3', 'CCRO3', 'CMIG4', 'CIEL3', 'COGN3', 'CPLE6', 'CSAN3', 'CPFE3', 
                'CMIN3', 'CVCB3', 'CYRE3', 'DXCO3', 'ECOR3', 'ELET3', 'ELET6', 'EMBR3', 'ENBR3', 'ENGI11', 'ENEV3', 'EGIE3', 'EQTL3', 'EZTC3', 'FLRY3', 'GGBR4', 'GOAU4', 'GOLL4', 'NTCO3', 'SOMA3', 'HAPV3', 'HYPE3', 'IGTI11', 'IRBR3', 'ITSA4', 'ITUB4', 'JBSS3', 'JHSF3', 'KLBN11', 'RENT3', 'LCAM3', 'LWSA3', 'LREN3', 'MGLU3', 'MRFG3', 'CASH3', 'BEEF3', 'MRVE3', 'MULT3', 'PCAR3', 'PETR3', 'PETR4', 'PRIO3', 'PETZ3', 'POSI3', 'QUAL3', 'RADL3', 'RDOR3', 'RAIL3', 'SBSP3', 'SANB11', 'CSNA3', 'SLCE3', 'SULA11', 'SUZB3', 'TAEE11', 'VIVT3', 'TIMS3', 'TOTS3', 'UGPA3', 'USIM5', 'VALE3', 'VIIA3', 'VBBR3', 'WEGE3', 'YDUQ3', 'ABCB4', 'AERI3', 'AESB3', 'ALSO3', 'AALR3', 'ALLD3', 'ALPA4', 'ALUP11', 'ABEV3', 'AMBP3', 'AMER3', 'ANIM3', 'ARZZ3', 'ARML3', 'ASAI3', 'AURE3', 'AZUL4', 'B3SA3', 'BMGB4', 'BIDI11', 'BPAN4', 'BRSR6', 'BBSE3', 'BMOB3', 'BKBR3', 'BLAU3', 
                'BOAS3', 'BRML3', 'BRPR3', 'BBDC3', 'BBDC4', 'BRAP4', 'BBAS3', 'AGRO3', 'BRKM5', 'BRFS3', 'BPAC11', 'CXSE3', 'CAML3', 'CRFB3', 'CBAV3', 'CCRO3', 'CEAB3', 'CMIG3', 'CMIG4', 'CIEL3', 'CLSA3', 'COGN3', 'CSMG3', 'CPLE3', 'CPLE6', 'CSAN3', 'CPFE3', 'CMIN3', 'CARD3', 'CURY3', 'CVCB3', 'CYRE3', 'DASA3', 'DXCO3', 'DEXP3', 'PNVL3', 'DIRR3', 'ECOR3', 'ELET3', 'ELET6', 'EMBR3', 'ENAT3', 'ENBR3', 'ENGI11', 'ENEV3', 'EGIE3', 'ENJU3', 'EQTL3', 'ESPA3', 'EVEN3', 'EZTC3', 'FESA4', 'FLRY3', 'GFSA3', 'GGBR4', 'GOAU4', 'GETT11', 'GOLL4', 'GGPS3', 'GRND3', 'GMAT3', 'NTCO3', 'SBFG3', 'SOMA3', 'GUAR3', 'HAPV3', 'HBOR3', 'HBSA3', 'HYPE3', 'IGTI11', 'PARD3', 'MEAL3', 'ROMI3', 'IFCM3', 'INTB3', 'MYPK3', 'RANI3', 'IRBR3', 'ITSA4', 'ITUB3', 'ITUB4', 'JALL3', 'JBSS3', 'JHSF3', 'KEPL3', 'KLBN11', 'LAVV3', 'LIGT3', 'RENT3', 'LCAM3', 'LWSA3', 'LOGG3', 'LOGN3', 'AMAR3', 'LREN3', 'MDIA3', 'MGLU3', 'POMO4', 'MRFG3', 'MATD3', 'CASH3', 'LEVE3', 'MILS3', 'BEEF3', 'MTRE3', 'MODL11', 'MOVI3', 'MRVE3', 'MLAS3', 'MULT3', 'NEOE3', 'NGRD3', 'OPCT3', 'ODPV3', 'MEGA3', 'ONCO3', 'ORVR3', 'PCAR3', 'PGMN3', 'PETR3', 'PETR4', 'RECV3', 'PRIO3', 'PETZ3', 'PLPL3', 'PSSA3', 'PTBL3', 'POSI3', 'QUAL3', 'LJQQ3', 'RADL3', 'RAIZ4', 'RAPT4', 'RCSL3', 'RCSL4', 'RDOR3', 'RAIL3', 'SBSP3', 'SAPR11', 'SANB11', 'STBP3', 'SMTO3', 'SEQL3', 'SEER3', 'CSNA3', 'SIMH3', 'SQIA3', 'SLCE3', 'SULA11', 'SUZB3', 'SYNE3', 'TAEE11', 'TASA4', 'TRAD3', 'TECN3', 'TCSA3', 'TGMA3', 'VIVT3', 'TEND3', 'TIMS3', 'TOTS3', 'TRPL4', 'TRIS3', 'TPIS3', 'TUPY3', 'UGPA3', 'UNIP6', 'USIM3', 'USIM5', 'VALE3', 'VLID3', 'VAMO3', 'VIIA3', 'VBBR3', 'VIVA3', 'VULC3', 'WEGE3', 'WEST3', 'WIZS3', 'YDUQ3']
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
names = ['Lucas Campos','Leandro Giron','Daniel Solano','Rafael Quintanilha']
passwords = ['lucassomatoria7@gmail.com','leandro.giron@gmail.com','contato@quantinvestimentos.com.br','rafael@quantbrasil.com.br']
usuario = st.text_input("Insira seu nome de usuário : ")
senha = st.text_input("Insira sua senha : ",type=password)
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
                
