#INTEGRATION DES VOLUMES 

global signal
global PKILL
global symbol

import pandas as pd
from binance.client import Client
import datetime as dt# client configuration
import json
import time
import pytz
import os
import datetime
from datetime import datetime, timedelta
import numpy as np
#from binance.exceptions import BinanceAPIException, BinanceOrderException
import requests

#from binance.client import Client
from binance.enums import *
from binance.exceptions import BinanceAPIException, BinanceOrderException

import asyncio
from binance import AsyncClient, BinanceSocketManager

#pd.set_option('display.max_columns', 500)
#pd.set_option('display.max_columns', None)
#pd.set_option('display.max_colwidth', None)
#pd.set_option("display.max_rows", None)
#pd.set_option('display.max_colwidth', 500)

#!/usr/bin/python

#VERSION V2  BOT_EMA200_DEMA40_EMA15_V.2
import sys

pd.set_option('display.precision', 8)
#pd.set_option('display.precision', 8)
#pd.set_option('display.precision', 7)

#api_key = 'API HERE'
#api_secret = 'SECRET API HERE'
api_key = "ORhiXPFtpMJp4ipwnY9SWBuGhGQPV7iHe05LlI796DWHtRkof14u19KnJ7ntB1vm"
api_secret = "g7ca65ISjgAzmmSG3qzQy7l0C5qqhy8UuYqbj14PhCJU82OD2eQSKfzuHn59LhWF"
client = Client(api_key, api_secret)


"""
symbol = "DOTUSDT"
symbol = "SUSHIBTC"
symbol = "WABIBTC"
symbol = "ATOMBTC"
"""


try:
    if sys.argv[1] != "" :
        print(sys.argv)
        symbol =sys.argv[1]
        symbol=symbol.upper()
        timeframe =sys.argv[2]
        print("sys.argv[1]:",sys.argv[1])
        print("sys.argv[2]:",sys.argv[2])
except Exception as h:
    #print(f'\nError MAIN THREAD : {h}') 
    #timeframe = "1m"
    timeframe = "4h"
    print("symbol:",symbol)
    print("timeframe:",timeframe)

def PKILL(signum, frame): 
    import os
    import subprocess
    global symbol
    global interval
    try:
        #print("signum:",signum)
        CMD_KILL_LAST_PRICE="/usr/bin/pkill -f \"last_price.py "+str(symbol)+"\" 2> /dev/null"
        #print(CMD_KILL_LAST_PRICE)
        stream = os.popen(CMD_KILL_LAST_PRICE)
        if signum == 15 :
            CMD_KILL="/usr/bin/pkill -f \"CREATE_ALL_TIMEFRAME_PEER_SYMBOL.sh "+str(symbol)+" "+str(interval) +"\" 2> /dev/null"
            #print(CMD_KILL)
            stream = os.popen(CMD_KILL)
            if (frame != "OTHER") :
                CMD_KILL="/usr/bin/pkill -f \""+str(symbol)+" "+str(interval) +"\" 2> /dev/null"
                #print(CMD_KILL)
                stream = os.popen(CMD_KILL)
            CMD_PS="ps -ef|egrep -i " +str(symbol)+"|egrep -i "+str(interval)+"|egrep -i THREAD_PTT_ftx|grep -v grep|awk '{print $2}'"
            #print ("CMD_PS=",CMD_PS)
            stream = os.popen(CMD_PS) 
            pid=stream.read().strip()
            #print ("PID=",pid)
            if  (pid != "") : 
                pid=int(pid)
                #os.kill(pid, 9)
                KILL="/usr/bin/kill -9 "+str(pid)
                time.sleep(1)
                #print("KILL=",KILL)
                stream = os.popen(KILL)
                exit(1) 
        else :
            #if (frame != "OTHER") :
                CMD_KILL="/usr/bin/pkill -f \""+str(symbol)+" "+str(interval) +"\" 2> /dev/null"
                #print(CMD_KILL)
                stream = os.popen(CMD_KILL)
                exit(1)
    except Exception as h:
        print("symbol:",symbol)
        
import signal
signal.signal(signal.SIGINT, PKILL)
signal.signal(signal.SIGTERM, PKILL)

###IMPORT POUR  RECUP_LAST_PRICE_IN_BINANCE
# from pandas import DataFrame
# from functools import reduce
# import pandas as pd
# import arrow
# import talib.abstract as ta
import requests
# import datetime
# import numpy as np
# import sys
# from pprint import pprint
# import json
# import time
# import pytz
# import os
from binance.client import Client
from binance.enums import *
from binance.exceptions import BinanceAPIException, BinanceOrderException
global NBR_LAST_PRICE
NBR_LAST_PRICE=0
global OLD_LAST_PRICE
OLD_LAST_PRICE=0

global Diff_last_price_OLD_LAST_PRICE
Diff_last_price_OLD_LAST_PRICE=0


def CALCUL_TIME_DIFFERENCE():
    global custom_info
    global time_difference
    DATE_ACHAT=str(custom_info["DATE_ACHAT"])
    DATE_VENTE=str(custom_info["DATE_VENTE"])
    DATE_ACHAT=DATE_ACHAT.split(".")[0]
    DATE_VENTE=DATE_VENTE.split(".")[0]
    print("DATE_ACHAT:",DATE_ACHAT)
    print("DATE_VENTE:",DATE_VENTE)
    DATE_ACHAT=datetime.strptime(DATE_ACHAT, '%Y-%m-%d %H:%M:%S')
    DATE_VENTE=datetime.strptime(DATE_VENTE, '%Y-%m-%d %H:%M:%S')
    time_difference = DATE_VENTE-DATE_ACHAT
    print(time_difference)
    time_difference=int(str(time_difference).split(":")[1])
    print("time_difference:",time_difference)


def RECUP_LAST_PRICE_IN_BINANCE(dataframe):
    print("ENTRER DANS RECUP_LAST_PRICE_IN_BINANCE : ")
    global PRIX
    global symbol
    global TYPE_BG_BIS
    global TAILLE_BG_BIS
    #global VAL_OPEN
    #global VAL_CLOSE
    global FRONT_MONTANT_COURT_EMA1H
    global NEW_OPEN_PRICE
    global Diff_LAST_PRICE_OPEN_PRICE
    global last_price
    global Diff_LAST_PRICE_OLD_File_price
    global FRONT_MONTANT_EMA15
    global DIFF_EMA1H_EMA15
    global LAST_VOLUME_VWAP_Price
    global FRONT_MONTANT_COURT_VOLUME
    global Diff_VOLUME_VWAP_LAST_PRICE_OLD_LAST_PRICE
    global LAST_PRICE
    global MULTIP 
    global custom_info

    
    # init
    api_key = "ORhiXPFtpMJp4ipwnY9SWBuGhGQPV7iHe05LlI796DWHtRkof14u19KnJ7ntB1vm"
    api_secret = "g7ca65ISjgAzmmSG3qzQy7l0C5qqhy8UuYqbj14PhCJU82OD2eQSKfzuHn59LhWF"
    
    """
    api_key = os.environ.get('binance_api')
    api_secret = os.environ.get('binance_secret')
    """
    VAL_CLOSE=dataframe.close.iloc[-1]
    client = Client(api_key, api_secret)
    #symbol="BNBBTC"
    ## get latest price from Binance API
    btc_price = client.get_symbol_ticker(symbol=symbol)
    # print full output (dictionary)
    print("btc_price: ",btc_price)
    PRIX=float(btc_price['price'])
    # MULTIP=len(str(VAL_CLOSE))
    print("MULTIP:",MULTIP)
    # PRIX=format(PRIX,'.8f')
    print("PRIX_COURANT : ",PRIX)
    print("VAL_CLOSE : ",VAL_CLOSE)
    #VAL_OPEN=int(float(dataframe['open'].iloc[val_mask_idxmin])*MULTIP)
    TAILLE_BG_BIS=float(PRIX)-float(VAL_CLOSE)
    # TAILLE_BG_BIS=CALCULE_TAILLE_BOUGIE(TAILLE_BG,MULTIP) 
    print("TAILLE_BG_BIS:",TAILLE_BG_BIS)
    if TAILLE_BG_BIS >= 0 :
        TYPE_BG_BIS="BG_VERTE"
    if TAILLE_BG_BIS < 0 :
        TYPE_BG_BIS="BG_ROUGE"
    print("TYPE_BG_BIS:",TYPE_BG_BIS)
    # exit()
    
    ###CALCULE FRONT_MONTANT_COURT_EMA1H
    #CLOSE=dataframe['CLOSE'].loc[val_mask_idxmin].astype(int)
    #NEW_OPEN_PRICE=int(float(NEW_OPEN_PRICE)*MULTIP)
    LAST_PRICE=int(float(PRIX)*MULTIP)
    custom_info["CLOSE"]=float(PRIX)
    #Diff_LAST_PRICE_OPEN_PRICE=(LAST_PRICE-NEW_OPEN_PRICE)
    #print("CLOSE:",CLOSE)
    #print("NEW_OPEN_PRICE:",NEW_OPEN_PRICE)
    print("LAST_PRICE:",LAST_PRICE)
    #print("Diff_LAST_PRICE_OPEN_PRICE:",Diff_LAST_PRICE_OPEN_PRICE)
    # if "." in str(last_price) :
    #     last_price=int(float(last_price)*MULTIP)
    # else:
    #     last_price=int(float(last_price))
    last_price=PRIX
    OLD_File_price=last_price
    print("OLD_File_price:",last_price)
    Diff_LAST_PRICE_OLD_File_price=(LAST_PRICE - OLD_File_price)
    print("Diff_LAST_PRICE_OLD_File_price:",Diff_LAST_PRICE_OLD_File_price)
    ###if Diff_LAST_PRICE_OPEN_PRICE > 0 :
    # if Diff_LAST_PRICE_OLD_File_price > 0 :
    #      FRONT_MONTANT_COURT_EMA1H=1
    # else:
    #      FRONT_MONTANT_COURT_EMA1H=0
    # print("FRONT_MONTANT_COURT_EMA1H:",FRONT_MONTANT_COURT_EMA1H)
    
    ###CALCULE FRONT_MONTANT_COURT_EMA15
    #EMA15=dataframe['EMA15'].iloc[-1].astype(int)
    dynamic_indicators(dataframe)
    global EMA15
    EMA15=EMA15.iloc[-1].astype(float)
    # VAL_EMA15=format(EMA15,'.8f')
    print("EMA15  dynamic_indicators:",format(EMA15,'.8f'))
    EMA15=int(float(EMA15)*MULTIP)
    print("EMA15 *MULTIP :",EMA15)
    DIFF_EMA1H_EMA15=(LAST_PRICE-EMA15)
    print("DIFF_EMA1H_EMA15:",DIFF_EMA1H_EMA15)
    # if DIFF_EMA1H_EMA15 > 0 :
    #      FRONT_MONTANT_EMA15=1
    # else:
    #      FRONT_MONTANT_EMA15=0
    # print("FRONT_MONTANT_EMA15:",FRONT_MONTANT_EMA15)
    
    # ###CALCULE VOLUME VWAP
    # VOLUME_VWAP_LAST_PRICE=CALCULE_VOLUME_VWAP(dataframe,LAST_PRICE)
    # VOLUME_VWAP_LAST_PRICE=int(float(VOLUME_VWAP_LAST_PRICE))
    # print("VOLUME_VWAP_LAST_PRICE:",VOLUME_VWAP_LAST_PRICE)

    # VOLUME_VWAP_OLD_File_price=CALCULE_VOLUME_VWAP(dataframe,OLD_File_price)
    # VOLUME_VWAP_OLD_File_price=int(float(VOLUME_VWAP_OLD_File_price))
    # print("VOLUME_VWAP_OLD_File_price:",VOLUME_VWAP_OLD_File_price)

    # Diff_VOLUME_VWAP_LAST_PRICE_OLD_LAST_PRICE=(VOLUME_VWAP_LAST_PRICE - VOLUME_VWAP_OLD_File_price)
    # print("Diff_VOLUME_VWAP_LAST_PRICE_OLD_LAST_PRICE:",Diff_VOLUME_VWAP_LAST_PRICE_OLD_LAST_PRICE)
    # ###if Diff_LAST_PRICE_OPEN_PRICE > 0 :
    # if Diff_VOLUME_VWAP_LAST_PRICE_OLD_LAST_PRICE > 0 :
    #      FRONT_MONTANT_COURT_VOLUME=1
    # else:
    #      FRONT_MONTANT_COURT_VOLUME=0
    # print("FRONT_MONTANT_COURT_VOLUME:",FRONT_MONTANT_COURT_VOLUME)
    # #time.sleep(0.5)
    print("SORTIE DANS RECUP_LAST_PRICE_IN_BINANCE : ")
    # exit()
 


global i
i=0
def RECUP_LAST_PRICE_IN_FILE(VAR_LAST_PRICE=False):
     #try:
        print("\nENTER DANS RECUP_LAST_PRICE_IN_FILE")
        global i
        global symbol
        global last_price
        global LAST_PRICE
        
        
        PAIR=symbol
        BOT="BOT_EMA200_DEMA40_EMA15"
        PATH_EMA200_DEMA40_EMA15="/root/BOT/freqtrade/user_data/strategies/FTX_BOT/"+BOT
        PATH=PATH_EMA200_DEMA40_EMA15
        PATH=PATH+"/LISTE_TRADING/"+PAIR
        FICHIER_PRICE=PATH+"/LAST_PRICE_"+PAIR
        FICHIER_COULEUR_VOLUME=PATH+"/COULEUR_VOLUME_"+PAIR
        
        if i == 0:
            print("ENTRE DANS RECUP_LAST_PRICE_IN_FILE FICHIER  = ",FICHIER_PRICE)
            i+=1
        cmd_READ_LAST_COULEUR_VOLUME="touch "+FICHIER_COULEUR_VOLUME+";tail -1 "+FICHIER_COULEUR_VOLUME
        #print("cmd_READ_PRICE=",cmd_READ_PRICE)
        import os
        stream = os.popen(cmd_READ_LAST_COULEUR_VOLUME)
        COMMANDE_READ_LAST_COULEUR_VOLUME= stream.read().strip()
        #print("Dans cmd_COMMANDE_BOT COMMANDE_BOT :",COMMANDE_READ_COULEUR_VOLUME)
        global COULEUR_VOLUME
        COULEUR_VOLUME=COMMANDE_READ_LAST_COULEUR_VOLUME
        print("COULEUR_VOLUME:",COULEUR_VOLUME)
        NBR_READ_LAST_PRICE = 0

        while True :
            cmd_READ_PRICE="touch "+FICHIER_PRICE+";tail -1 "+FICHIER_PRICE
            #print("cmd_READ_PRICE=",cmd_READ_PRICE)
            import os
            stream = os.popen(cmd_READ_PRICE)
            COMMANDE_READ_LAST_PRICE= stream.read().strip()
            # print("Dans cmd_COMMANDE_BOT COMMANDE_BOT :",COMMANDE_READ_LAST_PRICE)
            LEN_COMMANDE_READ_LAST_PRICE=len(COMMANDE_READ_LAST_PRICE.split())
            if LEN_COMMANDE_READ_LAST_PRICE == 0  and NBR_READ_LAST_PRICE == 0 :
                print("LEN_COMMANDE_READ_LAST_PRICE:",LEN_COMMANDE_READ_LAST_PRICE)
                NBR_READ_LAST_PRICE = 1
            # exit()
           
            if LEN_COMMANDE_READ_LAST_PRICE != 0 :
                #return
                break
            # else:
            #     RESTART_ONE_PAIR(symbol,timeframe)
            #     #time.sleep(1)
        #else:
           # time.sleep(1)
           
        global last_price_file
        last_price_file=COMMANDE_READ_LAST_PRICE.split()[2]
        last_price_file=(float(last_price_file))
        print("last_price_file:",last_price_file)
        #print("Diff_LAST_PRICE_OPEN_PRICE:",Diff_LAST_PRICE_OPEN_PRICE)
        # if "." in str(last_price_file) :
        #     last_price=int(float(last_price_file)*MULTIP)
        # else:
        #     last_price=int(float(last_price_file))
            
        # LAST_PRICE=int(float(last_price)*MULTIP)
        last_price=(float(last_price_file))
        LAST_PRICE=int(float(last_price_file)*MULTIP)
        print("LAST_PRICE:",LAST_PRICE)
        if VAR_LAST_PRICE != "" :
            return
        
                       
        
        global DATE_HEURE
        DATE_HEURE=COMMANDE_READ_LAST_PRICE.split()[0] +" "+COMMANDE_READ_LAST_PRICE.split()[1]
        print("DATE_HEURE:",DATE_HEURE)
        global VOLUME_ASK
        global PRICE_ASK
        global VOLUME_BID
        global PRICE_BID
        global PRICE_VOLUME_ASK
        global PRICE_VOLUME_BID
        global SPREAD

        ASK_BID=COMMANDE_READ_LAST_PRICE.split()[3]
        print("ASK_BID:",ASK_BID)
        if LEN_COMMANDE_READ_LAST_PRICE == 4 :
            VOLUME_ASK=ASK_BID.split("_")[0]
            PRICE_ASK=ASK_BID.split("_")[1]
            VOLUME_BID=ASK_BID.split("_")[2]
            PRICE_BID=ASK_BID.split("_")[3]
            print("VOLUME_ASK:",VOLUME_ASK)
            print("PRICE_ASK:",PRICE_ASK)
            print("VOLUME_BID:",VOLUME_BID)
            print("PRICE_BID:",PRICE_BID)
            (SOMME_VOLUMES,SOMME_VOLUMES_PRECEDENT)=CALCULE_SOMME_VOLUMES(dataframe)
            print("SOMME_VOLUMES_PRECEDENT:",SOMME_VOLUMES_PRECEDENT)
            print("SOMME_VOLUMES:",SOMME_VOLUMES)
            print("LEN_COMMANDE_READ_LAST_PRICE:",LEN_COMMANDE_READ_LAST_PRICE)
            
        if LEN_COMMANDE_READ_LAST_PRICE == 7 :
            PRICE_VOLUME_BID=float(ASK_BID.split("_")[4])
            PRICE_VOLUME_ASK=float(ASK_BID.split("_")[5])
            SPREAD=float(ASK_BID.split("_")[6])
            print("PRICE_VOLUME_ASK:",PRICE_VOLUME_ASK)
            print("PRICE_VOLUME_BID:",PRICE_VOLUME_BID)
            print("SPREAD:",SPREAD)
        

        # exit()

        
        global NEW_EMA1H
        global NEW_EMA1L
        global NEW_LAST_PRICE
        global NEW_OPEN_PRICE
        global NEW_HIGH_PRICE

        # if LEN_COMMANDE_READ_LAST_PRICE > 4 :
        if LEN_COMMANDE_READ_LAST_PRICE == 4 :
            NEW_EMAX=COMMANDE_READ_LAST_PRICE.split()
            print("ALL NEW_EMAX:",NEW_EMAX)
            NEW_EMAX=COMMANDE_READ_LAST_PRICE.split()[3]
            NEW_EMA1H=NEW_EMAX.split("_")[0]
            NEW_EMA1L=NEW_EMAX.split("_")[1]
            NEW_LAST_PRICE=NEW_EMAX.split("_")[2]
            # NEW_OPEN_PRICE=NEW_EMAX.split("_")[3]
            NEW_HIGH_PRICE=NEW_EMAX.split("_")[3]
            
            
            print("NEW_EMA1H:",NEW_EMA1H)
            print("NEW_EMA1L:",NEW_EMA1L)
            print("NEW_LAST_PRICE:",NEW_LAST_PRICE)
            # print("NEW_OPEN_PRICE:",NEW_OPEN_PRICE)
            print("NEW_HIGH_PRICE:",NEW_HIGH_PRICE)
            # exit()
        print("SORTIE DANS RECUP_LAST_PRICE_IN_FILE")
        return  last_price




global MULTIP   
# MULTIP=100000000 #8

pd.set_option('display.precision', 8)
#MULTIP=10000000 #7
#pd.set_option('display.precision', 7)
AUTO_RANGE="1 years ago UTC"

#interval='15m'
#interval='4h'
#interval='2h'
#interval='1h'
#interval='1h'
global nbr_interval
global interval
interval=timeframe
print("interval :",interval)
PKILL(15,"OTHER")
#PKILL("","")

Client.KLINE_INTERVAL_15MINUTE 
#klines = client.get_historical_klines(symbol, interval, "1 May,2022")
#klines = client.get_historical_klines(symbol, interval, "1 Dec,2020", "22 Apr,2021") # 1H
DATE_DEB="1 Sep,2020"
DATE_FIN="22 Apr,2021"

DATE_DEB="28 Juil,2020"
DATE_FIN="20 Mai,2021"

DATE_DEB="30 Jun,2021"
DATE_FIN="31 Jun,2021"
##DATE_DEB="4 Oct,2020"  #SUSHI
##DATE_FIN="20 Apr,2021" #SUSHI
#DATE_DEB="14 Sep,2021"
#DATE_FIN="20 Dec,2021"
#DATE_FIN="14 Dec,2021"
#DATE_FIN="4 Dec,2021"
global klines
global TEMP
global val_minute
global SOMME_VOLUMES_PRECEDENT
SOMME_VOLUMES_PRECEDENT=0
global SOMME_VOLUMES
SOMME_VOLUMES=0

nbr_interval=int(interval[:-1])
if "m" in  interval :
    val_minute=nbr_interval
    if nbr_interval == 1 :
        TEMP="MINUTE"
    else:
        TEMP="MINUTES"
        
if "h" in  interval :
    val_minute=nbr_interval*60
    if nbr_interval == 1 :
        TEMP="HEURE"
    else:
        TEMP="HEURES"
        
if ("J" in  interval) or  ("d" in  interval) :
    val_minute=nbr_interval*60*24
    if nbr_interval == 1 :
        TEMP="JOUR"
    else:
        TEMP="JOURS"  

if "M" in  interval :
    val_minute=nbr_interval*60*24*30
    TEMP="MOIS"
            
if "w" in  interval :
    if nbr_interval == 1 :
        val_minute=nbr_interval*60*24*7
        TEMP="SEMAINE"
    else:
        TEMP="SEMAINES"           

         


#nbr_interval=int(interval[:-1])
if ( "m" in  interval ) and (nbr_interval <= 60) :
    RANGE=200/(60/nbr_interval)
    if type(RANGE) == float : 
        RANGE=int(RANGE)+1
    AUTO_RANGE=str(RANGE*4)+"h"
    print("AUTO_RANGE=",AUTO_RANGE)
    #MULTIP=1000000000
    #pd.set_option('display.precision', 9)
    pd.options.display.float_format = '{:.9f}'.format
    #klines = client.get_historical_klines(symbol, interval, AUTO_RANGE)
else: 
    #MULTIP=100000000
    #pd.set_option('display.precision', 8)
    pd.options.display.float_format = '{:.8f}'.format
    AUTO_RANGE="1 years ago UTC"
    #DURE=60*
    RANGE=200/(60)
    if type(RANGE) == float : 
        RANGE=int(RANGE)+1
    AUTO_RANGE=str(RANGE*4)+"h"
    AUTO_RANGE="1 years ago UTC"
    print("AUTO_RANGE=",AUTO_RANGE)
    #klines = client.get_historical_klines(symbol, interval, "1 years ago UTC")

klines = client.get_historical_klines(symbol, interval, AUTO_RANGE)
#klines = client.get_historical_klines(symbol, interval, DATE_DEB,DATE_FIN) #4H
#klines = client.get_historical_klines(symbol, interval, "400d")
#klines = client.get_historical_klines(symbol, interval, "1 Nov,2020", "22 Apr,2021") #4H
#klines = client.get_historical_klines(symbol, interval, "1 Jan,2021", "22 Apr,2021")
#klines = client.get_historical_klines(symbol, interval, "1 Jan,2022", "20 Apr,2022")
#klines = client.get_historical_klines(symbol, interval, "30 Juin,2022")
#klines = client.get_historical_klines(symbol, interval, "1 Jan,2022", "10 Jan,2022")
"""
df['date'] = df.date.apply(lambda d: datetime.datetime.fromtimestamp(int(d)).strftime('%Y-%m-%d %H:%M:%S')) 
df['date'] = df.date.apply(lambda d: datetime.datetime.fromtimestamp(int(d)) + pd.Timedelta(seconds=1))
"""
"""
timestamp = client._get_earliest_valid_timestamp(symbol, interval)
print("timestamp ORG=",timestamp)
print("timestamp=",str(timestamp)[0:10])
DATE_TIMESTAMP= datetime.fromtimestamp(int(str(timestamp)[0:10])).strftime('%Y-%m-%d %H:%M:%S')
print(DATE_TIMESTAMP)
# request historical candle (or klines) data
klines = client.get_historical_klines(symbol, timeframe, timestamp)
#data = pd.DataFrame(klines)
#print("timestamp=",timestamp)
"""

def plot_fibonacci_retracement(df):
    """
    https://levelup.gitconnected.com/five-useful-pandas-scripts-for-financial-time-series-plots-99693c4025b2
    Plots the Fibonacci retracement of a pricing data.

    :param df: The pricing data.

    :return: The plot.
    """
    highest_swing = df['High'].idxmax()
    lowest_swing = df['Low'].idxmin()

    ratios = [0, 0.236, 0.382, 0.5 , 0.618, 0.786, 1]
    colors = ["black","r","g","b","cyan","magenta","yellow"]
    levels = []
    max_level = df['High'][highest_swing]
    min_level = df['Low'][lowest_swing]

    for ratio in ratios:
        if highest_swing > lowest_swing:
            levels.append(max_level - (max_level-min_level)*ratio)
        else:
            levels.append(min_level + (max_level-min_level)*ratio)

    # for i in range(len(levels)):
    #     plt.hlines(levels[i], df.index[0], df.index[-1], label="{:.1f}%".format(ratios[i]*100),colors=colors[i], linestyles="dashed")

def CALCULE_DF_VOLUME_VWAP(dataframe,c=False) :
    #global LAST_VOLUME_VWAP_Price
    #Typical Price = (High + Low + Close) / 3
    #VWAP = ∑ (Typical Price * Volume ) / ∑ Volume    
    #return np.cumsum(v*(h+l)/2) / np.cumsum(v)
    h=dataframe['high'].astype(float)
    l=dataframe['low'].astype(float)
    c=dataframe['close'].astype(float)
    v=dataframe['volume'].astype(float)
    #Typical_Price=(np.cumsum(v*(h+l)/2) / np.cumsum(v))
    dataframe['VWAP']=(np.cumsum(v*(h+l+c)/3) / np.cumsum(v))
    ####print("LAST_VOLUME_VWAP_Price:",LAST_VOLUME_VWAP_Price)
    print("VOLUME_VWAP_Price:\n",dataframe['VWAP'].tail())
    # LAST_VOLUME_VWAP_Price="{:.8f}".format(VOLUME_VWAP_Price.iloc[-1])
    # print("LAST_VOLUME_VWAP_Price:",LAST_VOLUME_VWAP_Price)
    #return LAST_VOLUME_VWAP_Price


def CALCULE_VOLUME_VWAP(dataframe,c=False) :
    global LAST_VOLUME_VWAP_Price
    #Typical Price = (High + Low + Close) / 3
    #VWAP = ∑ (Typical Price * Volume ) / ∑ Volume    
    #return np.cumsum(v*(h+l)/2) / np.cumsum(v)
    # h=dataframe['high'].astype(float)
    # l=dataframe['low'].astype(float)
    # c=dataframe['close'].astype(float)
    # v=dataframe['volume'].astype(float)
    h=float(dataframe['high'].iloc[-1])
    l=float(dataframe['low'].iloc[-1])
    if c == "":
        c=float(dataframe['close'].iloc[-1])
    v=float(dataframe['volume'].iloc[-1])
    #Typical_Price=(np.cumsum(v*(h+l)/2) / np.cumsum(v))
    VOLUME_VWAP_Price=(np.cumsum(v*(h+l+c)/3) / np.cumsum(v))
    LAST_VOLUME_VWAP_Price="{:.8f}".format(VOLUME_VWAP_Price[0])
    ####print("LAST_VOLUME_VWAP_Price:",LAST_VOLUME_VWAP_Price)
    # print("VOLUME_VWAP_Price:\n",VOLUME_VWAP_Price)
    # LAST_VOLUME_VWAP_Price="{:.8f}".format(VOLUME_VWAP_Price.iloc[-1])
    # print("LAST_VOLUME_VWAP_Price:",LAST_VOLUME_VWAP_Price)
    return LAST_VOLUME_VWAP_Price
    #exit()


def CALCULE_SOMME_VOLUMES(dataframe) :
  try:  
    global SOMME_VOLUMES_PRECEDENT
    global SOMME_VOLUMES
    df_volume=dataframe['volume']
    df1_volume=pd.DataFrame()
    #print("\ndf_volume:\n",df_volume.tail(10))
    #print("\n len(dataframe)-1 df_volume:",dataframe.index[-1])

    if dataframe.index[-1] == 0 :
        return
    #i=len(dataframe)-1
    i=dataframe.index[-1]
    j=0
    volume_old=0
    volume=0
    while  j < 10 :
            #print("i:",i)
            #print("j:",j)
            volume_old=float(df_volume.iloc[i-1])
            #print("Volume_old:", volume_old)
            volume=float(df_volume.iloc[i])
            #print("Volume:", volume)
            Add_Volume_Volume_old=int(volume+volume_old)*10
            #print("Add_Volume_Volume_old:", Add_Volume_Volume_old)
            #exit()
            #dict={'SUM_2_LINE': [Add_Volume_Volume_old]}
            dict=[Add_Volume_Volume_old]
            df1= pd.DataFrame(dict)
            df1_volume=pd.concat([df1_volume,df1])
            Add_Volume_Volume_old=0
            #print("df1_volume: \n",df1_volume[0].values)
            j+=1
            i-=1
                
                
    #print("ALL volume:",volume)       
    #print("ALL df1_volume:",df1_volume) 
    SOMME_VOLUMES=df1_volume.iloc[-1][0]
    SOMME_VOLUMES_PRECEDENT=df1_volume.iloc[-2][0]
    print("LAST SOMME_VOLUMES:",SOMME_VOLUMES)
    print("SOMME_VOLUMES_PRECEDENT:",SOMME_VOLUMES_PRECEDENT)
    return (SOMME_VOLUMES,SOMME_VOLUMES_PRECEDENT)
     #"""  
  except Exception as e:
       print("ERROR SOMME_VOLUMES:",symbol)
     #"""  
     
def TEST_MULTI_PAIR(dataframe):
    STR_OPEN=str(dataframe.iloc[-1].open)
    LEN_OPEN=len(STR_OPEN.split(".")[0])
    print("STR_OPEN:",STR_OPEN)
    print("LEN_OPEN:",LEN_OPEN)
    if LEN_OPEN  > 1 :
        MULTIP=1
    else:
        MULTIP=100000000
    print("MULTIP:",MULTIP)
    return MULTIP


def dynamic_indicators(dataframe) :
    global PRIX
    global EMA15
    # dynamic_dataframe=dataframe.copy
    NEW_CLOSE=dataframe['close']
    #var="0.00003381"
    # new_close="0.0000544"
    new_close=PRIX
    # print("\nNEW_CLOSE:\n",NEW_CLOSE.tail())
    NEW_CLOSE=NEW_CLOSE.shift(-1, axis = 0)
    # print("\nNEW_CLOSE SHIFT -1 :\n",NEW_CLOSE.tail())

    NEW_CLOSE.iloc[-1]=new_close
    # print("\nNEW_CLOSE:\n",NEW_CLOSE.tail())
    EMA15 = dataframe['close'].ewm(span = 15, adjust = False).mean()
    print("\nEMA15:\n",EMA15.tail())
    EMA15 = NEW_CLOSE.ewm(span = 15, adjust = False).mean()
    print("\nNEW EMA15:\n",EMA15.tail())
    
    # dataframe['EMA200'].append(new_close,ignore_index=True)
    # EMA15 = dataframe['close'].ewm(span = 15, adjust = False).mean()
    # dataframe['EMA15']= EMA15.apply(lambda x : (x*MULTIP)).astype(int)
    
    
def SAR_indicators(rel_df) :
    from PSAR import PSAR
    # data=pd.DataFrame()
    indic = PSAR()
    rel_df['SAR'] = rel_df.apply(lambda x: indic.calcPSAR(x['high'], x['low']), axis=1)
    # Add supporting data
    rel_df['EP'] = indic.ep_list
    rel_df['Trend'] = indic.trend_list
    rel_df['AF'] = indic.af_list
    rel_df=rel_df.fillna(0)
    print("\nSAR: \n",rel_df.tail())
    RECUP_LAST_PRICE_IN_BINANCE(rel_df)        
    # RECUP_LAST_PRICE_IN_FILE("FIRST")
    # PRIX=last_price_file
    print (f"float(PRIX) = {PRIX} ") 
    # rel_df['SAR'] = rel_df.apply(lambda x: (x['SAR']+PRIX)/2, axis=1)
    rel_df['SAR'] = rel_df.apply(lambda x: (x['SAR']+(PRIX/190)), axis=1)
    print("NEW SAR: \n",rel_df.tail())

    # exit()
    return rel_df
    
def HEIKIN_ASHI_indicators(rel_df) :
    
    #assigning existing columns to new variable HAdf
    DATE = rel_df[['date']].copy()
    HAdf = rel_df[['open', 'high', 'low', 'close','volume']].copy()
    OPEN=rel_df['open'].astype(float)
    HIGH= rel_df['high'].astype(float)
    LOW=rel_df['low'].astype(float)
    CLOSE=rel_df['close'].astype(float)
    HAdf['close'] = round((( OPEN + HIGH + LOW + CLOSE )/4),8)
    # print("\n HAdf['close']:\n", HAdf['close'])
    # exit()
    
    #round function to limit results to 2 decimal places

    for i in range(len(rel_df)):
        if i == 0:
            HAdf.iat[0,0] = round(((OPEN.iloc[0] + CLOSE.iloc[0])/2),8)
        else:
            HAdf.iat[i,0] = round(((HAdf.iat[i-1,0] + HAdf.iat[i-1,3])/2),8)

    #Taking the open and close columns we worked on in Step 2 & 3
    #Joining this data with the existing high/low data from rel_df
    #Taking the max value in the new row with columns open, close, high
    #Assigning that value to the high/low column in HAdf

    HAdf['high'] = HAdf.loc[:,['open', 'close']].join(HIGH).max(axis=1)
    HAdf['low'] = HAdf.loc[:,['open', 'close']].join(LOW).min(axis=1)
    # HAdf=DATE.append(HAdf,ignore_index=True)
    print("\nHAdf.tail(10):\n",HAdf.tail(10))
    return HAdf
    # exit()


def populate_indicators(btc_df) :
    try:
        global dataframe_date
        #TIMEDELTA=2
        #TIMEDELTA=1
        #global dataframe
        dataframe=btc_df[['date','open','high','low','close','volume']].copy()
        global MULTIP   
        OPEN=btc_df['open'].iloc[-1]
        DEC_OPEN=OPEN.split(".")[1]    
        MULTIP=10 ** len(DEC_OPEN)
        print("MULTIP :",MULTIP)
    except Exception as g:
        pass
    
    dataframe_date=dataframe
    dataframe=HEIKIN_ASHI_indicators(dataframe)
    dataframe=SAR_indicators(dataframe)
    SAR=dataframe['SAR']
    #dataframe=btc_df[['date','open','high','low','close']]
    #Calcule d'un moyenne entre la DEMA40 et la EMA15
    # EMA200=dataframe['close'].ewm(span = 200, adjust = False).mean()
    EMA200=dataframe['close'].ewm(span = 130, adjust = False).mean()
    #dataframe['EMA200'].append(EMA200,ignore_index=True)
    #print("EMA200\n: ",EMA200)
    dataframe['EMA200'] = EMA200
    EMA1H = dataframe['high'].ewm(span = 1, adjust = False).mean()
    #print("EMA1H:\n",EMA1H)
    dataframe['EMA1H'] = EMA1H
    EMA1L = dataframe['low'].ewm(span = 1, adjust = False).mean()
    #print("EMA1H:\n",EMA1H)
    dataframe['EMA1L'] = EMA1L
    # EMA15 = dataframe['close'].ewm(span = 15, adjust = False).mean()
    # EMA15 = dataframe['close'].ewm(span = 11, adjust = False).mean()
    EMA15 = dataframe['low'].ewm(span = 7, adjust = False).mean()
    dataframe['EMA15'] = EMA15
    dataframe['EMA15'] = EMA15
    # EMA40 = dataframe['close'].ewm(span = 40, adjust = False).mean()
    # DEMA40 = 2*EMA40 - EMA40.ewm(span = 40, adjust = False).mean()
    # dataframe['DEMA40'] = DEMA40
    global DEMA2V
    EMA2V = dataframe['volume'].ewm(span = 2, adjust = False).mean()
    DEMA2V = 2*EMA2V - EMA2V.ewm(span = 2, adjust = False).mean()
    dataframe['DEMA2V'] = DEMA2V
    print("\nDATAFRAME:\n",dataframe.tail())
    print("\nDATAFRAME_DATE:\n",dataframe_date.tail())
    print("\nDEMA2V:\n",DEMA2V.tail())
    #CALCULE_SOMME_VOLUMES(dataframe)
    # CALCULE_DF_VOLUME_VWAP(dataframe)
    # dynamic_indicators(dataframe)
    # exit()
    
    ####################### #CALCULE MIN #####################
    
    #max=df1[['DEMA40']].max(skipna=True)
    max_EMA200=dataframe[['EMA200']].max(skipna=True)
    min_EMA200=dataframe[['EMA200']].min(skipna=True)
    print("min_EMA200: ",min_EMA200)
    print("max_EMA200: ",max_EMA200)
    
    positions = np.flatnonzero(min_EMA200)
    #print("positions:",positions)
    print("LEN positions  min_EMA200:",len(positions))
    if len(positions) == 0 :
        min_EMA200=0
    positions = np.flatnonzero(max_EMA200)
    print("positions max_EMA200:",positions)
    print("LEN positions:",len(positions))
    if len(positions) == 0 :
        max_EMA200=0
        
    max_EMA15=dataframe[['EMA15']].max(skipna=True)
    min_EMA15=dataframe[['EMA15']].min(skipna=True)
    print("min_EMA15: ",min_EMA15)
    print("max_EMA15: ",max_EMA15)
    
    positions = np.flatnonzero(min_EMA15)
    #print("positions:",positions)
    print("LEN positions min_EMA15:",len(positions))
    if len(positions) == 0 :
        min_EMA15=0
    positions = np.flatnonzero(max_EMA15)
    #print("positions:",positions)
    print("LEN positions max_EMA15:",len(positions))
    if len(positions) == 0 :
        max_EMA15=0
        
    # MIN_INDEX_VALEUR_EMA200=dataframe.loc[dataframe['EMA200'] == min_EMA200.EMA200].index.values.astype(int)[0]
    # print ("MIN_INDEX_VALEUR_EMA200.EMA200 :",MIN_INDEX_VALEUR_EMA200)
    # print ("VAL min_EMA200.EMA200 :\n",dataframe.iloc[MIN_INDEX_VALEUR_EMA200])
    
    # MAX_INDEX_VALEUR_EMA200=dataframe.loc[dataframe['EMA200'] == max_EMA200.EMA200].index.values.astype(int)[0]
    # print ("\nMAX_INDEX_VALEUR_EMA200 :",MAX_INDEX_VALEUR_EMA200)
    # print ("VAL max_EMA200.EMA200 :\n",dataframe.iloc[MAX_INDEX_VALEUR_EMA200])

    # global MULTIP
    # #MULTIP=100000000
    # STR_OPEN=str(dataframe.iloc[-1].open)
    # LEN_OPEN=len(STR_OPEN.split(".")[0])
    # print("STR_OPEN:",STR_OPEN)
    # print("LEN_OPEN:",LEN_OPEN)
    # if LEN_OPEN  > 1 :
    #     MULTIP=1
    # print("MULTIP:",MULTIP)
    # MULTI=TEST_MULTI_PAIR(dataframe)
    ####################### #CALCULE CROISEMENT #####################
    dataframe['EMA1H_ORG']= EMA1H
    dataframe['EMA200']= dataframe['EMA200'].apply(lambda x : (np.round(x,decimals = 8))).astype(float)
    #dataframe['EMA200']= dataframe['EMA200'].apply(lambda x : (round(x,8))).astype(int)
    dataframe['EMA200_ORG']= EMA200
    OPEN = dataframe['open'].ewm(span = 1, adjust = True).mean()
    print("OPEN:\n",OPEN.tail())
    dataframe['OPEN'] = OPEN
    CLOSE = dataframe['close'].ewm(span = 1, adjust = True).mean()
    print("CLOSE:\n",CLOSE.tail())
    dataframe['CLOSE'] = CLOSE
    



    
    LOW = dataframe['low'].ewm(span = 1, adjust = True).mean()
    print("LOW:\n",LOW.tail())
    dataframe['LOW'] = LOW
    
    HIGH = dataframe['high'].ewm(span = 1, adjust = True).mean()
    print("HIGH:\n",HIGH.tail())
    dataframe['HIGH'] = HIGH
    dataframe['PSAR']= SAR
    dataframe['EMA1H']= EMA1H
    dataframe['EMA1L']= EMA1L
    dataframe['EMA200']= EMA200
    dataframe['EMA15']= EMA15
    LAST_CLOSE=CLOSE.iloc[-1].astype(int)
    print("LAST_CLOSE:\n",LAST_CLOSE)
    
    # if int(LAST_CLOSE) <= 0 :
    #     dataframe['OPEN']= OPEN.apply(lambda x : (x*MULTIP)).astype(float)
    #     dataframe['CLOSE']= CLOSE.apply(lambda x : (x*MULTIP)).astype(float)
    #     dataframe['LOW']= LOW.apply(lambda x : (x*MULTIP)).astype(float)
    #     dataframe['HIGH']= HIGH.apply(lambda x : (x*MULTIP)).astype(float)
    #     dataframe['PSAR']= SAR.apply(lambda x : (x*MULTIP)).astype(float)
    #     dataframe['EMA1H']= EMA1H.apply(lambda x : (x*MULTIP)).astype(float)
    #     dataframe['EMA1L']= EMA1L.apply(lambda x : (x*MULTIP)).astype(float)
    #     dataframe['EMA200']= EMA200.apply(lambda x : (x*MULTIP)).astype(float)
    #     dataframe['EMA15']= EMA15.apply(lambda x : (x*MULTIP)).astype(float)
    
    
    # dataframe['DEMA40']= DEMA40.apply(lambda x : (x*MULTIP)).astype(int)
    # dataframe['VWAP']= DEMA40.apply(lambda x : (x*MULTIP)).astype(int)
    #print("dataframe :\n",dataframe.tail())
    # dataframe['DIFF_EMA1L_EMA15']= dataframe.apply(lambda x : x['EMA1L'] - x['EMA15'],axis = 1).astype(int)
    ##print("dataframe DIFF_EMA1L_EMA15:\n",dataframe['DIFF_EMA1L_EMA15'])
    dataframe['DIFF_EMA1H_EMA15']= dataframe.apply(lambda x : x['EMA1H'] - x['EMA15'],axis = 1).astype(float)
    ##print("dataframe DIFF_EMA1H_EMA15:\n",dataframe['DIFF_EMA1H_EMA15'])
    ###dataframe['DIFF_DEMA40_EMA15']= dataframe.apply(lambda x : x['DEMA40'] - x['EMA15'],axis = 1).astype(float)
    ##print("dataframe DIFF_DEMA40_EMA15:\n",dataframe['DIFF_DEMA40_EMA15'])
    dataframe['DIFF_EMA200_EMA15']= dataframe.apply(lambda x : x['EMA200'] - x['EMA15'],axis = 1).astype(float)
    ##print("dataframe DIFF_EMA200_EMA15:\n",dataframe['DIFF_EMA200_EMA15'])
    dataframe['DIFF_EMA200_EMA1L']= dataframe.apply(lambda x : x['EMA200'] - x['EMA1L'],axis = 1).astype(float)
    ##print("dataframe DIFF_EMA200_EMA15:\n",dataframe['DIFF_EMA200_EMA1L'])
    dataframe['DIFF_EMA200_EMA1H']= dataframe.apply(lambda x : x['EMA200'] - x['EMA1H'],axis = 1).astype(float)
    ##print("dataframe DIFF_EMA200_EMA15:\n",dataframe['DIFF_EMA200_EMA1H'])    
    dataframe['DIFF_EMA200_CLOSE']= dataframe.apply(lambda x : x['EMA200'] - x['CLOSE'],axis = 1).astype(float)
    ##print("dataframe DIFF_EMA200_CLOSE:\n",dataframe['DIFF_EMA200_CLOSE'].tail())   
    dataframe['DIFF_EMA1H_EMA1L']= dataframe.apply(lambda x : x['EMA1H'] - x['EMA1L'],axis = 1).astype(float)
    ##print("dataframe DIFF_EMA1H_EMA1L:\n",dataframe['DIFF_EMA1H_EMA1L'])    
    ##print("dataframe DIFF_DEMA40_EMA15:\n",dataframe['DIFF_DEMA40_EMA15'])
    #dataframe['DIFF_EMA200_EMA15_MOINS_1']=dataframe.DIFF_EMA200_EMA15.shift(periods=-1).dropna().astype(int)
    #dataframe['DIFF_EMA200_EMA1L_MOINS_1']=dataframe.DIFF_EMA200_EMA1L.shift(periods=-1).dropna().astype(int)
    #dataframe['DIFF_EMA200_EMA1H_MOINS_1']=dataframe.DIFF_EMA200_EMA1H.shift(periods=-1).dropna().astype(int)
    dataframe['DIFF_EMA15_CLOSE']= dataframe.apply(lambda x : x['EMA15'] - x['CLOSE'],axis = 1).astype(float)
    dataframe['DIFF_EMA1L_SAR']= dataframe.apply(lambda x : x['low'] - x['SAR'],axis = 1).astype(float)
    print("dataframe['DIFF_EMA1L_SAR'] :\n",dataframe['DIFF_EMA1L_SAR'].tail())
    dataframe['DIFF_EMA1H_SAR']= dataframe.apply(lambda x : x['high'] - x['SAR'],axis = 1).astype(float)
    print("dataframe['DIFF_EMA1H_SAR'] :\n",dataframe['DIFF_EMA1H_SAR'].tail())


    #Calcule d'un moyenne entre la DEMA40 et la EMA15
    # MA_DEMA40_EMA15=(DEMA40+dataframe['EMA15'])/2
    #df=dataframe.copy()
    df=dataframe
    # LAST_DEMA40=df.iloc[-1].DEMA40
    LAST_EMA15=df.iloc[-1].EMA15
    pd.set_option('display.max_rows', None)
    #print("dataframe :\n",dataframe.head(150))
    print("dataframe :\n",dataframe.tail())
    # exit()
    
    ###print("\nidx_DEMA40 :\n",idx_DEMA40)
    ###print("\ndataframe ILOC idx_DEMA40 > EMA15 :\n",dataframe.iloc[idx_DEMA40].tail())
    print("\ndataframe INDEX  min_EMA200 :\n",min_EMA200.index)
    print("\nDATE_DEB={} , DATE_FIN={}".format(DATE_DEB,DATE_FIN))
    print("\nDATE_DEB={} , DATE_FIN={}".format(0,dataframe_date.date.tail(1)))
    print("\nDATE_DEB={} , DATE_FIN={}".format(0,dataframe_date.index[-1]))
    #last_index=dataframe.index[-1]
    LAST_INDEX=len(dataframe)-1
    index_courant=0
    val_idx_min=dataframe['EMA200'].idxmin()
    val_idx_max=dataframe['EMA200'].idxmax()
    print("\ndataframe idxmin_EMA200 : ",val_idx_min)
    print("dataframe idxmax_EMA200 : ",val_idx_max)
    # print("\ndataframe ILOC Min_EMA200 :\n",dataframe[['date','EMA200']].loc[val_idx_min])
    # print("\ndataframe ILOC Max_EMA200 :\n",dataframe[['date','EMA200']].loc[val_idx_max])
    print("\ndataframe ILOC Min_EMA200 :\n",dataframe[['EMA200']].loc[val_idx_min])
    print("\ndataframe ILOC Max_EMA200 :\n",dataframe[['EMA200']].loc[val_idx_max])
    print("\ndataframe ILOC Min_EMA200 :",dataframe[['EMA200']].loc[val_idx_min].values.astype(float)[0])
    print("\ndataframe ILOC Max_EMA200 :",dataframe[['EMA200']].loc[val_idx_max].values.astype(float)[0])

    LISTE_INDEX=dataframe.tail(1).index.values.astype(int)[0]
    print("LISTE_INDEX=",LISTE_INDEX)
    print("LAST_INDEX=",dataframe_date.iloc[-1].date)

    if val_idx_min > 0 :
        NBR=1
    else:
        NBR=0
        
   # # global DIFF_EMA200_EMA15_MOINS_1
   # # DIFF_EMA200_EMA15_MOINS_1=dataframe.DIFF_EMA200_EMA15.loc[val_idx_min-NBR]
   #  global OPEN_MOINS_1
   #  OPEN_MOINS_1=dataframe['OPEN'].loc[val_idx_min-NBR]
   #  global CLOSE_MOINS_1
   #  CLOSE_MOINS_1=dataframe['CLOSE'].loc[val_idx_min-NBR]
   
   #  global DIFF_EMA200_EMA1L_MOINS_1
   #  DIFF_EMA200_EMA1L_MOINS_1=dataframe.DIFF_EMA200_EMA1L.loc[val_idx_min-NBR]
   #  global DIFF_EMA200_EMA1H_MOINS_1
   #  DIFF_EMA200_EMA1H_MOINS_1=dataframe.DIFF_EMA200_EMA1H.loc[val_idx_min-NBR]
    
   #  global DIFF_EMA200_EMA15
   #  DIFF_EMA200_EMA15=dataframe.DIFF_EMA200_EMA15.loc[val_idx_min]
   #  global DIFF_EMA200_EMA15_MOINS_1
   #  DIFF_EMA200_EMA15_MOINS_1=DIFF_EMA200_EMA15
    
   #  if val_idx_min > 0 :
   #      DIFF_EMA200_EMA15_MOINS_1=dataframe.DIFF_EMA200_EMA15.loc[val_idx_min-1]
    
   #  global DIFF_EMA200_EMA1L
   #  DIFF_EMA200_EMA1L=dataframe.DIFF_EMA200_EMA1L.loc[val_idx_min]
   #  global DIFF_EMA200_EMA1H
   #  DIFF_EMA200_EMA1H=dataframe.DIFF_EMA200_EMA1H.loc[val_idx_min] 
    
   #  global TRAME_EMA200_EMA15_MOINS_1
   #  TRAME_EMA200_EMA15_MOINS_1=dataframe.loc[val_idx_min-NBR]
   #  global TRAME_EMA200_EMA15
   #  TRAME_EMA200_EMA15=dataframe.loc[val_idx_min]
    
    #DERTERMINATION DU POINT D ACHAT
    global VARIATION_EMA200_EMA15
    # VARIATION_EMA200_EMA15=DIFF_EMA200_EMA15-DIFF_EMA200_EMA15_MOINS_1

    global CUMUL_TAILLE_BG_ROUGE
    global CUMUL_TAILLE_BG_VERTE
    global custom_info
    # print("TRAME_EMA200_EMA15_MOINS_1:",TRAME_EMA200_EMA15_MOINS_1)
    # print("DIFF_EMA200_EMA15_MOINS_1:",DIFF_EMA200_EMA15_MOINS_1)
    # print("TRAME_EMA200_EMA15:",TRAME_EMA200_EMA15)
    # print("DIFF_EMA200_EMA15:",DIFF_EMA200_EMA15)
    # print("\nVARIATION_EMA200_EMA15  :",VARIATION_EMA200_EMA15)
    print("dataframe:;\n",dataframe.tail())

    #print("\ndataframe DESS CROSS LAST_CROISEMENT_EMA200_DESS_CROSS_EMA15 ILOC idx_EMA200_EMA15  :\n",LAST_CROISEMENT_EMA200_DESS_CROSS_EMA15)
    # print("\ndataframe DESS CROSS  LAST_CROISEMENT_EMA200_DESS_CROSS_EMA15_N2 ILOC idx_EMA200_EMA15  :\n",LAST_CROISEMENT_EMA200_DESS_CROSS_EMA15_N2)
    # print("\ndataframe DESS CROSS DERNIERE VALEUR DE EMA15 POUR LE CROISEMENT ENTRE EMA1H ET EMA200  :\n",LAST_CROISEMENT_EMA200_DESS_CROSS_EMA1H)
    
    # SPEED=CALCULE_GRADIENT(dataframe,"EMA15")
    # positions = np.flatnonzero(SPEED)
    # print("positions:",positions)
    # print("LEN positions:",len(positions))
    # global SPEED_EMA15
    # if len(positions) == 0 :
    #     SPEED_EMA15=0
    # else:
    #     dataframe['SPEED_EMA15'] = SPEED
    #     dataframe = dataframe.dropna()
    #     dataframe['SPEED_EMA15']= dataframe['SPEED_EMA15'].apply(lambda x : (np.round(x,decimals = 2))).astype(int)
    #     SPEED_EMA15=dataframe[['SPEED_EMA15']].loc[val_idx_min].values.astype(int)

    
    # SPEED=CALCULE_GRADIENT(dataframe,"EMA1L")
    # positions = np.flatnonzero(SPEED)
    # print("positions:",positions)
    # print("LEN positions:",len(positions))
    # global SPEED_EMA1L
    # if len(positions) == 0 :
    #     SPEED_EMA1L=0
    # else:
    #     dataframe['SPEED_EMA1L'] = SPEED
    #     dataframe = dataframe.dropna()
    #     dataframe['SPEED_EMA1L']= dataframe['SPEED_EMA1L'].apply(lambda x : (np.round(x,decimals = 2))).astype(int)
    #     SPEED_EMA1L=dataframe[['SPEED_EMA1L']].loc[val_idx_min].values.astype(int)
        
    # SPEED=CALCULE_GRADIENT(dataframe,"EMA1H")
    # dataframe['SPEED_EMA1H'] = SPEED
    # positions = np.flatnonzero(SPEED)
    # print("positions:",positions)
    # print("LEN positions:",len(positions))
    # global SPEED_EMA1H
    # if len(positions) == 0 :
    #     SPEED_EMA1H=0
    # else:
    #     dataframe = dataframe.dropna()
    #     dataframe['SPEED_EMA1H']= dataframe['SPEED_EMA1H'].apply(lambda x : (np.round(x,decimals = 2))).astype(int)
    #     SPEED_EMA1H=dataframe[['SPEED_EMA1H']].loc[val_idx_min].values.astype(int)
    
    # SPEED=CALCULE_GRADIENT(dataframe,"EMA200")
    # dataframe['SPEED_EMA200'] = SPEED
    # positions = np.flatnonzero(SPEED)
    # print("positions:",positions)
    # print("LEN positions:",len(positions))
    # global SPEED_EMA200
    # if len(positions) == 0 :
    #     SPEED_EMA200=0
    # else:
    #     dataframe = dataframe.dropna()
    #     dataframe['SPEED_EMA200']= dataframe['SPEED_EMA200'].apply(lambda x : (np.round(x,decimals = 2))).astype(int)
    #     SPEED_EMA200=dataframe[['SPEED_EMA200']].loc[val_idx_min].values.astype(int)
    
    global DIFF_EMA200_CLOSE
    DIFF_EMA200_CLOSE=dataframe[['DIFF_EMA200_CLOSE']].loc[val_idx_min].values.astype(int)
    
    print("dataframe :\n",dataframe.tail())
    print("SORTIE populate_indicators")
    #exit()
    return dataframe
    
    ##print("LISTE_INDEX 1030=",dataframe.iloc[1030].date)
    #mask = (dataframe.iloc[1030].date >= dataframe.iloc[LAST_INDEX].date)
    ##mask = (dataframe.date >=  dataframe.iloc[1030].date )
    #mask = ("2021-04-21 17:00:00"  >= dataframe.iloc[LAST_INDEX].date)
    #print("MASK=",mask)
    #mask = (df[LISTE_INDEX] >= df.loc[self.INDEX_DEB].date) and (df[LISTE_INDEX] <= df.loc[LAST_INDEX].date)

def CALCULE_GRADIENT(dataframe,COURBE) :
    print("ENTRER GRADIENT_COURBE :"+COURBE)
    # dataframe['EMA1H']
    GRADIENT_COURBE = np.gradient(dataframe[COURBE])
    vel = np.array([ [GRADIENT_COURBE] for i in range(GRADIENT_COURBE.size)])
    #print("\nGRADIENT_"+COURBE:",GRADIENT_COURBE)
    print("\nGRADIENT_"+COURBE+":",nparray_tail(GRADIENT_COURBE,5))
    SPEED = np.sqrt(GRADIENT_COURBE * GRADIENT_COURBE)
    print("\nSPEED:",nparray_tail(SPEED,5))
    #print("\nSPEED:",SPEED)
    """
    result = array_1.copy()
    result[mask_array == 0] = 0  # Indexes all elements that are zero and sets them to zero.
    result = np.ma.array(array1.copy(), mask=mask_array)
    """
    result = SPEED.copy()
    result[SPEED == 0] = 0  # Indexes all elements that are zero and sets them to zero.
    SPEED = np.ma.array(SPEED.copy(), mask=SPEED)
    tangent = np.array([1/SPEED] * 2) #.transpose() * vel
    print("tangent :",tangent)
    print("SORTIE GRADIENT_COURBE")
    return SPEED
    #exit()

def nparray_tail(x: np.array, n:int):
    """
    Returns tail N elements of array.
    :param x: Numpy array.
    :param n: N elements to return on end.
    :return: Last N elements of array.
    """
    if n == 0:
        return x[0:0]  # Corner case: x[-0:] will return the entire array but tail(0) should return an empty array.
    else:
        return x[-n:]  # Normal case: last N elements of array

def populate_indicators_INIT() :
    data = pd.DataFrame(klines)
     # create colums name
    data.columns = ['time','open', 'high', 'low', 'close', 'volume','close_time', 'qav','num_trades','taker_base_vol','taker_quote_vol', 'ignore']
    print(data)
    btc_df=data
    #global dataframe
    btc_df.time = btc_df.time.apply(lambda d: str(d)[0:10])
    btc_df.time = btc_df.time.apply(lambda d: int(d))
    print("btc_df.time=",btc_df.time)
    btc_df['date'] = btc_df['time'].apply(lambda x: time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(x)))
    print(btc_df)
    btc_df['date']= pd.to_datetime(btc_df['date'])
    print(btc_df.info())
    print(btc_df['date'])
    btc_df.date= btc_df.date.apply(lambda d: d + pd.Timedelta(hours=TIMEDELTA))
    print("\nResult Lambda: \n",btc_df.time)
    print(btc_df[['date','open','high','low','close','volume']])
    dataframe=populate_indicators(btc_df)
    # exit(0)
    return dataframe


def INIT(dataframe) :

    global TYPE
    global POINT_ENTRE_EMA200
    global POINT_ENTRE_EMA15
    global POINT_ENTRE_EMA1H
    global DERNIER_POINT_VENTE
    global TYPE_EMA15
    global val_mask_idxmin
    global val_mask_idxmin_ORG
    global val_mask_idxmax_ORG
    global LISTE_ACHAT
    global LISTE_VENTE
    global LISTE_DERNIER_VENTE
    global LISTE_GLOBALE
    global LISTE_ACHAT_VENTE
    global last_index
    global dataframe_date

    
    try :
        last_index=len(dataframe.index)-1
        print("last_index=",last_index)
        mask = (dataframe_date.date <=  dataframe_date.loc[last_index].date )
        #mask = (dataframe.date)
        #print("MASK=",mask)
        
        val_mask_idxmin=dataframe['EMA200'].loc[mask].idxmin()
        val_mask_idxmin_ORG=val_mask_idxmin
        val_mask_idxmax=dataframe['EMA200'].loc[mask].idxmax()
        val_mask_idxmax_ORG=val_mask_idxmin
        LISTE_ACHAT = []
        LISTE_VENTE = []
        LISTE_DERNIER_VENTE = []
        LISTE_GLOBALE = []
        LISTE_ACHAT_VENTE= pd.DataFrame(columns=['DATE_ACHAT','ACHAT','DATE_VENTE','VENTE','GAIN','CUMUL'])
        
        POINT_ENTRE_EMA200 = 0
        POINT_ENTRE_EMA15=0
        POINT_ENTRE_EMA1H=0
        DERNIER_POINT_VENTE=0
        #global TYPE
        TYPE=""
        ORDER=""
        LAST_ORDER=""
        TYPE_EMA15=""
    except Exception as b:
        pass

def TRAITEMENT_ANTI_FLUCTUATION(dataframe,val_mask_idxmin) :
    global DERNIER_POINT_VENTE
    global NBR_PREC
    global NBR_PREC_LONG
    global VAL_NBR_PREC_LONG
    if DERNIER_POINT_VENTE == 0 :
        return

    # # NBR_PREC=5
    # NBR_PREC_LONG=VAL_NBR_PREC_LONG
    # if val_mask_idxmin-NBR_PREC < 0 :
    #    NBR_PREC=0 
    #    NBR_PREC_LONG=0

    # if val_mask_idxmin-NBR_PREC_LONG < 0 :
    #    NBR_PREC_LONG=0
    #    NBR_PREC=0 

       
    if val_mask_idxmin-NBR_PREC > 0 :
          NBR_PREC_LONG=NBR_PREC 
    print("NBR_PREC=",NBR_PREC)
    print("NBR_PREC_LONG=",NBR_PREC_LONG)
    
    last_index=len(dataframe)-1
    print("last_index=",last_index)
    if val_mask_idxmin >= last_index :
        val_mask_idxmin=last_index

        
    # if  DERNIER_POINT_VENTE == 1 :
    #    NBR_PREC=3
    #    NBR_PREC_LONG=VAL_NBR_PREC_LONG
       
    # if  (val_mask_idxmin-NBR_PREC < 0 ):
    #    NBR_PREC=0
       
    # if  (val_mask_idxmin-NBR_PREC_LONG < 0 ):
    #    NBR_PREC_LONG=0      
      
    while True :
       signal.signal(signal.SIGINT, PKILL)
       signal.signal(signal.SIGTERM, PKILL)
       VAL_EMA15_COURANT=dataframe.EMA15.loc[val_mask_idxmin].astype(int)
       VAL_EMA15_PRECEDENT=dataframe.EMA15.loc[val_mask_idxmin-NBR_PREC].astype(int)
       VAL_EMA15_PRECEDENT_LONG=dataframe.EMA15.loc[val_mask_idxmin-NBR_PREC_LONG].astype(int)
       VAL_EMA1H_COURANT=dataframe.EMA1H.loc[val_mask_idxmin].astype(int)
       VAL_EMA200_COURANT=dataframe.EMA200.loc[val_mask_idxmin].astype(int)
       
       print("\nDEBUT TRAITEMENT ANTI FLUCTUATION")
       print("VAL_EMA15_COURANT=",VAL_EMA15_COURANT)
       print("VAL_EMA15_PRECEDENT_LONG=",VAL_EMA15_PRECEDENT_LONG)
       print("VAL_EMA15_PRECEDENT=",VAL_EMA15_PRECEDENT)
       #if (VAL_EMA15_COURANT-VAL_EMA15_PRECEDENT_LONG > 0 ) :
       DETECTION_FRONT(dataframe,val_mask_idxmin)
       #if (FRONT_MONTANT_EMA1H == 0 ) and (FRONT_MONTANT_COURT_EMA1H == 1 ) :
       if (FRONT_MONTANT_EMA1H == 0 ) and (FRONT_MONTANT_COURT_EMA1H == 1 ) and (int(VAL_EMA1H_COURANT <= VAL_EMA200_COURANT) ):
       #if (VAL_EMA15_COURANT-VAL_EMA15_PRECEDENT > 0 ) :
           print("TRAITEMENT ANTI FLUCTUATION")
           print("\nINDEX COURANT=\n",dataframe.loc[val_mask_idxmin])
           DERNIER_POINT_VENTE=0
           break
       else:
           print("RECUPERATION DERNIERE BOUGIE TRAITEMENT ANTI FLUCTUATION")
          # if  FLAG_BEST_NBR_TAILLE_BG == 0 :
           last_index=len(dataframe)-1
           print("last_index=",last_index)
           if val_mask_idxmin >= last_index :
             val_mask_idxmin=last_index
             break
           else:
             val_mask_idxmin+=1
         #  else:
         #      DERNIER_POINT_VENTE=1
         #      break
       #if val_mask_idxmin > last_index : #A COMMENTER EN VRAI TRAIDING
           #A COMMENTER EN VRAI TRAIDING

       global TYPE
       if (TYPE == "HAUT_FINALE_EMA200") and ( int(VAL_EMA1H_COURANT - VAL_EMA200_COURANT) <= -50) :
           print("\nPOINT HAUT ON QUITTE LA COURBE")
           #print("\nINDEX COURANT=\n",dataframe.loc[val_mask_idxmin])
       print("FIN TRAITEMENT ANTI FLUCTUATION\n")
       #exit()
       
def MSG_COMMAND(ORDER):
    #import requests
    global symbol
    import json
    symbol=custom_info["symbol"] 
    #PAIR=self.custom_info["PAIR"]
    print("ENTRER DANS MSG_COMMAND  : ",ORDER)
    print("DANS MSG_COMMAND symbol : ",symbol)
    MSG="DANS TRADING  RECEPTION DU MESSAGE POUR LA  PAIR: " + str(symbol) + " DE L ORDRE:\n " + str(ORDER)
    VAR="https://api.telegram.org/bot1703103353:AAFTnMpkee5ea_2hfVEYPprgi7D5kn-A57s/sendMessage?chat_id=1884218992=&text=" + MSG 
    VAR_SARAH="https://api.telegram.org/bot5116065198:AAHfOuF3QfT5w26MvAt0tw8726znZK7kruc/sendMessage?chat_id=2032377684=&text=" + MSG
    r = requests.get(VAR_SARAH) 
    r = requests.get(VAR) 
    
def SYNCHRONISATION_INDICE(dataframe,val_mask_idxmin) : 
    #try:
        print("\nENTRER DANS SYNCHRONISATION_INDICE")
        
        #DEBUT RECHERCHE CROISEMENT DIFF_EMA1L_EMA15 GOLDEN CROSS
        global idx_EMA200_EMA15
        global idx_EMA200_EMA1L
        global idx_EMA200_EMA1H
        global idx_SUP_EMA200_EMA15
        global idx_SUP_EMA200_EMA1L
        global idx_SUP_EMA200_EMA1H
        global idx_INF_EMA200_EMA15
        global idx_INF_EMA200_EMA1L
        global idx_INF_EMA200_EMA1H
        global idx_SUP_EMA1H_EMA1L
    
        mask_idx=(dataframe.date <= dataframe.loc[val_mask_idxmin].date)    
        idx_EMA200_CLOSE=np.argwhere(np.diff(np.sign(dataframe['DIFF_EMA200_CLOSE'].loc[mask_idx])) > 0).reshape(-1) + 0
        idx_EMA200_EMA15=np.argwhere(np.diff(np.sign(dataframe['DIFF_EMA200_EMA15'].loc[mask_idx])) > 0).reshape(-1) + 0
        idx_EMA200_EMA1L=np.argwhere(np.diff(np.sign(dataframe['DIFF_EMA200_EMA1L'].loc[mask_idx])) > 0).reshape(-1) + 0
        idx_EMA200_EMA1H=np.argwhere(np.diff(np.sign(dataframe['DIFF_EMA200_EMA1H'].loc[mask_idx])) > 0).reshape(-1) + 0
        idx_EMA1H_EMA1L=np.argwhere(np.diff(np.sign(dataframe['DIFF_EMA1H_EMA1L'].loc[mask_idx])) > 0).reshape(-1) + 0
        """
        print("np.diff(np.sign(dataframe['DIFF_EMA200_EMA15'])) < 0):",np.diff(np.sign(dataframe['DIFF_EMA200_EMA15'])) == 0)
        print("dataframe['DIFF_EMA200_EMA15'] == 0 :\n",(dataframe['DIFF_EMA200_EMA15'] == 0))
        print("dataframe['DIFF_EMA200_EMA15'].where(dataframe['DIFF_EMA200_EMA15'] == 0) :\n",dataframe['DIFF_EMA200_EMA15'].where(dataframe['DIFF_EMA200_EMA15'] == 0).dropna())
        print("dataframe['DIFF_EMA200_EMA15'].where(dataframe['DIFF_EMA200_EMA15'] == 0) :\n",dataframe['DIFF_EMA200_EMA15'].where(dataframe['DIFF_EMA200_EMA15'] == 0).where(dataframe.index.values < 900 ).dropna())
        exit()
        """
        print("val_mask_idxmin:",val_mask_idxmin)
        #exit()
        """
        ###idx_SUP_DEMA40=np.pad(np.diff(np.array(dataframe["DIFF_DEMA40_EMA15"]).astype(int)), (1,0), 'constant', constant_values = (0,))
        idx_SUP_EMA200_CLOSE=np.pad(np.diff(np.array(dataframe['DIFF_EMA200_EMA15'].loc[mask_idx]).astype(int)), (1,0), 'constant', constant_values = (0,))
        idx_SUP_EMA200_EMA15=np.pad(np.diff(np.array(dataframe['DIFF_EMA200_EMA15'].loc[mask_idx]).astype(int)), (1,0), 'constant', constant_values = (0,))
        idx_SUP_EMA200_EMA1L=np.pad(np.diff(np.array(dataframe['DIFF_EMA200_EMA1L'].loc[mask_idx]).astype(int)), (1,0), 'constant', constant_values = (0,))
        idx_SUP_EMA200_EMA1H=np.pad(np.diff(np.array(dataframe['DIFF_EMA200_EMA1H'].loc[mask_idx]).astype(int)), (1,0), 'constant', constant_values = (0,))
        idx_SUP_EMA1H_EMA1L=np.pad(np.diff(np.array(dataframe['DIFF_EMA1H_EMA1L'].loc[mask_idx]).astype(int)), (1,0), 'constant', constant_values = (0,))
    
        idx_INF_EMA200_CLOSE=np.argwhere(np.diff(np.sign(dataframe['DIFF_EMA200_EMA15'].loc[mask_idx])) < 0).reshape(-1) + 0
        idx_INF_EMA200_EMA15=np.argwhere(np.diff(np.sign(dataframe['DIFF_EMA200_EMA15'].loc[mask_idx])) < 0).reshape(-1) + 0
        idx_INF_EMA200_EMA1L=np.argwhere(np.diff(np.sign(dataframe['DIFF_EMA200_EMA1L'].loc[mask_idx])) < 0).reshape(-1) + 0
        idx_INF_EMA200_EMA1H=np.argwhere(np.diff(np.sign(dataframe['DIFF_EMA200_EMA1H'].loc[mask_idx])) < 0).reshape(-1) + 0
        idx_INF_EMA200_EMA1H=np.argwhere(np.diff(np.sign(dataframe['DIFF_EMA1H_EMA1L'].loc[mask_idx])) < 0).reshape(-1) + 0
    
        DATE_COURANT=dataframe.date.loc[val_mask_idxmin]
        print("DATE_COURANT",DATE_COURANT)
    
        global LAST_CROISEMENT_EMA200_GOLDEN_CROSS_CLOSE
        global LAST_CROISEMENT_EMA200_GOLDEN_CROSS_CLOSE_INDEX
        global LAST_CROISEMENT_EMA200_GOLDEN_CROSS_CLOSE_TAIL
        #LAST_CROISEMENT_EMA200_GOLDEN_CROSS_CLOSE_TAIL=dataframe[['date','DIFF_EMA200_CLOSE','DIFF_EMA200_EMA15']].where(dataframe['EMA15']-dataframe['EMA200'] < 0).dropna() #.iloc[idx_EMA200_CLOSE]
        #LAST_CROISEMENT_EMA200_GOLDEN_CROSS_CLOSE_TAIL.where([LAST_CROISEMENT_EMA200_GOLDEN_CROSS_CLOSE_TAIL.index.values <= val_mask_idxmin])
        LAST_CROISEMENT_EMA200_GOLDEN_CROSS_CLOSE_TAIL=dataframe.iloc[idx_EMA200_CLOSE].tail()
        LAST_CROISEMENT_EMA200_GOLDEN_CROSS_CLOSE=dataframe.where(dataframe['DIFF_EMA200_CLOSE'] == 0).iloc[-1]
        LAST_CROISEMENT_EMA200_GOLDEN_CROSS_CLOSE_INDEX=dataframe.where(dataframe['DIFF_EMA200_CLOSE'] == 0).index[-1]
        print("\ndataframe GOLDEN CROSS TAIL ILOC idx_EMA200_CLOSE > CLOSE :\n",LAST_CROISEMENT_EMA200_GOLDEN_CROSS_CLOSE_TAIL)
        #exit()

        """
        #exit()
        if len(idx_EMA200_EMA15) != 0 :
            #LAST CROISEMENT EMA200 EMA15
            print("\nLAST CROISEMENT EMA200 EMA15")
            print("idx_EMA200_EMA15:",idx_EMA200_EMA15)
            print("len(idx_EMA200_EMA15):",len(idx_EMA200_EMA15))
            global LAST_CROISEMENT_EMA200_GOLDEN_CROSS_EMA15
            global LAST_CROISEMENT_EMA200_GOLDEN_CROSS_EMA15_INDEX
            global LAST_CROISEMENT_EMA200_GOLDEN_CROSS_EMA15_TAIL
            LAST_CROISEMENT_EMA200_GOLDEN_CROSS_EMA15_TAIL=dataframe.iloc[idx_EMA200_EMA15].tail()
            LAST_CROISEMENT_EMA200_GOLDEN_CROSS_EMA15=dataframe.iloc[idx_EMA200_EMA15].iloc[-1]
            LAST_CROISEMENT_EMA200_GOLDEN_CROSS_EMA15_INDEX=dataframe.iloc[idx_EMA200_EMA15].index[-1]
            print("\ndataframe GOLDEN CROSS TAIL ILOC idx_EMA200_EMA15 > EMA15 :\n",LAST_CROISEMENT_EMA200_GOLDEN_CROSS_EMA15.tail())
            print("\ndataframe GOLDEN CROSS DERNIERE LIGNE ILOC idx_EMA200_EMA15  :\n",LAST_CROISEMENT_EMA200_GOLDEN_CROSS_EMA15)
            print("\ndataframe GOLDEN CROSS DATE DERNIERE VALEUR DE EMA15 POUR LE CROISEMENT ENTRE EMA15 ET EMA200  :",LAST_CROISEMENT_EMA200_GOLDEN_CROSS_EMA15.date)
            print("\ndataframe GOLDEN CROSS DERNIERE VALEUR DE EMA15 POUR LE CROISEMENT ENTRE EMA15 ET EMA200  :",LAST_CROISEMENT_EMA200_GOLDEN_CROSS_EMA15.EMA15)
            print("\ndataframe GOLDEN CROSS INDEX ILOC idx_EMA200_EMA15 > EMA15 :",LAST_CROISEMENT_EMA200_GOLDEN_CROSS_EMA15_INDEX)
            #print("\ndataframe GOLDEN CROSS ILOC idx_SUP_EMA200_EMA15 > EMA15 :\n",dataframe.iloc[idx_SUP_EMA200_EMA15].tail())
     
        
            # VALEUR MAX EMA200
            print("\nVALEUR MAX EMA200")
            val_idx_min=dataframe['EMA200'].idxmin()
            val_idx_max=dataframe['EMA200'].idxmax()
            print("\ndataframe idxmin_EMA200 : ",val_idx_min)
            print("dataframe idxmax_EMA200 : ",val_idx_max)
            print("\ndataframe ILOC Min_EMA200 :\n",dataframe[['date','EMA200']].loc[val_idx_min])
            print("\ndataframe ILOC Max_EMA200 :\n",dataframe[['date','EMA200']].loc[val_idx_max])
            print("\ndataframe ILOC Min_EMA200 :",dataframe[['EMA200']].loc[val_idx_min].values.astype(int)[0])
            print("\ndataframe ILOC Max_EMA200 :",dataframe[['EMA200']].loc[val_idx_max].values.astype(int)[0])  
            DATE_Max_EMA200=dataframe[['date']].loc[val_idx_max][0]
            print("\nDATE_Max_EMA2000 :",DATE_Max_EMA200)  
            print("DATE_Max_EMA200 et LAST_CROISEMENT_EMA200_GOLDEN_CROSS_EMA15.date")
            print("{} et {}".format(DATE_Max_EMA200, LAST_CROISEMENT_EMA200_GOLDEN_CROSS_EMA15.date))
            DIFF_DATE_Max_EMA200_LAST_CROISEMENT_EMA200_GOLDEN_CROSS_EMA15_date=DATE_Max_EMA200 < LAST_CROISEMENT_EMA200_GOLDEN_CROSS_EMA15.date
            print("DIFF_DATE_Max_EMA200_LAST_CROISEMENT_EMA200_GOLDEN_CROSS_EMA15_date: ",DIFF_DATE_Max_EMA200_LAST_CROISEMENT_EMA200_GOLDEN_CROSS_EMA15_date)
            if DATE_Max_EMA200 < LAST_CROISEMENT_EMA200_GOLDEN_CROSS_EMA15.date :
                print("DATE_Max_EMA200 < LAST_CROISEMENT_EMA200_GOLDEN_CROSS_EMA15.date")
                print("SOMMET BAS EMA200")
                global val_mask_idxmin_ORG
                val_mask_idxmin_ORG=LAST_CROISEMENT_EMA200_GOLDEN_CROSS_EMA15_INDEX
            else:
                print("DATE_Max_EMA200 > LAST_CROISEMENT_EMA200_GOLDEN_CROSS_EMA15.date")
                print("POINT SOMMET HAUT EMA200")
                global POINT_SOMMET_HAUT_EMA200
                POINT_SOMMET_HAUT_EMA200=1
            ##exit()    
            
            if len(idx_EMA200_EMA15) == 0 :
                idx_EMA200_EMA15=val_mask_idxmin
                #LAST_CROISEMENT_EMA200_GOLDEN_CROSS_EMA15=dataframe.DIFF_EMA200_EMA15.iloc[val_mask_idxmin].astype(int)
                LAST_CROISEMENT_EMA200_GOLDEN_CROSS_EMA15=dataframe.EMA200.iloc[val_mask_idxmin].astype(int)
        """    
        print("dataframe.date.loc[idx_EMA200_EMA15]:",dataframe.date.loc[idx_EMA200_EMA15])
        #print("dataframe.date.loc[idx_EMA200_EMA15].tail():",dataframe.date.loc[idx_EMA200_EMA15].tail())
        #print("dataframe.date.loc[idx_EMA200_EMA15].iloc[-1]:",dataframe.date.loc[idx_EMA200_EMA15].iloc[-1])
        global DIFF_EMA200_EMA15_MOINS_1
        global DIFF_EMA200_EMA15
        global SPEED_EMA15
        global DIFF_EMA200_CLOSE
        global VAL_EMA15_PRECEDENT_LONG
        global POINT_ENTRE_EMA200
        DIFF_EMA200_EMA15=dataframe.DIFF_EMA200_EMA15.iloc[val_mask_idxmin].astype(int)
        DIFF_EMA200_EMA15_MOINS_1=dataframe.DIFF_EMA200_EMA15.iloc[val_mask_idxmin-1].astype(int)
        DIFF_EMA200_CLOSE=dataframe.DIFF_EMA200_CLOSE.iloc[val_mask_idxmin].astype(int)
        DIFF_EMA200_CLOSE_MOINS_1=dataframe.DIFF_EMA200_CLOSE.iloc[val_mask_idxmin-1].astype(int)
        print("DATE_COURANT",DATE_COURANT)
        print("SPEED_EMA15",SPEED_EMA15)
        print("DIFF_EMA200_EMA15_MOINS_1:",DIFF_EMA200_EMA15_MOINS_1)
        print("DIFF_EMA200_EMA15:",DIFF_EMA200_EMA15)
        print("DIFF_EMA200_CLOSE_MOINS_1:",DIFF_EMA200_CLOSE_MOINS_1)
        print("DIFF_EMA200_CLOSE:",DIFF_EMA200_CLOSE)
        #if  DIFF_EMA200_EMA15_MOINS_1 == 0 and DIFF_EMA200_EMA15 < 0 :
        #if  DIFF_EMA200_CLOSE_MOINS_1 <= 0 and DIFF_EMA200_CLOSE == 0 :
        #if dataframe.EMA200.iloc[val_mask_idxmin].astype(int) == dataframe.CLOSE.iloc[val_mask_idxmin].astype(int) and DIFF_EMA200_EMA15 < 0 : #and (SPEED_EMA15 == 0) :
        if  DIFF_EMA200_CLOSE >= 0  and  DIFF_EMA200_CLOSE <= 10 and POINT_ENTRE_EMA200 == 0 :#and val_mask_idxmin >= 200 :
        #if  DIFF_EMA200_EMA15 >= 0  and  DIFF_EMA200_EMA15 <=20 and  DIFF_EMA200_CLOSE == 0 :# and val_mask_idxmin >= 200 :
        #if  DIFF_EMA200_EMA15 == 0  : # and  DIFF_EMA200_EMA15 <= 10  and val_mask_idxmin >= 200 :
            LAST_CROISEMENT_EMA200_GOLDEN_CROSS_EMA15=dataframe.EMA200.iloc[val_mask_idxmin].astype(int)
            #LAST_CROISEMENT_EMA200_GOLDEN_CROSS_EMA15_INDEX=dataframe.iloc[val_mask_idxmin].astype(int)
            VAL_EMA15_PRECEDENT_LONG=int(LAST_CROISEMENT_EMA200_GOLDEN_CROSS_EMA15.astype(int))
            TRAME_COURANT=dataframe.iloc[val_mask_idxmin]
            print("DATE_COURANT CROISEMENT",TRAME_COURANT)
            print("CROISEMENT DESS CROSS")
            DATE_COURANT=dataframe.date.loc[val_mask_idxmin]
            MESSAGE="CROISEMENT DESS CROSS: "+ str(DATE_COURANT) + "\nval_mask_idxmin: "+ str(val_mask_idxmin) + "\nLAST_CROISEMENT_EMA200_GOLDEN_CROSS_EMA15: "+ str(LAST_CROISEMENT_EMA200_GOLDEN_CROSS_EMA15)
            ###MSG_COMMAND(MESSAGE)
            #exit()            

        #if  DIFF_EMA200_CLOSE_MOINS_1 > 0 and DIFF_EMA200_CLOSE < 0  and val_mask_idxmin >= 200 :
        if  DIFF_EMA200_CLOSE <= 0  and  DIFF_EMA200_CLOSE >= -10 :#and val_mask_idxmin >= 200 :
        #if  DIFF_EMA200_EMA15 <= 0  and  DIFF_EMA200_EMA15 >= -10 and val_mask_idxmin >= 200 :
        #if dataframe.EMA200.iloc[val_mask_idxmin].astype(int) == dataframe.CLOSE.iloc[val_mask_idxmin].astype(int) and DIFF_EMA200_EMA15 < 0 : #and (SPEED_EMA15 == 0) :
            TRAME_COURANT=dataframe.iloc[val_mask_idxmin]
            print("DATE_COURANT CROISEMENT",TRAME_COURANT)
            print("CROISEMENT GOLDEN CROSS")
            DATE_COURANT=dataframe.date.loc[val_mask_idxmin]
            MESSAGE="CROISEMENT GOLDEN CROSS: "+ str (DATE_COURANT)
            #MSG_COMMAND(MESSAGE)
            #exit()
        #if val_mask_idxmin >= 200 :
        #    exit()

        
        global LAST_CROISEMENT_EMA200_GOLDEN_CROSS_EMA1L
        global LAST_CROISEMENT_EMA200_GOLDEN_CROSS_EMA1L_INDEX
        global LAST_CROISEMENT_EMA200_GOLDEN_CROSS_EMA1L_TAIL
        LAST_CROISEMENT_EMA200_GOLDEN_CROSS_EMA1L_TAIL=dataframe.iloc[idx_EMA200_EMA1L].tail()
        if DATE_COURANT >= dataframe.date.loc[idx_EMA200_EMA1L].iloc[-1] :
            LAST_CROISEMENT_EMA200_GOLDEN_CROSS_EMA1L=dataframe.iloc[idx_EMA200_EMA1L].iloc[-1]
            LAST_CROISEMENT_EMA200_GOLDEN_CROSS_EMA1L_INDEX=dataframe.iloc[idx_EMA200_EMA1L].index[-1]
            print("\ndataframe GOLDEN CROSS DERNIERE LIGNE ILOC idx_EMA200_EMA1L  :\n",LAST_CROISEMENT_EMA200_GOLDEN_CROSS_EMA1L)
            print("\ndataframe GOLDEN CROSS DERNIERE VALEUR DE EMA1L POUR LE CROISEMENT ENTRE EMA1L ET EMA200  :",LAST_CROISEMENT_EMA200_GOLDEN_CROSS_EMA1L.EMA1L)
            print("\ndataframe GOLDEN CROSS TAIL ILOC idx_EMA200_EMA1L > EMA1L :\n",LAST_CROISEMENT_EMA200_GOLDEN_CROSS_EMA1L_TAIL)
            print("\ndataframe GOLDEN CROSS INDEX ILOC idx_EMA200_EMA1L > EMA1L :",LAST_CROISEMENT_EMA200_GOLDEN_CROSS_EMA1L_INDEX)
            print("\ndataframe GOLDEN CROSS ILOC idx_SUP_EMA200_EMA1L > EMA1L :\n",dataframe.iloc[idx_SUP_EMA200_EMA1L].tail())
            
        global LAST_CROISEMENT_EMA200_GOLDEN_CROSS_EMA1H
        global LAST_CROISEMENT_EMA200_GOLDEN_CROSS_EMA1H_INDEX
        global LAST_CROISEMENT_EMA200_GOLDEN_CROSS_EMA1H_TAIL
        LAST_CROISEMENT_EMA200_GOLDEN_CROSS_EMA1H_TAIL=dataframe.iloc[idx_EMA200_EMA1H].tail()
        LAST_CROISEMENT_EMA200_GOLDEN_CROSS_EMA1H=dataframe.iloc[idx_EMA200_EMA1H].iloc[-1]
        LAST_CROISEMENT_EMA200_GOLDEN_CROSS_EMA1H_INDEX=dataframe.iloc[idx_EMA200_EMA1H].index[-1]
        print("\ndataframe TAIL ILOC idx_EMA200_EMA1H > EMA1H :\n",LAST_CROISEMENT_EMA200_GOLDEN_CROSS_EMA1H_TAIL)
        print("\ndataframe INDEX ILOC idx_EMA200_EMA1H > EMA1H :",LAST_CROISEMENT_EMA200_GOLDEN_CROSS_EMA1H_INDEX)
        print("\ndataframe DERNIERE LIGNE ILOC idx_EMA200_EMA1H  :\n",LAST_CROISEMENT_EMA200_GOLDEN_CROSS_EMA1H)
        print("\ndataframe DERNIERE VALEUR DE EMA1H POUR LE CROISEMENT ENTRE EMA1H ET EMA200  :",LAST_CROISEMENT_EMA200_GOLDEN_CROSS_EMA1H.EMA1H)
        print("\ndataframe ILOC idx_SUP_EMA200_EMA1L > EMA1H :\n",dataframe.iloc[idx_SUP_EMA200_EMA1L].tail())
    
           
        # CROISEMENT DIFF_EMA1H_EMA1L == 0 DESS CROSS
        global LAST_CROISEMENT_EMA1H_EMA1L_DESS_CROSS
        global LAST_CROISEMENT_EMA1H_EMA1L_DESS_CROSS_INDEX
        global LAST_CROISEMENT_EMA1H_EMA1L_DESS_CROSS_TAIL
        LAST_CROISEMENT_EMA1H_EMA1L_DESS_CROSS_TAIL=dataframe.iloc[idx_INF_EMA200_EMA1H].tail()
        LAST_CROISEMENT_EMA1H_EMA1L_DESS_CROSS=dataframe.iloc[idx_INF_EMA200_EMA1H].iloc[-1]
        LAST_CROISEMENT_EMA1H_EMA1L_DESS_CROSS_INDEX=dataframe.iloc[idx_INF_EMA200_EMA1H].index[-1]
        print("\ndataframe TAIL ILOC idx_INF_EMA200_EMA1H  :\n",LAST_CROISEMENT_EMA1H_EMA1L_DESS_CROSS_TAIL)
        print("\ndataframe INDEX ILOC idx_EMA1H_EMA1L :",LAST_CROISEMENT_EMA1H_EMA1L_DESS_CROSS_INDEX)
        print("\ndataframe DERNIERE LIGNE ILOC idx_EMA1H_EMA1L  :",LAST_CROISEMENT_EMA1H_EMA1L_DESS_CROSS)
        print("\ndataframe DERNIERE VALEUR DE EMA1H POUR LE CROISEMENT ENTRE EMA1H ET_EMA1L EN DESS CROSS :",LAST_CROISEMENT_EMA1H_EMA1L_DESS_CROSS.EMA1H)
        print("\ndataframe ILOC DIFF_EMA1H_EMA1L=0 :\n",dataframe.where(dataframe['DIFF_EMA1H_EMA1L'] == 0).sort_index().dropna().drop_duplicates().tail())
        print("\ndataframe ILOC idx_SUP_EMA1H_EMA1L :\n",dataframe.iloc[idx_SUP_EMA1H_EMA1L].where(dataframe['DIFF_EMA1H_EMA1L'] == 0).sort_index().dropna().drop_duplicates().tail())
        print("\ndataframe ILOC idx_INF_EMA200_EMA1H  :\n",dataframe.iloc[idx_INF_EMA200_EMA1H].sort_index().dropna().drop_duplicates().tail())
        #exit()
        
            #DEBUT RECHERCHE CROISEMENT DIFF_EMA1L_EMA15 DESS CROSS
    
        global LAST_CROISEMENT_EMA200_DESS_CROSS_EMA15
        global LAST_CROISEMENT_EMA200_DESS_CROSS_EMA15_INDEX
        global LAST_CROISEMENT_EMA200_DESS_CROSS_EMA15_TAIL
        LAST_CROISEMENT_EMA200_DESS_CROSS_EMA15_TAIL=dataframe.iloc[idx_INF_EMA200_EMA15].tail()
        print("\ndataframe DESS CROSS TAIL ILOC idx_EMA200_EMA15  :\n",LAST_CROISEMENT_EMA200_DESS_CROSS_EMA15_TAIL)
    
        if DATE_COURANT >= dataframe.date.loc[idx_INF_EMA200_EMA15].iloc[-1] and val_mask_idxmin >= 2  :
            LAST_CROISEMENT_EMA200_DESS_CROSS_EMA15=dataframe.iloc[idx_INF_EMA200_EMA15].iloc[-1]
            LAST_CROISEMENT_EMA200_DESS_CROSS_EMA15_INDEX=dataframe.iloc[idx_INF_EMA200_EMA15].index[-1]
            print("\ndataframe DESS CROSS INDEX ILOC idx_EMA200_EMA15  :",LAST_CROISEMENT_EMA200_DESS_CROSS_EMA15_INDEX)
            #LAST_CROISEMENT_EMA200_DESS_CROSS_EMA15_N2=dataframe.iloc[idx_INF_EMA200_EMA15].iloc[-2]
            #print("\ndataframe DESS CROSS  LAST_CROISEMENT_EMA200_DESS_CROSS_EMA15_N2 ILOC idx_EMA200_EMA15  :\n",LAST_CROISEMENT_EMA200_DESS_CROSS_EMA15_N2)
            print("\ndataframe DESS CROSS LAST_CROISEMENT_EMA200_DESS_CROSS_EMA15 ILOC idx_EMA200_EMA15  :\n",LAST_CROISEMENT_EMA200_DESS_CROSS_EMA15)
            print("\ndataframe DESS CROSS DERNIERE VALEUR DE EMA15 POUR LE CROISEMENT ENTRE EMA15 ET EMA200  :",LAST_CROISEMENT_EMA200_DESS_CROSS_EMA15.EMA15)
            print("\ndataframe DESS CROSS ILOC idx_INF_EMA200 > EMA15 :\n",dataframe.iloc[idx_INF_EMA200_EMA15].where(dataframe.DIFF_EMA200_EMA15 != 0).dropna().tail())
            
        global LAST_CROISEMENT_EMA200_DESS_CROSS_EMA1L
        global LAST_CROISEMENT_EMA200_DESS_CROSS_EMA1L_INDEX
        global LAST_CROISEMENT_EMA200_DESS_CROSS_EMA1L_TAIL
        LAST_CROISEMENT_EMA200_DESS_CROSS_EMA1L_TAIL=dataframe.iloc[idx_EMA200_EMA1L].tail()
        LAST_CROISEMENT_EMA200_DESS_CROSS_EMA1L=dataframe.iloc[idx_EMA200_EMA1L].iloc[-1]
        LAST_CROISEMENT_EMA200_DESS_CROSS_EMA1L_INDEX=dataframe.iloc[idx_EMA200_EMA1L].index[-1]
        print("\ndataframe DESS CROSS TAIL ILOC idx_EMA200_EMA1L > EMA1L :\n",LAST_CROISEMENT_EMA200_DESS_CROSS_EMA1L_TAIL)
        print("\ndataframe DESS CROSS INDEX ILOC idx_EMA200_EMA1L > EMA1L :",LAST_CROISEMENT_EMA200_DESS_CROSS_EMA1L_INDEX)
        print("\ndataframe DESS CROSS DERNIERE LIGNE ILOC idx_EMA200_EMA1L  :\n",LAST_CROISEMENT_EMA200_DESS_CROSS_EMA1L)
        print("\ndataframe DESS CROSS DERNIERE VALEUR DE EMA1L POUR LE CROISEMENT ENTRE EMA1L ET EMA200  :\n",LAST_CROISEMENT_EMA200_DESS_CROSS_EMA1L.EMA1L)
        print("\ndataframe DESS CROSS ILOC idx_INF_EMA200 > EMA1L :\n",dataframe.iloc[idx_INF_EMA200_EMA1L].tail())
        
        global LAST_CROISEMENT_EMA200_DESS_CROSS_EMA1H
        global LAST_CROISEMENT_EMA200_DESS_CROSS_EMA1H_INDEX
        global LAST_CROISEMENT_EMA200_DESS_CROSS_EMA1H_TAIL
        LAST_CROISEMENT_EMA200_DESS_CROSS_EMA1H_TAIL=dataframe.iloc[idx_EMA200_EMA1H].tail()
        LAST_CROISEMENT_EMA200_DESS_CROSS_EMA1H=dataframe.iloc[idx_EMA200_EMA1H].iloc[-1]
        LAST_CROISEMENT_EMA200_DESS_CROSS_EMA1H_INDEX=dataframe.iloc[idx_EMA200_EMA1H].index[-1]
        print("\ndataframe DESS CROSS TAIL ILOC idx_EMA200_EMA1H > EMA1H :\n",LAST_CROISEMENT_EMA200_DESS_CROSS_EMA1H_TAIL)
        print("\ndataframe DESS CROSS INDEX ILOC idx_EMA200_EMA1H > EMA1H :",LAST_CROISEMENT_EMA200_DESS_CROSS_EMA1H_INDEX)
        print("\ndataframe DESS CROSS DERNIERE LIGNE ILOC idx_EMA200_EMA1H  :\n",LAST_CROISEMENT_EMA200_DESS_CROSS_EMA1H)
        print("\ndataframe DESS CROSS DERNIERE VALEUR DE EMA1H POUR LE CROISEMENT ENTRE EMA1H ET EMA200  :\n",LAST_CROISEMENT_EMA200_DESS_CROSS_EMA1H.EMA1H)
        print("\ndataframe DESS CROSS ILOC idx_INF_EMA200 > EMA1H :\n",dataframe.iloc[idx_INF_EMA200_EMA1H].tail())
        #exit()
    
         
        global MASK_idx_EMA200_EMA15
        global MASK_idx_EMA200_EMA1L
        global MASK_idx_EMA200_EMA1H
        global MASK_idx_SUP_EMA200_EMA15
        global MASK_idx_SUP_EMA200_EMA1L
        global MASK_idx_SUP_EMA200_EMA1H
        global MASK_idx_INF_EMA200_EMA15
        global MASK_idx_INF_EMA200_EMA1L
        global MASK_idx_INF_EMA200_EMA1H
        global MASK_idx_SUP_EMA1H_EMA1L  
        
        global NEW_idx_EMA200_EMA15
        global NEW_idx_EMA200_EMA1L
        global NEW_idx_EMA200_EMA1H
        global NEW_idx_SUP_EMA200_EMA15
        global NEW_idx_SUP_EMA200_EMA1L
        global NEW_idx_SUP_EMA200_EMA1H
        global NEW_idx_INF_EMA200_EMA15
        global NEW_idx_INF_EMA200_EMA1L
        global NEW_idx_INF_EMA200_EMA1H
        global NEW_idx_SUP_EMA1H_EMA1L  
        
        NEW_idx_INF_EMA200_EMA1H=val_mask_idxmin
        NEW_idx_SUP_EMA1H_EMA1L=val_mask_idxmin
    
        MASK_idx_EMA200_EMA15=idx_EMA200_EMA15 <= val_mask_idxmin
        MASK_idx_EMA200_EMA1L=idx_EMA200_EMA1L <= val_mask_idxmin
        MASK_idx_EMA200_EMA1H=idx_EMA200_EMA1H <= val_mask_idxmin
        MASK_idx_SUP_EMA200_EMA15=idx_SUP_EMA200_EMA15 <= val_mask_idxmin
        MASK_idx_SUP_EMA200_EMA1L=idx_SUP_EMA200_EMA1L <= val_mask_idxmin
        MASK_idx_SUP_EMA200_EMA1H=idx_SUP_EMA200_EMA1H <= val_mask_idxmin
        MASK_idx_INF_EMA200_EMA15=idx_INF_EMA200_EMA15 <= val_mask_idxmin
        MASK_idx_INF_EMA200_EMA1L=idx_INF_EMA200_EMA1L <= val_mask_idxmin
        MASK_idx_INF_EMA200_EMA1H=idx_INF_EMA200_EMA1H <= val_mask_idxmin
        MASK_idx_SUP_EMA1H_EMA1L =idx_SUP_EMA1H_EMA1L <= val_mask_idxmin  
        
        NEW_idx_EMA200_EMA15=idx_EMA200_EMA15[MASK_idx_EMA200_EMA15]
        NEW_idx_EMA200_EMA1L=idx_EMA200_EMA1L[MASK_idx_EMA200_EMA1L]
        NEW_idx_EMA200_EMA1H=idx_EMA200_EMA1H[MASK_idx_EMA200_EMA1H]
        NEW_idx_SUP_EMA200_EMA15=idx_SUP_EMA200_EMA15[MASK_idx_SUP_EMA200_EMA15]
        NEW_idx_SUP_EMA200_EMA1L=idx_SUP_EMA200_EMA1L[MASK_idx_SUP_EMA200_EMA1L]
        NEW_idx_SUP_EMA200_EMA1H=idx_SUP_EMA200_EMA1H[MASK_idx_SUP_EMA200_EMA1H]
        NEW_idx_INF_EMA200_EMA15=idx_INF_EMA200_EMA15[MASK_idx_INF_EMA200_EMA15]
        NEW_idx_INF_EMA200_EMA1L=idx_INF_EMA200_EMA1L[MASK_idx_INF_EMA200_EMA1L]
        NEW_idx_INF_EMA200_EMA1H=idx_INF_EMA200_EMA1H[MASK_idx_INF_EMA200_EMA1H]
        NEW_idx_SUP_EMA1H_EMA1L=idx_SUP_EMA1H_EMA1L[MASK_idx_SUP_EMA1H_EMA1L]
        if len(MASK_idx_INF_EMA200_EMA1H) == 0  :
            #global MASK_idx_INF_EMA200_EMA1H
            MASK_idx_INF_EMA200_EMA1H=val_mask_idxmin
            #global NEW_idx_INF_EMA200_EMA1H
            NEW_idx_INF_EMA200_EMA1H=val_mask_idxmin

    
        print("val_mask_idxmin:",val_mask_idxmin)
        print("idx_INF_EMA200_EMA1H:\n",idx_INF_EMA200_EMA1H)
        print("MASK_idx_INF_EMA200_EMA1H=idx_INF_EMA200_EMA1H <= val_mask_idxmin :\n",MASK_idx_INF_EMA200_EMA1H)
        print("NEW_idx_INF_EMA200_EMA1H=idx_INF_EMA200_EMA1H[MASK_idx_INF_EMA200_EMA1H]:\n",NEW_idx_INF_EMA200_EMA1H)
        print("dataframe.iloc[NEW_idx_INF_EMA200_EMA1H]:\n",dataframe.iloc[NEW_idx_INF_EMA200_EMA1H].tail())
        print("SORTIE DANS SYNCHRONISATION_INDICE\n")
        #exit()
        """
        
        """
    except Exception as g:
        time.sleep(0)
        """


def DETECTION_FRONT(dataframe,val_mask_idxmin) : 
    try:
         global VAL_EMA200_idxmin_ORG
         global val_mask_ORG_idxmin
         global val_mask_ORG_idxmax
         global mask_ORG
         global FRONT_MONTANT_EMA200
         global FRONT_MONTANT_EMA15
         global FRONT_MONTANT_EMA1L
         global FRONT_MONTANT_EMA1H
         global FRONT_MONTANT_COURT_EMA200
         global FRONT_MONTANT_COURT_EMA15
         global FRONT_MONTANT_COURT_EMA1L
         global FRONT_MONTANT_COURT_EMA1H
         global FRONT_MONTANT_COURT_EMA1H_N1
         global FRONT_MONTANT_COURT_EMA1H_N2
         global FRONT_MONTANT_COURT_EMA1H_N3 
         global FRONT_MONTANT_COURT_EMA1H_N4 
         global FRONT_NEUTRE_EMA15
         global FRONT_NEUTRE_EMA1L
         global FRONT_NEUTRE_EMA1H
         global FRONT_NEUTRE_COURT_EMA200
         global FRONT_NEUTRE_COURT_EMA15
         global FRONT_NEUTRE_COURT_EMA1L
         global FRONT_NEUTRE_COURT_EMA1H
         global TYPE_FRONT_EMA1H_N1
         global TYPE_FRONT_EMA1H_N2
         global TYPE_FRONT_EMA1H_N3
         global TYPE_FRONT_EMA1H_N4
         global TYPE_FRONT_EMA200
         global TYPE_FRONT_EMA15
         global TYPE_FRONT_EMA1L
         global TYPE_FRONT_EMA1H
         global TYPE_FRONT_COURT_EMA15
         global TYPE_FRONT_COURT_EMA1L
         global TYPE_FRONT_COURT_EMA1H
         global TYPE_FRONT_COURT_EMA200
         global FRONT_NEUTRE_EMA15
         global VAL_EMA15_COURANT
         global VAL_EMA15_PRECEDENT
         global VAL_EMA15_PRECEDENT_COURT
         global VAL_EMA15_PRECEDENT_LONG
         global VAL_EMA1L_PRECEDENT
         global VAL_EMA1H_PRECEDENT
         global FRONT_NEUTRE_EMA200
         global FRONT_MONTANT_EMA200
         global VAL_EMA200_COURANT
         global VAL_EMA200_PRECEDENT
         global VAL_EMA200_PRECEDENT_LONG
         global VAL_EMA200_PRECEDENT_COURT
         global VAL_EMA1L_PRECEDENT_COURT
         global VAL_EMA1H_PRECEDENT_COURT
         global VAL_EMA1H_COURANT
         global NBR_PREC
         # global NBR_PREC_LONG
         global VAL_NBR_PREC_LONG
         global LAST_FRONT_NEUTRE_EMA15
         global VAL_EMA15_PRECEDENT_COURT_MOINS_DEUX
         global VAL_EMA1L_PRECEDENT_COURT_MOINS_DEUX
         global VAL_EMA1H_PRECEDENT_COURT_MOINS_DEUX
         global VAL_EMA15_PRECEDENT_COURT_MOINS_TROIS
         global VAL_EMA1L_PRECEDENT_COURT_MOINS_TROIS
         global VAL_EMA1H_PRECEDENT_COURT_MOINS_TROIS
         global VAL_EMA15_PRECEDENT_COURT_MOINS_QUATRE
         global VAL_EMA1L_PRECEDENT_COURT_MOINS_QUATRE
         global VAL_EMA1H_PRECEDENT_COURT_MOINS_QUATRE
         global VAL_EMA15_DATE_MAX
         global VAL_EMA1H_DATE_MAX
         global VAL_EMA1L_DATE_MAX
         global VAL_EMA200_DATE_MAX
         global DATE_COURANTE
         global FLAG_BEST_NBR_TAILLE_BG
         global LAST_CROISEMENT_EMA200_GOLDEN_CROSS_EMA15
         # LAST_CROISEMENT_EMA200_GOLDEN_CROSS_EMA15_INDEX
         #global LAST_CROISEMENT_EMA1H_EMA1L_DESS_CROSS_INDEX
         global LAST_CROISEMENT_EMA1H_EMA1L_DESS_CROSS
         global DIFF_EMA200_CLOSE
         global  VAL_EMA15_PRECEDENT_LONG
         global val_mask_idxmin_ORG
         global dataframe_date

        
         print("\nENTRER DANS DETECTION_FRONT")


         DATE_COURANTE=dataframe_date.date.loc[val_mask_idxmin]
         #custom_info["HEURE_CROISEMENT_PAIR"]=DATE_COURANTE
         print("\nDATE COURANT=",DATE_COURANTE)
         
         """
         last_index=len(dataframe)-1
         if val_mask_idxmin >= last_index :
           val_mask_idxmin=last_index
         """
         
         #last_index=len(dataframe)-1
         """
         TEST_MODE_REEL=CALCUL_DATE_COURANTE(dataframe,val_mask_idxmin)
         if   TEST_MODE_REEL == 1 :
           val_mask_idxmin=last_index
         """
         """
         if FLAG_BEST_NBR_TAILLE_BG == 1 :
            val_mask_idxmin=DETECT_MODE_REEL(dataframe,val_mask_idxmin)
         """
         last_index=len(dataframe)-1
         print("last_index=",last_index)
         if val_mask_idxmin >= last_index :
            val_mask_idxmin=last_index  
         
         FRONT_MONTANT_EMA200=0
         FRONT_MONTANT_EMA15=0
         FRONT_MONTANT_COURT_EMA200=0 
         FRONT_MONTANT_COURT_EMA15=0
         FRONT_MONTANT_COURT_EMA1L=0
         FRONT_MONTANT_COURT_EMA1H=0
         FRONT_MONTANT_COURT_EMA1H_N1=0
         FRONT_MONTANT_COURT_EMA1H_N2=0
         FRONT_MONTANT_COURT_EMA1H_N3=0 
         FRONT_MONTANT_COURT_EMA1H_N4=0
         FRONT_MONTANT_EMA1L=0
         FRONT_MONTANT_EMA1H=0
         FRONT_NEUTRE_EMA200=0
         FRONT_NEUTRE_EMA15=0
         FRONT_NEUTRE_EMA1L=0
         FRONT_NEUTRE_EMA1H=0
         FRONT_NEUTRE_COURT_EMA200=0
         FRONT_NEUTRE_COURT_EMA15=0
         FRONT_NEUTRE_COURT_EMA1L=0
         FRONT_NEUTRE_COURT_EMA1H=0
         VAL_EMA15_PRECEDENT_COURT=0
         VAL_EMA200_PRECEDENT_COURT=0
         TYPE_FRONT_EMA15=0
         TYPE_FRONT_EMA200=0
         TYPE_FRONT_COURT_EMA15=0
         TYPE_FRONT_COURT_EMA1L=0
         TYPE_FRONT_COURT_EMA1H=0
         TYPE_FRONT_COURT_EMA200=0
         TYPE_FRONT_EMA1L=0
         TYPE_FRONT_EMA1H=0
         TYPE_FRONT_EMA1H_N1=0
         TYPE_FRONT_EMA1H_N2=0
         TYPE_FRONT_EMA1H_N3=0
         TYPE_FRONT_EMA1H_N4=0
         TYPE_FRONT_COURT_EMA15=0
         TYPE_FRONT_COURT_EMA1L=0
         TYPE_FRONT_COURT_EMA1H=0
         TYPE_FRONT_COURT_EMA200=0
        # VAL_EMA15_COURANT=0
         VAL_EMA15_PRECEDENT=0
         VAL_EMA15_PRECEDENT_COURT=0
         VAL_EMA1L_PRECEDENT=0
         VAL_EMA1H_PRECEDENT=0
         VAL_EMA200_COURANT=0
         VAL_EMA200_PRECEDENT_COURT=0
         VAL_EMA200_PRECEDENT_LONG=0
         VAL_EMA1L_PRECEDENT_COURT=0
         VAL_EMA1H_PRECEDENT_COURT=0
         VAL_EMA15_PRECEDENT_COURT_MOINS_DEUX=0
         VAL_EMA1L_PRECEDENT_COURT_MOINS_DEUX=0
         VAL_EMA1H_PRECEDENT_COURT_MOINS_UN=0
         VAL_EMA1H_PRECEDENT_COURT_MOINS_DEUX=0
         VAL_EMA1H_PRECEDENT_COURT_MOINS_TROIS=0



           
         """  
         if FLAG_BEST_NBR_TAILLE_BG == 1 :
            last_index=len(dataframe)-1
            val_mask_idxmin = last_index 
         """  
         last_index=len(dataframe)-1
         val_mask_idxmin = last_index 
         
         print("\n val_mask_idxmin=",val_mask_idxmin)
         # print("\nDataframe MASK EMA200 MIN=\n",dataframe[["date","EMA200"]].loc[val_mask_idxmin_ORG])
         # VAL_EMA200_idxmin_ORG=dataframe.EMA200.loc[val_mask_idxmin_ORG]
         # print("Dataframe MASK EMA200 MIN=",VAL_EMA200_idxmin_ORG)

         # #if ("J" in  interval) or  ("d" in  interval) or  ("w" in  interval) or  ("M" in  interval)  :
         # mask_ORG=(dataframe.date <= dataframe.loc[val_mask_idxmin].date)
         # #else :
         # #    mask_ORG=(dataframe.date >= dataframe.loc[val_mask_idxmin_ORG].date)  # and (dataframe.date <= dataframe.loc[val_mask_idxmin].date)
         # #mask_ORG=(dataframe.date >= dataframe.loc[val_mask_idxmin].date)
         # #print("mask_ORG=\n",mask_ORG)
         # val_mask_ORG_idxmax=dataframe['EMA200'].loc[mask_ORG].idxmax()
         # val_mask_ORG_idxmin=dataframe['EMA200'].loc[mask_ORG].idxmin()
         # #val_mask_EMA15_ORG_idxmax=dataframe['EMA15'].loc[mask_ORG].idxmax()
         # print("INDEX idxmin=",val_mask_ORG_idxmin)
         # print("INDEX idxmax=",val_mask_ORG_idxmax)
         # print("\nDataframe MASK EMA200 MAX=\n",dataframe[["date","EMA200"]].loc[val_mask_ORG_idxmax])
         # print("\nDataframe MASK EMA200 MIN=\n",dataframe[["date","EMA200"]].loc[val_mask_ORG_idxmin])
         # #print("Dataframe MASK EMA200 MAX=",dataframe.EMA200.loc[val_mask_ORG_idxmax])
         print("\nINDEX COURANT=\n",dataframe.loc[val_mask_idxmin])


         global VAL_EMA200_MAX
         global VAL_EMA200_DATE_MAX
         """
         VAL_EMA200_MAX=dataframe.EMA200.loc[val_mask_ORG_idxmax].astype(int)
         VAL_EMA200_DATE_MAX=dataframe.date.loc[val_mask_ORG_idxmax]
         VAL_EMA200_DATE_COURANT=dataframe.date.loc[val_mask_idxmin]
         """
         # #mask_EMA15 = (dataframe.date <=  dataframe.loc[val_mask_idxmin].date )
         # VAL_EMA200_MIN=dataframe.EMA15.loc[val_mask_ORG_idxmin].astype(int)
         # print("\nVAL_EMA200_MIN=",VAL_EMA200_MIN)        
         # val_mask_EMA15_idxmax=dataframe['EMA15'].loc[mask_ORG].idxmax()
         # VAL_EMA15_MAX=dataframe.EMA15.loc[val_mask_EMA15_idxmax].astype(int)
         # print("\nVAL_EMA15_MAX=",VAL_EMA15_MAX)
         # VAL_EMA15_DATE_MAX=dataframe.date.loc[val_mask_EMA15_idxmax]
         # VAL_EMA15_DATE_COURANT=dataframe.date.loc[val_mask_EMA15_idxmax]
         # #if (val_mask_idxmin != " " ) : #and (VAL_EMA200_DATE_MAX >= VAL_EMA200_DATE_COURANT) :
             
         # val_mask_EMA1L_idxmax=dataframe['EMA1L'].loc[mask_ORG].idxmax()
         # VAL_EMA1L_MAX=dataframe.EMA1L.loc[val_mask_EMA1L_idxmax].astype(int)
         # print("\nVAL_EMA1L_MAX=",VAL_EMA1L_MAX)
         # VAL_EMA1L_DATE_MAX=dataframe.date.loc[val_mask_EMA1L_idxmax]  
         # VAL_EMA1L_DATE_COURANT=dataframe.date.loc[val_mask_EMA1L_idxmax]
         
         # val_mask_EMA1H_idxmax=dataframe['EMA1H'].loc[mask_ORG].idxmax()
         # VAL_EMA1H_MAX=dataframe.EMA1H.loc[val_mask_EMA1H_idxmax].astype(int)
         # print("\nVAL_EMA1H_MAX=",VAL_EMA1H_MAX)
         # VAL_EMA1H_DATE_MAX=dataframe.date.loc[val_mask_EMA1H_idxmax] 
         # VAL_EMA1H_DATE_COURANT=dataframe.date.loc[val_mask_EMA1H_idxmax]

         # val_mask_EMA200_idxmax=dataframe['EMA200'].loc[mask_ORG].idxmax()
         # VAL_EMA200_MAX=dataframe.EMA200.loc[val_mask_EMA200_idxmax].astype(int)
         # print("\nVAL_EMA200_MAX=",VAL_EMA200_MAX)
         # VAL_EMA200_DATE_MAX=dataframe.date.loc[val_mask_EMA200_idxmax]
         # VAL_EMA200_DATE_COURANT=dataframe.date.loc[val_mask_EMA200_idxmax]
         #  #if (val_mask_idxmin >= 0 ) :
         # NBR_PREC=15
         NBR_PREC=1

         # NBR_PREC=200
         NBR_PREC_LONG=VAL_NBR_PREC_LONG
         NBR_PREC_LONG=8


         print("NBR_PREC=",NBR_PREC)
         print("NBR_PREC_LONG=",NBR_PREC_LONG)
         NBR_PREC_MOINS_1=1
         # NBR_PREC_MOINS_2=2
         # NBR_PREC_MOINS_3=3
         # NBR_PREC_MOINS_4=4

         # if val_mask_idxmin <= VAL_NBR_PREC_LONG :
         #      NBR_PREC_MOINS_1=0
         #     NBR_PREC_MOINS_2=0
         #     NBR_PREC_MOINS_3=0
         #     NBR_PREC_MOINS_4=0
         #     NBR_PREC=0
         #     NBR_PREC_LONG=0
         # print("NBR_PREC_MOINS_1=",NBR_PREC_MOINS_1)
         # print("NBR_PREC_MOINS_2=",NBR_PREC_MOINS_2)
         # print("NBR_PREC_MOINS_3=",NBR_PREC_MOINS_3)
         # print("NBR_PREC_MOINS_4=",NBR_PREC_MOINS_4)

         # exit()
         #VAL_CLOSE_PRECEDENT=dataframe.close.loc[val_mask_idxmin-NBR_PREC]
         VAL_EMA200_COURANT=dataframe.EMA200.loc[val_mask_idxmin].astype(float)
         VAL_EMA15_COURANT=dataframe.EMA15.loc[val_mask_idxmin].astype(float)
         ###VAL_EMA15_COURANT=dataframe.EMA1H.loc[val_mask_idxmin].astype(int)

         VAL_EMA1L_COURANT=dataframe.EMA1L.loc[val_mask_idxmin].astype(float)
         VAL_EMA1H_COURANT=dataframe.EMA1H.loc[val_mask_idxmin].astype(float)
         VAL_EMA15_PRECEDENT=dataframe.EMA15.loc[val_mask_idxmin-NBR_PREC].astype(float)
         VAL_EMA200_PRECEDENT_COURT=dataframe.EMA200.loc[val_mask_idxmin-NBR_PREC_MOINS_1].astype(float)
         VAL_EMA15_PRECEDENT_COURT=dataframe.EMA15.loc[val_mask_idxmin-NBR_PREC_MOINS_1].astype(float)
         VAL_EMA1L_PRECEDENT_COURT=dataframe.EMA1L.loc[val_mask_idxmin-NBR_PREC_MOINS_1].astype(float)
         VAL_EMA1H_PRECEDENT_COURT=dataframe.EMA1H.loc[val_mask_idxmin-NBR_PREC_MOINS_1].astype(float)
       
         # VAL_EMA15_PRECEDENT_COURT_MOINS_DEUX=dataframe.EMA15.loc[val_mask_idxmin-NBR_PREC_MOINS_2].astype(int)
         # VAL_EMA1L_PRECEDENT_COURT_MOINS_DEUX=dataframe.EMA1L.loc[val_mask_idxmin-NBR_PREC_MOINS_2].astype(int)
         # VAL_EMA1H_PRECEDENT_COURT_MOINS_DEUX=dataframe.EMA1H.loc[val_mask_idxmin-NBR_PREC_MOINS_2].astype(int)
         
         # VAL_EMA15_PRECEDENT_COURT_MOINS_TROIS=dataframe.EMA15.loc[val_mask_idxmin-NBR_PREC_MOINS_3].astype(int)
         # VAL_EMA1L_PRECEDENT_COURT_MOINS_TROIS=dataframe.EMA1L.loc[val_mask_idxmin-NBR_PREC_MOINS_3].astype(int)
         # VAL_EMA1H_PRECEDENT_COURT_MOINS_TROIS=dataframe.EMA1H.loc[val_mask_idxmin-NBR_PREC_MOINS_3].astype(int)
         
         # VAL_EMA15_PRECEDENT_COURT_MOINS_QUATRE=dataframe.EMA15.loc[val_mask_idxmin-NBR_PREC_MOINS_4].astype(int)
         # VAL_EMA1L_PRECEDENT_COURT_MOINS_QUATRE=dataframe.EMA1L.loc[val_mask_idxmin-NBR_PREC_MOINS_4].astype(int)
         # VAL_EMA1H_PRECEDENT_COURT_MOINS_QUATRE=dataframe.EMA1H.loc[val_mask_idxmin-NBR_PREC_MOINS_4].astype(int)
         print("VAL_EMA1H_PRECEDENT_COURT:",VAL_EMA1H_PRECEDENT_COURT)
         # print("VAL_EMA1H_PRECEDENT_COURT_MOINS_DEUX:",VAL_EMA1H_PRECEDENT_COURT_MOINS_DEUX)
         # print("VAL_EMA1H_PRECEDENT_COURT_MOINS_TROIS:",VAL_EMA1H_PRECEDENT_COURT_MOINS_TROIS)
         # print("VAL_EMA1H_PRECEDENT_COURT_MOINS_QUATRE:",VAL_EMA1H_PRECEDENT_COURT_MOINS_QUATRE)
         # print("VAL_EMA1H_PRECEDENT_COURT-VAL_EMA1H_PRECEDENT_COURT_MOINS_DEUX:",VAL_EMA1H_PRECEDENT_COURT-VAL_EMA1H_PRECEDENT_COURT_MOINS_DEUX)
         # print("VAL_EMA1H_PRECEDENT_COURT_MOINS_DEUX-VAL_EMA1H_PRECEDENT_COURT_MOINS_TROIS:",VAL_EMA1H_PRECEDENT_COURT_MOINS_DEUX-VAL_EMA1H_PRECEDENT_COURT_MOINS_TROIS)
         # print("VAL_EMA1H_PRECEDENT_COURT_MOINS_TROIS-VAL_EMA1H_PRECEDENT_COURT_MOINS_QUATRE:",VAL_EMA1H_PRECEDENT_COURT_MOINS_TROIS-VAL_EMA1H_PRECEDENT_COURT_MOINS_QUATRE)
         # #exit()
  
         VAL_EMA200_PRECEDENT=dataframe.EMA200.loc[val_mask_idxmin-NBR_PREC].astype(float)
         VAL_EMA15_PRECEDENT=dataframe.EMA15.loc[val_mask_idxmin-NBR_PREC].astype(float)
         ###VAL_EMA15_PRECEDENT_LONG=dataframe.EMA1H.loc[val_mask_idxmin-NBR_PREC_LONG].astype(int)
         VAL_EMA15_PRECEDENT_LONG=dataframe.EMA15.loc[val_mask_idxmin-NBR_PREC_LONG].astype(float)
         #VAL_EMA15_PRECEDENT_LONG=int(LAST_CROISEMENT_EMA200_GOLDEN_CROSS_EMA15.EMA15.astype(int))
         #VAL_EMA15_PRECEDENT_LONG=int(LAST_CROISEMENT_EMA200_GOLDEN_CROSS_EMA15.astype(int))
         #print("VAL_EMA15_PRECEDENT_LONG=",VAL_EMA15_PRECEDENT_LONG)
         #exit()
         
         # VAL_EMA200_PRECEDENT_LONG=dataframe.EMA200.loc[val_mask_idxmin_ORG].astype(int)
         VAL_EMA200_PRECEDENT_LONG=dataframe.EMA200.loc[val_mask_idxmin-NBR_PREC_LONG].astype(float)
         #VAL_EMA200_PRECEDENT_LONG=dataframe.EMA200.loc[val_mask_idxmin-50].astype(int)

         VAL_EMA1L_PRECEDENT=dataframe.EMA1L.loc[val_mask_idxmin-NBR_PREC].astype(float)

         VAL_EMA1L_PRECEDENT_LONG=dataframe.EMA1L.loc[val_mask_idxmin-NBR_PREC_LONG].astype(float)
         ##VAL_EMA1L_PRECEDENT_LONG=int(LAST_CROISEMENT_EMA1H_EMA1L_DESS_CROSS.DIFF_EMA1H_EMA1L.astype(int))
         VAL_EMA1H_PRECEDENT=dataframe.EMA1H.loc[val_mask_idxmin-NBR_PREC].astype(float)
         VAL_EMA1H_PRECEDENT_LONG=dataframe.EMA1H.loc[val_mask_idxmin-NBR_PREC_LONG].astype(float)
         ##VAL_EMA1H_PRECEDENT_LONG=int(LAST_CROISEMENT_EMA1H_EMA1L_DESS_CROSS.DIFF_EMA1H_EMA1L.astype(int))
         #VAL_EMA1H_COURANT=dataframe.EMA1H.loc[val_mask_idxmin].astype(int)
         #VAL_EMA1H_PRECEDENT=dataframe.EMA1H.loc[val_mask_idxmin-3].astype(int)
         #print("VAL_EMA15_PRECEDENT_LONG=",VAL_EMA15_PRECEDENT_LONG)
         #exit()
         VAL_CLOSE=dataframe.close.loc[val_mask_idxmin]
         #print("LAST_CROISEMENT_EMA200_GOLDEN_CROSS_EMA15: ",LAST_CROISEMENT_EMA200_GOLDEN_CROSS_EMA15)
         #print("LAST_CROISEMENT_EMA200_GOLDEN_CROSS_EMA15: ",LAST_CROISEMENT_EMA200_GOLDEN_CROSS_EMA15.EMA15.astype(int))
         #print("LAST_CROISEMENT_EMA1H_EMA1L_DESS_CROSS: ",LAST_CROISEMENT_EMA1H_EMA1L_DESS_CROSS.DIFF_EMA1H_EMA1L.astype(int))
         #exit()

         # print("mask_ORG_idxmax=",val_mask_ORG_idxmax)
         # print("VAL_EMA200_MAX=",VAL_EMA200_MAX)
         # print("VAL_EMA200_DATE_MAX=",VAL_EMA200_DATE_MAX)
         # print("mask_idxmin=",val_mask_idxmin)
         # print("VAL_CLOSE=",VAL_CLOSE)
         # print("VAL_EMA200_idxmin_ORG=",VAL_EMA200_idxmin_ORG)
         # print("VAL_EMA200_COURANT=",VAL_EMA200_COURANT)
         # exit()

         print("VAL_EMA200_PRECEDENT=",VAL_EMA200_PRECEDENT)
         print("VAL_EMA200_PRECEDENT_LONG=",VAL_EMA200_PRECEDENT_LONG)
         print("VAL_EMA200_COURANT-VAL_EMA200_PRECEDENT_LONG > 0 =",VAL_EMA200_COURANT-VAL_EMA200_PRECEDENT_LONG > 0)
         # print("VAL_EMA15_DATE_COURANT",VAL_EMA15_DATE_COURANT)
         print("VAL_EMA15_COURANT=",VAL_EMA15_COURANT)
         print("VAL_EMA15_PRECEDENT_LONG=",VAL_EMA15_PRECEDENT_LONG)
         print("VAL_EMA15_COURANT-VAL_EMA15_PRECEDENT_LONG > 0 :",VAL_EMA15_COURANT-VAL_EMA15_PRECEDENT_LONG >0)
         # print("TYPE_EMA15=",TYPE_EMA15)
         # print("VAL_EMA200_DATE_MAX",VAL_EMA200_DATE_MAX)
         # print("VAL_EMA200_DATE_COURANT",VAL_EMA200_DATE_COURANT)
         # print("VAL_EMA15_COURANT=",VAL_EMA15_COURANT)         
         # print("VAL_EMA15_DATE_COURANT",VAL_EMA15_DATE_COURANT)
         # print("VAL_EMA15_DATE_MAX",VAL_EMA15_DATE_MAX)
         # print("VAL_EMA1L_COURANT=",VAL_EMA1L_COURANT)         
         # print("VAL_EMA1L_DATE_COURANT",VAL_EMA1L_DATE_COURANT)
         # print("VAL_EMA1L_DATE_MAX",VAL_EMA1L_DATE_MAX)
         # print("VAL_EMA1H_COURANT=",VAL_EMA1H_COURANT)         
         # print("VAL_EMA1H_DATE_COURANT",VAL_EMA1H_DATE_COURANT)
         # print("VAL_EMA1H_DATE_MAX",VAL_EMA1H_DATE_MAX)
         print("VAL_EMA1L_PRECEDENT_LONG",VAL_EMA1L_PRECEDENT_LONG)
         print("VAL_EMA1H_PRECEDENT_LONG",VAL_EMA1H_PRECEDENT_LONG)
         # exit()
         # if  DIFF_EMA200_CLOSE >= 0  and  DIFF_EMA200_CLOSE <= 10 :
             #exit()       
             
         #print("VAL_EMA200_DATE_MAX >= VAL_EMA200_DATE_COURANT :",VAL_EMA200_DATE_MAX >= VAL_EMA200_DATE_COURANT)
         
         #if (VAL_EMA200_DATE_MAX >= VAL_EMA200_DATE_COURANT) and (VAL_EMA200_COURANT-VAL_EMA200_PRECEDENT_LONG > 0) :
          
         if (VAL_EMA200_COURANT-VAL_EMA200_PRECEDENT_LONG > 0) :
             print("FRONT MONTANT EMA200: CONDITION ACHAT")
             FRONT_MONTANT_EMA200=1
             TYPE_FRONT_EMA200="FRONT MONTANT EMA200"

             
         if (VAL_EMA200_COURANT-VAL_EMA200_PRECEDENT_LONG < 0) :
             print("FRONT DESCENDANT EMA200")
             FRONT_MONTANT_EMA200=0
             TYPE_FRONT_EMA200="FRONT DESCENDANT EMA200"

         
         if (VAL_EMA200_COURANT-VAL_EMA200_PRECEDENT_LONG == 0) :
             print("FRONT NEUTRE EMA200: CONDITION ACHAT")
             FRONT_NEUTRE_EMA200=1 
             TYPE_FRONT_EMA200="FRONT NEUTRE EMA200"
                        
         #if (VAL_EMA15_DATE_MAX >= VAL_EMA15_DATE_COURANT) and (VAL_EMA15_COURANT-VAL_EMA15_PRECEDENT_LONG >0) :
         if (VAL_EMA15_COURANT-VAL_EMA15_PRECEDENT_LONG > 0) :
             print("FRONT MONTANT EMA15: CONDITION ACHAT")
             FRONT_MONTANT_EMA15=1
             TYPE_FRONT_EMA15="FRONT MONTANT EMA15"
              
         if (VAL_EMA15_COURANT-VAL_EMA15_PRECEDENT_LONG < 0) :
             print("FRONT DESCENDANT EMA15")
             FRONT_MONTANT_EMA15=0
             TYPE_FRONT_EMA15="FRONT DESCENDANT EMA15"
             #exit()

         if (VAL_EMA15_COURANT-VAL_EMA15_PRECEDENT_LONG == 0) :
             print("FRONT NEUTRE EMA15: CONDITION ACHAT")
             FRONT_NEUTRE_EMA15=1 
             TYPE_FRONT_EMA15="FRONT NEUTRE EMA15"
         
         if (VAL_EMA1L_COURANT-VAL_EMA1L_PRECEDENT_LONG > 0) :
             print("FRONT MONTANT EMA1L: CONDITION ACHAT")
             FRONT_MONTANT_EMA1L=1
             TYPE_FRONT_EMA1L="FRONT MONTANT EMA1L"
             
         if (VAL_EMA1L_COURANT-VAL_EMA1L_PRECEDENT_LONG < 0) :
             print("FRONT DESCENDANT EMA1L")
             FRONT_MONTANT_EMA1L=0
             TYPE_FRONT_EMA1L="FRONT DESCENDANT EMA1L"
         
         if (VAL_EMA1L_COURANT-VAL_EMA1L_PRECEDENT_LONG == 0) :
             print("FRONT NEUTRE EMA1L: CONDITION ACHAT")
             FRONT_NEUTRE_EMA1L=1 
             TYPE_FRONT_EMA1L="FRONT NEUTRE EMA1L"
             
         if (VAL_EMA1H_COURANT-VAL_EMA1H_PRECEDENT > 0) :
             print("FRONT MONTANT EMA1H: CONDITION ACHAT")
             FRONT_MONTANT_EMA1H=1
             TYPE_FRONT_EMA1H="FRONT MONTANT  EMA1H"
             
         if (VAL_EMA1H_COURANT-VAL_EMA1H_PRECEDENT < 0) :
             print("FRONT DESCENDANT EMA1H")
             FRONT_MONTANT_EMA1H=0
             TYPE_FRONT_EMA1H="FRONT DESCENDANT EMA1H"
          
         if (VAL_EMA1H_COURANT-VAL_EMA1H_PRECEDENT_LONG == 0) :
             print("FRONT NEUTRE EMA1H: CONDITION ACHAT")
             FRONT_NEUTRE_EMA1H=1 
             TYPE_FRONT_EMA1H="FRONT NEUTRE EMA1H"         
              
                       ################COURT ################  
         if (VAL_EMA200_COURANT-VAL_EMA200_PRECEDENT_COURT > 0) :
              print("FRONT MONTANT COURT EMA200: CONDITION ACHAT")
              FRONT_MONTANT_COURT_EMA200=1
              TYPE_FRONT_COURT_EMA200="FRONT MONTANT COURT EMA200"
             
         if (VAL_EMA200_COURANT-VAL_EMA200_PRECEDENT_COURT < 0) :
              print("FRONT DESCENDANT COURT EMA200")
              FRONT_MONTANT_COURT_EMA200=0
              TYPE_FRONT_COURT_EMA200="FRONT DESCENDANT EMA200"
         
         if (VAL_EMA200_COURANT-VAL_EMA200_PRECEDENT_COURT == 0) :
              print("FRONT NEUTRE COURT EMA200: CONDITION ACHAT")
              FRONT_NEUTRE_COURT_EMA200=1 
              TYPE_FRONT_COURT_EMA200="FRONT NEUTRE COURT EMA200"
              
         if (VAL_EMA15_COURANT-VAL_EMA15_PRECEDENT_COURT > 0) :
              print("FRONT MONTANT COURT EMA15: CONDITION ACHAT")
              FRONT_MONTANT_COURT_EMA15=1
              TYPE_FRONT_COURT_EMA15="FRONT MONTANT COURT EMA15"
             
         if (VAL_EMA15_COURANT-VAL_EMA15_PRECEDENTT_COURT < 0) :
              print("FRONT DESCENDANT COURT EMA15")
              FRONT_MONTANT_COURT_EMA15=0
              TYPE_FRONT_COURT_EMA15="FRONT DESCENDANT COURT EMA15"
             
         if (VAL_EMA15_COURANT-VAL_EMA15_PRECEDENT_COURT == 0) :
               print("FRONT NEUTRE EMA15: CONDITION ACHAT")
               FRONT_NEUTRE_COURT_EMA15=1 
               LAST_FRONT_NEUTRE_EMA15=VAL_EMA15_COURANT
               TYPE_FRONT_EMA15="FRONT NEUTRE COURT EMA15"  
             
            
         if (VAL_EMA1L_COURANT-VAL_EMA1L_PRECEDENT_COURT > 0) :
              print("FRONT MONTANT COURT EMA1L: CONDITION ACHAT")
              FRONT_MONTANT_COURT_EMA1L=1
              TYPE_FRONT_EMA1L="FRONT MONTANT COURT EMA1L"
              DIFF_FRONT_MONTANT_COURT_EMA1L=(float(VAL_EMA1L_COURANT-VAL_EMA1L_PRECEDENT_COURT)*MULTIP)/100
              print("DIFF_FRONT_MONTANT_COURT_EMA1L: ",DIFF_FRONT_MONTANT_COURT_EMA1L)
 

         if (VAL_EMA1L_COURANT-VAL_EMA1L_PRECEDENT_COURT <= 0) :
              print("FRONT DESCENDANT COURT EMA1L")
              FRONT_MONTANT_COURT_EMA1L=0
              TYPE_FRONT_EMA1L="FRONT DESCENDANT COURT EMA1L"
         
         if (VAL_EMA1L_COURANT-VAL_EMA1L_PRECEDENT == 0) :
             print("FRONT NEUTRE COURT EMA1L: CONDITION ACHAT")
             FRONT_NEUTRE_COURT_EMA1L=1 
             TYPE_FRONT_EMA1L="FRONT NEUTRE EMA1L"
             
             
          # FRONT_MONTANT_COURT_EMA1H_N1    
         if (VAL_EMA1H_COURANT-VAL_EMA1H_PRECEDENT_COURT > 0) :
              print("FRONT MONTANT COURT EMA1H: CONDITION ACHAT")
              FRONT_MONTANT_COURT_EMA1H=1
              TYPE_FRONT_EMA1H="FRONT MONTANT COURT EMA1H"
             
         if (VAL_EMA1H_COURANT-VAL_EMA1H_PRECEDENT_COURT <= 0) :
              print("FRONT DESCENDANT COURT EMA1H")
              FRONT_MONTANT_COURT_EMA1H=0
              TYPE_FRONT_EMA1H="FRONT DESCENDANT COURT EMA1H"
         
         if (VAL_EMA1H_COURANT-VAL_EMA1H_PRECEDENT_COURT == 0) :
              print("FRONT MONTANT COURT EMA1H: CONDITION ACHAT")
              FRONT_MONTANT_COURT_EMA1H=1 
              TYPE_FRONT_EMA1H="FRONT MONTANT COURT EMA1H"
         

         # #FRONT_MONTANT_COURT_EMA1H_N2
         # if (VAL_EMA1H_PRECEDENT_COURT-VAL_EMA1H_PRECEDENT_COURT_MOINS_DEUX > 0) :
         #     print("FRONT MONTANT COURT EMA1H_N2: CONDITION ACHAT")
         #     FRONT_MONTANT_COURT_EMA1H_N2=1
         #     TYPE_FRONT_EMA1H_N2="FRONT MONTANT COURT EMA1H_N2"
             
         # if (VAL_EMA1H_PRECEDENT_COURT-VAL_EMA1H_PRECEDENT_COURT_MOINS_DEUX <= 0) :
         #     print("FRONT DESCENDANT COURT EMA1H_N2")
         #     FRONT_MONTANT_COURT_EMA1H_N2=0
         #     TYPE_FRONT_EMA1H_N2="FRONT DESCENDANT COURT EMA1H_N2"
         
         # if (VAL_EMA1H_PRECEDENT_COURT-VAL_EMA1H_PRECEDENT_COURT_MOINS_DEUX == 0) :
         #     print("FRONT MONTANT COURT EMA1H_N2: CONDITION ACHAT")
         #     FRONT_MONTANT_COURT_EMA1H_N2=1 
         #     TYPE_FRONT_EMA1H_N2="FRONT MONTANT COURT EMA1H_N2"        
            
         # #FRONT_MONTANT_COURT_EMA1H_N3
         # if (VAL_EMA1H_PRECEDENT_COURT_MOINS_DEUX-VAL_EMA1H_PRECEDENT_COURT_MOINS_TROIS > 0) :
         #     print("FRONT MONTANT COURT EMA1H_N3: CONDITION ACHAT")
         #     FRONT_MONTANT_COURT_EMA1H_N3=1
         #     TYPE_FRONT_EMA1H_N3="FRONT MONTANT COURT EMA1H_N3"
             
         # if (VAL_EMA1H_PRECEDENT_COURT_MOINS_DEUX-VAL_EMA1H_PRECEDENT_COURT_MOINS_TROIS <= 0) :
         #     print("FRONT DESCENDANT COURT EMA1H_N3")
         #     FRONT_MONTANT_COURT_EMA1H_N3=0
         #     TYPE_FRONT_EMA1H_N3="FRONT DESCENDANT COURT EMA1H_N3"
         
         # if (VAL_EMA1H_PRECEDENT_COURT_MOINS_DEUX-VAL_EMA1H_PRECEDENT_COURT_MOINS_TROIS == 0) :
         #     print("FRONT MONTANT COURT EMA1H_N3: CONDITION ACHAT")
         #     FRONT_MONTANT_COURT_EMA1H_N3=1 
         #     TYPE_FRONT_EMA1H_N3="FRONT MONTANT COURT EMA1H_N3"     
             
         # #FRONT_MONTANT_COURT_EMA1H_N4
         # if (VAL_EMA1H_PRECEDENT_COURT_MOINS_TROIS-VAL_EMA1H_PRECEDENT_COURT_MOINS_QUATRE > 0) :
         #     print("FRONT MONTANT COURT EMA1H_N4: CONDITION ACHAT")
         #     FRONT_MONTANT_COURT_EMA1H_N4=1
         #     TYPE_FRONT_EMA1H_N4="FRONT MONTANT COURT EMA1H_N4"
             
         # if (VAL_EMA1H_PRECEDENT_COURT_MOINS_TROIS-VAL_EMA1H_PRECEDENT_COURT_MOINS_QUATRE <= 0) :
         #     print("FRONT DESCENDANT COURT EMA1H_N4")
         #     FRONT_MONTANT_COURT_EMA1H_N4=0
         #     TYPE_FRONT_EMA1H_N4="FRONT DESCENDANT COURT EMA1H_N4"
         
         # if (VAL_EMA1H_PRECEDENT_COURT_MOINS_TROIS-VAL_EMA1H_PRECEDENT_COURT_MOINS_QUATRE == 0) :
         #     print("FRONT MONTANT COURT EMA1H_N4: CONDITION ACHAT")
         #     FRONT_MONTANT_COURT_EMA1H_N4=1 
         #     TYPE_FRONT_EMA1H_N4="FRONT MONTANT COURT EMA1H_N4"    
             
         print("NBR_TAILLE_BG=",NBR_TAILLE_BG)
         print("TAILLE_BG=",TAILLE_BG)
         print("SORTIE DANS DETECTION_FRONT\n")
         # exit()
         """
         if  (FLAG_BEST_NBR_TAILLE_BG == 1) and (TRAITEMENT_REELLE == 1) :
             print("TRAITEMENT_REELLE=1 et  FLAG_BEST_NBR_TAILLE_BG=",FLAG_BEST_NBR_TAILLE_BG)
         """
    except Exception as g:
        time.sleep(0)

        
def TRANSITION_ACHAT_VENTE(dataframe,val_mask_idxmin) : 

        global POINT_ENTRE_EMA200
        global LAST_ORDER
        global ORDER
        global VAL_ACHAT
        global DERNIER_POINT_VENTE
        global FLAG_BEST_NBR_TAILLE_BG
        global LAST_CROISEMENT_EMA200_GOLDEN_CROSS_EMA15_INDEX
        global dataframe_date

        """
        TEST_MODE_REEL=CALCUL_DATE_COURANTE(dataframe,val_mask_idxmin)
        if   TEST_MODE_REEL == 1 :
          val_mask_idxmin=last_index
        """
        # #"""
        # if FLAG_BEST_NBR_TAILLE_BG == 1 :
        #    val_mask_idxmin=DETECT_MODE_REEL(dataframe,val_mask_idxmin)
        # #"""
        """
        last_index=len(dataframe)-1
        print("last_index=",last_index)
        if val_mask_idxmin >= last_index :
            val_mask_idxmin=last_index  
        """

        VAL_CLOSE=dataframe.close.loc[val_mask_idxmin]
        #LAST_CROISEMENT_EMA200_GOLDEN_CROSS_EMA15_INDEX=dataframe.iloc[idx_EMA200_EMA15].index[-1]
        print("\nENTRER DANS TRANSITION_ACHAT_VENTE")
        print("\ndataframe ILOC idx_EMA200_EMA15 > EMA15 :\n",LAST_CROISEMENT_EMA200_GOLDEN_CROSS_EMA15_TAIL)
        print("\ndataframe INDEX ILOC idx_EMA200_EMA15 > EMA15 :",LAST_CROISEMENT_EMA200_GOLDEN_CROSS_EMA15_INDEX)
        print("\ndataframe DERNIERE LIGNE ILOC idx_EMA200_EMA15 >IBM EMA15 :\n",LAST_CROISEMENT_EMA200_GOLDEN_CROSS_EMA15)
        print("\ndataframe EMA15 DERNIERE LIGNE ILOC idx_EMA200_EMA15 > EMA15 :",LAST_CROISEMENT_EMA200_GOLDEN_CROSS_EMA15.EMA15)
        LAST_DATE_CROISEMENT_EMA200_EMA15=dataframe.loc[LAST_CROISEMENT_EMA200_GOLDEN_CROSS_EMA15_INDEX].date
        print("\ndataframe.loc[LAST_CROISEMENT_EMA200_GOLDEN_CROSS_EMA15_INDEX].date > EMA15 :",LAST_DATE_CROISEMENT_EMA200_EMA15)
        mask_LAST_CROISEMENT_EMA200_GOLDEN_CROSS_EMA15=(dataframe.date >= dataframe.loc[LAST_CROISEMENT_EMA200_GOLDEN_CROSS_EMA15_INDEX].date) 
        #print("\nDataframe MASK mask_LAST_CROISEMENT_EMA200_GOLDEN_CROSS_EMA15 =\n",mask_LAST_CROISEMENT_EMA200_GOLDEN_CROSS_EMA15)
        val_mask_EMA15_idxmax=dataframe['EMA15'].loc[mask_ORG].idxmax()
        val_mask_EMA15_idxmin=dataframe['EMA15'].loc[mask_LAST_CROISEMENT_EMA200_GOLDEN_CROSS_EMA15].idxmin()
        val_mask_EMA15_idxmax=dataframe['EMA15'].loc[mask_LAST_CROISEMENT_EMA200_GOLDEN_CROSS_EMA15].idxmax()
        print("INDEX val_mask_EMA15_idxmin=",val_mask_EMA15_idxmin)
        print("INDEX val_mask_EMA15_idxmax=",val_mask_EMA15_idxmax)
        print("LAST INDEX :",last_index)
        print("\nDataframe MASK val_mask_EMA15_idxmin MIN=\n",dataframe[["date","EMA15"]].loc[val_mask_EMA15_idxmin])
        print("\nDataframe MASK val_mask_EMA15_idxmax MAX=\n",dataframe[["date","EMA15"]].loc[val_mask_EMA15_idxmax])
        DATE_MIN=dataframe.date.loc[val_mask_EMA15_idxmin]
        DATE_MAX=dataframe.date.loc[val_mask_EMA15_idxmax]
        DATE_COURANT=dataframe_date.date.loc[val_mask_idxmin]
        DATE_MIN=DATE_MIN.strftime("%Y-%m-%d %H:%M:%S")
        DATE_MAX=DATE_MAX.strftime("%Y-%m-%d %H:%M:%S")
        DATE_COURANT=DATE_COURANT.strftime("%Y-%m-%d %H:%M:%S")
        EMA15_MIN=dataframe.EMA15.loc[val_mask_EMA15_idxmin]
        EMA15_COURANT=dataframe.EMA15.loc[val_mask_idxmin]

        print("DATE_MIN",DATE_MIN)
        print("EMA15_MIN:", EMA15_MIN)
        print("DATE_COURANT",DATE_COURANT)
        print("EMA15_COURANT:",EMA15_COURANT)
        print("DATE_MAX",DATE_MAX)
        VAL_EMA1H_MAX=dataframe.EMA1H.loc[val_mask_EMA15_idxmax]
        print("\nDataframe  VAL_EMA1H_MAX =",VAL_EMA1H_MAX)
        VAL_EMA1H_COURANT=dataframe.EMA1H.loc[val_mask_idxmin]
        print("Dataframe  VAL_EMA1H_COURANT =",VAL_EMA1H_COURANT)
        EMA15=dataframe.EMA15.loc[val_mask_idxmin].astype(int)
        #print("LAST_DATE_CROISEMENT_EMA200_EMA15:",LAST_DATE_CROISEMENT_EMA200_EMA15)
        print("LAST_CROISEMENT_EMA200_GOLDEN_CROSS_EMA15.EMA15:",LAST_CROISEMENT_EMA200_GOLDEN_CROSS_EMA15.EMA15)
        print("Dataframe  EMA15 =",EMA15)
        EMA1L=dataframe.EMA1L.loc[val_mask_idxmin].astype(int)
        print("Dataframe  EMA1L =",EMA1L)
        EMA1H=dataframe.EMA1H.loc[val_mask_idxmin].astype(int)
        print("Dataframe  EMA1H =",EMA1H)
        EMA200=dataframe.EMA200.loc[val_mask_idxmin].astype(int)
        print("Dataframe  EMA200 =",EMA200)
        print("FRONT_MONTANT_EMA200 =",FRONT_MONTANT_EMA200)
        print("EMA15_COURANT >= LAST_CROISEMENT_EMA200_GOLDEN_CROSS_EMA15.EMA15:",EMA15_COURANT >= LAST_CROISEMENT_EMA200_GOLDEN_CROSS_EMA15.EMA15)
        print("EMA15_COURANT - EMA15_MIN > 1:",EMA15_COURANT - EMA15_MIN > 1)
        print("DATE_COURANT >= DATE_MIN:",DATE_COURANT >= DATE_MIN)
        print("ZONE ACHAT : (EMA15_COURANT >= LAST_CROISEMENT_EMA200_GOLDEN_CROSS_EMA15.EMA15 ) and (EMA15_COURANT - EMA15_MIN > 1) and (DATE_COURANT >= DATE_MIN):",\
              (EMA15_COURANT >= LAST_CROISEMENT_EMA200_GOLDEN_CROSS_EMA15.EMA15 ) and (int(EMA15_COURANT) - int(EMA15_MIN) > 1) and (DATE_COURANT >= DATE_MIN))

        VAL_EMA15_COURANT=dataframe.EMA15.loc[val_mask_idxmin].astype(int)
        VAL_EMA200_COURANT=dataframe.EMA200.loc[val_mask_idxmin].astype(int)
        DIFF_EMA200_EMA15=dataframe.DIFF_EMA200_EMA15.loc[val_mask_idxmin].astype(int)

        DIFF_EMA1H_COURANT_EMA1H_MAX=VAL_EMA1H_COURANT-VAL_EMA1H_MAX
        print("\nVAL_EMA1H_COURANT:",VAL_EMA1H_COURANT)
        print("VAL_EMA1H_MAX:",VAL_EMA1H_MAX)
        print("DIFF_EMA1H_COURANT_EMA1H_MAX:",DIFF_EMA1H_COURANT_EMA1H_MAX)
        DIFF_EMA1H_EMA200=EMA1H-EMA200
        print("ZONE VENTE : (DIFF_EMA1H_COURANT_EMA1H_MAX <= 0 ) and (DATE_COURANT >= DATE_MAX) and ( POINT_ENTRE_EMA200 == 1 ) and (float(VAL_CLOSE) > float(VAL_ACHAT)*1.01) :" \
              ,(DIFF_EMA1H_COURANT_EMA1H_MAX <= 0 ) and (DATE_COURANT >= DATE_MAX) and ( POINT_ENTRE_EMA200 == 1 ) and (float(VAL_CLOSE) > float(VAL_ACHAT)) and  (TYPE_BG == "BG_VERTE"))
        #VENTE AU MAXIMUN DE LA EMA1H
        if (DIFF_EMA1H_COURANT_EMA1H_MAX <= 0 ) and (DATE_COURANT >= DATE_MAX) and ( POINT_ENTRE_EMA200 == 1 )  and (float(VAL_CLOSE) > float(VAL_ACHAT)) : #and  (TYPE_BG == "BG_VERTE"):
            print("POINT DE VENTE : (DIFF_EMA1H_COURANT_EMA1H_MAX == 0) :",(DIFF_EMA1H_COURANT_EMA1H_MAX == 0 ))
            if (DIFF_EMA1H_COURANT_EMA1H_MAX == 0 ) and ( POINT_ENTRE_EMA200 == 1 ) :
                print("\nDATE_COURANT",DATE_COURANT)
                print("(DIFF_EMA1H_EMA200 == 0) :",DIFF_EMA1H_EMA200)
                global POINT_DE_VENTE
                POINT_DE_VENTE="OK"
                print("(POINT DE VENTE) :",POINT_DE_VENTE)
                POINT_ENTRE_EMA200=0
                #print("POINT_ENTRE_EMA1H=1")
                print("OK OK OK DERNIER_POINT_VENTE DANS TRANSITION_ACHAT_VENTE OK OK OK")
                #DERNIER_POINT_VENTE=1
                ORDER="SELL"
                print(ORDER)
                #LAST_ORDER="SELL"
                EXEC_ORDER(dataframe)
                POINT_ENTRE_EMA200 = 0
                #time.sleep(3)
                
        print("\nZONE VENTE ABSOLUE  VENTE TOUTE COURBE : (VAL_EMA15_COURANT >= VAL_EMA200_COURANT ) and (DATE_COURANT >= DATE_MAX) and (DIFF_EMA200_EMA15 == 0) and ( POINT_ENTRE_EMA200 == 1 )\
              and (float(VAL_CLOSE) > float(VAL_ACHAT)*1.01) and (VAL_CLOSE > VAL_ACHAT) : ",
              (VAL_EMA15_COURANT >= VAL_EMA200_COURANT ) and (DATE_COURANT >= DATE_MAX) and (DIFF_EMA200_EMA15 == 0) and ( POINT_ENTRE_EMA200 == 1 ) 
              and (float(VAL_CLOSE) > float(VAL_ACHAT)*1.01)) 
        if  (VAL_EMA15_COURANT >= VAL_EMA200_COURANT ) and (DATE_COURANT >= DATE_MAX) and (DIFF_EMA200_EMA15 == 0)  and ( POINT_ENTRE_EMA200 == 1 ) \
            and (float(VAL_CLOSE) > float(VAL_ACHAT)*1.01) and (DERNIER_POINT_VENTE == 0): #and (TYPE_BG == "BG_VERTE"): 
            POINT_DE_VENTE="VENTE_TOUTE_COURBE"
            print("(ZONE VENTE ABSOLUE  POINT DE VENTE TOUTE COURBE ) :",POINT_DE_VENTE)
            ORDER="SELL"
            print(ORDER)
            #LAST_ORDER="SELL"
            EXEC_ORDER(dataframe)
            POINT_ENTRE_EMA200 = 0
            #time.sleep(3)
            
            #print("DIFF_EMA1H_EMA200:",DIFF_EMA1H_EMA200)  (DIFF_EMA1H_EMA200 >= 0 )  and (DIFF_EMA1H_EMA200 < 15 ) andand (EMA1L <= VAL_EMA15_COURANT) and (EMA1H >= VAL_EMA15_COURANT)\
        #if  (FRONT_MONTANT_EMA200 == 1) \
        #if (FRONT_MONTANT_EMA200 == 0) and (FRONT_MONTANT_EMA15 == 0) and (DATE_COURANT > DATE_MIN) \
        #and (FRONT_MONTANT_COURT_EMA1L == 1) and (FRONT_MONTANT_COURT_EMA1H == 1)  and (VAL_EMA15_COURANT >= VAL_EMA200_COURANT ) and (POINT_ENTRE_EMA200 == 0) :
        print("\nZONE ACHAT : (EMA15_COURANT >= LAST_CROISEMENT_EMA200_GOLDEN_CROSS_EMA15.EMA15 ) and (EMA15_COURANT - EMA15_MIN > 1) and (DATE_COURANT >= DATE_MIN) :",\
              (FRONT_MONTANT_EMA200 == 1) and (FRONT_MONTANT_EMA15 == 1) and (EMA15_COURANT >= LAST_CROISEMENT_EMA200_GOLDEN_CROSS_EMA15.EMA15 ) and (int(EMA15_COURANT) - int(EMA15_MIN) > 1) and (DATE_COURANT >= DATE_MIN) and  (TYPE_BG == "BG_ROUGE"))
         
        # 1 CAS ACHAT EMA15 sup DERNIER CROISEMENT AVEC EMA200
        if   (FRONT_MONTANT_EMA200 == 1)  and (EMA15_COURANT >= LAST_CROISEMENT_EMA200_GOLDEN_CROSS_EMA15.EMA15 ) and (EMA15_COURANT - EMA15_MIN > 1) and (DATE_COURANT >= DATE_MIN) and (POINT_ENTRE_EMA200 == 0) and  (TYPE_BG == "BG_VERTE") \
            and (DERNIER_POINT_VENTE == 0) : 
            print("DATE_COURANT ZONE ACHAT EMA200",DATE_COURANT)
            print("EMA1H DANS ZONE ACHAT EMA200 : DIFF_EMA1H_EMA200:",DIFF_EMA1H_EMA200)
            ORDER="BUY"
            print(ORDER)
            #LAST_ORDER="BUY"
            EXEC_ORDER(dataframe)
            POINT_ENTRE_EMA200 = 1 #VEROUILAGE ACHAT ET VENTE NORMAL
            VAL_ACHAT=dataframe.close.loc[val_mask_idxmin]
            #time.sleep(3)
        print("\nSORTIR DANS TRANSITION_ACHAT_VENTE")
            
def ULTIMATE_NINJA(dataframe,val_mask_idxmin) :
        print("\nENTRER DANS ZONE ULTIMATE_NINJA ")
        global POINT_ENTRE_EMA200
        global ORDER
        global LAST_ORDER
        global FIRST_VENTE
        global VAL_ACHAT
        global DATE_COURANTE
        global SPEED_EMA200
        global FLAG_BEST_NBR_TAILLE_BG
        global custom_info
        global TAILLE_BG
        global TAILLE_BG_N1
        global TAILLE_BG_N2
        global TYPE_BG
        global TYPE_BG_N1
        global TYPE_BG_N2
        
        """
        if FLAG_BEST_NBR_TAILLE_BG == 1 :
           val_mask_idxmin=DETECT_MODE_REEL(dataframe,val_mask_idxmin)
        """
        """
        last_index=len(dataframe)-1
        print("last_index=",last_index)
        
        if val_mask_idxmin >= last_index :
            val_mask_idxmin=last_index  
        """
          
        CLOSE= dataframe['CLOSE'].loc[val_mask_idxmin].astype(int)
        VAL_EMA1H_COURANT=dataframe.EMA1H.loc[val_mask_idxmin].astype(int)
        #EMA1H=dataframe.EMA1H.loc[val_mask_idxmin]
        EMA1L=dataframe.EMA1L.loc[val_mask_idxmin].astype(int)
        EMA1H=dataframe.EMA1H.loc[val_mask_idxmin].astype(int)
        VAL_EMA15_COURANT=dataframe.EMA15.loc[val_mask_idxmin].astype(int)
        DATE_COURANT=dataframe.date.loc[val_mask_idxmin]
        DATE_COURANT=DATE_COURANT.strftime("%Y-%m-%d %H:%M:%S")  
        custom_info["HEURE_CROISEMENT_PAIR"]=dataframe.date.loc[val_mask_idxmin]
        print("DATE_COURANT",DATE_COURANT)
        print("EMA1L:",EMA1L)
        print("EMA1H:",VAL_EMA1H_COURANT)
        print("VAL_EMA200_COURANT:",VAL_EMA200_COURANT)
        print("CLOSE:",CLOSE)
        print("VAL_EMA15_COURANT:",VAL_EMA15_COURANT)
        print("FRONT_MONTANT_COURT_EMA1L:",FRONT_MONTANT_COURT_EMA1L)
        print("FRONT_MONTANT_COURT_EMA1H:",FRONT_MONTANT_COURT_EMA1H)
        print("FRONT_MONTANT_COURT_EMA15:",FRONT_MONTANT_COURT_EMA15)
        print("(FRONT_MONTANT_EMA15 == 0):",(FRONT_MONTANT_EMA15 == 0))
        print("(EMA1L <= VAL_EMA15_COURANT): ",(EMA1L <= VAL_EMA15_COURANT))
        #print("(int(EMA1H) >= int(VAL_EMA15_COURANT)): ",(int(EMA1H) >= int(VAL_EMA15_COURANT)))
        print("(FRONT_MONTANT_COURT_EMA1L == 1): ",(FRONT_MONTANT_COURT_EMA1L == 1))
        print("(FRONT_MONTANT_COURT_EMA1H == 1): ",(FRONT_MONTANT_COURT_EMA1H == 1))
        print("((EMA1L <= VAL_EMA15_COURANT) and  (int(VAL_EMA1H_COURANT) >= int(VAL_EMA15_COURANT))\
        and (FRONT_MONTANT_COURT_EMA1L == 1) and (FRONT_MONTANT_COURT_EMA1H == 0): ",(EMA1L <= VAL_EMA15_COURANT) and (int(VAL_EMA1H_COURANT) >= int(VAL_EMA15_COURANT)) \
        and (FRONT_MONTANT_COURT_EMA1L == 1) and (FRONT_MONTANT_COURT_EMA1H == 0) and  (TYPE_BG == "BG_ROUGE"))
        # 1 CAS ACHAT EMA1H > EMA15 > EMA1L (FRONT_MONTANT_COURT_EMA15 ==1) and and ( ORDER != LAST_ORDER ) 
        """
        if (EMA1L <= VAL_EMA15_COURANT) and (int(VAL_EMA1H_COURANT) >= int(VAL_EMA15_COURANT)) and (CLOSE <= VAL_EMA15_COURANT) \
           and (FRONT_MONTANT_EMA1L == 0)  and (POINT_ENTRE_EMA200 == 0)  and (DERNIER_POINT_VENTE == 0) and  (TYPE_BG == "BG_ROUGE") \
           or (EMA1L <= VAL_EMA15_COURANT) and (int(VAL_EMA1H_COURANT) >= int(VAL_EMA15_COURANT)) and (CLOSE <= VAL_EMA15_COURANT) and (VAL_EMA15_COURANT == VAL_EMA200_COURANT ) \
       and (FRONT_MONTANT_EMA1L == 0) and (FRONT_MONTANT_COURT_EMA1H == 1)  and (POINT_ENTRE_EMA200 == 0)  and (DERNIER_POINT_VENTE == 0) :
        """
        if (EMA1L <= VAL_EMA15_COURANT) and (int(VAL_EMA1H_COURANT) >= int(VAL_EMA15_COURANT)) and (CLOSE <= VAL_EMA15_COURANT) \
           and (FRONT_MONTANT_EMA1L == 0)  and (POINT_ENTRE_EMA200 == 0)  and (DERNIER_POINT_VENTE == 0) and  (TYPE_BG == "BG_ROUGE") :
           #and (FRONT_MONTANT_COURT_EMA1L == 1) and (FRONT_MONTANT_COURT_EMA1H == 1) and (POINT_ENTRE_EMA200 == 0)  and (DERNIER_POINT_VENTE == 0) : #\
        # | (EMA1L <= VAL_EMA15_COURANT) and (int(VAL_EMA1H_COURANT) >= int(VAL_EMA15_COURANT)) and ( ORDER != LAST_ORDER ) and (FRONT_MONTANT_EMA1H == 0) \
       #  and (FRONT_MONTANT_COURT_EMA1H == 1) and (FRONT_MONTANT_EMA15 == 0) and (FRONT_MONTANT_COURT_EMA15 == 0)  and (POINT_ENTRE_EMA200 == 0)  and (DERNIER_POINT_VENTE == 0) : #and  (TYPE_BG == "BG_ROUGE") :
             print("\n# 1 CAS ACHAT EMA1H > EMA15 >EMA1L")
             print("EMA1H DANS ZONE ACHAT ULTIMATE_NINJA ")
             ORDER="BUY"
             print(ORDER)
             #LAST_ORDER="BUY"
             EXEC_ORDER(dataframe)
             POINT_ENTRE_EMA200 = 1 #VEROUILAGE ACHAT ET VENTE NORMAL
             VAL_ACHAT=dataframe.close.loc[val_mask_idxmin]
        

        # 3eme CAS ACHAT EMA1H > EMA15 et EMA1L > EMA15  SONT TOUTE MONTANTE and (LAST_ORDER == "SELL")
        print("EMA1H:",VAL_EMA1H_COURANT)
        print("VAL_EMA200_COURANT:",VAL_EMA200_COURANT)
        #if (FRONT_MONTANT_EMA15 == 1) and (EMA1L >= VAL_EMA15_COURANT) and (int(VAL_EMA1H_COURANT) >= int(VAL_EMA15_COURANT)) and ( ORDER != LAST_ORDER )  \ and (VAL_EMA15_COURANT > VAL_EMA200_COURANT )
        if (FRONT_MONTANT_EMA1H == 1) and  (int(EMA1L) >= int(VAL_EMA15_COURANT)) and  (int(EMA1H) >= int(VAL_EMA15_COURANT))   and (POINT_ENTRE_EMA200 == 0)  and (DERNIER_POINT_VENTE == 0) \
        and ( ORDER != LAST_ORDER ) and (SPEED_EMA15 >= 0) and (SPEED_EMA200 == 0)  and (FRONT_MONTANT_EMA15 == 1 ): 
        #if  (int(EMA1H) == int(VAL_EMA15_COURANT) ) :
             print("\n# 3eme CAS ACHAT EMA1H == EMA15 et EMA15 > EMA200 ET ELLE SONT TOUTE MONTANTE")
             print("EMA1H ET EMA1L AU DESSUS EMA15 FRONT MONTANT DANS ZONE ACHAT ULTIMATE_NINJA ")
             ORDER="BUY"
             print(ORDER)
             #LAST_ORDER="BUY"
             EXEC_ORDER(dataframe)
             VAL_ACHAT=dataframe.close.loc[val_mask_idxmin]
             POINT_ENTRE_EMA200 = 1 #VEROUILAGE ACHAT ET VENTE NORMAL
             #exit()
        
        # 4eme CAS ACHAT EMA1H < EMA15 et EMA1H > EMA1H ET EMA1L ET EMA1H SONT TOUTE MONTANTE and (LAST_ORDER == "SELL")
        print("EMA1H:",VAL_EMA1H_COURANT)
        print("VAL_EMA200_COURANT:",VAL_EMA200_COURANT)
        if (FRONT_MONTANT_EMA15 == 0) and (FRONT_MONTANT_EMA1H == 1) and (FRONT_MONTANT_COURT_EMA1H == 0) and (FRONT_MONTANT_COURT_EMA1L == 0)   \
        and (POINT_ENTRE_EMA200 == 0)  and (DERNIER_POINT_VENTE == 0) and ( ORDER != LAST_ORDER ) and (SPEED_EMA15 >= 1) and (SPEED_EMA200 >= 0) : 
        #if  (int(EMA1H) == int(VAL_EMA15_COURANT) ) :
             print("\n# 4eme CAS ACHAT EMA1H < EMA15 et EMA1H > EMA1H ET EMA1L ET EMA1H SONT TOUTE MONTANTE ")
             print("EMA1H ET EMA1L EN DESSOUS EMA200 FRONT MONTANT DANS ZONE ACHAT ULTIMATE_NINJA ")
             ORDER="BUY"
             print(ORDER)
             #LAST_ORDER="BUY"
             EXEC_ORDER(dataframe)
             VAL_ACHAT=dataframe.close.loc[val_mask_idxmin]
             POINT_ENTRE_EMA200 = 1 #VEROUILAGE ACHAT ET VENTE NORMAL
             #exit()        
        
        """
        if (FRONT_MONTANT_EMA15 == 1) and (FRONT_MONTANT_COURT_EMA15 == 1) and (EMA1L >= VAL_EMA15_COURANT) and (int(VAL_EMA1H_COURANT) >= int(VAL_EMA15_COURANT)) and ( ORDER != LAST_ORDER )  \
         and (FRONT_MONTANT_COURT_EMA1H == 1) and (FRONT_MONTANT_EMA1H == 1)  and (POINT_ENTRE_EMA200 == 0) and (VAL_EMA15_COURANT <= VAL_EMA200_COURANT )  and (DERNIER_POINT_VENTE == 0)  : # and  (TYPE_BG == "BG_ROUGE"):
             print("\n# 2eme CAS ACHAT EMA1H > EMA15 et EMA1L > EMA15 ET ELLE SONT TOUTE MONTANTE")
             print("EMA1H ET EMA1L AU DESSUS EMA15 FRONT MONTANT DANS ZONE ACHAT ULTIMATE_NINJA ")
             ORDER="BUY"
             print(ORDER)
             LAST_ORDER="BUY"
             EXEC_ORDER(dataframe)
             POINT_ENTRE_EMA200 = 1 #VEROUILAGE ACHAT ET VENTE NORMAL
             VAL_ACHAT=dataframe.close.loc[val_mask_idxmin]
        """
          # FIATS = ['EURUSDT', 'GBPUSDT', 'JPYUSDT', 'USDUSDT', 'DOWN', 'UP'] 
          # all(item not in coin['symbol'] for item in FIATS)
          
        #LISTE = [30,40,50,100,200]

        LISTE = ['20','30','40','50','100','200']
        LISTE_EMA15_EMA200 = [5,10,20,30,40,50,60,70,100,200]
        DIFF_EMA1H_EMA15=(int(VAL_EMA1H_COURANT) - int(VAL_EMA15_COURANT))
        print("\nEMA1H DANS ZONE VENTE ULTIMATE_NINJA")
        print("DIFF_EMA1H_EMA15:",DIFF_EMA1H_EMA15)
        print("all(DIFF_EMA1H_EMA15 >= item for item in LISTE) :",(DIFF_EMA1H_EMA15 >= int(item) for item in LISTE))
        """
        print("(FRONT_MONTANT_EMA15 == 0) and (EMA1L <= VAL_EMA15_COURANT) and (int(VAL_EMA1H_COURANT) >= int(VAL_EMA15_COURANT)) \
         and (FRONT_MONTANT_COURT_EMA1L == 0) and (FRONT_MONTANT_COURT_EMA1H == 0) and (DIFF_EMA1H_EMA15 >= item for item in LISTE) :",\
             (FRONT_MONTANT_EMA15 == 0) and (EMA1L <= VAL_EMA15_COURANT) and (int(VAL_EMA1H_COURANT) >= int(VAL_EMA15_COURANT))\
              and (FRONT_MONTANT_COURT_EMA1L == 0) and (FRONT_MONTANT_COURT_EMA1H == 0) and all(DIFF_EMA1H_EMA15 >= item for item in LISTE))
         #1 CAS VENTE SUR GRANDE BOUGIE  
        """
        """ 
        if (FRONT_MONTANT_EMA15 == 0) and (EMA1L <= VAL_EMA15_COURANT) and (int(VAL_EMA1H_COURANT) >= int(VAL_EMA15_COURANT))\
         and (FRONT_MONTANT_COURT_EMA1L == 0) and (FRONT_MONTANT_COURT_EMA1H == 0) and all(DIFF_EMA1H_EMA15 >= item for item in LISTE)  and ( POINT_ENTRE_EMA200 == 2 ) \
             and (float(VAL_CLOSE) > float(VAL_ACHAT)*1.01) : 
         """
        print("LISTE=",LISTE)
        print("(FRONT_MONTANT_EMA15 ==1) and (EMA1L >= VAL_EMA15_COURANT) and (FRONT_MONTANT_COURT_EMA1L == 0) and (FRONT_MONTANT_COURT_EMA1H == 0) \
              and (DIFF_EMA1H_EMA15 >= item for item in LISTE)(FRONT_MONTANT_EMA15 == 1) and (EMA1L >= VAL_EMA15_COURANT) and (FRONT_MONTANT_COURT_EMA1L == 0) and (FRONT_MONTANT_COURT_EMA1H == 0) \
                  and (DIFF_EMA1H_EMA15 >= int(item) for item in LISTE) and (POINT_ENTRE_EMA200 == 2)  and (VAL_EMA15_COURANT - VAL_EMA200_COURANT >= int(item) for item in LISTE_EMA15_EMA200) \
                  and (VAL_EMA15_COURANT > VAL_EMA200_COURANT) and (float(VAL_CLOSE) > float(VAL_ACHAT)) :",\
              (FRONT_MONTANT_EMA15 == 1) and (EMA1L >= VAL_EMA15_COURANT) and (FRONT_MONTANT_COURT_EMA1L == 0) and (FRONT_MONTANT_COURT_EMA1H == 0) \
                  and (DIFF_EMA1H_EMA15 >= int(item) for item in LISTE) and (POINT_ENTRE_EMA200 == 2)  and (VAL_EMA15_COURANT - VAL_EMA200_COURANT >= int(item) for item in LISTE_EMA15_EMA200) \
                  and (VAL_EMA15_COURANT > VAL_EMA200_COURANT) and (float(VAL_CLOSE) > float(VAL_ACHAT)) and  (TYPE_BG == "BG_VERTE") )
        index=0    
        while index < len(LISTE_EMA15_EMA200) :
         TBG=LISTE_EMA15_EMA200[index]
         print(TBG)
         index += 1 
         #and int((VAL_EMA15_COURANT - VAL_EMA200_COURANT) >= TBG) and (FRONT_MONTANT_COURT_EMA1L == 0)
         """
         if (FRONT_MONTANT_EMA15 == 1) and (EMA1L >= VAL_EMA15_COURANT)  and (FRONT_MONTANT_COURT_EMA1H == 0) and ( ORDER != LAST_ORDER )  \
            and (DIFF_EMA1H_EMA15 >= int(item) for item in LISTE) and (POINT_ENTRE_EMA200 == 1) and (float(VAL_CLOSE) > float(VAL_ACHAT)) \
            : #and  (TYPE_BG == "BG_VERTE")  : and (EMA1L != VAL_EMA1H_COURANT)
         """
         DATE_COURANTE_VENTE = DATE_COURANTE - pd.Timedelta(minutes=val_minute)
         if (FRONT_MONTANT_EMA1H == 1 )  and (FRONT_MONTANT_COURT_EMA1H == 0 ) and (DATE_COURANTE_VENTE == VAL_EMA1H_DATE_MAX)  \
            and (FRONT_MONTANT_EMA15 == 1) and (EMA1L >= VAL_EMA15_COURANT) and ( ORDER != LAST_ORDER )  \
            and (POINT_ENTRE_EMA200 == 1) and (float(VAL_CLOSE) > float(VAL_ACHAT)) :
            #and (DIFF_EMA1H_EMA15 >= int(item) for item in LISTE) and (POINT_ENTRE_EMA200 == 1) and (float(VAL_CLOSE) > float(VAL_ACHAT)) :
             print("POINT DE VENTE HAUT EMA1H: CONDITION ACHAT \nDATE_COURANTE_VENTE: ",DATE_COURANTE_VENTE)
             print("EMA1H DANS ZONE DE VENTE ULTIMATE_NINJA ")
             ###custom_info["HEURE_CROISEMENT_PAIR"]=DATE_COURANTE_VENTE
             ORDER="SELL"
             #LAST_ORDER="SELL"
             print(ORDER)
             EXEC_ORDER(dataframe)    
             POINT_ENTRE_EMA200 = 0 #DEVEROUILAGE ACHAT ET VENTE NORMAL  \ #and (VAL_EMA15_COURANT - VAL_EMA200_COURANT >= int(item) for item in LISTE_EMA15_EMA200) \
             FIRST_VENTE+=1
             #exit()
             
        #and (DATE_COURANTE_VENTE == VAL_EMA1H_DATE_MAX) and (DIFF_EMA200_EMA15 >= 2)
        DIFF_EMA200_EMA15=dataframe.DIFF_EMA200_EMA15.loc[val_mask_idxmin].astype(int)
        #DATE_COURANTE_VENTE = DATE_COURANTE - pd.Timedelta(minutes=val_minute)
        """
        if (FRONT_MONTANT_EMA1L == 1 ) and (FRONT_MONTANT_COURT_EMA1L == 0 ) and (FRONT_MONTANT_EMA1H == 1 ) and (FRONT_MONTANT_COURT_EMA1H == 0 )   \
            and (EMA1L <= VAL_EMA15_COURANT) and ( ORDER != LAST_ORDER )  \
            and (POINT_ENTRE_EMA200 == 2) and (float(VAL_CLOSE) > float(VAL_ACHAT)) :
        """
        #"""
        if (custom_info["ACHAT_EN_DESSOUS_EMA200"] == 0) and (FRONT_MONTANT_EMA1L == 1 ) and (FRONT_MONTANT_COURT_EMA1L == 1 ) and (FRONT_MONTANT_EMA1H == 1 ) and (FRONT_MONTANT_COURT_EMA1H == 1 )   \
            and (EMA1L >= VAL_EMA15_COURANT) and ( ORDER != LAST_ORDER ) and (POINT_ENTRE_EMA200 == 1) and (float(VAL_CLOSE) > float(VAL_ACHAT)) :
            #and (POINT_ENTRE_EMA200 == 2) and (float(VAL_CLOSE) > float(VAL_ACHAT)) :
        #"""
            #and (DIFF_EMA1H_EMA15 >= int(item) for item in LISTE) and (POINT_ENTRE_EMA200 == 1) and (float(VAL_CLOSE) > float(VAL_ACHAT)) :
            print("POINT DE VENTE SOMMET EMA1H: CONDITION VENTE \nDATE_COURANTE_VENTE: ",DATE_COURANTE_VENTE)
            print("EMA1H DANS ZONE DE VENTE ULTIMATE_NINJA ")
            #custom_info["HEURE_CROISEMENT_PAIR"]=DATE_COURANTE_VENTE
            ORDER="SELL"
            #LAST_ORDER="SELL"
            print(ORDER)
            EXEC_ORDER(dataframe)    
            POINT_ENTRE_EMA200 = 0 #DEVEROUILAGE ACHAT ET VENTE NORMAL  \ #and (VAL_EMA15_COURANT - VAL_EMA200_COURANT >= int(item) for item in LISTE_EMA15_EMA200) \
            FIRST_VENTE+=1
            #exit()       
            
        if (custom_info["ACHAT_EN_DESSOUS_EMA200"] == 0) and (FRONT_MONTANT_EMA1L == 1 ) and (FRONT_MONTANT_COURT_EMA1L == 1 ) and (FRONT_MONTANT_EMA1H == 1 ) and (FRONT_MONTANT_COURT_EMA1H == 1 )   \
            and (EMA1L >= VAL_EMA15_COURANT) and ( ORDER != LAST_ORDER ) and (POINT_ENTRE_EMA200 == 1) and (float(VAL_CLOSE) > float(VAL_ACHAT)) \
            and (SPEED_EMA15 > 0) and (SPEED_EMA200 > 20 )     :
            print("POINT DE VENTE SOMMET SUR ACCELERATION SPEED_EMA200 EMA1H: CONDITION VENTE \nDATE_COURANTE_VENTE: ",DATE_COURANTE_VENTE)
            print("EMA1H DANS ZONE DE VENTE ULTIMATE_NINJA ")
            #custom_info["HEURE_CROISEMENT_PAIR"]=DATE_COURANTE_VENTE
            ORDER="SELL"
            #LAST_ORDER="SELL"
            print(ORDER)
            EXEC_ORDER(dataframe)    
            POINT_ENTRE_EMA200 = 0 #DEVEROUILAGE ACHAT ET VENTE NORMAL  \ #and (VAL_EMA15_COURANT - VAL_EMA200_COURANT >= int(item) for item in LISTE_EMA15_EMA200) \
            FIRST_VENTE+=1
            #exit()  
            
        if (custom_info["ACHAT_EN_DESSOUS_EMA200"] == 0) and (FRONT_MONTANT_EMA1L == 1 ) and (FRONT_MONTANT_COURT_EMA1L == 1 ) and (FRONT_MONTANT_EMA1H == 1 ) and (FRONT_MONTANT_COURT_EMA1H == 1 )   \
            and (EMA1L >= VAL_EMA15_COURANT) and ( ORDER != LAST_ORDER ) and (POINT_ENTRE_EMA200 == 1) and (float(VAL_CLOSE) > float(VAL_ACHAT)) \
            and (SPEED_EMA1L == 0) and (TYPE_BG_N2 == "BG_VERTE") and (TYPE_BG_N1 == "BG_VERTE") and (TYPE_BG == "BG_ROUGE")  :
            print("POINT DE VENTE SOMMET EMA1H SUR ACCELERATION SPEED_EMA200 EMA1H == 0 : CONDITION VENTE \nDATE_COURANTE_VENTE: ",DATE_COURANTE_VENTE)
            print("EMA1H DANS ZONE DE VENTE ULTIMATE_NINJA ")
            #custom_info["HEURE_CROISEMENT_PAIR"]=DATE_COURANTE_VENTE
            ORDER="SELL"
            #LAST_ORDER="SELL"
            print(ORDER)
            EXEC_ORDER(dataframe)    
            POINT_ENTRE_EMA200 = 0 #DEVEROUILAGE ACHAT ET VENTE NORMAL  \ #and (VAL_EMA15_COURANT - VAL_EMA200_COURANT >= int(item) for item in LISTE_EMA15_EMA200) \
            FIRST_VENTE+=1
            #exit()   
        
        if  (custom_info["ACHAT_EN_DESSOUS_EMA200"] == 1) and (EMA1H > VAL_EMA200_COURANT) and (float(VAL_CLOSE) > float(VAL_ACHAT)) and (POINT_ENTRE_EMA200 == 1) :
            print("POINT DE VENTE AU DEPASSEMENT DU SOMMET EMA200  SUITE  ACHAT EN DESSOUS EMA200 :\nDATE_COURANTE_VENTE: ",DATE_COURANTE_VENTE)
            print("EMA1H DANS ZONE DE VENTE ULTIMATE_NINJA ")
            print("ACHAT_EN_DESSOUS_EMA200: ",custom_info["ACHAT_EN_DESSOUS_EMA200"])
            #custom_info["HEURE_CROISEMENT_PAIR"]=DATE_COURANTE_VENTE
            ORDER="SELL"
            #LAST_ORDER="SELL"
            print(ORDER)
            EXEC_ORDER(dataframe)    
            POINT_ENTRE_EMA200 = 0 #DEVEROUILAGE ACHAT ET VENTE NORMAL  \ #and (VAL_EMA15_COURANT - VAL_EMA200_COURANT >= int(item) for item in LISTE_EMA15_EMA200) \
            #exit()    
            
        print("SORTIE DANS ZONE ULTIMATE_NINJA\n")
    
def Delay_new_frame(delai=False):
    global custom_info
    global DERNIER_POINT_VENTE
    val_minute=1
    now=datetime.now()
    #print(now)
    #hour=now.strftime("%Y-%m-%d %H:%M:%S")
    #custom_info["HEURE_CROISEMENT_PAIR"]=hour[:-3]+":00"
    new_hour=now  #  + timedelta(hours=2)   
    new_hour=new_hour.strftime("%Y-%m-%d %H:%M:%S")
    new_hour=new_hour.split(".")[0]
    seconde=new_hour.split(":")[2]
    if (delai != ""):
        Diff_seconde=delai
        DERNIER_POINT_VENTE = 1
    else:
        if 59-int(seconde)-2 >= 0 :
            Diff_seconde=59-int(seconde)-2
        else:
            Diff_seconde=59-int(seconde)
    new_hour=datetime.strptime(new_hour, '%Y-%m-%d %H:%M:%S')
    DATE_FUTUR=new_hour  + pd.Timedelta(seconds=Diff_seconde)
    #Diff_seconde=10
    #print(seconde)
    print("Delais d Attente de la prochaine minute de : ",Diff_seconde," secondes (",DATE_FUTUR,")")
    time.sleep(int(Diff_seconde))
    
def CALCULE_SECONDE():
    now=datetime.now()
    new_hour=now  #+ timedelta(hours=2)   
    new_hour=new_hour.strftime("%Y-%m-%d %H:%M:%S")
    new_hour=new_hour.split(".")[0]
    seconde=new_hour[-2:]
    #new_hour=new_hour[:-3]  
    return seconde

def CALCULE_FIN_CYCLE():
    from datetime import datetime, timedelta
    import pandas as pd
    global DATE_VENTE_FUTUR
    global TEMPS
    now=datetime.now()
    new_hour=now  #+ timedelta(hours=2)   
    new_hour=new_hour.strftime("%Y-%m-%d %H:%M:%S")
    new_hour=new_hour.split(".")[0]
    seconde=new_hour[-2:]
    new_hour=datetime.strptime(new_hour, '%Y-%m-%d %H:%M:%S')
    DATE_FUTUR=new_hour  + pd.Timedelta(minutes=TEMPS)
    print("new_hour:",new_hour)
    print("DATE_FUTUR:",DATE_FUTUR)
    DATE_FUTUR=DATE_FUTUR.strftime("%Y-%m-%d %H:%M:%S")
    DATE_VENTE_FUTUR=DATE_FUTUR[:-3]
    print("DATE_VENTE_FUTURR:",DATE_VENTE_FUTUR)
    return DATE_FUTUR      

def CALCULE_RENTABILITE():
    a = 1000 
    t = 5
    i = 0
    j = 30
    
    while (i < j):
        print ("jour",i);
        b=(a*t/100)+a
        print (b)
        a  = b 
        i = i+1


def ULTIMATE_NINJA_NEW(dataframe,val_mask_idxmin) :
        print("\nENTRER DANS ZONE ULTIMATE_NINJA NEW")
        #TRAITEMENT_BOUGIE(dataframe,val_mask_idxmin)
        global POINT_ENTRE_EMA200
        global ORDER
        global LAST_ORDER
        global FIRST_VENTE
        global VAL_ACHAT
        global DATE_COURANTE
        global SPEED_EMA200
        global FLAG_BEST_NBR_TAILLE_BG
        global custom_info
        global TAILLE_BG
        global TAILLE_BG_N1
        global TAILLE_BG_N2
        global TAILLE_BG_N3
        global TYPE_BG_BIS
        global TAILLE_BG_BIS
        global TYPE_BG
        global TYPE_BG_N1
        global TYPE_BG_N2
        global TYPE_BG_N3
        global VAL_OPEN
        global VAL_CLOSE
        global VAL_OPEN_N1
        global VAL_CLOSE_N1
        global VAL_OPEN_N2
        global VAL_CLOSE_N2    
        global VAL_OPEN_N3
        global VAL_CLOSE_N3
        global DIFF_EMA200_CLOSE
        global DIFF_EMA200_EMA15
        global CUMUL_TAILLE_BG_ROUGE
        global CUMUL_TAILLE_BG_VERTE
        global CUMUL_TAILLE_BG_N1_N2
        global CUMUL_TAILLE_BG_N1_N2_N3

        global LAST_CROISEMENT_EMA1H_EMA1L_DESS_CROSS
        
        global FRONT_MONTANT_EMA15
        global FRONT_MONTANT_EMA1H
        global FRONT_MONTANT_EMA1L
        global FRONT_MONTANT_EMA200
        global FRONT_MONTANT_COURT_EMA15
        global FRONT_MONTANT_COURT_EMA1H
        global FRONT_MONTANT_COURT_EMA1L
        global FRONT_MONTANT_COURT_EMA200
        global FRONT_NEUTRE_COURT_EMA200
        global FRONT_NEUTRE_COURT_EMA15
        global FRONT_NEUTRE_COURT_EMA1L
        global FRONT_NEUTRE_EMA1L
        global TYPE_FRONT_EMA15
        global TYPE_FRONT_EMA1L
        global TYPE_FRONT_EMA1H
        global TYPE_FRONT_EMA200
        global TYPE_FRONT_COURT_EMA15
        global TYPE_FRONT_COURT_EMA1L
        global TYPE_FRONT_COURT_EMA1H
        global TYPE_FRONT_COURT_EMA200
        
        global VAL_EMA15_COURANT
        global VAL_EMA15_PRECEDENT
        global VAL_EMA1L_COURANT
        global VAL_EMA1H_COURANT
        global VAL_EMA200_COURANT
        global DERNIER_POINT_VENTE
        global last_price
        global COULEUR_VOLUME
        global VOLUME_ASK
        global PRICE_ASK
        global VOLUME_BID
        global PRICE_BID
        global DATE_HEURE
        global NEW_EMA1H
        global NEW_EMA1L
        global NEW_LAST_PRICE
        global MULTIP
        global FIRST_ACHAT
        global NBR_LAST_PRICE
        global OLD_LAST_PRICE
        global GAIN_RELATIF
        global NBR_Diff_last_price_OLD_LAST_PRICE
        global Diff_LAST_PRICE_OLD_File_price
        global time_difference
        global DERNIERE_VENTE_POSITIVE
        global PRIX
        global COMPTEUR_ACHAT_VENTE
        global COMPTEUR_VENTE_RELATIVE
        global FRONT_MONTANT_COURT_VOLUME
        # global Diff_VOLUME_VWAP_LAST_PRICE_OLD_LAST_PRICE
        global LAST_PRICE
        global Diff_VAL_ACHAT_GAIN1_MOINS_VAL_ACHAT
        global DIFF_EMA1H_EMA15
        global LAST_VOLUME_VWAP_Price
        global PRIX
        global Diff_VOLUME_VWAP_Diff_VOLUME_VWAP_OLD
        global dataframe_date
        global Diff_last_price_OLD_LAST_PRICE
        global last_price_file
        global NEW_HIGH_PRICE
        global NEW_OPEN_PRICE
        global GAIN_OLD
        global GAIN1
        global DIFF_VAL_CLOSE_INF_VAL_CLOSE_N2
        global PRICE_VOLUME_ASK
        global PRICE_VOLUME_BID
        global SPREAD
        global DIFF_NEW_HIGH_PRICE_SUP_NEW_OPEN_PRICE
        # GAIN1=0
        global DATE_VENTE_FUTUR
        global TEMPS
        global CYCLE_COURT
        global GAIN_ABSOLUE_RELATIF
        global GAIN_ABSOLUE
        global VAL_ACHAT_INITIALE
        global COMPTEUR_GAIN_ZERO
        global DIFF_SAR_SUP_PRIX
        global COMPTEUR_DIFF_GAIN1_EGAL
        global NBR_COMPTEUR_DIFF_GAIN1
        global VAL_ACHAT_INITIALE   
        global DIFF_GAIN1_INF_GAIN_OLD
        global DIFF_SAR_SUP_EMA15
        global DIFF_SAR_SUP_OPEN

        # if NEW_EMA1L!= "None" :
        #     FRONT_MONTANT_COURT_EMA1H=NEW_EMA1L
        # if NEW_EMA1H != "None" :
        #     FRONT_MONTANT_COURT_EMA1H=NEW_EMA1H
        # if NEW_LAST_PRICE == 1 :
        #     TYPE_BG = "BG_VERTE"
        # if NEW_LAST_PRICE == 0 :
        #     TYPE_BG = "BG_ROUGE"

        #else:
           #global FRONT_MONTANT_COURT_EMA1H

        
        
        """
        if FLAG_BEST_NBR_TAILLE_BG == 1 :
           val_mask_idxmin=DETECT_MODE_REEL(dataframe,val_mask_idxmin)
        """
        last_index=len(dataframe)-1
        print("last_index=",last_index)
        print("val_mask_idxmin=",val_mask_idxmin)

        """
        if val_mask_idxmin >= last_index :
            val_mask_idxmin=last_index  
        """
        """
        if val_mask_idxmin == last_index :
           val_mask_idxmin=val_mask_idxmin-1
        """
        #if FLAG_BEST_NBR_TAILLE_BG == 1 :
        #    val_mask_idxmin=last_index  


        EMA200=dataframe['EMA200'].iloc[last_index].astype(int)
        OPEN=dataframe['OPEN'].loc[last_index].astype(int)    
        open=dataframe['open'].loc[last_index].astype(float)    
        CLOSE=dataframe['CLOSE'].loc[last_index].astype(int)
        HIGH=dataframe['HIGH'].loc[last_index].astype(int)
        VAL_EMA1H_COURANT=dataframe.EMA1H.loc[val_mask_idxmin].astype(int)
        VAL_EMA1H_COURANT_N1=dataframe.EMA1H.iloc[-1].astype(int)
        VAL_EMA1H_COURANT_N2=dataframe.EMA1H.iloc[-2].astype(int)
        DIFF_EMA1H_COURANT_N1=(VAL_EMA1H_COURANT - VAL_EMA1H_COURANT_N1 > 0)
        DIFF_EMA1H_N1_N2=(VAL_EMA1H_COURANT_N1 - VAL_EMA1H_COURANT_N2 <= 0)
        TEST_ACHAT_REBOND_EMA1H=(DIFF_EMA1H_COURANT_N1 == True) and  (DIFF_EMA1H_N1_N2 == True)
        DIFF_EMA1H_COURANT_N2=(VAL_EMA1H_COURANT - VAL_EMA1H_COURANT_N2 > 0)
        TEST_VENTE_SOMMET_EMA1H=(DIFF_EMA1H_COURANT_N2 == True) and ((TYPE_BG_N2 == "BG_VERTE") or (TYPE_BG_N1 == "BG_VERTE")) 

        #EMA1H=dataframe.EMA1H.loc[val_mask_idxmin]
        EMA1L=dataframe.EMA1L.iloc[-1].astype(int)
        EMA1H=dataframe.EMA1H.iloc[-1].astype(int)
        EMA200=dataframe.EMA200.iloc[-1].astype(int)
        VAL_EMA15_COURANT=dataframe.EMA15.iloc[-1].astype(int)
        PSAR=dataframe.PSAR.iloc[-1].astype(int)
        DATE_COURANT=dataframe_date.date.loc[val_mask_idxmin]
        DATE_COURANT=DATE_COURANT.strftime("%Y-%m-%d %H:%M:%S")  
        #custom_info["HEURE_CROISEMENT_PAIR"]=dataframe.date.loc[last_index]
        now=datetime.now()
        #print(now)
        hour=now.strftime("%Y-%m-%d %H:%M:%S")
        custom_info["HEURE_CROISEMENT_PAIR"]=hour[:-3]+":00"
        
        Diff_VOLUME_COURANT_VOLUME_PRECEDENT=0
        
        if last_index >= 5 :
            VOLUME_PRECEDENT=dataframe.volume.iloc[-2]
            VOLUME_COURANT=dataframe.volume.iloc[-1]
            Diff_VOLUME_COURANT_VOLUME_PRECEDENT=(float(VOLUME_COURANT)-float(VOLUME_PRECEDENT))
            # Diff_VOLUME_COURANT_VOLUME_PRECEDENT=int(Diff_VOLUME_COURANT_VOLUME_PRECEDENT*MULTIP)
            print("Diff_VOLUME_COURANT_VOLUME_PRECEDENT:",Diff_VOLUME_COURANT_VOLUME_PRECEDENT)
            # TEST_K_AND_M_IN_VOLUME="K" in VOLUME_COURANT or "M" in VOLUME_COURANT
            VOLUME_COURANT=str(VOLUME_COURANT).split(".")[0]
            # VOLUME_COURANT=str(VOLUME_COURANT).replace(".","")
            TEST_K_AND_M_IN_VOLUME=len(VOLUME_COURANT)  >= 4
            print("TEST_K_AND_M_IN_VOLUME:",TEST_K_AND_M_IN_VOLUME)
            if TEST_K_AND_M_IN_VOLUME == True :
                print("VOLUME_COURANT:",VOLUME_COURANT)
                # exit()
            # exit()

        # open=(format(open,'.8f'))
        # NEW_OPEN_PRICE=(format(NEW_OPEN_PRICE,'.8f'))
        # last_price=(format(last_price,'.8f'))
        print("DATE_COURANT",DATE_COURANT)
        print("EMA1L:",EMA1L)
        print("EMA1H:",VAL_EMA1H_COURANT)
        print("VAL_EMA200_COURANT:",VAL_EMA200_COURANT)
        print("EMA200:",EMA200)
        print("OPEN:",OPEN)
        print("open:",(format(open,'.8f')))
        print("CLOSE:",CLOSE)
        print("VAL_EMA15_COURANT:",VAL_EMA15_COURANT)
        print("VAL_EMA1H_COURANT_N2:",VAL_EMA1H_COURANT_N2)
        print("VAL_EMA1H_COURANT_N1:",VAL_EMA1H_COURANT_N1)
        print("VAL_EMA1H_COURANT:",VAL_EMA1H_COURANT)
        print("DIFF_EMA1H_N1_N2:",DIFF_EMA1H_N1_N2)
        print("DIFF_EMA1H_COURANT_N1:",DIFF_EMA1H_COURANT_N1)
        print("TEST_ACHAT_REBOND_EMA1H:",TEST_ACHAT_REBOND_EMA1H)
        print("DIFF_EMA1H_COURANT_N2:",DIFF_EMA1H_COURANT_N2)
        print("TEST_VENTE_SOMMET_EMA1H:",TEST_VENTE_SOMMET_EMA1H)
        print("FRONT_MONTANT_COURT_EMA1H:",FRONT_MONTANT_COURT_EMA1H)
        print("FRONT_MONTANT_COURT_EMA1L:",FRONT_MONTANT_COURT_EMA1L)
        print("FRONT_MONTANT_COURT_EMA15:",FRONT_MONTANT_COURT_EMA15)
        print("(FRONT_MONTANT_EMA15 == 0):",(FRONT_MONTANT_EMA15 == 0))
        print("FRONT_MONTANT_EMA15 :",FRONT_MONTANT_EMA15 )
        print("(EMA1L <= VAL_EMA15_COURANT): ",(EMA1L <= VAL_EMA15_COURANT))
        #print("(int(EMA1H) >= int(VAL_EMA15_COURANT)): ",(int(EMA1H) >= int(VAL_EMA15_COURANT)))
        print("(FRONT_MONTANT_COURT_EMA1L == 1): ",(FRONT_MONTANT_COURT_EMA1L == 1))
        print("(FRONT_MONTANT_COURT_EMA1H == 1): ",(FRONT_MONTANT_COURT_EMA1H == 1))
        # print("TRAME_EMA200_EMA15_MOINS_1: \n",TRAME_EMA200_EMA15_MOINS_1)
        # print("DIFF_EMA200_EMA15_MOINS_1:",DIFF_EMA200_EMA15_MOINS_1)
        # print("TRAME_EMA200_EMA15: \n",TRAME_EMA200_EMA15)
        # print("DIFF_EMA200_EMA15:",DIFF_EMA200_EMA15)
        # print("\nVARIATION_EMA200_EMA15  :",VARIATION_EMA200_EMA15)
        print("dataframe:;\n",dataframe.tail())
        #exit()
        #if  int(DIFF_EMA200_EMA15_MOINS_1) < 0 :# and int(DIFF_EMA200_EMA15) >= 0:
        #if  int(DIFF_EMA200_EMA15_MOINS_1) == -1 :
        #if  int(DIFF_EMA200_EMA15_MOINS_1) < 0 :
            #exit()

       # if  int(DIFF_EMA200_EMA15_MOINS_1) < 0 and int(VARIATION_EMA200_EMA15) >= 0:

        """
        print("((EMA1L <= VAL_EMA15_COURANT) and  (int(VAL_EMA1H_COURANT) >= int(VAL_EMA15_COURANT))\
        and (FRONT_MONTANT_COURT_EMA1L == 1) and (FRONT_MONTANT_COURT_EMA1H == 0): ",(EMA1L <= VAL_EMA15_COURANT) and (int(VAL_EMA1H_COURANT) >= int(VAL_EMA15_COURANT)) \
        and (FRONT_MONTANT_COURT_EMA1L == 1) and (FRONT_MONTANT_COURT_EMA1H == 0) and  (TYPE_BG == "BG_ROUGE"))
        """    
        # 1er CAS ACHAT  EMA15 < EMA200  .EMA15 DESCENDANTE EMA1H < EMA15 et EMA1L < EMA15 ET DIFF_EMA200_CLOSE >= 50 ET EMA1H ET EMA15 SONT TOUTE MONTANTE and (LAST_ORDER == "SELL")
        #print("LAST_CROISEMENT_EMA200_GOLDEN_CROSS_EMA15: \n",LAST_CROISEMENT_EMA200_GOLDEN_CROSS_EMA15)
        # if  GAIN1 < 0 :
        #     TYPE_BG == "BG_ROUGE"
        print("DATE_COURANT: ",DATE_COURANT)
        # print("DATE et EMA200 ORIGINE DANS TRAITEMENT REELLE=\n",dataframe_date[["date","EMA200"]].loc[val_mask_idxmin_ORG])
        print("DATE DANS TRAITEMENT REELLE=\n",dataframe_date[["date"]].loc[val_mask_idxmin_ORG])
        print("EMA200 ORIGINE DANS TRAITEMENT REELLE=\n",dataframe[["EMA200"]].loc[val_mask_idxmin_ORG])
        print("last_index=",last_index)
        print("val_mask_idxmin:",val_mask_idxmin)
        print("TYPE_BG:",TYPE_BG)
        print("TYPE_BG_N1:",TYPE_BG_N1)
        print("TYPE_BG_N2:",TYPE_BG_N2)
        print("TYPE_BG_N3:",TYPE_BG_N3)
        print("TYPE_BG_BIS:",TYPE_BG_BIS)
        print("TAILLE_BG_BIS=",TAILLE_BG_BIS)
        print("TAILLE_BG=",TAILLE_BG)
        print("TAILLE_BG_N1=",TAILLE_BG_N1)
        print("TAILLE_BG_N2=",TAILLE_BG_N2)
        print("TAILLE_BG_N3=",TAILLE_BG_N3)
        print("CUMUL_TAILLE_BG_VERTE:",CUMUL_TAILLE_BG_VERTE)
        print("CUMUL_TAILLE_BG_ROUGE:",CUMUL_TAILLE_BG_ROUGE)
        print("CUMUL_TAILLE_BG_N1_N2_N3",CUMUL_TAILLE_BG_N1_N2_N3)
        print("TEST_ACHAT_REBOND_EMA1H:",TEST_ACHAT_REBOND_EMA1H)
        print("TEST_VENTE_SOMMET_EMA1H:",TEST_VENTE_SOMMET_EMA1H)
        print("FRONT_NEUTRE_EMA200 :",FRONT_NEUTRE_EMA200 )
        print("FRONT_NEUTRE_COURT_EMA200 :",FRONT_NEUTRE_COURT_EMA200 )
        print("FRONT_MONTANT_EMA200 :",FRONT_MONTANT_EMA200 )
        print("FRONT_MONTANT_COURT_EMA200 :",FRONT_MONTANT_COURT_EMA200 )
        print("FRONT_MONTANT_EMA15 :",FRONT_MONTANT_EMA15 )
        print("FRONT_MONTANT_COURT_EMA15 :",FRONT_MONTANT_COURT_EMA15 )
        print("FRONT_NEUTRE_EMA15 :",FRONT_NEUTRE_EMA15 )
        print("FRONT_MONTANT_EMA1H :",FRONT_MONTANT_EMA1H )
        print("FRONT_MONTANT_COURT_EMA1H :",FRONT_MONTANT_COURT_EMA1H )
        print("FRONT_MONTANT_EMA1L :",FRONT_MONTANT_EMA1L )
        print("FRONT_MONTANT_COURT_EMA1L :",FRONT_MONTANT_COURT_EMA1L )
        print("COULEUR_VOLUME :",COULEUR_VOLUME )
        print(" (int(EMA1L) <= int(VAL_EMA15_COURANT)) :", (int(EMA1L) <= int(VAL_EMA15_COURANT))  )
        print(" (int(EMA1H) >= int(VAL_EMA15_COURANT)) :", (int(EMA1H) >= int(VAL_EMA15_COURANT))  )
        print("(VAL_EMA15_COURANT < VAL_EMA200_COURANT) :",(VAL_EMA15_COURANT < VAL_EMA200_COURANT) )
        print("EMA1H:",VAL_EMA1H_COURANT)
        # print("SPEED_EMA1L:",SPEED_EMA1L)
        # print("SPEED_EMA1H:",SPEED_EMA1H)
        print("OPEN=",OPEN)
        print("open:",open)
        print("CLOSE=",CLOSE)
        print("VAL_CLOSE=",VAL_CLOSE)
        print("DIFF_CLOSE_OPEN=",CLOSE-OPEN)
        print("VAL_OPEN_N1=",VAL_OPEN_N1)
        print("VAL_CLOSE_N1=",VAL_CLOSE_N1)
        print("DIFF_CLOSE_N1_OPEN_N1=",VAL_CLOSE_N1-VAL_OPEN_N1)
        print("VAL_OPEN_N2=",VAL_OPEN_N2)
        print("VAL_CLOSE_N2=",VAL_CLOSE_N2)
        print("DIFF_CLOSE_N2_OPEN_N2=",VAL_CLOSE_N2-VAL_OPEN_N2)
        print("VAL_OPEN_N3=",VAL_OPEN_N3)
        print("VAL_CLOSE_N3=",VAL_CLOSE_N3)
        print("DIFF_CLOSE_N3_OPEN_N3=",VAL_CLOSE_N3-VAL_OPEN_N3)
        # print("OPEN_MOINS_1=",OPEN_MOINS_1)
        # print("CLOSE_MOINS_1=",CLOSE_MOINS_1)
        print("(float(VAL_CLOSE) - float(VAL_CLOSE_N1) < 0) :",(float(VAL_CLOSE) - float(VAL_CLOSE_N1) < 0) ) 
        print("(float(VAL_CLOSE) - float(VAL_CLOSE_N2) < 0) :",(float(VAL_CLOSE) - float(VAL_CLOSE_N2) < 0) ) 
        print("(float(VAL_CLOSE_N1) - float(VAL_CLOSE_N2) < 0) :",(float(VAL_CLOSE_N1) - float(VAL_CLOSE_N2) < 0) )
        global COMPTEUR_GAIN_ZERO


        #VAL_ACHAT=dataframe.close.loc[val_mask_idxmin]
        #VAL_ACHAT=RECUP_LAST_PRICE_IN_FILE()
        """
        #On quitte la fonction car pic de fin de TRAIDE
        if   (COULEUR_VOLUME == "ROUGE") and  (POINT_ENTRE_EMA200 == 0) \
             and ((FRONT_MONTANT_EMA15 == 0)  and int(EMA1H) < int(VAL_EMA15_COURANT)) or  ((FRONT_MONTANT_EMA1H == 0) and (FRONT_MONTANT_EMA1L == 0)) :
             print("PIC  DESCENDANT SOUS EMA15 ON N ACHETE PAS ")
             DERNIER_POINT_VENTE=1
             return
        """
         
        # SOMME_VOLUMES=CALCULE_SOMME_VOLUMES(dataframe)
        # print("TEST_ACHAT_REBOND_EMA1H NEW:",TEST_ACHAT_REBOND_EMA1H)
        # # 3eme CAS REACHAT SUR REBOND PARTOUT
        # print("SOMME_VOLUMES:",SOMME_VOLUMES)
        # if (FRONT_MONTANT_EMA1H == 1) and (FRONT_MONTANT_COURT_EMA1H == 1) \
        # and  (POINT_ENTRE_EMA200 == 0)  and (DERNIER_POINT_VENTE == 0) and ( ORDER != LAST_ORDER) \
        # and  (FRONT_MONTANT_EMA200 >= 0 ) and  (FRONT_MONTANT_EMA15 >= 0 ) \
        # and ((TYPE_BG_N2 == "BG_ROUGE") or (TYPE_BG_N1 == "BG_ROUGE") or (TYPE_BG == "BG_ROUGE") and (COULEUR_VOLUME == "VERTE")) \
        # and SOMME_VOLUMES <= 250 :
        #      print("\n1eme CAS REACHAT SUR REBOND NEW")
        #      ORDER="BUY"
        #      custom_info["SCENARIO"]="3eme CAS REACHAT SUR REBOND RRV"
        #      print(ORDER)
        #      EXEC_ORDER(dataframe)
        #      #VAL_ACHAT=dataframe.close.loc[val_mask_idxmin]
        #      POINT_ENTRE_EMA200 = 1 #VEROUILAGE ACHAT ET VENTE NORMAL
        #      ###exit()
        
        
        seconde=int(CALCULE_SECONDE())
        print("\nSeconde:",seconde)
        # Diff_last_price_OLD_LAST_PRICE=0
        ACTION=""
        #exit() 
        
        DIFF_EMA1L_SAR=dataframe['DIFF_EMA1L_SAR'].iloc[-1].astype(float)
        DIFF_EMA1H_SAR=dataframe['DIFF_EMA1H_SAR'].iloc[-1].astype(float)
        
        
        PRECEDENT_SAR=dataframe['SAR'].iloc[-2].astype(float)
        SAR=dataframe['SAR'].iloc[-1].astype(float)
        PRECEDENT_SAR=(np.round(PRECEDENT_SAR,5))
        SAR=(np.round(SAR,5))
        NEW_PRECEDENT_SAR=str(PRECEDENT_SAR).replace(".","")
        NEW_SAR=str(SAR).replace(".","")
        if len(NEW_PRECEDENT_SAR) == 3 :
            NEW_PRECEDENT_SAR=str(NEW_PRECEDENT_SAR)+"0"
        if len(NEW_SAR) == 3 :
            NEW_SAR=str(NEW_SAR)+"0"
        DIFF_SAR_PRECEDENT_SAR=float(NEW_SAR)-float(NEW_PRECEDENT_SAR)
        
        
        # if DIFF_SAR_PRECEDENT_SAR > -6 :
        #     ACHAT_SUR_SAR=True
        # else:
        #     ACHAT_SUR_SAR=False
            
        # if DIFF_SAR_PRECEDENT_SAR < 0 :
        #     VENTE_SUR_SAR=True
        # else:
        #     VENTE_SUR_SAR=False

        
        # if DIFF_SAR_PRECEDENT_SAR >= -1 :
        #    ACHAT_SUR_SAR=True
           
        ##FONCTION IMPORTANTE DE RECUPERATION DU PRIX
        # RECUP_LAST_PRICE_IN_FILE --> RECUPERATION DU PRIX EN MODE PASSIVE -->NOT LIMIT
        # RECUP_LAST_PRICE_IN_BINANCE  --> RECUPERATION DU PRIX EN MODE ACTIVE --> BANISSEMENT POSSIBLE
        (SOMME_VOLUMES,SOMME_VOLUMES_PRECEDENT)=CALCULE_SOMME_VOLUMES(dataframe)
        # if  GAIN1 < 0 or COMPTEUR_ACHAT_VENTE == 0 or DIFF_EMA1H_SAR == 0 :
        # if  GAIN1 < 0   or DIFF_EMA1H_SAR == 0  or DIFF_EMA1L_SAR == 0 or  DIFF_VAL_CLOSE_INF_VAL_CLOSE_N1 == True:
        # if  GAIN1 < 0 and DIFF_VAL_CLOSE_INF_VAL_CLOSE_N1 == True:
        DIFF_NEW_HIGH_PRICE_SUP_NEW_OPEN_PRICE=float(NEW_HIGH_PRICE) > float(NEW_OPEN_PRICE)
        DIFF_VAL_CLOSE_INF_VAL_CLOSE_N2=abs(float(TAILLE_BG)) - abs(float(TAILLE_BG_N1))
        DIFF_VAL_CLOSE_INF_VAL_CLOSE_N2=DIFF_VAL_CLOSE_INF_VAL_CLOSE_N2 <= 0

        if  DIFF_VAL_CLOSE_INF_VAL_CLOSE_N2 == True or DIFF_NEW_HIGH_PRICE_SUP_NEW_OPEN_PRICE == True : # or VENTE_SUR_SAR == True :
            # time.sleep(1)
            RECUP_LAST_PRICE_IN_BINANCE(dataframe)        
            # dynamic_indicators(dataframe)
            print (f"float(PRIX) != float(last_price) :\n {PRIX} != {last_price}") 
            #if float(PRIX) != float(last_price) :
            print("RECUPERATION DU PRIX SUR BINANCE: ",PRIX)
            last_price=float(PRIX)
            VAL_CLOSE=float(PRIX)
            LAST_CLOSE=PRIX
            GAIN_ABSOLUE_RELATIF=(float(LAST_CLOSE) - float(VAL_ACHAT_INITIALE))
            GAIN_ABSOLUE_RELATIF=np.round(GAIN_ABSOLUE_RELATIF,decimals = 4)
            # custom_info["CLOSE"]=PRIX
            # last_price=PRIX
        # else:
            # RECUP_LAST_PRICE_IN_FILE()
            # LAST_PRICE=last_price_file
            # # LAST_PRICE=int(float(last_price_file)*MULTIP)
            # # last_price=float(last_price_file)
            # # custom_info["CLOSE"]=last_price_file
            # print("RECUPERATION DU PRIX SUR BINANCE SOCKET: ",LAST_PRICE)
            # LAST_PRICE=int(float(last_price_file)*MULTIP)
            # # CHECK_GAIN_SORTIE_POSITIF(last_price)
            # # PRIX=last_price
            
        
        # DIFF_EMA1H_SAR=(VAL_CLOSE - SAR)
        # if NEW_EMA1H != 0 :
        #     DIFF_EMA1H_SAR=(float(NEW_EMA1H) - float(SAR))
        #     DIFF_EMA1H_SAR=int(float(DIFF_EMA1H_SAR)*MULTIP)

        

        #exit()
        if NBR_LAST_PRICE == 0 :
            OLD_LAST_PRICE=last_price
            NBR_LAST_PRICE=1
            #time.sleep(2)
        else:
            
            # if seconde in [00,10,15,20,25,30,35,40,45,50,55] :
            #    RECUP_LAST_PRICE_IN_BINANCE(dataframe)
            #    print (f"float(PRIX) != float(last_price) :\n {PRIX} != {last_price}") 
            #    if float(PRIX) != float(last_price) :
            #       print("RECUPERATION DU PRIX SUR BINANCE: ",PRIX)
            #       last_price=float(PRIX)
            #       #exit()
                
            SEUIL=-2
            Diff_last_price_OLD_LAST_PRICE=(float(last_price)-float(OLD_LAST_PRICE))
            Diff_last_price_OLD_LAST_PRICE=int(Diff_last_price_OLD_LAST_PRICE*MULTIP)

            if last_price != OLD_LAST_PRICE :
                if Diff_last_price_OLD_LAST_PRICE < SEUIL and COULEUR_VOLUME=="VERT" :
                    ACTION="VENTE_CAR_BAISSE_DU_PRIX"
                    NBR_LAST_PRICE=0
                if Diff_last_price_OLD_LAST_PRICE > SEUIL and COULEUR_VOLUME=="ROUGE" :
                    ACTION="ACHAT_CAR_HAUSSE_DU_PRIX"
                    NBR_LAST_PRICE=0
                #OLD_LAST_PRICE=last_price
                #NBR_LAST_PRICE=0
                #OLD_LAST_PRICE=last_price
                #time.sleep(1)
            else:
                print(f"PRIX IDENTIQUE float(PRIX) == float(last_price) :\n {PRIX} = {last_price}") 
             
        TRAME_COURANTE=dataframe.iloc[last_index]
        # DIFF_NEW_HIGH_PRICE_SUP_NEW_OPEN_PRICE=float(NEW_HIGH_PRICE) > float(NEW_OPEN_PRICE)
        # if TAILLE_BG_BIS != 0 and ( FRONT_MONTANT_EMA1H == 0) :
        #     TAILLE_BG=TAILLE_BG_BIS
        #     TYPE_BG=TYPE_BG_BIS
        # if (float(TAILLE_BG) > 0 and float(TAILLE_BG_N1) >0) or ( float(TAILLE_BG) < 0 and float(TAILLE_BG_N1) < 0) :
        # DIFF_VAL_CLOSE_INF_VAL_CLOSE_N2=abs(float(TAILLE_BG)) - abs(float(TAILLE_BG_N1))
        # DIFF_VAL_CLOSE_INF_VAL_CLOSE_N2=DIFF_VAL_CLOSE_INF_VAL_CLOSE_N2 <= 0

        if float(TAILLE_BG) > 0 and float(TAILLE_BG_N1) <0 :
             DIFF_VAL_CLOSE_INF_VAL_CLOSE_N2=False
        if float(TAILLE_BG)  <0 :
             DIFF_VAL_CLOSE_INF_VAL_CLOSE_N2=True
             
             # if GAIN1 < 0 :
        # if ( DIFF_VAL_CLOSE_INF_VAL_CLOSE_N2 == True) :
        #     TAILLE_BG=float(VAL_CLOSE) - float(VAL_CLOSE_N2)
        #     TYPE_BG="BG_ROUGE"
        # else:
        #     TYPE_BG="BG_VERTE"
                
        global QUANTITE_ACHAT
        global QUANTITE_VENTE
        QUANTITE_ACHAT=last_price-PRICE_VOLUME_ASK
        QUANTITE_VENTE=PRICE_VOLUME_BID-last_price
        # Prev_index_CINQ=dataframe['SAR'].iloc[-5].astype(float)
        Prev_index_CINQ=dataframe['SAR'].iloc[-1].astype(float)
        DIFF_SAR_SUP_PRIX= Prev_index_CINQ > last_price
        # DIFF_SAR_SUP_PRIX= SAR > last_price
        DIFF_SAR_SUP_OPEN=Prev_index_CINQ >= VAL_OPEN
        DIFF_SAR_SUP_EMA15=(Prev_index_CINQ > VAL_EMA15_COURANT) and (DIFF_SAR_SUP_OPEN == True)
        
        if DIFF_SAR_SUP_PRIX == True :
            ACHAT_SUR_SAR=True
            VENTE_SUR_SAR=False
        else:
            ACHAT_SUR_SAR=False
            VENTE_SUR_SAR=True

            
        print(DATE_HEURE)
        print("\nPOINT_ENTRE_EMA200 : ",POINT_ENTRE_EMA200)
        print("\nDERNIER_POINT_VENTE: ",DERNIER_POINT_VENTE)
        print("TEST_ACHAT_REBOND_EMA1H NEW:",TEST_ACHAT_REBOND_EMA1H)
        if (POINT_ENTRE_EMA200 == 0) :
            print("!!!!! PAIR : {} EN MODE ACHAT ".format(symbol))    
        else:
            print("!!!!! PAIR : {} EN MODE VENTE ".format(symbol)) 
        print("!!!!! TYPE_BG=",TYPE_BG)
        print("!!!!!! TAILLE_BG:",TAILLE_BG)
        print("!!!!! TAILLE_BG_BIS=",TAILLE_BG_BIS)
        print("!!!!! TYPE_BG_BIS=",TYPE_BG_BIS)
        # print("!!!!!! COULEUR_VOLUME :",COULEUR_VOLUME )
        print("!!!!!! open:",(format(open,'.8f')))
        print("!!!!!! HIGH :",int(HIGH) )
        print("!!!!!! VAL_OPEN_N1 :",float(VAL_OPEN_N1))
        print("!!!!!! VAL_CLOSE_N1 :",float(VAL_CLOSE_N1))
        print("!!!!!! HIGH > VAL_CLOSE_N1 :",(float(HIGH) >= float(VAL_CLOSE_N1)))
        print("!!!!!! VAL_CLOSE :",float(VAL_CLOSE_N1))
        print("!!!!!! VAL_CLOSE_N1 :",float(VAL_CLOSE_N1))
        # print("!!!!!! DIFF_VAL_CLOSE_INF_VAL_CLOSE_N1 :",(DIFF_VAL_CLOSE_INF_VAL_CLOSE_N1))
        print("!!!!!! DIFF_VAL_CLOSE_INF_VAL_CLOSE_N2 :",(DIFF_VAL_CLOSE_INF_VAL_CLOSE_N2))
        NEW_OPEN_PRICE=open
        print("!!!!!! NEW_OPEN_PRICE :",(NEW_OPEN_PRICE))
        print("!!!!!! NEW_HIGH_PRICE :",(NEW_HIGH_PRICE))
        print("!!!!!! DIFF_NEW_HIGH_PRICE_SUP_NEW_OPEN_PRICE :",(DIFF_NEW_HIGH_PRICE_SUP_NEW_OPEN_PRICE))
        print("!!!!!! last_price_file :",(last_price_file))
        print("!!!!!! last_price :",(last_price))
        print("!!!!!! Diff_VOLUME_COURANT_VOLUME_PRECEDENT:",Diff_VOLUME_COURANT_VOLUME_PRECEDENT)
        print("SOMME_VOLUME_ASK:",VOLUME_ASK)
        print("SOMME_VOLUME_BID:",VOLUME_BID)
        print("PRICE_VOLUME_ASK:",PRICE_ASK)
        print("PRICE_VOLUME_BID:",PRICE_BID)
        print(DATE_HEURE)
        print("!!!!!! PRICE EMA200:",EMA200)
        print("!!!!!! EMA1L:",EMA1L)
        print("!!!!!! EMA1H:",EMA1H)
        print("!!!!!! NEW_EMA1H:",NEW_EMA1H)
        print("!!!!!! PRICE_VOLUME_ASK:",PRICE_VOLUME_ASK)
        print("!!!!!! PRICE_VOLUME_BID:",PRICE_VOLUME_BID)
        print("!!!!!! SPREAD:",SPREAD)
        print("!!!!!! QUANTITE_ACHAT:",QUANTITE_ACHAT)
        print("!!!!!! QUANTITE_VENTE:",QUANTITE_VENTE)
        print("!!!!!! VAL_EMA15_COURANT:",VAL_EMA15_COURANT)
        print("!!!!!! (int(EMA1L) >= int(VAL_EMA15_COURANT)) :", (int(EMA1L) >= int(VAL_EMA15_COURANT))  )
        print("!!!!!! (int(EMA1H) >= int(VAL_EMA15_COURANT)) :", (int(EMA1H) >= int(VAL_EMA15_COURANT))  )
        print("!!!!!! (VAL_EMA15_COURANT < VAL_EMA200_COURANT) :",(VAL_EMA15_COURANT < VAL_EMA200_COURANT) )
        # exit()
        # print("!!!!!! PRICE LAST_VOLUME_VWAP_Price:",LAST_VOLUME_VWAP_Price)
        # time.sleep(1)
        # if "VAL_ACHAT" in custom_info :
        #     VAL_ACHAT=int(float(custom_info["VAL_ACHAT"])*MULTIP)
        # print("!!!!!! VAL_ACHAT:",int(VAL_ACHAT))
        # if OLD_LAST_PRICE != "" :
        #     print("!!!!!! OLD_LAST_PRICE:",OLD_LAST_PRICE+"!!!!!!!!")
        # print("!!!!!! last_price:",last_price)
        # LAST_PRICE=int(float(last_price)*MULTIP)
        # EMA1L=dataframe['EMA1L'].iloc[-1].astype(int)
        # EMA1L=int(EMA1L)
        # #NEW_EMA1L=int(float(NEW_EMA1L)*MULTIP)
        # Diff_LAST_PRICE_EMA1L=LAST_PRICE - EMA1L
        # #Diff_LAST_PRICE_EMA1L=LAST_PRICE - NEW_EMA1L
        # print("!!!!!! LAST_PRICE:",LAST_PRICE)
        # #%and (COULEUR_VOLUME=="ROUGE")
        # if ( (DIFF_EMA1H_EMA15 <= 0 ) or (DIFF_EMA1H_EMA15 > 50 )   and (TYPE_BG == "BG_VERTE")   ) \
        # and (COMPTEUR_ACHAT_VENTE == 0) and (int(FRONT_MONTANT_EMA15) == 1):
        #     print("!!!!!SIGNAL ENTRE INITIALE !!!!!!!")
        #     COMPTEUR_ACHAT_VENTE=1  
            
        # COMPTEUR_ACHAT_VENTE=1       
        # if Diff_last_price_OLD_LAST_PRICE != "" and (COMPTEUR_ACHAT_VENTE == 1):
        if (COMPTEUR_ACHAT_VENTE >= 0):
            #Diff_last_price_OLD_LAST_PRICE=int(Diff_last_price_OLD_LAST_PRICE*MULTIP)
            print("!!!!!! Diff_last_price_OLD_LAST_PRICE:",Diff_last_price_OLD_LAST_PRICE)
            #print("!!!!!! Diff_LAST_PRICE_OPEN_PRICE:",Diff_LAST_PRICE_OPEN_PRICE)
            # print("!!!!!! Diff_LAST_PRICE_EMA1L:",Diff_LAST_PRICE_EMA1L)
            # print("!!!!!! Diff_LAST_PRICE_OLD_File_price:",Diff_LAST_PRICE_OLD_File_price)
            # print("!!!!!! DIFF_EMA1H_EMA15:",DIFF_EMA1H_EMA15)
            print("!!!!!! FRONT_MONTANT_COURT_EMA1H:",FRONT_MONTANT_COURT_EMA1H)
            print("!!!!!! FRONT_MONTANT_COURT_EMA1L:",FRONT_MONTANT_COURT_EMA1L)
            print("!!!!!! FRONT_MONTANT_EMA1H:",FRONT_MONTANT_EMA1H)
            print("!!!!!! FRONT_MONTANT_EMA1L:",FRONT_MONTANT_EMA1L)
            print("!!!!!! FRONT_MONTANT_COURT_EMA200:",FRONT_MONTANT_COURT_EMA200)
            print("!!!!!! FRONT_MONTANT_EMA200:",FRONT_MONTANT_EMA200)
            print("!!!!!! LAST_PRICE: ",LAST_PRICE)
            print("!!!!!! LAST_PRICE >= VAL_EMA15_COURANT:",(int(LAST_PRICE) >= int(VAL_EMA15_COURANT)))
            print("!!!!!! FRONT_MONTANT_EMA15:",FRONT_MONTANT_EMA15)
            print("!!!!!! FRONT_NEUTRE_EMA15:",FRONT_NEUTRE_EMA15)
            print("!!!!!! FRONT_MONTANT_COURT_EMA15 :",FRONT_MONTANT_COURT_EMA15 )
            print("!!!!!! DIFF_EMA1L_SAR :",DIFF_EMA1L_SAR)
            print("!!!!!! DIFF_EMA1H_SAR :",DIFF_EMA1H_SAR)
            print("!!!!!! PRECEDENT_SAR :",PRECEDENT_SAR)
            print("!!!!!! SAR :",SAR)
            print("!!!!!! PSAR :",PSAR)
            print("!!!!!! TAIL PSAR :\n",dataframe['SAR'].tail())
            print("!!!!!! DIFF_SAR_SUP_PRIX :",DIFF_SAR_SUP_PRIX)
            print("!!!!!! DIFF_SAR_SUP_OPEN :",DIFF_SAR_SUP_OPEN)
            print("!!!!!! DIFF_SAR_SUP_EMA15 :",DIFF_SAR_SUP_EMA15 )


            # mask = (dataframe.iloc[-1].SAR >= dataframe.iloc[-5].SAR )
            mask = (dataframe['SAR'].tail(2).index)
            mask_min = (dataframe['SAR'].tail(10).index)
            # Len_Prev_index=len(dataframe)-3
            # Len_last_index=len(dataframe)-1
            Prev_index=dataframe['SAR'].iloc[-2].astype(float)
            VAR_last_index=dataframe['SAR'].iloc[-1].astype(float)
            # print("!!!!!! Len_Prev_index :",Len_Prev_index)
            # print("!!!!!! Len_last_index :",Len_last_index)
            print("!!!!!! Prev_index :",Prev_index)
            print("!!!!!! VAR_last_index :",VAR_last_index)
            VARIATION=VAR_last_index > Prev_index
            TEST_VARIATION_POSITIVE=VARIATION 
            last_index=len(dataframe)-1
            print("!!!!!! VARIATION :",VARIATION)
            print("!!!!!! TEST_VARIATION_POSITIVE :",TEST_VARIATION_POSITIVE)
            print("!!!!!! MASK :",mask)
            print("!!!!!! last_index :",last_index)
            INDEXMAX=dataframe['SAR'].loc[mask].idxmax().astype(int)
            VAL_MAX_PSAR=dataframe['SAR'].iloc[INDEXMAX].astype(float)
            # print("!!!!!! INDEXMAX : {} MAX PSAR : ",format(INDEXMAX))
            print("!!!!!! last_index - INDEXMAX  :",last_index - INDEXMAX )
            print(f"!!!!!! INDEXMAX : {INDEXMAX} MAX PSAR : {VAL_MAX_PSAR}")
            INDEXMIN=dataframe['SAR'].loc[mask_min].idxmin().astype(int)
            VAL_MIN_PSAR=dataframe['SAR'].iloc[INDEXMIN].astype(float)
            print(f"!!!!!! INDEXMIN : {INDEXMIN} MIN PSAR : {VAL_MIN_PSAR}")
            DIFF_last_index_MOINS_INDEXMIN=last_index - INDEXMIN
            print("!!!!!! DIFF_last_index_MOINS_INDEXMIN :",DIFF_last_index_MOINS_INDEXMIN)
            print("!!!!!! NEW_PRECEDENT_SAR :",NEW_PRECEDENT_SAR)
            print("!!!!!! NEW_SAR :",NEW_SAR)
            print("!!!!!! DIFF_SAR_PRECEDENT_SAR :",DIFF_SAR_PRECEDENT_SAR)
            print("!!!!!! ACHAT_SUR_SAR :",ACHAT_SUR_SAR)
            print("!!!!!! VENTE_SUR_SAR :",VENTE_SUR_SAR)

            if POINT_ENTRE_EMA200 == 1 :
                CALCULE_DIFF_TIME()
            if (POINT_ENTRE_EMA200 == 0) :
                print("!!!!!!!!!!!!  MODE ACHAT SHORT !!!!!!!!!!!!")
            else:
                print("!!!!!!!!!!!!  MODE ACHAT LONGUE !!!!!!!!!!!!")
            print("!!!!!! COMPTEUR_VENTE_RELATIVE:",COMPTEUR_VENTE_RELATIVE)
            print("!!!!!! COMPTEUR_ACHAT_VENTE:",COMPTEUR_ACHAT_VENTE)
            print("!!!!!! DATE_VENTE_FUTUR :",DATE_VENTE_FUTUR)
            print("!!!!!! VARIATION :",VARIATION)
            print("!!!!!! TEST_VARIATION_POSITIVE :",TEST_VARIATION_POSITIVE)
            print("!!!!!! LAST_ORDER :",LAST_ORDER)
            print("!!!!!! POINT_ENTRE_EMA200 :",POINT_ENTRE_EMA200)
            print("!!!!!! CYCLE_COURT :",CYCLE_COURT)
            print("!!!!!! VAL_ACHAT_INITIALE :",VAL_ACHAT_INITIALE)
            DIFF_GAIN_ABSOLUE_RELATIF_SUP_GAIN_ABSOLUE=float(GAIN_ABSOLUE_RELATIF) > float(GAIN_ABSOLUE)
            print("!!!!!! GAIN_ABSOLUE_RELATIF :",GAIN_ABSOLUE_RELATIF)
            print("!!!!!! GAIN_ABSOLUE :",GAIN_ABSOLUE)
            print("!!!!!! DIFF_GAIN_ABSOLUE_RELATIF_SUP_GAIN_ABSOLUE :",DIFF_GAIN_ABSOLUE_RELATIF_SUP_GAIN_ABSOLUE)
            print("!!!!!! VAL_EMA15_COURANT < VAL_OPEN :",VAL_EMA15_COURANT < VAL_OPEN) 
            print("!!!!!! VOLUME PRECEDENT:",(VOLUME_PRECEDENT))
            print("!!!!!! VOLUME COURANT:",(VOLUME_COURANT))
            print("!!!!!! Diff_VOLUME_COURANT_VOLUME_PRECEDENT:",Diff_VOLUME_COURANT_VOLUME_PRECEDENT)

            
            
            # print("!!!!!! FRONT_MONTANT_COURT_VOLUME:",FRONT_MONTANT_COURT_VOLUME)
            # print("!!!!!! Diff_VOLUME_VWAP_LAST_PRICE_OLD_LAST_PRICE:",Diff_VOLUME_VWAP_LAST_PRICE_OLD_LAST_PRICE)
            global OLD_DATE_HEURE
            global OLD_Diff_VOLUME_VWAP_LAST_PRICE_OLD_LAST_PRICE
            if OLD_DATE_HEURE != DATE_HEURE :
               OLD_DATE_HEURE=DATE_HEURE
           

            # OLD_LAST_PRICE=PRIX
            OLD_LAST_PRICE=VAL_CLOSE_N1
            print("!!!!!! OLD_LAST_PRICE:",OLD_LAST_PRICE)
            # if (POINT_ENTRE_EMA200 == 1)  :   
            #     while True :  
            #         #Delay_new_frame(3)
            #         RECUP_LAST_PRICE_IN_BINANCE(dataframe)
            #         last_price=PRIX
            #         print("!!!!!! last_price:",last_price)
            #         NEW_Diff_VOLUME_VWAP_LAST_PRICE_OLD_LAST_PRICE=(float(last_price)-float(OLD_LAST_PRICE))
            #         NEW_Diff_VOLUME_VWAP_LAST_PRICE_OLD_LAST_PRICE=int(NEW_Diff_VOLUME_VWAP_LAST_PRICE_OLD_LAST_PRICE*MULTIP)
                    
            #         #if OLD_Diff_VOLUME_VWAP_LAST_PRICE_OLD_LAST_PRICE != Diff_VOLUME_VWAP_LAST_PRICE_OLD_LAST_PRICE :
            #         Diff_VOLUME_VWAP_Diff_VOLUME_VWAP_OLD=int(NEW_Diff_VOLUME_VWAP_LAST_PRICE_OLD_LAST_PRICE) - int(Diff_VOLUME_VWAP_LAST_PRICE_OLD_LAST_PRICE)
            #         print("!!!!!! OLD_LAST_PRICE:",OLD_LAST_PRICE)
            #         print("!!!!!! Diff_VOLUME_VWAP_LAST_PRICE_OLD_LAST_PRICE:",Diff_VOLUME_VWAP_LAST_PRICE_OLD_LAST_PRICE)
            #         # print("!!!!!! NEW_Diff_VOLUME_VWAP_LAST_PRICE_OLD_LAST_PRICE:",NEW_Diff_VOLUME_VWAP_LAST_PRICE_OLD_LAST_PRICE)
            #         # print("!!!!!! Diff_VOLUME_VWAP_Diff_VOLUME_VWAP_OLD:",Diff_VOLUME_VWAP_Diff_VOLUME_VWAP_OLD)
            #         OLD_LAST_PRICE=PRIX
            #         # if Diff_VOLUME_VWAP_Diff_VOLUME_VWAP_OLD <= 0  or (int(Diff_VOLUME_VWAP_LAST_PRICE_OLD_LAST_PRICE) < 0): #and int(Diff_VOLUME_VWAP_LAST_PRICE_OLD_LAST_PRICE) >= 0 :
            #         if (int(Diff_VOLUME_VWAP_LAST_PRICE_OLD_LAST_PRICE) >= 0):
            #             break
            #         # else :
            #         #     Delay_new_frame(3)
            # time.sleep(0.1)
            global SEUIL_SORTIE
            SEUIL_SORTIE=0
            #if (Diff_last_price_OLD_LAST_PRICE < SEUIL_SORTIE)  and (POINT_ENTRE_EMA200 == 0) :
                
                # A DECOMMENTER
            # if (int(FRONT_MONTANT_COURT_EMA1H) == 0)  and (POINT_ENTRE_EMA200 == 0) \
            #     and (int(FRONT_MONTANT_EMA15) != 1) : # and (int(FRONT_MONTANT_COURT_VOLUME) != 1): # and (int(FRONT_MONTANT_COURT_EMA15) != 1) :
                # #Delay_new_frame()
                # if (int(FRONT_MONTANT_EMA15) == 0) and (DIFF_EMA1H_EMA15 < 0 ):
                #     print("!!!!!VALEUR EMA15 NEGATIVE!!!!!!!")
                #     #Delay_new_frame(60*10)
                #     #Delay_new_frame("")
                #     COMPTEUR_ACHAT_VENTE=0
                # else:
                #     GAIN_RELATIF=0
                #     Delay_new_frame("")
                    

          
                                        
                    
                #return
                
            # if (int(COMPTEUR_ACHAT_VENTE) >= 1) and GAIN_RELATIF >= 30  :  # PRIX
            #      print("!!!!!BOUGIE ROUGE  NEGATIVE!!!!!!!")
            #      # print("DERNIERE_VENTE_POSITIVE > LAST_PRICE")
            #      # print(f"{DERNIERE_VENTE_POSITIVE} > {LAST_PRICE}")
            #      time.sleep(0.1)
            #      Delay_new_frame(110)
            #      COMPTEUR_ACHAT_VENTE=0
            #      GAIN_RELATIF=0
            #      return

            
            # if GAIN_RELATIF == 0 :
            #   print("GAIN_RELATIF NEGATIF:",GAIN_RELATIF)
            #   DERNIER_POINT_VENTE = 1
            #   Delay_new_frame() 

            # if  (TYPE_BG == "BG_ROUGE") and (POINT_ENTRE_EMA200 == 0) :
            #   print("BG_ROUGE PAUSE:")
            #   Delay_new_frame("") 
            
            Diff_GAIN2_GAIN1_LAST_PRICE=0
            # and (COMPTEUR_ACHAT_VENTE == 1)
            
            
            if (POINT_ENTRE_EMA200 == 1) and last_price != "" :
                VAL_ACHAT=float(custom_info["VAL_ACHAT"]) 
                # VAL_ACHAT=(float(VAL_ACHAT)*MULTIP)
                # VAL_ACHAT=int(VAL_ACHAT)     
                RECUP_LAST_PRICE_IN_BINANCE(dataframe)
                print("VAL_ACHAT: ",VAL_ACHAT)
                print("last_price: ",last_price)
                last_price=(float(last_price))
                LAST_PRICE_OLD=(float(last_price))
                print("LAST_PRICE_OLD: ",LAST_PRICE_OLD)
                # GAIN_MOINS_UN_POURCENT=(VAL_ACHAT) * 0.85
                GAIN_MOINS_UN_POURCENT=(VAL_ACHAT) * 0.9999
                print("!!!!! GAIN_MOINS_UN_POURCENT: ",GAIN_MOINS_UN_POURCENT)
                print("!!!!! MULTIP: ",MULTIP)
                LEN_VAL_ACHAT=len(str(VAL_ACHAT))
                LEN_LAST_PRICE=len(str(last_price))
                P=LEN_LAST_PRICE-LEN_VAL_ACHAT
                if P > 0 :
                   VAL_ACHAT=str(VAL_ACHAT).replace(".","")
                   VAL_ACHAT =int(VAL_ACHAT) * (10 ** P)
                   print("P: ",P)
                   print("VAL_ACHAT: ",VAL_ACHAT)
                   last_price=str(last_price).replace(".","")
                   last_price=int(last_price)
                GAIN1=((last_price) - (VAL_ACHAT))
                GAIN1=round(GAIN1,8)
                print("!!!!! FIRST  GAIN1: ",GAIN1)
                # GAIN1=(float(GAIN1)*MULTIP)
                if "." in str(GAIN1) :
                   GAIN1=str(GAIN1).replace(".","")
                   GAIN1=float(GAIN1)
                    # b=GAIN1*100
                    # # print(b)
                    # GAIN1=round(GAIN1)
                    # print(c)
                # GAIN1=(float(GAIN1)*MULTIP)
                # GAIN1=check_gain(GAIN1)
                if "None" in str(GAIN1) :
                    GAIN1 = 0
                # GAIN1=float(GAIN1)   
                # GAIN1=check_gain(GAIN1)
                print("!!!!! GAIN_OLD: ",GAIN_OLD)
                print("!!!!! GAIN1: ",GAIN1)
                DIFF_GAIN1_INF_GAIN_OLD=int(GAIN1) < int(GAIN_OLD)
                print("!!!!! DIFF_GAIN1_INF_GAIN_OLD : ",DIFF_GAIN1_INF_GAIN_OLD)
                DIFF_GAIN1_EGAL_GAIN_OLD= int(GAIN1) == int(GAIN_OLD)
                print("!!!!! DIFF_GAIN1_EGAL_GAIN_OLD : ",DIFF_GAIN1_EGAL_GAIN_OLD)
                GAIN_OLD=int(GAIN1)     
                if (DIFF_GAIN1_EGAL_GAIN_OLD == True)  :
                   NBR_COMPTEUR_DIFF_GAIN1=1
                   COMPTEUR_DIFF_GAIN1_EGAL+=1        
                   print("!!!!! NBR_COMPTEUR_DIFF_GAIN1 : ",NBR_COMPTEUR_DIFF_GAIN1)
                   print("!!!!! COMPTEUR_DIFF_GAIN1_EGAL : ",COMPTEUR_DIFF_GAIN1_EGAL)
                # global VAL_ACHAT_INITIALE   
                if GAIN1 > 0 :
                    custom_info["VAL_ACHAT_INITIALE"]=(last_price)
                    VAL_ACHAT_INITIALE=(last_price)
                 # if custom_info["VAL_ACHAT_INITIALE"] == "" :
                 #     custom_info["VAL_ACHAT_INITIALE"]=0
                 # # VAL_ACHAT_INITIALE=(custom_info["VAL_ACHAT_INITIALE"]


            if (int(EMA1L) < int(VAL_EMA15_COURANT)) and  (int(EMA1H) < int(VAL_EMA15_COURANT)) :
                COMPTEUR_GAIN_ZERO=0
                print("!!!!!! REINITIALISATION DU COMPTEUR_GAIN_ZERO :",COMPTEUR_GAIN_ZERO)


            print("Diff_VOLUME_COURANT_VOLUME_PRECEDENT:",Diff_VOLUME_COURANT_VOLUME_PRECEDENT)

            # if  (TYPE_BG == "BG_VERTE")  and  (int(Diff_VOLUME_COURANT_VOLUME_PRECEDENT) > 0):
            # if (TYPE_BG == "BG_VERTE")  and  int(TAILLE_BG) > 0 \
            # or ( (TYPE_BG == "BG_VERTE")  and ( int(TAILLE_BG) > int(TAILLE_BG_N1) )) \
            # if  ( FRONT_MONTANT_EMA15 == 1) and ( FRONT_MONTANT_COURT_EMA1H == 1)   :
            # if (int(EMA1L) >= int(VAL_EMA15_COURANT)) and  (int(EMA1H) >= int(VAL_EMA15_COURANT)) \
           # if (TYPE_BG == "BG_VERTE")  or  int(TAILLE_BG) > 0 :
               #(TYPE_BG == "BG_VERTE") and
               # and ((TYPE_BG == "BG_VERTE") or (TYPE_BG_N1 == "BG_VERTE") or (TYPE_BG_BIS == "BG_VERTE"))\

           # !!!!!!!!!!!!!! DEB ACHAT 
            print("!!!!!TEST_K_AND_M_IN_VOLUME !!!",TEST_K_AND_M_IN_VOLUME)
            print("!!!!!DEB ACHAT SAR !!!")
            print("!!!!!LAST_ORDER !!!",LAST_ORDER)
            # if DIFF_EMA1H_SAR  > 0 and DIFF_VAL_CLOSE_INF_VAL_CLOSE_N1 == False :
                # and (( FRONT_MONTANT_EMA15 == 1) or ( FRONT_MONTANT_COURT_EMA15 == 1)) \ and (int(TAILLE_BG) > 0) and ( FRONT_MONTANT_EMA1H == 1)
            # if (LAST_ORDER != "BUY")  and (DIFF_NEW_HIGH_PRICE_SUP_NEW_OPEN_PRICE == True and (int(TAILLE_BG) > 0) \
            #     and (float(PRIX) >=  float(VAL_MAX_PSAR))) and (last_index - INDEXMAX != 0) \            
            # if (LAST_ORDER != "BUY") or (DIFF_VAL_CLOSE_INF_VAL_CLOSE_N2 == False)  and (float(TAILLE_BG) > 0) : #or (TYPE_BG_BIS == "BG_VERTE") :
            #  if   (int(TAILLE_BG) > 0) and (DIFF_NEW_HIGH_PRICE_SUP_NEW_OPEN_PRICE == True ) \
            #  and ((ACHAT_SUR_SAR == True)) :
             # and (( FRONT_MONTANT_EMA1L == 1) and ( FRONT_MONTANT_EMA1H == 1)) or (FRONT_MONTANT_COURT_EMA15 == 1)\
             # or  (float(TAILLE_BG) > 0) and (DIFF_NEW_HIGH_PRICE_SUP_NEW_OPEN_PRICE == True ) and (DIFF_VAL_CLOSE_INF_VAL_CLOSE_N2 == False)  \
             # or ((TEST_VARIATION_POSITIVE == True)   ) :
            # if (LAST_ORDER != "BUY") and  (POINT_ENTRE_EMA200 == 0) and (FRONT_MONTANT_COURT_EMA200 == 1)  and (FRONT_MONTANT_COURT_EMA15 == 1) \
            # if (LAST_ORDER != "BUY") and  (POINT_ENTRE_EMA200 == 0) and (TYPE_BG == "BG_VERTE") and (DIFF_SAR_SUP_PRIX == False) and (TAILLE_BG_BIS >0): 
             #and  (DIFF_VAL_CLOSE_INF_VAL_CLOSE_N2 == False) : #and ((TYPE_BG_N1 == "BG_ROUGE") or (TYPE_BG_N2 == "BG_ROUGE"))  : 
            # if (LAST_ORDER != "BUY") and  (POINT_ENTRE_EMA200 == 0) and (( FRONT_MONTANT_EMA1L == 1) or ( FRONT_MONTANT_EMA1H == 1)) and (FRONT_MONTANT_COURT_EMA15 == 1) \
            # if (LAST_ORDER != "BUY") and  (POINT_ENTRE_EMA200 == 0) and (FRONT_MONTANT_EMA15 == 1) and (FRONT_MONTANT_COURT_EMA15 == 1) and (FRONT_MONTANT_EMA1H == 1) :
            # if (LAST_ORDER != "BUY") and  (POINT_ENTRE_EMA200 == 0)  and (FRONT_MONTANT_EMA1H == 1) :
            # if (LAST_ORDER != "BUY") and  (POINT_ENTRE_EMA200 == 0) and TEST_K_AND_M_IN_VOLUME == True :
            if ((LAST_ORDER != "BUY") and  (POINT_ENTRE_EMA200 == 0) and (TYPE_BG_BIS == "BG_VERTE")  and (TYPE_BG == "BG_VERTE") and (DIFF_SAR_SUP_PRIX == False)) \
                or ((LAST_ORDER != "BUY") and  (POINT_ENTRE_EMA200 == 0) and (TYPE_BG_BIS == "BG_VERTE")  and (TYPE_BG == "BG_ROUGE") and (DIFF_SAR_SUP_PRIX == True) and (FRONT_MONTANT_EMA1H == 1)) : 
             # if (VAL_EMA15_COURANT <= VAL_OPEN) and float(VOLUME_COURANT) > 0 and (DIFF_VAL_CLOSE_INF_VAL_CLOSE_N2 == False) \
             #        and (FRONT_MONTANT_EMA200 == 1) and (FRONT_MONTANT_COURT_EMA200 == 1) \
             #            or ((TYPE_BG_BIS == "BG_VERTE") and (int(TAILLE_BG_BIS) > 0)) :
                        # or ((TYPE_BG == "BG_VERTE") and (int(TAILLE_BG) > 0)) :
             # if (DIFF_VAL_CLOSE_INF_VAL_CLOSE_N2 == False) and (FRONT_MONTANT_EMA200 == 1) and (FRONT_MONTANT_COURT_EMA200 == 1) and (FRONT_MONTANT_COURT_EMA15 == 1) \
             # if  ((TYPE_BG_BIS == "BG_VERTE") and (float(TAILLE_BG_BIS) > 0) and (FRONT_MONTANT_COURT_EMA15 == 1) ) :
                        # or ((TYPE_BG_BIS == "BG_VERTE") and (int(TAILLE_BG_BIS) > 0) and (FRONT_MONTANT_COURT_EMA15 == 1) ) \
              # if (DIFF_VAL_CLOSE_INF_VAL_CLOSE_N2 == False)  and (FRONT_MONTANT_COURT_EMA15 == 1) \
               if (FRONT_MONTANT_EMA15 == 1 or FRONT_MONTANT_COURT_EMA15 == 1) and ((TYPE_BG_BIS == "BG_VERTE") and (float(TAILLE_BG_BIS) > 0) ) :
                        # or ((TYPE_BG_BIS == "BG_VERTE") and (int(TAILLE_BG_BIS) > 0) and ((TYPE_BG == "BG_VERTE") and (int(TAILLE_BG) > 0)) ) :
                # and float(GAIN_ABSOLUE) >= 0 :
            # if (LAST_ORDER != "BUY") and  (POINT_ENTRE_EMA200 == 0) and (( FRONT_MONTANT_EMA1L == 1)) and (FRONT_MONTANT_COURT_EMA15 == 1) and float(GAIN_ABSOLUE) >= 0 :
             # if  (DIFF_SAR_SUP_PRIX == False) and (TYPE_BG == "BG_VERTE" or float(TAILLE_BG_BIS) >= 0)  :
              # if  (TYPE_BG == "BG_VERTE")  :
              # if  (TYPE_BG_BIS == "BG_VERTE")  :
             # if  (DIFF_SAR_SUP_PRIX == False) and (TYPE_BG == "BG_VERTE")  :
                 # or (TYPE_BG == "BG_VERTE" and TAILLE_BG_BIS > 0  ):
              # if  ( (float(TAILLE_BG) > 0 ) )  or (( FRONT_MONTANT_EMA15 == 1) and ( FRONT_MONTANT_COURT_EMA15 == 1)) :
              #  if ((DIFF_NEW_HIGH_PRICE_SUP_NEW_OPEN_PRICE == True ) and (DIFF_VAL_CLOSE_INF_VAL_CLOSE_N2 == False) and (float(TAILLE_BG) > 0)) \
              #  or ((ACHAT_SUR_SAR == True) and (float(TAILLE_BG) > 0) ) \
              #  or (TYPE_BG_BIS == "BG_VERTE" and TAILLE_BG_BIS > 0) :
                # or ( and  (LAST_ORDER != "BUY")  and  (int(TAILLE_BG) > 0)) :
                # or  ((DIFF_VAL_CLOSE_INF_VAL_CLOSE_N2 == True) and (ACHAT_SUR_SAR==True)) \
                # or ((DIFF_NEW_HIGH_PRICE_SUP_NEW_OPEN_PRICE == True) and (int(TAILLE_BG) > 0) ) :
               # or ( ACHAT_SUR_SAR==True and DIFF_VAL_CLOSE_INF_VAL_CLOSE_N2 == True and (int(TAILLE_BG) > 0) and ( FRONT_MONTANT_COURT_EMA1L == 1) )  :
               # or ((TYPE_BG_N1 == "BG_VERTE") and   (TYPE_BG_N2 == "BG_VERTE") and  ACHAT_SUR_SAR==True):

               # if ( DIFF_NEW_HIGH_PRICE_SUP_NEW_OPEN_PRICE == True)\
               # or  ((DIFF_VAL_CLOSE_INF_VAL_CLOSE_N2 == True) and (ACHAT_SUR_SAR==True)) \
               # or (ACHAT_SUR_SAR==True) \
               # or   float(DIFF_EMA1L_SAR) > 0 and ( DIFF_NEW_HIGH_PRICE_SUP_NEW_OPEN_PRICE == True) \
               # or ((DIFF_VAL_CLOSE_INF_VAL_CLOSE_N2 == True) and (DIFF_NEW_HIGH_PRICE_SUP_NEW_OPEN_PRICE == True )) \
               # or   float(DIFF_EMA1L_SAR) > 0 and (TYPE_BG == "BG_VERTE")  :
                if (DIFF_NEW_HIGH_PRICE_SUP_NEW_OPEN_PRICE == True ) :
                 time.sleep(4)
                 # RECUP_LAST_PRICE_IN_BINANCE(dataframe)
                # if DATE_VENTE_FUTUR = "" :
                # TEMPS=2
                CALCULE_FIN_CYCLE()
                VENTE_SUR_SAR=False
                custom_info["couleur"]="ACHAT_SUR_SAR"
                BOOLLEEN_NINJA(TAILLE_BG,dataframe,"ACHAT") 
                # Delay_new_frame(30)
                print("!!!!!! CLOTURE ACHAT SHORT  ET DEBUT ACHAT LONGUE : ",last_price)
                # LAST_ORDER = "BUY"
                return
            
            # if (LAST_ORDER != "SELL")   and  (POINT_ENTRE_EMA200 == 1) and float(GAIN1) >= float(GAIN_OLD) and float(GAIN_OLD) > 0 \
            #     and ( COMPTEUR_VENTE_RELATIVE >= 2 and VAL_EMA15_COURANT < VAL_EMA200_COURANT) :
            #         print ("ENTRER DANS VENTE COMPTEUR_VENTE_RELATIVE == 3")
            #         # GAIN1 = GAIN_OLD     
            #         custom_info["couleur"]="COMPTEUR_VENTE_RELATIVE == 3  : " + str(GAIN1)
            #         RECUP_LAST_PRICE_IN_BINANCE(dataframe)
            #         BOOLLEEN_NINJA(TAILLE_BG,dataframe,"VENTE") 
            #         # LAST_ORDER = "SELL"
            #         CYCLE_COURT=False   
            #         COMPTEUR_VENTE_RELATIVE==0    
            #         Delay_new_frame(120)
                    
            # if (LAST_ORDER != "SELL")   and  (POINT_ENTRE_EMA200 == 1) and (int(GAIN1) > 0) \
            #     or (last_index - INDEXMAX == 1 ) \
            #     or ((DIFF_VAL_CLOSE_INF_VAL_CLOSE_N2 == True) or (DIFF_NEW_HIGH_PRICE_SUP_NEW_OPEN_PRICE == True ) and (int(GAIN1) >= 0)) \
            #     or (VENTE_SUR_SAR==True and (int(GAIN1) >= 0)) :
            #     print("!!!!!! INDEXMAX :",INDEXMAX)
            #     print("!!!!!! last_index :",last_index)
            #     print("!!!!!! last_index - INDEXMAX  :",last_index - INDEXMAX )
            #     custom_info["couleur"]="VENTE_SUR_SAR last_index > INDEXMAX  PSAR : " + str(GAIN1)
            #     BOOLLEEN_NINJA(TAILLE_BG,dataframe,"VENTE") 
            #     LAST_ORDER = "SELL"
            #     # return
            
            if (LAST_ORDER != "SELL")   and  (POINT_ENTRE_EMA200 == 1) and DIFF_last_index_MOINS_INDEXMIN <= 1  and float(GAIN1) > 0 :
                print(f"!!!!!! DELAIS 1 MINUTE SUR POINT DE SUPPORT INDEXMIN {DIFF_last_index_MOINS_INDEXMIN}  : {VAL_MIN_PSAR}")
                Delay_new_frame(5)

            # if (LAST_ORDER != "SELL")   and  (POINT_ENTRE_EMA200 == 1) and GAIN1 > 0 :
            #     # or (LAST_ORDER != "SELL" and POINT_ENTRE_EMA200 == 1 and DIFF_SAR_SUP_PRIX == True  and GAIN1 > 0 ) : 
            #     if  float(GAIN_ABSOLUE) < 0  or   (DIFF_GAIN_ABSOLUE_RELATIF_SUP_GAIN_ABSOLUE == False and float(GAIN1) > 0 ) \
            #       or ((DIFF_VAL_CLOSE_INF_VAL_CLOSE_N2 == False) and (DIFF_NEW_HIGH_PRICE_SUP_NEW_OPEN_PRICE == True ) and (float(GAIN1) > 0))  or (float(GAIN1) >= 5) :
            #       # or (DIFF_SAR_SUP_PRIX == True and GAIN_OLD > 0 )  or (float(GAIN1) > 0 and float(GAIN_OLD) > 0) \
            #       # or (last_price_file < VAL_CLOSE_N1 and float(GAIN1) > 0 and DIFF_VAL_CLOSE_INF_VAL_CLOSE_N2 == False ) :
            #       # or (COMPTEUR_DIFF_GAIN1_EGAL >= NBR_COMPTEUR_DIFF_GAIN1 ) :
            #         # GAIN1 = GAIN_OLD     
            #         custom_info["couleur"]="VENTE SUR DIFF_GAIN_ABSOLUE_RELATIF_SUP_GAIN_ABSOLUE : " + str(GAIN1)
            #         RECUP_LAST_PRICE_IN_BINANCE(dataframe)
            #         BOOLLEEN_NINJA(TAILLE_BG,dataframe,"VENTE") 
            #         # LAST_ORDER = "SELL"
            #         CYCLE_COURT=False
            #         if  (DIFF_SAR_SUP_PRIX == True ) :
            #               Delay_new_frame(30)
            #         # if COMPTEUR_DIFF_GAIN1_EGAL >= NBR_COMPTEUR_DIFF_GAIN1 :
            #         #    COMPTEUR_DIFF_GAIN1_EGAL == 0
            #         # COMPTEUR_GAIN_ZERO=0
            #         # return
            
            if (LAST_ORDER != "SELL")   and  (POINT_ENTRE_EMA200 == 1)  and (GAIN1 == 0 and GAIN_ABSOLUE >= 0) :
                return

            
            # if (LAST_ORDER != "SELL")   and  (POINT_ENTRE_EMA200 == 1) and (FRONT_MONTANT_EMA1H >= 0) and (FRONT_MONTANT_COURT_EMA15 == 0) :
            if (LAST_ORDER != "SELL")   and  (POINT_ENTRE_EMA200 == 1)   :
               if (GAIN1 > 0 and  DIFF_GAIN1_INF_GAIN_OLD == True and TYPE_BG_BIS == "BG_VERTE" ) \
                or ((LAST_ORDER != "SELL")   and  (POINT_ENTRE_EMA200 == 1) and (TYPE_BG_BIS == "BG_ROUGE" )  ) \
                    or ((LAST_ORDER != "SELL")   and  (POINT_ENTRE_EMA200 == 1) and (TEST_VARIATION_POSITIVE == False) ) :
                    # or (((LAST_ORDER != "SELL")   and  (POINT_ENTRE_EMA200 == 1) and (TEST_VARIATION_POSITIVE == True) and DIFF_SAR_SUP_EMA15 == True)) :
                 # if (  float(GAIN1) > 0 and (VAL_EMA15_COURANT < VAL_OPEN) ) or float(GAIN1) >= 5 or (GAIN_MOINS_UN_POURCENT > last_price) or (TYPE_BG == "BG_ROUGE") or  GAIN1 < 0 :
                 # if (  float(GAIN1) > 0 and (VAL_EMA15_COURANT < VAL_OPEN) ) or float(GAIN1) >= 5 or (GAIN_MOINS_UN_POURCENT > last_price) or (TYPE_BG_BIS == "BG_ROUGE") or  GAIN1 < 0 :
                 # if  (  float(GAIN1) > 0 and (VAL_EMA15_COURANT < VAL_OPEN) ) or float(GAIN1) >= 5 or (GAIN_MOINS_UN_POURCENT > last_price) or (TYPE_BG_BIS == "BG_ROUGE" and GAIN1 > 0) or  GAIN1 < 0 :
                 # if  (  float(GAIN1) > 0 and (VAL_EMA15_COURANT < VAL_OPEN) ) or float(GAIN1) >= 5 or (GAIN_MOINS_UN_POURCENT > last_price) or ((TYPE_BG_BIS == "BG_ROUGE" ) and (DIFF_VAL_CLOSE_INF_VAL_CLOSE_N2 == True)) \
                 # if  (  float(GAIN1) > 0 and (VAL_EMA15_COURANT < VAL_OPEN) ) or float(GAIN1) >= 5 or ((TYPE_BG_BIS == "BG_ROUGE" ) and (DIFF_VAL_CLOSE_INF_VAL_CLOSE_N2 == True)) \
                 #   or ((TYPE_BG_BIS == "BG_ROUGE" ) and (FRONT_MONTANT_EMA1H == 1)) or ((TYPE_BG_BIS == "BG_ROUGE" )) or (TEST_VARIATION_POSITIVE == False) or (FRONT_MONTANT_EMA1L == 0) \
                 #       or ( VENTE_SUR_SAR == True) or (DIFF_SAR_SUP_PRIX == True and GAIN1 > 0 ) : or  (TYPE_BG_BIS == "BG_ROUGE" and GAIN1 < 0 )
                 if (DIFF_SAR_SUP_PRIX == True and GAIN1 > 0 ) or float(GAIN1) >= 15 or  (DIFF_SAR_SUP_PRIX == True and TEST_VARIATION_POSITIVE == True and GAIN1 > 0) \
                    or  (TYPE_BG_BIS == "BG_ROUGE" and TEST_VARIATION_POSITIVE == True and GAIN1 >= 0)  \
                        or ( GAIN1 < -1 and DIFF_VAL_CLOSE_INF_VAL_CLOSE_N2 == True and TYPE_BG_BIS == "BG_ROUGE" ) \
                   or ( DIFF_GAIN1_INF_GAIN_OLD == True  and GAIN1 > 0 and (TYPE_BG_BIS == "BG_VERTE" ) ) :    
                    print ("ENTRER DANS VENTE FINALE")
                    # GAIN1 = GAIN_OLD     
                    custom_info["couleur"]="VENTE FINALE : " + str(GAIN1)
                    # RECUP_LAST_PRICE_IN_BINANCE(dataframe)
                    BOOLLEEN_NINJA(TAILLE_BG,dataframe,"VENTE") 
                    # LAST_ORDER = "SELL"
                    CYCLE_COURT=False 
                    if  (DIFF_SAR_SUP_PRIX == True ) and (TEST_VARIATION_POSITIVE == True) :
                    #       Delay_new_frame(120)
                    # else:
                            Delay_new_frame("")
                    # if  (DIFF_SAR_SUP_EMA15 == True ) and (TEST_VARIATION_POSITIVE == True) :
                    #    Delay_new_frame(180)


            
            # if (LAST_ORDER != "SELL")   and  (POINT_ENTRE_EMA200 == 1) and float(GAIN1) > 0 and (DIFF_SAR_SUP_PRIX == True) : 
            if (LAST_ORDER != "SELL")   and  (POINT_ENTRE_EMA200 == 1) and GAIN1 >= 0 :
                # if ( int(COMPTEUR_DIFF_GAIN1_EGAL) >= int(NBR_COMPTEUR_DIFF_GAIN1) ) and ( FRONT_MONTANT_EMA1H == 1) and GAIN1 >= 0 :
                if ( int(COMPTEUR_DIFF_GAIN1_EGAL) >= int(NBR_COMPTEUR_DIFF_GAIN1) ) : #and GAIN1 >= 0 :
                  # if (  float(GAIN1) > 0 and (TYPE_BG_BIS == "BG_VERTE")) \
                  # if (  float(GAIN1) > 0 and (TYPE_BG == "BG_ROUGE") or (TYPE_BG_BIS == "BG_ROUGE") and GAIN1 >= 0) \
                  # if (  float(GAIN1) > 0  or (TYPE_BG_BIS == "BG_ROUGE") and GAIN1 >= 0) \
                  #     or (last_index - INDEXMAX == 1  and DIFF_SAR_SUP_PRIX==True and GAIN1 > 0) :
                  # if (  DIFF_SAR_SUP_PRIX==True  and (TYPE_BG_BIS == "BG_ROUGE") ) :
                  if ( (TYPE_BG_BIS == "BG_VERTE") ) :
                    print ("ENTRER DANS RESISTANCE GAIN")
                    # GAIN1 = GAIN_OLD     
                    custom_info["couleur"]="RESISTANCE GAIN  : " + str(GAIN1)
                    RECUP_LAST_PRICE_IN_BINANCE(dataframe)
                    BOOLLEEN_NINJA(TAILLE_BG,dataframe,"VENTE") 
                    # LAST_ORDER = "SELL"
                    CYCLE_COURT=False
                    if COMPTEUR_DIFF_GAIN1_EGAL >= NBR_COMPTEUR_DIFF_GAIN1 :
                        COMPTEUR_DIFF_GAIN1_EGAL == 0
                        # Delay_new_frame(30)
                    # COMPTEUR_GAIN_ZERO=0
                    # return
                    if  (TYPE_BG_BIS == "BG_ROUGE") and float(GAIN1) <= 0 or (last_index - INDEXMAX == 0  and VENTE_SUR_SAR==True and int(GAIN1) <= 0) :
                        Delay_new_frame(60)
                    else :
                        Delay_new_frame(90)

                    
            # if (LAST_ORDER != "SELL")   and  (POINT_ENTRE_EMA200 == 1)  and ((TYPE_BG_BIS == "BG_ROUGE") and (DIFF_SAR_SUP_PRIX == True )) and float(GAIN1) >= 0 : 
            #     # if (float(HIGH) >= float(VAL_CLOSE_N1)) and  (DIFF_SAR_SUP_PRIX == True ) and VENTE_SUR_SAR==True:
            #     # if (DIFF_SAR_SUP_PRIX == True ) :
            #         print ("ENTRER DANS VENTE TYPE_BG_BIS BG_ROUGE")
            #         # GAIN1 = GAIN_OLD     
            #         custom_info["couleur"]="VENTE  TYPE_BG_BIS BG_ROUGE  : " + str(GAIN1)
            #         RECUP_LAST_PRICE_IN_BINANCE(dataframe)
            #         BOOLLEEN_NINJA(TAILLE_BG,dataframe,"VENTE") 
            #         LAST_ORDER = "SELL"
            #         CYCLE_COURT=False     
            #         Delay_new_frame("")
    
    
            return         
            # if (LAST_ORDER != "SELL")   and  (POINT_ENTRE_EMA200 == 1) : 
            #     now=datetime.now()
            #     new_hour=now  #+ timedelta(hours=2)   
            #     new_hour=new_hour.strftime("%Y-%m-%d %H:%M:%S")
            #     if DATE_VENTE_FUTUR in new_hour and  GAIN1 > 0:
            #        DATE_VENTE_FUTUR=""
            #        print("!!!!!! new_hour  :",new_hour )
            #        print("!!!!!! DATE_VENTE_FUTUR  :",DATE_VENTE_FUTUR )
            #        custom_info["couleur"]="VENTE SUR DATE_VENTE_FUTUR : " + str(GAIN1)
            #        RECUP_LAST_PRICE_IN_BINANCE(dataframe)
            #        BOOLLEEN_NINJA(TAILLE_BG,dataframe,"VENTE") 
            #        LAST_ORDER = "SELL"
            #        CYCLE_COURT=False
            #        # Delay_new_frame(20*1)
            #     if   ((DIFF_VAL_CLOSE_INF_VAL_CLOSE_N2 == True) and (DIFF_NEW_HIGH_PRICE_SUP_NEW_OPEN_PRICE == True ) and (int(GAIN1) > 0)) \
            #         or ((DIFF_VAL_CLOSE_INF_VAL_CLOSE_N2 == False) and (DIFF_NEW_HIGH_PRICE_SUP_NEW_OPEN_PRICE == True ) and (int(GAIN1) > 0)) :
            #         # or (last_index - INDEXMAX != 0) or (PSAR == EMA1H) :
            #         custom_info["couleur"]="VENTE SUR DATE_VENTE_FUTUR : " + str(GAIN1)
            #         RECUP_LAST_PRICE_IN_BINANCE(dataframe)
            #         BOOLLEEN_NINJA(TAILLE_BG,dataframe,"VENTE") 
            #         LAST_ORDER = "SELL"
            #         CYCLE_COURT=False
            #         # Delay_new_frame(20*1)
            #     if  int(GAIN1) >= 200  or (GAIN_OLD > 0 and GAIN1 < GAIN_OLD) or (VENTE_SUR_SAR == True and  GAIN1 > 0 ):
            #         # GAIN1 = GAIN_OLD     
            #         custom_info["couleur"]="VENTE SUR GAIN1 < GAIN_OLD: " + str(GAIN1)
            #         RECUP_LAST_PRICE_IN_BINANCE(dataframe)
            #         BOOLLEEN_NINJA(TAILLE_BG,dataframe,"VENTE") 
            #         LAST_ORDER = "SELL"
            #         CYCLE_COURT=False
            #         # Delay_new_frame(60*1)

                    
                    
            # return    
            # print("\n!!!!!DEB VENTE SAR !!!")
            # # if  GAIN1 > 0 or DIFF_NEW_HIGH_PRICE_SUP_NEW_OPEN_PRICE == True :  or ( DIFF_EMA1L_SAR < 0 and  GAIN1 <= 0) 
            # if (LAST_ORDER != "SELL")   and  (POINT_ENTRE_EMA200 == 1) and (DIFF_NEW_HIGH_PRICE_SUP_NEW_OPEN_PRICE == False ) :
            #   if  (int(GAIN1) > 0 and DIFF_NEW_HIGH_PRICE_SUP_NEW_OPEN_PRICE == False) and VENTE_SUR_SAR==True and (int(TAILLE_BG) > 0) \
            #     or (DIFF_NEW_HIGH_PRICE_SUP_NEW_OPEN_PRICE == False) or (DIFF_SAR_PRECEDENT_SAR == 0) or (int(TAILLE_BG) <= 0)\
            #      or ((DIFF_VAL_CLOSE_INF_VAL_CLOSE_N2 == True)  and VENTE_SUR_SAR==True)  :
            #     # and DIFF_NEW_HIGH_PRICE_SUP_NEW_OPEN_PRICE == True  and ( FRONT_MONTANT_EMA1H == 1)  :
            #     ACHAT_SUR_SAR=False
            #     custom_info["couleur"]="VENTE_SUR_SAR GAIN PSAR : " + str(GAIN1)
            #     if DIFF_EMA1L_SAR <= 0 :
            #           print("!!!!!! VENTE FUTUR BG_ROUGE: \nCLOTURE ACHAT LONGUE  ET DEBUT ACHAT SHORT : ")
            #     else:
            #         print("!!!!!! CLOTURE ACHAT LONGUE  ET DEBUT ACHAT SHORT : ",NEW_HIGH_PRICE)  
            #     BOOLLEEN_NINJA(TAILLE_BG,dataframe,"VENTE") 
            # #   # return
            
            # if (POINT_ENTRE_EMA200 == 1) and (LAST_ORDER != "SELL")  :
            if (POINT_ENTRE_EMA200 == 1) and ((float(GAIN1) < float(GAIN_OLD)  ) ) or (DIFF_SAR_SUP_PRIX == True and POINT_ENTRE_EMA200 == 1) :
                # or (POINT_ENTRE_EMA200 == 1 and GAIN_OLD <= 0) :
            # if (POINT_ENTRE_EMA200 == 1) and (DIFF_SAR_SUP_PRIX == True ) and  GAIN1 <= 0:
                print("!!!!!INTERCEPTION  VENTE !!!")
                # custom_info["MODE_GAIN"]="GAIN_RELATIF"
                RECUP_LAST_PRICE_IN_BINANCE(dataframe)
                # if len(str(PRIX)) == 2 :
                #     PRIX=str(PRIX)+"0"
                # RECUP_LAST_PRICE_IN_FILE()
                # PRIX=last_price_file
                # print("RECUPERATION DU PRIX SUR BINANCE SOCKET: ",PRIX)
                print("!!!!! 1 ere RECUPERATION DU PRIX SUR BINANCE: ",PRIX)
                VAL_ACHAT=float(custom_info["VAL_ACHAT"]) 
                GAIN1=(float(PRIX) - float(VAL_ACHAT))
                print("!!!!! GAIN_OLD: ",GAIN_OLD)
                print("!!!!! 1 er GAIN1: ",GAIN1)
                #POUR FUTUR SHORT PRIX NEGATIF
                # if  GAIN1 > 0 or (float(PRIX) <=  float(last_price_file)) :
                #POUR FUTUR SHORT PRIX POSITIF
                # if  GAIN1 >= 0 or (float(PRIX) >  float(last_price_file)) :
                # if GAIN1 <= 0 and GAIN1 <= GAIN_OLD and GAIN_OLD > 0  or GAIN1 >= 200  or  float(PRIX) <= float(VAL_ACHAT) :
                # if  float(PRIX) <= float(VAL_ACHAT) :
                #     # GAIN1 = GAIN_OLD
                #     # LAST_ORDER = "BUY"
                #     custom_info["couleur"]="INTERCEPTION GAIN1   : " + str(GAIN1)
                #     BOOLLEEN_NINJA(TAILLE_BG,dataframe,"VENTE") 
                #     return
                PRIX_OLD=PRIX
                LEN_PRIX_OLD=len(str(PRIX))
                # time.sleep(3)
                if (DIFF_SAR_SUP_PRIX == False ) or (GAIN_OLD == 0) and (float(PRIX) > float(VAL_ACHAT)) or (float(GAIN_OLD) > 0):
                    Delay_new_frame(8)
                else:
                    Delay_new_frame(1)
                RECUP_LAST_PRICE_IN_BINANCE(dataframe)   
                # if len(str(PRIX)) == 2 :
                #     PRIX=str(PRIX)+"0"
                # RECUP_LAST_PRICE_IN_FILE()
                # PRIX=last_price_file
                # print("RECUPERATION DU PRIX SUR BINANCE SOCKET: ",PRIX)
                # LAST_PRICE=int(float(last_price_file)*MULTIP)
                # custom_info["CLOSE"]=LAST_PRICE
                print("!!!!! 2 eme RECUPERATION DU PRIX SUR BINANCE: ",PRIX)
                if LEN_PRIX_OLD > len(str(PRIX)):
                    PRIX=str(PRIX)+"0"
                if  float(PRIX_OLD) <= float(PRIX) and GAIN1 >= 0 or (float(PRIX) < float(VAL_ACHAT)) :
                    custom_info["couleur"]="INTERCEPTION VENTE_SUR_SAR  : " + str(GAIN1)
                    print("!!!!! 2 eme RECUPERATION ET PRIX IDENTIQUE ==> ORDRE  VENTE  ")
                    # LAST_ORDER = "BUY"
                    BOOLLEEN_NINJA(TAILLE_BG,dataframe,"VENTE") 
                    CYCLE_COURT=True
                    # COMPTEUR_GAIN_ZERO=0
                    Delay_new_frame(120)
                else:
                    print("!!!!! 2 eme RECUPERATION ET PRIX DIFFERENT SUR BINANCE ")
                    # return
                LAST_ORDER = "SELL"

            
            return   
                
            print("!!!!!DEB ACHAT !!!")
            if (LAST_ORDER != "BUY")  and DIFF_VAL_CLOSE_INF_VAL_CLOSE_N2 == False and (DIFF_NEW_HIGH_PRICE_SUP_NEW_OPEN_PRICE == True) \
                and (int(LAST_PRICE) >= int(VAL_EMA15_COURANT)) \
                and (int(TAILLE_BG)) > 0\
                and  float(DIFF_EMA1L_SAR) > 0 and (TYPE_BG == "BG_VERTE") \
                or (int(TAILLE_BG) > 1 and DIFF_VAL_CLOSE_INF_VAL_CLOSE_N2 == False and (DIFF_NEW_HIGH_PRICE_SUP_NEW_OPEN_PRICE == True)) \
                or ( FRONT_MONTANT_EMA1H == 1) and (TYPE_BG == "BG_VERTE") :
                # and  DIFF_VAL_CLOSE_INF_VAL_CLOSE_N1 == False \
                # and (int(CLOSE) >= int(VAL_EMA15_COURANT)) \
                # and ( ( FRONT_MONTANT_EMA15 == 1) or  ( FRONT_MONTANT_COURT_EMA15 == 1) ) :
             # or ( DIFF_NEW_HIGH_PRICE_SUP_NEW_OPEN_PRICE == True and  int(TAILLE_BG) > int(TAILLE_BG_N1) and (TYPE_BG == "BG_VERTE")) :
             # or ( ( FRONT_MONTANT_EMA1L == 1) or  ( FRONT_MONTANT_EMA1H == 1)) :
             # or (int(EMA1H) > int(VAL_EMA15_COURANT) and ( FRONT_MONTANT_EMA1L == 1) or  ( FRONT_MONTANT_EMA1H == 1)) :
              # or ( (int(EMA1L) > int(VAL_EMA15_COURANT)) and (int(EMA1H) > int(VAL_EMA15_COURANT)) 
              # and ( FRONT_MONTANT_EMA15 == 1)    ) :
            # and ( ( FRONT_MONTANT_COURT_EMA1H == 1) ) and ( ( FRONT_MONTANT_EMA15 == 1) ) :
             # if (int(EMA1H) >= int(VAL_EMA15_COURANT)) or ( ( FRONT_MONTANT_COURT_EMA1H == 1) )\
             #     or ( (DIFF_NEW_HIGH_PRICE_SUP_NEW_OPEN_PRICE == True) )  : 
                # if ( ( FRONT_MONTANT_EMA15 == 1) )   \
                # or ( ( FRONT_MONTANT_COURT_EMA1H == 1) ) :
                    # LAST_ORDER="SELL"
                    custom_info["couleur"]=TYPE_BG
                    BOOLLEEN_NINJA(TAILLE_BG,dataframe,"ACHAT") 
                    print("!!!!!! CLOTURE ACHAT SHORT  ET DEBUT ACHAT LONGUE : ",last_price)

                    # POINT_ENTRE_EMA200 = 1 #VEROUILAGE ACHAT ET VENTE NORMAL
                    # Diff_GAIN2_GAIN1_LAST_PRICE=0
                    #Delay_new_frame("")
                    
            # if Diff_LAST_PRICE_OLD_File_price < 0  :
            #     NBR_Diff_last_price_OLD_LAST_PRICE = -1    
           
            #  #ORDRE  DE VENTE      
            # if Diff_LAST_PRICE_OLD_File_price > 0  :
            #    NBR_Diff_last_price_OLD_LAST_PRICE = 1
                   # or ( GAIN1 > 1 ) and DIFF_VAL_CLOSE_INF_VAL_CLOSE_N1 == False \
                   # and  (int(PSAR) >= int(VAL_EMA15_COURANT)) or (int(PSAR) >= int(EMA1L) ) \
            if (POINT_ENTRE_EMA200 == 1) and (LAST_ORDER != "SELL")  :
               if (  DIFF_NEW_HIGH_PRICE_SUP_NEW_OPEN_PRICE == True and  FRONT_MONTANT_EMA1H == 1 and  GAIN1 > 0) :
                   custom_info["couleur"]="SORTIE FINALE  : " + str(GAIN1)
                   BOOLLEEN_NINJA(TAILLE_BG,dataframe,"VENTE") 

                 # !!!!!!!!!!!!!! DEB VENTE 
                
            print("!!!!!DEB VENTE !!!")
            GAIN1=float(GAIN1)
            if (POINT_ENTRE_EMA200 == 1) and (LAST_ORDER != "SELL")  :
               # if (int(TAILLE_BG) <= 0 )  \
               # if ( DIFF_NEW_HIGH_PRICE_SUP_NEW_OPEN_PRICE == False and  DIFF_EMA1L_SAR > 0 and GAIN1 > 0) \
                  # or  DIFF_EMA1L_SAR < 0 :
               if (float(DIFF_EMA1L_SAR) < 0 and DIFF_NEW_HIGH_PRICE_SUP_NEW_OPEN_PRICE == False  and ( FRONT_MONTANT_EMA1H == 1) \
                   and GAIN1 > 0) \
                    and ( DIFF_NEW_HIGH_PRICE_SUP_NEW_OPEN_PRICE == False and  GAIN1 <= 0)\
                    or ( DIFF_EMA1L_SAR < 0 and  GAIN1 <= 0)\
                    or ((TAILLE_BG < 0 or TAILLE_BG_N1 < 0 or TAILLE_BG_N2 < 0 or TAILLE_BG_N3 < 0) and  GAIN1 <= 0)\
                    or (( FRONT_MONTANT_EMA1L == 0) and ( FRONT_MONTANT_EMA1H == 0)  and  GAIN1 <= 0):
                       
                   #2 LIGNE CI-DESSUS POUR QUITTER LA COURBE AU PLUS HAUT
                   
                   # or ((TAILLE_BG < 0 or TAILLE_BG_N1 < 0) and  GAIN1 <= 0)\

                   # or (int(TAILLE_BG) <= 0 ) \
                   # and ( DIFF_NEW_HIGH_PRICE_SUP_NEW_OPEN_PRICE == True and  GAIN1 > 0) \
                   # or  (TYPE_BG == "BG_VERTE" and  GAIN1 == 0) \
                   # and  (DIFF_VAL_CLOSE_INF_VAL_CLOSE_N1 == True and DIFF_NEW_HIGH_PRICE_SUP_NEW_OPEN_PRICE == False and GAIN1 <= 0) \
                   # or  (abs(int(TAILLE_BG)) <= abs(int(TAILLE_BG_N1)) ) \
                   # and DIFF_VAL_CLOSE_INF_VAL_CLOSE_N1 == False :
                   # or (  DIFF_NEW_HIGH_PRICE_SUP_NEW_OPEN_PRICE == True and  FRONT_MONTANT_EMA1H == 1 and  GAIN1 <= 0) :

                   # or (FRONT_MONTANT_EMA1H == 0 and  GAIN1 <= 0) :
                   # and  (DIFF_VAL_CLOSE_INF_VAL_CLOSE_N1 == True and GAIN1 > 0) :
                   # or ( DIFF_EMA1L_SAR < 0 or  GAIN1 <= 0) :

                # or ( DIFF_NEW_HIGH_PRICE_SUP_NEW_OPEN_PRICE == False ) \
                # or DIFF_VAL_CLOSE_INF_VAL_CLOSE_N1 == True  \
                # or  (int(PSAR) <= int(VAL_EMA15_COURANT)) or (int(PSAR) >= int(EMA1L) ) \
                    
                # or  DIFF_EMA1L_SAR <= 0 \
                # or  DIFF_EMA1H_SAR <= 0 \
                # or  (TYPE_BG == "BG_VERTE" and TYPE_BG_N1 == "BG_VERTE" and TYPE_BG_N2 == "BG_ROUGE"):
                
                # or ((int(PSAR) - int(VAL_EMA15_COURANT) >= 0) and (int(PSAR) - int(VAL_EMA15_COURANT) <= 3)) :
                custom_info["couleur"]="GAIN PSAR : " + str(GAIN1)
                # CHECK_GAIN_SORTIE_POSITIF(NEW_OPEN_PRICE)
                 
                # if DIFF_EMA1H_SAR <= 0 or (int(PSAR) > int(VAL_EMA15_COURANT)) :
                   # CHECK_GAIN_SORTIE_POSITIF(NEW_OPEN_PRICE)
                if DIFF_EMA1L_SAR <= 0 :
                     print("!!!!!! VENTE FUTUR BG_ROUGE: \nCLOTURE ACHAT LONGUE  ET DEBUT ACHAT SHORT : ")
                else:
                #     BOOLLEEN_NINJA(TAILLE_BG,dataframe,"VENTE") 
                    print("!!!!!! CLOTURE ACHAT LONGUE  ET DEBUT ACHAT SHORT : ",NEW_HIGH_PRICE)  
                BOOLLEEN_NINJA(TAILLE_BG,dataframe,"VENTE") 
                return
                                     
                     
                if  GAIN1 > 0 and (TYPE_BG_BIS == "BG_ROUGE") and  (POINT_ENTRE_EMA200 == 1) and (LAST_ORDER != "SELL") :
                     custom_info["couleur"]="GAIN POSITIF : " + str(GAIN1)
                     BOOLLEEN_NINJA(TAILLE_BG,dataframe,"VENTE") 
                     
                # if  ( FRONT_NEUTRE_EMA15 == 1)  and (TYPE_BG == "BG_VERTE")  \
                #  or ( FRONT_MONTANT_EMA1H == 0) and ( DIFF_VAL_CLOSE_INF_VAL_CLOSE_N1 == True) :
                if   ( DIFF_VAL_CLOSE_INF_VAL_CLOSE_N1 == True) and GAIN1 > 0 and ((last_price) > (VAL_ACHAT)) :
                        custom_info["couleur"]="\nFIN FRONT_NEUTRE_EMA15 : " + str(GAIN1)
                        BOOLLEEN_NINJA(TAILLE_BG,dataframe,"VENTE")            
                        
                if  ( ( FRONT_MONTANT_EMA1H == 0)  ) and int(TAILLE_BG) < int(TAILLE_BG_N1) \
                    or (( FRONT_MONTANT_EMA1L == 0) and ( FRONT_MONTANT_EMA1H == 0) and GAIN1 < -1 ) \
                    or DIFF_EMA1H_SAR <= 0 :    
                        custom_info["couleur"]="\nFIN CROISSANCE COURBE : " + str(GAIN1)
                        BOOLLEEN_NINJA(TAILLE_BG,dataframe,"VENTE")     
                        DERNIER_POINT_VENTE=1
                        print("!!!!!FIN CROISSANCE COURBE!!!!!!!\n!!! BOT EN MODE ATTENTE 5 MN !!!")
                        Delay_new_frame(60*2)
                     
                # if  ( ( FRONT_MONTANT_EMA1H == 0) and ( FRONT_MONTANT_EMA15 == 0)) and int(TAILLE_BG) < int(TAILLE_BG_N1) \
                #     or (( FRONT_MONTANT_EMA1L == 0) and ( FRONT_MONTANT_EMA1H == 0) and GAIN1 < -1 ) :    
                #         custom_info["couleur"]="FIN CROISSANCE : " + str(GAIN1)
                #         BOOLLEEN_NINJA(TAILLE_BG,dataframe,"VENTE") 
                        
                if (GAIN1 < 0  and DIFF_VAL_CLOSE_INF_VAL_CLOSE_N1 == True)  or  GAIN1 >= 100 :  
                      custom_info["couleur"]="GAIN NEGATIF DIFF_VAL_CLOSE_INF_VAL_CLOSE_N1 : " + str(GAIN1)
                      BOOLLEEN_NINJA(TAILLE_BG,dataframe,"VENTE")                         
             
            # if  (( FRONT_MONTANT_COURT_EMA1H == 0) and ( FRONT_MONTANT_EMA15 == 0)) \ and  (TYPE_BG == "BG_ROUGE") 
            if GAIN1 > 0 and ((last_price) > (VAL_ACHAT))   :
             if (POINT_ENTRE_EMA200 == 1) and (LAST_ORDER != "SELL") \
             or (DIFF_NEW_HIGH_PRICE_SUP_NEW_OPEN_PRICE == False) \
             or (int(EMA1H) < int(VAL_EMA15_COURANT)) \
             or  ( int(TAILLE_BG) < int(TAILLE_BG_N1) ) \
             or ( DIFF_VAL_CLOSE_INF_VAL_CLOSE_N1 == True) :
             # or ( FRONT_MONTANT_EMA1H == 0)  :
            # and (float(last_price) > float(VAL_ACHAT)) :
             # if  (( FRONT_MONTANT_COURT_EMA1H == 0) ) \
             #    or (DIFF_NEW_HIGH_PRICE_SUP_NEW_OPEN_PRICE == False) \
             #    or ( int(TAILLE_BG) < int(TAILLE_BG_N1))  :
                 print("DEB VENTE DIFF_NEW_HIGH_PRICE_SUP_NEW_OPEN_PRICE : ",DIFF_NEW_HIGH_PRICE_SUP_NEW_OPEN_PRICE)
                 # POINT_ENTRE_EMA200 = 1
                 # DERNIER_POINT_VENTE = 0
                 # LAST_ORDER = "BUY"
                 #Delay_new_frame(2)           
                 custom_info["couleur"]=TYPE_BG
                 BOOLLEEN_NINJA(TAILLE_BG,dataframe,"VENTE") 
                 # exit()
                 # Diff_GAIN2_GAIN1_LAST_PRICE=0
        print("NBR_Diff_last_price_OLD_LAST_PRICE : ",NBR_Diff_last_price_OLD_LAST_PRICE)
        #time.sleep(0.2)
        # return
                
        # print("SOMME_VOLUMES_PRECEDENT:",SOMME_VOLUMES_PRECEDENT)
        # print("SOMME_VOLUMES:",SOMME_VOLUMES)
        # DIFF_SOMME_VOLUMES_SOMME_VOLUMES_PRECEDENT=(int(SOMME_VOLUMES) - int(SOMME_VOLUMES_PRECEDENT))
        # print("DIFF_SOMME_VOLUMES_SOMME_VOLUMES_PRECEDENT:",DIFF_SOMME_VOLUMES_SOMME_VOLUMES_PRECEDENT)
        # # 2eme CAS REACHAT SUR REBOND PARTOUT
        # if ACTION != "" :
        #     print("ACTION:",ACTION)
        #     #time.sleep(1)
        print("SORTIE DANS ZONE ULTIMATE_NINJA NEW\n")
        # print("!!!!!!!!!!!!!!!!!TEST!!!!!!!TEST!!!!!!!TEST!!!!!!!TEST")
        # exit()    
        
def CHECK_GAIN_SORTIE_POSITIF(VAL_ACHAT):
        global NEW_HIGH_PRICE
        print("\nEntrer DANS CHECK_GAIN_SORTIE_POSITIF")
        # Delay_new_frame(60*1)
        RECUP_LAST_PRICE_IN_FILE()
        Delay_new_frame(3)
        while float(NEW_HIGH_PRICE) < float(VAL_ACHAT) :
            RECUP_LAST_PRICE_IN_FILE()
            Delay_new_frame(3)
        DIFF_NEW_HIGH_PRICE_SUP_NEW_OPEN_PRICE=float(NEW_HIGH_PRICE) > float(VAL_ACHAT)
        if (DIFF_NEW_HIGH_PRICE_SUP_NEW_OPEN_PRICE == True) :
            print("RECUPERATION DU PRIX DE VENTE SUR MODJU SUR BINANCE SOCKET: ",float(NEW_HIGH_PRICE))
            # break
        BOOLLEEN_NINJA(TAILLE_BG,dataframe,"VENTE") 
        print("!!!!!! CLOTURE ACHAT LONGUE ET DEBUT ACHAT SHORT: ",float(NEW_HIGH_PRICE))
        print("SORTIE DE CHECK_GAIN_SORTIE_POSITIF\n")
        # Delay_new_frame(60*1)
        # exit()

def check_string(string):
    if "-" in str(string) :
        nbr=str(string).split("-")[1]
        nbr=int(nbr)
        string=format(string,".8f")
        deb=string.split(".")[0]
        fin=string.split(".")[1]
        len_deb=len(deb)+1
        gain=string[:nbr+len_deb]
        gain=float(gain)
        gain=int(gain * 10**nbr)
        print("gain:",gain)
        return gain

def BOOLLEEN_NINJA(Diff_last_price_OLD_LAST_PRICE,dataframe,ORDRE)  :
        global ORDER
        global POINT_ENTRE_EMA200
        global DERNIER_POINT_VENTE
        global LAST_ORDER
        global COULEUR_VOLUME
        global SEUIL_SORTIE
        global FRONT_MONTANT_EMA15
        global DERNIERE_VENTE_POSITIVE
        global PRIX
        global COMPTEUR_ACHAT_VENTE
        global COMPTEUR_VENTE_RELATIVE
        # global Diff_VOLUME_VWAP_LAST_PRICE_OLD_LAST_PRICE
        global COMPTEUR_NEGATIF
        global COMPTEUR_GAIN_ZERO
        global GAIN1
        global TIME_DEB_CYCLE_ACHAT
        global TIME_DEB_ACHAT
        global GAIN_RELATIF
        global TYPE_BG
        global  FLAG_SIMULATION
        global DIFF_VAL_CLOSE_INF_VAL_CLOSE_N2
        
        #custom_info["GAIN_RELATIF"]

        print("\nEntrer dans BOOLLEEN_NINJA" )
        print("ORDRE:",ORDRE )
        print("POINT_ENTRE_EMA200:",POINT_ENTRE_EMA200 )
        print("DERNIER_POINT_VENTE:",DERNIER_POINT_VENTE )
        print("LAST_ORDER:",LAST_ORDER )
        print("COMPTEUR_ACHAT_VENTE:",COMPTEUR_ACHAT_VENTE)

    
        #if (Diff_last_price_OLD_LAST_PRICE > 0) and (ORDRE == "ACHAT") and  (COULEUR_VOLUME == "VERT") \
        #if (Diff_last_price_OLD_LAST_PRICE > 0) and (ORDRE == "ACHAT") and (TYPE_BG == "BG_VERTE") \
        #and  (FRONT_MONTANT_COURT_EMA1H == 1) and (FRONT_MONTANT_EMA15 == 1) \
        #and  (FRONT_MONTANT_COURT_EMA1H == 1) and (Diff_LAST_PRICE_OLD_File_price >= 0) \
        #if (Diff_last_price_OLD_LAST_PRICE > 0) and (ORDRE == "ACHAT") and (Diff_VOLUME_VWAP_LAST_PRICE_OLD_LAST_PRICE >= 0) \
            # and (POINT_ENTRE_EMA200 == 0)  and (DERNIER_POINT_VENTE == 0) and (LAST_ORDER != "BUY") :

        if (ORDRE == "ACHAT")  and (POINT_ENTRE_EMA200 == 0)  and (DERNIER_POINT_VENTE == 0) and (( FRONT_MONTANT_EMA1L == 1) or ( FRONT_MONTANT_EMA1H == 1)) :
            # if (DIFF_SOMME_VOLUMES_SOMME_VOLUMES_PRECEDENT < 0) \
             #and  (int(DIFF_SOMME_VOLUMES_SOMME_VOLUMES_PRECEDENT) < 0) \
              print("1er ACHAT  Diff_last_price_OLD_LAST_PRICE")
              FIRST_ACHAT=1
              ORDER="BUY"
              custom_info["SCENARIO"]="ACHAT DANS ULTIMATE_NINJA_NEW " 
              print(ORDER)
              EXEC_ORDER(dataframe)
              #VAL_ACHAT=dataframe.close.loc[val_mask_idxmin]
              POINT_ENTRE_EMA200 = 1 #VEROUILAGE ACHAT ET VENTE NORMAL 
              TIME_DEB_ACHAT=datetime.now()  
              if COMPTEUR_ACHAT_VENTE == 0 :
                 TIME_DEB_CYCLE_ACHAT=datetime.now() 
                 # Delay_new_frame(10)
              # else:
              #      Delay_new_frame(5)
              # LAST_ORDER="BUY"
              
              # Delay_new_frame("")
              # Delay_new_frame(1)
              # if GAIN_RELATIF < 0 :
              #        print("DANS ACHAT COMPTEUR_NEGATIF :",COMPTEUR_NEGATIF)
              #        # Delay_new_frame(30*COMPTEUR_NEGATIF)
              #        # Delay_new_frame("")
              #        # Delay_new_frame(5)
              #        Delay_new_frame(10*GAIN_RELATIF)

              # else:
              #     print(f"DANS ACHAT ATTENTE {COMPTEUR_GAIN_ZERO} MINUTE :")
              #     Delay_new_frame(5)


              #   print("GAIN_RELATIF NEGATIF:",GAIN_RELATIF)
              # if COMPTEUR_ACHAT_VENTE == 1 :
              #  Delay_new_frame("")
               # Delay_new_frame(20)
              # if COMPTEUR_GAIN_ZERO > 0 and COMPTEUR_ACHAT_VENTE != 0 :
              #    COMPTEUR_GAIN_ZERO=3
              #    print(f"COMPTEUR_GAIN_ZERO NEGATIF ATTENTE {COMPTEUR_GAIN_ZERO} MINUTE :")
              #    Delay_new_frame(60*COMPTEUR_GAIN_ZERO)
              #    COMPTEUR_GAIN_ZERO=0
                 # if  DIFF_VAL_CLOSE_INF_VAL_CLOSE_N1 == True :
                 # Delay_new_frame("")
              
              if COMPTEUR_GAIN_ZERO > 0  and (DIFF_NEW_HIGH_PRICE_SUP_NEW_OPEN_PRICE == True) :
                  # print(f"DANS ACHAT COMPTEUR_GAIN_ZERO NEGATIF ATTENTE {COMPTEUR_GAIN_ZERO} MINUTE :")
                  print(f"DANS ACHAT COMPTEUR_GAIN_ZERO NEGATIF ATTENTE {COMPTEUR_GAIN_ZERO}0 SECONDE :")
                  # Delay_new_frame(10)
                  Delay_new_frame(4*COMPTEUR_GAIN_ZERO)
                  # COMPTEUR_GAIN_ZERO=0              
                
        #if ((ACTION=="VENTE_CAR_BAISSE_DU_PRIX") and (float(last_price) > float(VAL_ACHAT)) \ and (int(LAST_PRICE) >= int(VAL_ACHAT))
        #if ((Diff_last_price_OLD_LAST_PRICE < SEUIL_SORTIE) or (FRONT_MONTANT_COURT_EMA1H == 0)) and (ORDRE == "VENTE") \
        #if ((FRONT_MONTANT_COURT_EMA1H == 0)) and (ORDRE == "VENTE") \
        # if (ORDRE == "VENTE") and  (FRONT_MONTANT_COURT_EMA1H == 1) \
            # and (POINT_ENTRE_EMA200 == 1)  and (DERNIER_POINT_VENTE == 0) and (LAST_ORDER != "SELL") :
                #and (int(DERNIER_POINT_VENTE) == 1)

        if ("VENTE" in ORDRE )  and (int(POINT_ENTRE_EMA200) == 1)  :
                print("VENTE DANS ULTIMATE_NINJA_NEW : ")
                print("COMPTEUR_ACHAT_VENTE:",COMPTEUR_ACHAT_VENTE )
                ORDER="SELL"
                custom_info["SCENARIO"]="VENTE DANS ULTIMATE_NINJA_NEW : " + str(COMPTEUR_ACHAT_VENTE)
                print(ORDER)
                EXEC_ORDER(dataframe)

                #VAL_ACHAT=dataframe.close.loc[val_mask_idxmin]
                POINT_ENTRE_EMA200 = 0 #VEROUILAGE ACHAT ET VENTE NORMAL
                # LAST_ORDER="SELL"
                #•DERNIER_POINT_VENTE=1
                COMPTEUR_ACHAT_VENTE+=1
                COMPTEUR_VENTE_RELATIVE+=1

                # GAIN1=0
                if POINT_ENTRE_EMA200 == 1 :
                    CALCULE_DIFF_TIME()
                    
                # if GAIN_RELATIF > 0  :
                #     print("!!!!!VENTE DEGAIN POSITIF !!!!!!!")
                #     Delay_new_frame(5)
                # Delay_new_frame("")
                # Delay_new_frame(1)
              

                #time.sleep(2)
                #exit()  
                #CALCUL_TIME_DIFFERENCE()
                #print("time_difference:",time_difference)
                #exit()
                # if GAIN_RELATIF >= 70  :
                #     print("!!!!!VENTE DE GROS VOLUME!!!!!!!\n!!! BOT EN MODE ATTENTE 4 MN !!!")
                #     Delay_new_frame(60*4)
                #     #return   
                # else:
                #     Delay_new_frame("")
                
                # if GAIN_RELATIF < -1 and (TYPE_BG_N1 == "BG_VERTE") :
                #     print("!!!!!VENTE DE GROS VOLUME!!!!!!!\n!!! BOT EN MODE ATTENTE 3 MN !!!")
                #     Delay_new_frame(60*3)
                
                # if GAIN_RELATIF > -5 and GAIN_RELATIF < 20 : # and  COMPTEUR_ACHAT_VENTE >= 1 :
                #     print("!!!!!GAIN INFERIEUR A 20 !!!!!!!\n!!! BOT EN MODE ATTENTE 4 MN !!!")
                #     Delay_new_frame(60*4)
                #     return
                
                # if GAIN_RELATIF <= 0 :
                #     print("GAIN_RELATIF NEGATIF:",GAIN_RELATIF)
                #     DERNIER_POINT_VENTE=1
                #     Delay_new_frame(1)
                # else:
                #     print("GAIN_RELATIF POSITIF:",GAIN_RELATIF)
                #     DERNIERE_VENTE_POSITIVE=custom_info["CLOSE"]
                #     #DERNIERE_VENTE_POSITIVE=PRIX
                #     DERNIER_POINT_VENTE=0  
                #     COMPTEUR_ACHAT_VENTE+=1
                
                if float(GAIN_RELATIF) < 0 :
                      COMPTEUR_NEGATIF+=1
                #      #if COMPTEUR_NEGATIF == 2  and CUMUL_GAIN < 100 :
                      if COMPTEUR_NEGATIF >= 1  :
                          print(f"DANS VENTE COMPTEUR_NEGATIF GAIN NEGATIF ATTENTE {COMPTEUR_NEGATIF} MINUTE :")
                          # COMPTEUR_GAIN_ZERO=0
                          # print(f"COMPTEUR_NEGATIF GAIN NEGATIF ATTENTE 1 MINUTE :")

                              # TYPE_BG == "BG_ROUGE"
                          # if COMPTEUR_NEGATIF == 1:
                            # COMPTEUR_NEGATIF=0
                            # Delay_new_frame(2)
                            # Delay_new_frame("")
                          if (float(TAILLE_BG) > 0) and COMPTEUR_NEGATIF <= 2 :
                                   Delay_new_frame(60)
                          else:
                                  # Delay_new_frame("")
                                   Delay_new_frame(120)

                            # Delay_new_frame(60*COMPTEUR_NEGATIF)
                           
                          # Delay_new_frame(60*COMPTEUR_NEGATIF)
                         # COMPTEUR_NEGATIF+=1
                         
                          if COMPTEUR_NEGATIF >= 2:
                               COMPTEUR_NEGATIF=0
                               
                if float(GAIN_RELATIF) == 0 :
                      COMPTEUR_GAIN_ZERO+=1  
                      Delay_new_frame(3)
                      # Delay_new_frame("")

                if COMPTEUR_GAIN_ZERO >= 3  : 
                    # Delay_new_frame("")
                    # COMPTEUR_NEGATIF=0
                    Delay_new_frame(120)
                    COMPTEUR_GAIN_ZERO=0
                              
                # if float(GAIN_RELATIF) == 0 :
                #       COMPTEUR_GAIN_ZERO+=1
                #       #if COMPTEUR_NEGATIF == 2  and CUMUL_GAIN < 100 :
                # if COMPTEUR_GAIN_ZERO > 0 and float(GAIN_RELATIF) == 0 and float(CUMUL_GAIN_RELATIF) != 0 :
                #   print(f" DANS VENTE COMPTEUR_GAIN_ZERO  ATTENTE {COMPTEUR_GAIN_ZERO} MINUTE :")
                #   # COMPTEUR_GAIN_ZERO+=1
                #   COMPTEUR_NEGATIF=0
                #   # Delay_new_frame(60*COMPTEUR_GAIN_ZERO)
                #   if (float(TAILLE_BG) > 0) :
                #       Delay_new_frame(60)
                #   else:
                #       if (DIFF_VAL_CLOSE_INF_VAL_CLOSE_N2 == True) :
                #            Delay_new_frame(240)
                #       else:
                #           Delay_new_frame("")

                #   if int(COMPTEUR_GAIN_ZERO) >= 3  :
                #         COMPTEUR_GAIN_ZERO=1  
                #   # Delay_new_frame("")
                  
                  
               
                if float(GAIN_RELATIF) > 0 :
                      COMPTEUR_NEGATIF=0
                      COMPTEUR_GAIN_ZERO=0
                      # Delay_new_frame(90)
                      Delay_new_frame(10)
                
                LAST_ORDER="SELL"
        print("Sortie dans BOOLLEEN_NINJA")

def CALCULE_DIFF_TIME():
    global TIME_DEB_CYCLE_ACHAT
    global TIME_DEB_ACHAT
    global DIFF_TIME_SECOND 
    global DIFF_TIME_MINUTE  
    # global cv
    
    if COMPTEUR_ACHAT_VENTE == 0 :
        TIME_DEB=TIME_DEB_CYCLE_ACHAT
    else:
        TIME_DEB=TIME_DEB_ACHAT
       
    TIME_FIN=datetime.now()    
    DIFF_TIME=(TIME_FIN-TIME_DEB)
    DIFF_TIME_SECOND=int(DIFF_TIME.total_seconds())
    DIFF_TIME_MINUTE=(DIFF_TIME_SECOND/60)
    DIFF_TIME_MINUTE=(np.round(DIFF_TIME_MINUTE,2))
    DIFF_TIME_SECOND=str(DIFF_TIME_MINUTE).split(".")[1]
    DIFF_TIME_MINUTE=str(DIFF_TIME_MINUTE).split(".")[0]
    # print("DIFF_TIME_SECOND  : ",DIFF_TIME_SECOND)
    # print("DIFF_TIME_MINUTE  : ",DIFF_TIME_MINUTE)
    print(f"!!!!!! DIFF_TIME : {DIFF_TIME_MINUTE} MINUTES {DIFF_TIME_SECOND} SECONDES")

                    
def ULTIMATE_NINJA_BIS(dataframe,val_mask_idxmin) :
        print("\nENTRER DANS ZONE ULTIMATE_NINJA BIS")
        #TRAITEMENT_BOUGIE(dataframe,val_mask_idxmin)
        global POINT_ENTRE_EMA200
        global ORDER
        global LAST_ORDER
        global FIRST_VENTE
        global FIRST_ACHAT
        global VAL_ACHAT
        global DATE_COURANTE
        global SPEED_EMA200
        global FLAG_BEST_NBR_TAILLE_BG
        global custom_info
        global TAILLE_BG
        global TAILLE_BG_N1
        global TAILLE_BG_N2
        global TAILLE_BG_N3
        global TYPE_BG
        global TYPE_BG_N1
        global TYPE_BG_N2
        global TYPE_BG_N3
        global VAL_OPEN
        global VAL_CLOSE
        global VAL_OPEN_N1
        global VAL_CLOSE_N1
        global VAL_OPEN_N2
        global VAL_CLOSE_N2    
        global VAL_OPEN_N3
        global VAL_CLOSE_N3
        global DIFF_EMA200_CLOSE
        global DIFF_EMA200_EMA15
        global CUMUL_TAILLE_BG_ROUGE
        global CUMUL_TAILLE_BG_VERTE
        global CUMUL_TAILLE_BG_N1_N2
        global CUMUL_TAILLE_BG_N1_N2_N3
        

        global LAST_CROISEMENT_EMA1H_EMA1L_DESS_CROSS
        
        global FRONT_MONTANT_EMA15
        global FRONT_MONTANT_EMA1H
        global FRONT_MONTANT_EMA1L
        global FRONT_MONTANT_EMA200
        global FRONT_MONTANT_COURT_EMA15
        global FRONT_MONTANT_COURT_EMA1H
        global FRONT_MONTANT_COURT_EMA1L
        global FRONT_MONTANT_COURT_EMA200
        global FRONT_NEUTRE_COURT_EMA200
        global FRONT_NEUTRE_COURT_EMA15
        global FRONT_NEUTRE_COURT_EMA1L
        global FRONT_NEUTRE_EMA1L
        global TYPE_FRONT_EMA15
        global TYPE_FRONT_EMA1L
        global TYPE_FRONT_EMA1H
        global TYPE_FRONT_EMA200
        global TYPE_FRONT_COURT_EMA15
        global TYPE_FRONT_COURT_EMA1L
        global TYPE_FRONT_COURT_EMA1H
        global TYPE_FRONT_COURT_EMA200
        
        global VAL_EMA15_COURANT
        global VAL_EMA1L_COURANT
        global VAL_EMA1H_COURANT
        global VAL_EMA200_COURANT
        global DERNIER_POINT_VENTE
        global last_price
        global COULEUR_VOLUME
        global VOLUME_ASK
        global PRICE_ASK
        global VOLUME_BID
        global PRICE_BID
        global dataframe_date
                
        
        """
        if FLAG_BEST_NBR_TAILLE_BG == 1 :
           val_mask_idxmin=DETECT_MODE_REEL(dataframe,val_mask_idxmin)
        """
        last_index=len(dataframe)-1
        print("last_index=",last_index)
        """
        if val_mask_idxmin >= last_index :
            val_mask_idxmin=last_index  
        """
        """
        if val_mask_idxmin == last_index :
           val_mask_idxmin=val_mask_idxmin-1
        """
        #if FLAG_BEST_NBR_TAILLE_BG == 1 :
        #    val_mask_idxmin=last_index  


        EMA200=dataframe['EMA200'].loc[val_mask_idxmin].astype(int)    
        OPEN=dataframe['OPEN'].loc[val_mask_idxmin].astype(int)    
        CLOSE=dataframe['CLOSE'].loc[val_mask_idxmin].astype(int)
        VAL_EMA1H_COURANT=dataframe.EMA1H.loc[val_mask_idxmin].astype(int)
        VAL_EMA1H_COURANT_N1=dataframe.EMA1H.loc[val_mask_idxmin-1].astype(int)
        VAL_EMA1H_COURANT_N2=dataframe.EMA1H.loc[val_mask_idxmin-2].astype(int)
        DIFF_EMA1H_COURANT_N1=(VAL_EMA1H_COURANT - VAL_EMA1H_COURANT_N1 > 0)
        DIFF_EMA1H_N1_N2=(VAL_EMA1H_COURANT_N1 - VAL_EMA1H_COURANT_N2 <= 0)
        TEST_ACHAT_REBOND_EMA1H=(DIFF_EMA1H_COURANT_N1 == True) and  (DIFF_EMA1H_N1_N2 == True)
        DIFF_EMA1H_COURANT_N2=(VAL_EMA1H_COURANT - VAL_EMA1H_COURANT_N2 > 0)
        TEST_VENTE_SOMMET_EMA1H=(DIFF_EMA1H_COURANT_N2 == True) and ((TYPE_BG_N2 == "BG_VERTE") or (TYPE_BG_N1 == "BG_VERTE")) 

        #EMA1H=dataframe.EMA1H.loc[val_mask_idxmin]
        EMA1L=dataframe.EMA1L.loc[val_mask_idxmin].astype(int)
        EMA1H=dataframe.EMA1H.loc[val_mask_idxmin].astype(int)
        VAL_EMA15_COURANT=dataframe.EMA15.loc[val_mask_idxmin].astype(int)
        DATE_COURANT=dataframe_date.date.loc[val_mask_idxmin]
        DATE_COURANT=DATE_COURANT.strftime("%Y-%m-%d %H:%M:%S")  
        custom_info["HEURE_CROISEMENT_PAIR"]=dataframe.date.loc[last_index]
        print("DATE_COURANT",DATE_COURANT)
        print("EMA1L:",EMA1L)
        print("EMA1H:",VAL_EMA1H_COURANT)
        print("VAL_EMA200_COURANT:",VAL_EMA200_COURANT)
        print("EMA200:",EMA200)
        print("OPEN:",OPEN)
        print("CLOSE:",CLOSE)
        print("VAL_EMA15_COURANT:",VAL_EMA15_COURANT)
        print("VAL_EMA1H_COURANT_N2:",VAL_EMA1H_COURANT_N2)
        print("VAL_EMA1H_COURANT_N1:",VAL_EMA1H_COURANT_N1)
        print("VAL_EMA1H_COURANT:",VAL_EMA1H_COURANT)
        print("DIFF_EMA1H_N1_N2:",DIFF_EMA1H_N1_N2)
        print("DIFF_EMA1H_COURANT_N1:",DIFF_EMA1H_COURANT_N1)
        print("TEST_ACHAT_REBOND_EMA1H:",TEST_ACHAT_REBOND_EMA1H)
        print("DIFF_EMA1H_COURANT_N2:",DIFF_EMA1H_COURANT_N2)
        print("TEST_VENTE_SOMMET_EMA1H:",TEST_VENTE_SOMMET_EMA1H)
        print("FRONT_MONTANT_COURT_EMA1L:",FRONT_MONTANT_COURT_EMA1L)
        print("FRONT_MONTANT_COURT_EMA1H:",FRONT_MONTANT_COURT_EMA1H)
        print("FRONT_MONTANT_COURT_EMA15:",FRONT_MONTANT_COURT_EMA15)
        print("(FRONT_MONTANT_EMA15 == 0):",(FRONT_MONTANT_EMA15 == 0))
        print("FRONT_MONTANT_EMA15 :",FRONT_MONTANT_EMA15 )
        print("(EMA1L <= VAL_EMA15_COURANT): ",(EMA1L <= VAL_EMA15_COURANT))
        #print("(int(EMA1H) >= int(VAL_EMA15_COURANT)): ",(int(EMA1H) >= int(VAL_EMA15_COURANT)))
        print("(FRONT_MONTANT_COURT_EMA1L == 1): ",(FRONT_MONTANT_COURT_EMA1L == 1))
        print("(FRONT_MONTANT_COURT_EMA1H == 1): ",(FRONT_MONTANT_COURT_EMA1H == 1))
        
        print("TRAME_EMA200_EMA15_MOINS_1: \n",TRAME_EMA200_EMA15_MOINS_1)
        print("DIFF_EMA200_EMA15_MOINS_1:",DIFF_EMA200_EMA15_MOINS_1)
        print("TRAME_EMA200_EMA15: \n",TRAME_EMA200_EMA15)
        print("DIFF_EMA200_EMA15:",DIFF_EMA200_EMA15)
        print("\nVARIATION_EMA200_EMA15  :",VARIATION_EMA200_EMA15)
        print("dataframe:;\n",dataframe.tail())
        #exit()
        #if  int(DIFF_EMA200_EMA15_MOINS_1) < 0 :# and int(DIFF_EMA200_EMA15) >= 0:
        #if  int(DIFF_EMA200_EMA15_MOINS_1) == -1 :
        #if  int(DIFF_EMA200_EMA15_MOINS_1) < 0 :
            #exit()

       # if  int(DIFF_EMA200_EMA15_MOINS_1) < 0 and int(VARIATION_EMA200_EMA15) >= 0:

            
        """
        print("((EMA1L <= VAL_EMA15_COURANT) and  (int(VAL_EMA1H_COURANT) >= int(VAL_EMA15_COURANT))\
        and (FRONT_MONTANT_COURT_EMA1L == 1) and (FRONT_MONTANT_COURT_EMA1H == 0): ",(EMA1L <= VAL_EMA15_COURANT) and (int(VAL_EMA1H_COURANT) >= int(VAL_EMA15_COURANT)) \
        and (FRONT_MONTANT_COURT_EMA1L == 1) and (FRONT_MONTANT_COURT_EMA1H == 0) and  (TYPE_BG == "BG_ROUGE"))
        """    
        # 1er CAS ACHAT  EMA15 < EMA200  .EMA15 DESCENDANTE EMA1H < EMA15 et EMA1L < EMA15 ET DIFF_EMA200_CLOSE >= 50 ET EMA1H ET EMA15 SONT TOUTE MONTANTE and (LAST_ORDER == "SELL")
        #print("LAST_CROISEMENT_EMA200_GOLDEN_CROSS_EMA15: \n",LAST_CROISEMENT_EMA200_GOLDEN_CROSS_EMA15)
        print("DATE_COURANT",DATE_COURANT)
        print("DATE et EMA200 ORIGINE DANS TRAITEMENT REELLE=\n",dataframe[["date","EMA200"]].loc[val_mask_idxmin_ORG])
        print("last_index=",last_index)
        print("val_mask_idxmin:",val_mask_idxmin)
        print("TYPE_BG:",TYPE_BG)
        print("TYPE_BG_N1:",TYPE_BG_N1)
        print("TYPE_BG_N2:",TYPE_BG_N2)
        print("TYPE_BG_N3:",TYPE_BG_N3)
        print("TAILLE_BG=",TAILLE_BG)
        print("TAILLE_BG_N1=",TAILLE_BG_N1)
        print("TAILLE_BG_N2=",TAILLE_BG_N2)
        print("TAILLE_BG_N3=",TAILLE_BG_N3)
        print("CUMUL_TAILLE_BG_VERTE:",CUMUL_TAILLE_BG_VERTE)
        print("CUMUL_TAILLE_BG_ROUGE:",CUMUL_TAILLE_BG_ROUGE)
        print("CUMUL_TAILLE_BG_N1_N2_N3",CUMUL_TAILLE_BG_N1_N2_N3)
        print("TEST_ACHAT_REBOND_EMA1H:",TEST_ACHAT_REBOND_EMA1H)
        print("TEST_VENTE_SOMMET_EMA1H:",TEST_VENTE_SOMMET_EMA1H)
        print("FRONT_MONTANT_EMA200 :",FRONT_MONTANT_EMA200 )
        print("FRONT_MONTANT_EMA15 :",FRONT_MONTANT_EMA15 )
        print("FRONT_MONTANT_COURT_EMA15 :",FRONT_MONTANT_COURT_EMA15 )
        print("FRONT_MONTANT_EMA1L :",FRONT_MONTANT_EMA1L )
        print("FRONT_MONTANT_COURT_EMA1L :",FRONT_MONTANT_COURT_EMA1L )
        print("FRONT_MONTANT_EMA1H :",FRONT_MONTANT_EMA1H )
        print("FRONT_MONTANT_COURT_EMA1H :",FRONT_MONTANT_COURT_EMA1H )
        print(" (int(EMA1L) <= int(VAL_EMA15_COURANT)) :", (int(EMA1L) <= int(VAL_EMA15_COURANT))  )
        print(" (int(EMA1H) >= int(VAL_EMA15_COURANT)) :", (int(EMA1L) >= int(VAL_EMA15_COURANT))  )
        print("(VAL_EMA15_COURANT < VAL_EMA200_COURANT) :",(VAL_EMA15_COURANT < VAL_EMA200_COURANT) )
        print("EMA1H:",VAL_EMA1H_COURANT)
        print("SPEED_EMA1L:",SPEED_EMA1L)
        print("SPEED_EMA1H:",SPEED_EMA1H)
        print("OPEN=",OPEN)
        print("CLOSE=",CLOSE)
        print("DIFF_CLOSE_OPEN=",CLOSE-OPEN)
        print("VAL_OPEN_N1=",VAL_OPEN_N1)
        print("VAL_CLOSE_N1=",VAL_CLOSE_N1)
        print("DIFF_CLOSE_N1_OPEN_N1=",VAL_CLOSE_N1-VAL_OPEN_N1)
        print("VAL_OPEN_N2=",VAL_OPEN_N2)
        print("VAL_CLOSE_N2=",VAL_CLOSE_N2)
        print("DIFF_CLOSE_N2_OPEN_N2=",VAL_CLOSE_N2-VAL_OPEN_N2)
        print("VAL_OPEN_N3=",VAL_OPEN_N3)
        print("VAL_CLOSE_N3=",VAL_CLOSE_N3)
        print("DIFF_CLOSE_N3_OPEN_N3=",VAL_CLOSE_N3-VAL_OPEN_N3)
        print("OPEN_MOINS_1=",OPEN_MOINS_1)
        print("CLOSE_MOINS_1=",CLOSE_MOINS_1)
        print("(float(VAL_CLOSE) - float(VAL_CLOSE_N1) < 0) :",(float(VAL_CLOSE) - float(VAL_CLOSE_N1) < 0) ) 
        print("(float(VAL_CLOSE_N1) - float(VAL_CLOSE_N2) < 0) :",(float(VAL_CLOSE_N1) - float(VAL_CLOSE_N2) < 0) )
        print("SOMME_VOLUME_ASK:",VOLUME_ASK)
        print("SOMME_VOLUME_BID:",VOLUME_BID)
        print("PRICE_VOLUME_ASK:",PRICE_ASK)
        print("PRICE_VOLUME_BID:",PRICE_BID)
        #VAL_ACHAT=dataframe.close.loc[val_mask_idxmin]
        VAL_ACHAT=RECUP_LAST_PRICE_IN_FILE()
        
        #On quitte la fonction car pic de fin de TRAIDE
        if   (COULEUR_VOLUME == "ROUGE") and  (POINT_ENTRE_EMA200 == 0) \
             and ((FRONT_MONTANT_EMA15 == 0)  and int(EMA1H) < int(VAL_EMA15_COURANT)) or  ((FRONT_MONTANT_EMA1H == 0) and (FRONT_MONTANT_EMA1L == 0)) :
             print("PIC  DESCENDANT SOUS EMA15 ON N ACHETE PAS ")
             DERNIER_POINT_VENTE=1
             return
        
        """
        if (FRONT_MONTANT_EMA200 == 0 )    and (DERNIER_POINT_VENTE == 0) and ( ORDER != LAST_ORDER ) and (int(EMA1H) <= int(VAL_EMA15_COURANT)) \
        and ((TYPE_BG_N1 == "BG_ROUGE") and (TYPE_BG == "BG_VERTE") and ((CUMUL_TAILLE_BG_ROUGE <= -8) or (CUMUL_TAILLE_BG_VERTE >= 8))) :  
        # and ((VAL_EMA15_COURANT < VAL_EMA200_COURANT) and (TYPE_BG_N1 == "BG_ROUGE") and (TYPE_BG == "BG_VERTE") and ((CUMUL_TAILLE_BG_ROUGE <= -10) or (CUMUL_TAILLE_BG_VERTE >= 10))) :        
        #and ((VAL_EMA15_COURANT < VAL_EMA200_COURANT) and (TYPE_BG_N2 == "BG_ROUGE") and (TYPE_BG_N1 == "BG_ROUGE") and (TYPE_BG == "BG_ROUGE")) :
        # and ((VAL_EMA15_COURANT < VAL_EMA200_COURANT) and (TYPE_BG_N1 == "BG_ROUGE") and (SPEED_EMA1L == 0)) :        #and ((VAL_EMA15_COURANT < VAL_EMA200_COURANT) and (TYPE_BG_N2 == "BG_ROUGE") and (TYPE_BG_N1 == "BG_ROUGE") and (TYPE_BG == "BG_ROUGE")) :
            #and (SPEED_EMA15 >= 0) and (SPEED_EMA200 == 0)  and (FRONT_MONTANT_EMA15 == 1 ): 
             print("\n# 1er CAS ACHAT  EMA15 < EMA200 . EMA15 DESCENDANTE EMA1H < EMA15 et EMA1L < EMA15 ET DIFF_EMA200_CLOSE >= 50 ET EMA1H ET EMA15 SONT TOUTE MONTANTE ")
             print("EMA1H ET EMA1L AU DESSUS EMA15 FRONT MONTANT DANS ZONE ACHAT ULTIMATE_NINJA BIS")
             ORDER="BUY"
             custom_info["SCENARIO"]="1er CAS ACHAT"
             print(ORDER)
             #LAST_ORDER="BUY" and (VAL_EMA15_COURANT < VAL_EMA200_COURANT) and (abs(DIFF_EMA200_CLOSE) >= 50)
             EXEC_ORDER(dataframe)
             VAL_ACHAT=dataframe.close.loc[val_mask_idxmin]
             POINT_ENTRE_EMA200 = 1 #VEROUILAGE ACHAT ET VENTE NORMAL
             #exit()
        """
        #exit()
        #(TYPE_BG_N2 == "BG_ROUGE") and 
        """
        if (TYPE_BG_N1 == "BG_ROUGE") and (TYPE_BG == "BG_VERTE") and ((CUMUL_TAILLE_BG_ROUGE <= -8) or (CUMUL_TAILLE_BG_VERTE >= 8)) \
            and (int(EMA1H) <= int(VAL_EMA15_COURANT)):
            print("DANS TEST CUMUL_TAILLE_BG_ROUGE:",CUMUL_TAILLE_BG_ROUGE)
            exit()
        """
            
        # 2eme CAS ACHAT EN DESSOUS EMA200
        print("EMA1H:",VAL_EMA1H_COURANT)
        print("VAL_EMA200_COURANT:",VAL_EMA200_COURANT)
        # and (FRONT_MONTANT_COURT_EMA1H == 0) and (FRONT_MONTANT_COURT_EMA1L == 0) (VAL_EMA15_COURANT < VAL_EMA200_COURANT) and
        #and (FRONT_MONTANT_EMA200 == 0 )  and (POINT_ENTRE_EMA200 == 0)  and (DERNIER_POINT_VENTE == 0) and ( ORDER != LAST_ORDER ) \
        #if (FRONT_MONTANT_EMA15 == 0) and  (int(EMA1L) <= int(VAL_EMA15_COURANT))   \ and (SPEED_EMA1L == 0)  \ and (CUMUL_TAILLE_BG_ROUGE <= -30) \
        #and ( (TYPE_BG_N3 == "BG_ROUGE") and (TYPE_BG_N2 == "BG_ROUGE") and (TYPE_BG_N1 == "BG_ROUGE") and (TYPE_BG == "BG_VERTE")) :
        #and OPEN < EMA200 and (CUMUL_TAILLE_BG_N1_N2 <= -15)\
        #and (CUMUL_TAILLE_BG_N1_N2 <= -15) and (FRONT_MONTANT_COURT_EMA1L == 1)\

        if (int(EMA1L) <= int(VAL_EMA15_COURANT)) and ((FRONT_MONTANT_COURT_EMA15 == 1) or (FRONT_NEUTRE_EMA15 == 1))  and (TAILLE_BG <= 200) \
        and (VAL_EMA15_COURANT < VAL_EMA200_COURANT) and (CUMUL_TAILLE_BG_N1_N2_N3 <= -150) \
        and (FRONT_MONTANT_EMA200 >= 0 )  and (POINT_ENTRE_EMA200 == 0)  and (DERNIER_POINT_VENTE == 0) and ( ORDER != LAST_ORDER ) \
        and ( (TYPE_BG_N3 == "BG_ROUGE") and (TYPE_BG_N2 == "BG_ROUGE") and (TYPE_BG_N1 == "BG_ROUGE") and (TYPE_BG == "BG_VERTE")) :
             print("\n2eme CAS ACHAT INITIALE 3 BG_ROUGE et 1 BG_VERTE ET EMA15  EN DESSOUS EMA200")
             #print("EMA1H ET EMA1L AU DESSUS EMA15 FRONT MONTANT DANS ZONE ACHAT ULTIMATE_NINJA BIS")
             ORDER="BUY"
             custom_info["SCENARIO"]="2eme CAS ACHAT INITIALE GRAND CREUX \n3 BG_ROUGE et 1 BG_VERTE ET EMA15 EN DESSOUS EMA200 <= -150"
             print(ORDER)
             EXEC_ORDER(dataframe)
             #VAL_ACHAT=dataframe.close.loc[val_mask_idxmin]
             POINT_ENTRE_EMA200 = 1 #VEROUILAGE ACHAT ET VENTE NORMAL
             ###exit()
        """   
        # 2eme CAS ACHAT AU DESSUS EMA200     
        if (int(EMA1L) <= int(VAL_EMA15_COURANT)) and ((FRONT_MONTANT_COURT_EMA15 >= 0) or (FRONT_NEUTRE_EMA15 == 1))  and (TAILLE_BG <= 200) \
        and (FRONT_MONTANT_EMA200 >= 0 )  and (POINT_ENTRE_EMA200 == 0)  and (DERNIER_POINT_VENTE == 0) and ( ORDER != LAST_ORDER ) \
        and (VAL_EMA15_COURANT >= VAL_EMA200_COURANT) and (CUMUL_TAILLE_BG_N1_N2_N3 > -150) \
        and ( (TYPE_BG_N3 == "BG_ROUGE") and (TYPE_BG_N2 == "BG_ROUGE") and (TYPE_BG_N1 == "BG_ROUGE") and (TYPE_BG == "BG_VERTE")) :
             print("\n2eme CAS ACHAT INITIALE 3 BG_ROUGE et 1 BG_VERTE ET EMA15 AU DESSUS EMA200")
             #print("EMA1H ET EMA1L AU DESSUS EMA15 FRONT MONTANT DANS ZONE ACHAT ULTIMATE_NINJA BIS")
             ORDER="BUY"
             custom_info["SCENARIO"]="2eme CAS ACHAT INITIALE \n3 BG_ROUGE et 1 BG_VERTE ET EMA15 AU DESSUS EMA200 > -150"
             print(ORDER)
             EXEC_ORDER(dataframe)
             #VAL_ACHAT=dataframe.close.loc[val_mask_idxmin]
             POINT_ENTRE_EMA200 = 1 #VEROUILAGE ACHAT ET VENTE NORMAL
             ###exit()
        """

        """                            
        # 2eme CAS ACHAT  EMA15 < EMA200  .EMA15 DESCENDANTE EMA1H < EMA15 et EMA1L < EMA15 ET DIFF_EMA200_CLOSE >= 50 ET EMA1H ET EMA15 SONT TOUTE MONTANTE and (LAST_ORDER == "SELL")
        print("EMA1H:",VAL_EMA1H_COURANT)
        print("VAL_EMA200_COURANT:",VAL_EMA200_COURANT)
        if (int(EMA1L) <= int(VAL_EMA15_COURANT))   \
        and (FRONT_MONTANT_EMA200 >= 0 )  and (POINT_ENTRE_EMA200 == 10)  and (DERNIER_POINT_VENTE == 0) and ( ORDER != LAST_ORDER ) \
        and ( (TYPE_BG_N3 == "BG_ROUGE") and (TYPE_BG_N1 == "BG_ROUGE") and (TYPE_BG == "BG_ROUGE")) :
        # and ( (TYPE_BG_N3 == "BG_ROUGE") and (TYPE_BG_N2 == "BG_ROUGE") and (TYPE_BG_N1 == "BG_ROUGE") and (TYPE_BG == "BG_ROUGE")) :
             print("\n# 2eme CAS ACHAT INITIALE ")
             ORDER="BUY"
             custom_info["SCENARIO"]="2eme CAS ACHAT INITIALE"
             print(ORDER)
             EXEC_ORDER(dataframe)
             #VAL_ACHAT=dataframe.close.loc[val_mask_idxmin]
             POINT_ENTRE_EMA200 = 1 #VEROUILAGE ACHAT ET VENTE NORMAL
             ##exit()
        """   
        """   
        print("TEST_ACHAT_REBOND_EMA1H:",TEST_ACHAT_REBOND_EMA1H)
        # 3eme CAS REACHAT SUR REBOND PARTOUT
        if (TEST_ACHAT_REBOND_EMA1H == True) \
        and (FRONT_MONTANT_EMA1H == 1) and (FRONT_MONTANT_COURT_EMA1H == 1) \
        and  (POINT_ENTRE_EMA200 == 0)  and (DERNIER_POINT_VENTE == 0) and ( ORDER != LAST_ORDER ) :
        #and ((TYPE_BG_N2 == "BG_ROUGE") and (TYPE_BG_N1 == "BG_ROUGE") and (TYPE_BG == "BG_VERTE")) :
        #and ( (TYPE_BG_N3 == "BG_ROUGE") and (TYPE_BG_N2 == "BG_ROUGE") and (TYPE_BG_N1 == "BG_ROUGE") and (TYPE_BG == "BG_VERTE")) :
             print("\n3eme CAS REACHAT SUR REBOND TEST_ACHAT_REBOND_EMA1H")
             ORDER="BUY"
             custom_info["SCENARIO"]="3eme CAS REACHAT SUR REBOND TEST_ACHAT_REBOND_EMA1H"
             print(ORDER)
             EXEC_ORDER(dataframe)
             #VAL_ACHAT=dataframe.close.loc[val_mask_idxmin]
             POINT_ENTRE_EMA200 = 1 #VEROUILAGE ACHAT ET VENTE NORMAL
             ###exit()
        """   

        print("TEST_ACHAT_REBOND_EMA1H:",TEST_ACHAT_REBOND_EMA1H)
        # 3eme CAS REACHAT SUR REBOND PARTOUT
        if (FRONT_MONTANT_EMA1H == 1) and (FRONT_MONTANT_COURT_EMA1H == 1) \
        and  (POINT_ENTRE_EMA200 == 6660)  and (DERNIER_POINT_VENTE == 0) and ( ORDER != LAST_ORDER ) \
        and  (FRONT_MONTANT_EMA200 >= 0 ) and  (FRONT_MONTANT_EMA15 >= 0 ) \
        and ((TYPE_BG_N2 == "BG_ROUGE") and (TYPE_BG_N1 == "BG_ROUGE") and (TYPE_BG == "BG_VERTE")) :
             print("\n3eme CAS REACHAT SUR REBOND")
             ORDER="BUY"
             custom_info["SCENARIO"]="3eme CAS REACHAT SUR REBOND RRV"
             print(ORDER)
             EXEC_ORDER(dataframe)
             #VAL_ACHAT=dataframe.close.loc[val_mask_idxmin]
             POINT_ENTRE_EMA200 = 1 #VEROUILAGE ACHAT ET VENTE NORMAL
             ###exit()
          
            
            
         # 3eme CAS REACHAT DYNAMIQUE SUR REBOND PARTOUT
         # VAL_CLOSE_ORG=RECUP_LAST_PRICE_IN_FILE()
         # #time.sleep(3)
         # VAL_CLOSE=RECUP_LAST_PRICE_IN_FILE()
         # if VAL_CLOSE == "" :
         #     VAL_CLOSE=RECUP_LAST_PRICE_IN_FILE()           
         # #VAL_EMA1H_PRECEDENT_COURT=dataframe.EMA1H.loc[val_mask_idxmin-1].astype(int)
         # #VAL_EMA1H_PRECEDENT_COURT=dataframe.EMA1H.loc[val_mask_idxmin-1].astype(int)
         # VAL_CLOSE_ORG=dataframe.close.loc[val_mask_idxmin]
         # DIFF_CLOSE_VAL_CLOSE=int((float(VAL_CLOSE) - float(VAL_CLOSE_ORG))*MULTIP) >  0
         # print("\nVAL_CLOSE: {} VAL_CLOSE_ORG : {}".format(VAL_CLOSE,VAL_CLOSE_ORG))
         # print("float(VAL_CLOSE) - float(VAL_CLOSE_ORG) > 0 : {}".format(DIFF_CLOSE_VAL_CLOSE))  
        #global COULEUR_VOLUME
        if (FRONT_MONTANT_EMA1H == 1) and (FRONT_MONTANT_COURT_EMA1H == 1) \
         and  (POINT_ENTRE_EMA200 == 0)  and (DERNIER_POINT_VENTE == 0) and ( ORDER != LAST_ORDER ) \
         and  (FRONT_MONTANT_EMA200 >= 0 ) and  (FRONT_MONTANT_EMA15 >= 0 ) \
         and ((TYPE_BG_N2 == "BG_ROUGE") and (TYPE_BG_N1 == "BG_ROUGE") and (COULEUR_VOLUME  == "vert")) :
              print("\n3eme CAS REACHAT DYNAMIQUE SUR REBOND PARTOUT")
              ORDER="BUY"
              custom_info["SCENARIO"]="3eme CAS REACHAT DYNAMIQUE SUR REBOND PARTOUT"
              print(ORDER)
              EXEC_ORDER(dataframe)
              #VAL_ACHAT=dataframe.close.loc[val_mask_idxmin]
              POINT_ENTRE_EMA200 = 1 #VEROUILAGE ACHAT ET VENTE NORMAL
              ###exit()             
        """
         2eme CAS REACHAT SUR REBOND PARTOUT
        print("EMA1H:",VAL_EMA1H_COURANT)
        print("VAL_EMA200_COURANT:",VAL_EMA200_COURANT)
        # and (FRONT_MONTANT_COURT_EMA1H == 0) and (FRONT_MONTANT_COURT_EMA1L == 0) (VAL_EMA15_COURANT < VAL_EMA200_COURANT) and
        #and (FRONT_MONTANT_EMA200 == 0 )  and (POINT_ENTRE_EMA200 == 0)  and (DERNIER_POINT_VENTE == 0) and ( ORDER != LAST_ORDER ) \
        if (FRONT_MONTANT_EMA15 == 1) and  (int(EMA1L) >= int(VAL_EMA15_COURANT))   \
        and (OPEN > VAL_EMA15_COURANT) and  (CLOSE <= VAL_EMA15_COURANT) \
        and (FRONT_MONTANT_EMA200 >= 0 )  and (POINT_ENTRE_EMA200 == 0)  and (DERNIER_POINT_VENTE == 0) and ( ORDER != LAST_ORDER ) \
        and ((TYPE_BG_N2 == "BG_VERTE") and (TYPE_BG_N1 == "BG_ROUGE") and (TYPE_BG == "BG_ROUGE")) :
        #and ( (TYPE_BG_N3 == "BG_ROUGE") and (TYPE_BG_N2 == "BG_ROUGE") and (TYPE_BG_N1 == "BG_ROUGE") and (TYPE_BG == "BG_VERTE")) :
             print("\n2eme CAS REACHAT SUR REBOND")
             ORDER="BUY"
             custom_info["SCENARIO"]="2eme CAS REACHAT SUR REBOND"
             print(ORDER)
             EXEC_ORDER(dataframe)
             #VAL_ACHAT=dataframe.close.loc[val_mask_idxmin]
             POINT_ENTRE_EMA200 = 1 #VEROUILAGE ACHAT ET VENTE NORMAL
             ###exit()
        """
             
        """                            
        # 3er CAS ACHAT  EMA15 < EMA200  .EMA15 DESCENDANTE EMA1H < EMA15 et EMA1L < EMA15 ET DIFF_EMA200_CLOSE >= 50 ET EMA1H ET EMA15 SONT TOUTE MONTANTE and (LAST_ORDER == "SELL")
        print("EMA1H:",VAL_EMA1H_COURANT)
        print("VAL_EMA200_COURANT:",VAL_EMA200_COURANT)
        if (FRONT_MONTANT_EMA15 == 0) and  (int(EMA1L) <= int(VAL_EMA15_COURANT)) and (int(EMA1H) <= int(VAL_EMA15_COURANT))   \
        and (FRONT_MONTANT_EMA200 == 0 )  and (POINT_ENTRE_EMA200 == 10)  and (DERNIER_POINT_VENTE == 0) and ( ORDER != LAST_ORDER ) \
        and int(LAST_CROISEMENT_EMA1H_EMA1L_DESS_CROSS.DIFF_EMA1H_EMA1L.astype(int) >= 0)\
        and int(LAST_CROISEMENT_EMA1H_EMA1L_DESS_CROSS.DIFF_EMA1H_EMA1L.astype(int) <= 5) :
             print("\n# 3eme CAS ACHAT")
             #print("EMA1H ET EMA1L AU DESSUS EMA15 FRONT MONTANT DANS ZONE ACHAT ULTIMATE_NINJA BIS")
             ORDER="BUY"
             custom_info["SCENARIO"]="3eme CAS ACHAT"
             print(ORDER)
             EXEC_ORDER(dataframe)
             #VAL_ACHAT=dataframe.close.loc[val_mask_idxmin]
             POINT_ENTRE_EMA200 = 1 #VEROUILAGE ACHAT ET VENTE NORMAL
             #exit()    
        """                            
        
        # 4eme CAS ACHAT AU DESSUS EMA200     
        if (FRONT_MONTANT_EMA15 == 1) and (FRONT_MONTANT_EMA200 >= 0 ) and  (int(EMA1L) >= int(VAL_EMA15_COURANT))   \
        and (VAL_EMA15_COURANT >= VAL_EMA200_COURANT) and (VAL_OPEN_N1 < EMA200 and  VAL_CLOSE_N1 >= EMA200) \
        and (TYPE_BG_N1 == "BG_VERTE")  and (TYPE_BG == "BG_VERTE")\
        and (POINT_ENTRE_EMA200 == 0)  and (DERNIER_POINT_VENTE == 0) and ( ORDER != LAST_ORDER ) : 
             print("4eme CAS ACHAT AU DESSUS EMA200 BOUGIE VERTE TRAVERSANTE EMA200")
             ORDER="BUY"
             custom_info["SCENARIO"]="4eme CAS ACHAT AU DESSUS EMA200 BOUGIE VERTE TRAVERSANTE EMA200"
             print(ORDER)
             EXEC_ORDER(dataframe)
             #VAL_ACHAT=dataframe.close.loc[val_mask_idxmin]
             POINT_ENTRE_EMA200 = 1 #VEROUILAGE ACHAT ET VENTE NORMAL
             ##exit()   
            
        """     
        #5eme CAS REACHAT SUR REBOND PARTOUT     
        print("EMA1H:",VAL_EMA1H_COURANT)
        print("VAL_EMA200_COURANT:",VAL_EMA200_COURANT)
        # and (FRONT_MONTANT_COURT_EMA1H == 0) and (FRONT_MONTANT_COURT_EMA1L == 0) (VAL_EMA15_COURANT < VAL_EMA200_COURANT) and
        #and (FRONT_MONTANT_EMA200 == 0 )  and (POINT_ENTRE_EMA200 == 0)  and (DERNIER_POINT_VENTE == 0) and ( ORDER != LAST_ORDER ) \
        #if (FRONT_MONTANT_EMA15 == 0) and  (int(EMA1L) <= int(VAL_EMA15_COURANT))   \ and (SPEED_EMA1L == 0)  \ and (CUMUL_TAILLE_BG_ROUGE <= -30) \
        #and ( (TYPE_BG_N3 == "BG_ROUGE") and (TYPE_BG_N2 == "BG_ROUGE") and (TYPE_BG_N1 == "BG_ROUGE") and (TYPE_BG == "BG_VERTE")) :
        if (int(EMA1L) <= int(VAL_EMA15_COURANT))   \
        and (OPEN > VAL_EMA15_COURANT) and  (CLOSE <= VAL_EMA15_COURANT) \
        and ( (CUMUL_TAILLE_BG_N1_N2 <= -15) or (CUMUL_TAILLE_BG_N1_N2_N3 <= -15) )\
        and (FRONT_MONTANT_EMA200 >= 0 )  and (POINT_ENTRE_EMA200 == 0)  and (DERNIER_POINT_VENTE == 0) and ( ORDER != LAST_ORDER ) \
        and ( (TYPE_BG_N3 == "BG_VERTE") or (TYPE_BG_N2 == "BG_VERTE") )  and (TYPE_BG_N1 == "BG_ROUGE") and (TYPE_BG == "BG_ROUGE") :
            print("\n5eme CAS ACHAT INITIALE SUR REBOND EMA15")
            ORDER="BUY"
            custom_info["SCENARIO"]="5eme CAS ACHAT INITIALE SUR REBOND EMA15"
            print(ORDER)
            EXEC_ORDER(dataframe)
            #VAL_ACHAT=dataframe.close.loc[val_mask_idxmin]
            POINT_ENTRE_EMA200 = 1 #VEROUILAGE ACHAT ET VENTE NORMAL
            ###exit()     
        """
        #global last_price
        #VAL_CLOSE_DYNAMIQUE=RECUP_LAST_PRICE(symbol) 
        VAL_CLOSE_DYNAMIQUE=RECUP_LAST_PRICE_IN_FILE()
        EMA15=dataframe.EMA15.loc[val_mask_idxmin].astype(int)
        if VAL_CLOSE_DYNAMIQUE == "" :
            VAL_CLOSE_DYNAMIQUE=RECUP_LAST_PRICE_IN_FILE()
        #VAL_CLOSE_DYNAMIQUE=last_price
        VAL_CLOSE_DYNAMIQUE=(float(VAL_CLOSE_DYNAMIQUE)*MULTIP)
        #6eme CAS ACHAT EN DESSOUS EMA200  
        # and (VAL_EMA15_COURANT < VAL_EMA200_COURANT) and int(VAL_CLOSE_DYNAMIQUE) <= int(float(EMA15)*MULTIP)  \
        #and (FRONT_MONTANT_COURT_EMA1H == 1) and (TYPE_BG_N1 == "BG_VERTE")  and (COULEUR_VOLUME == "VERT")\
        # global COULEUR_VOLUME
        print("VAL_CLOSE_DYNAMIQUE:",VAL_CLOSE_DYNAMIQUE)
        if (FRONT_MONTANT_COURT_EMA15 == 1) and  (int(EMA1L) >= int(VAL_EMA15_COURANT))   \
        and (VAL_EMA15_COURANT < VAL_EMA200_COURANT)  \
        and (FRONT_MONTANT_COURT_EMA1H == 1) and(FRONT_MONTANT_COURT_EMA1L == 1)  and (COULEUR_VOLUME == "VERT")\
        and (POINT_ENTRE_EMA200 == 0)  and (DERNIER_POINT_VENTE == 0) and ( ORDER != LAST_ORDER ) : 
             print("6eme CAS ACHAT DYNAMIQUE ABSOLUE BOUGIE VERTE TRAVERSANTE FRONT MONTANT EMA15 EN DESSOUS EMA200 :",VAL_CLOSE_DYNAMIQUE)
             ORDER="BUY"
             custom_info["SCENARIO"]="6eme CAS ACHAT DYNAMIQUE ABSOLUE BOUGIE VERTE TRAVERSANTE FRONT MONTANT EMA15 EN DESSOUS EMA200 : "+ str(VAL_CLOSE_DYNAMIQUE)
             print(ORDER)
             EXEC_ORDER(dataframe)
             #VAL_ACHAT=dataframe.close.loc[val_mask_idxmin]
             POINT_ENTRE_EMA200 = 1 #VEROUILAGE ACHAT ET VENTE NORMAL
             #exit()                    

        # 6eme CAS ACHAT EN DESSOUS EMA200     
        if (FRONT_MONTANT_COURT_EMA15 == 1) and  (int(EMA1L) >= int(VAL_EMA15_COURANT))   \
        and (VAL_EMA15_COURANT < VAL_EMA200_COURANT) and (VAL_OPEN_N1 <= VAL_EMA15_COURANT and  VAL_CLOSE_N1 >= VAL_EMA15_COURANT) \
        and (FRONT_MONTANT_COURT_EMA1H == 1) and (TYPE_BG_N1 == "BG_VERTE")  and (TYPE_BG == "BG_VERTE")\
        and (POINT_ENTRE_EMA200 == 0)  and (DERNIER_POINT_VENTE == 0) and ( ORDER != LAST_ORDER ) : 
             print("6eme CAS ACHAT ABSOLUE BOUGIE VERTE TRAVERSANTE FRONT MONTANT EMA15 EN DESSOUS EMA200")
             ORDER="BUY"
             custom_info["SCENARIO"]="6eme CAS ACHAT ABSOLUE BOUGIE VERTE TRAVERSANTE FRONT MONTANT EMA15 EN DESSOUS EMA200"
             print(ORDER)
             EXEC_ORDER(dataframe)
             #VAL_ACHAT=dataframe.close.loc[val_mask_idxmin]
             POINT_ENTRE_EMA200 = 1 #VEROUILAGE ACHAT ET VENTE NORMAL
             #exit()            

        """
        if   (FRONT_MONTANT_COURT_EMA1L == 1 ) \
        and  (FRONT_MONTANT_EMA15 == 1) and (VAL_EMA15_COURANT <= VAL_EMA200_COURANT) \
        and OPEN <= VAL_EMA15_COURANT and  CLOSE >= VAL_EMA15_COURANT  \
        and ( (TYPE_BG_N2 == "BG_VERTE") or (TYPE_BG_N1 == "BG_VERTE") ) and (TYPE_BG == "BG_VERTE") \
        and (POINT_ENTRE_EMA200 == 0)  and (DERNIER_POINT_VENTE == 0) and ( ORDER != LAST_ORDER ) : 
        # and (TYPE_BG_N2 == "BG_VERTE") and (TYPE_BG_N1 == "BG_VERTE") and (TYPE_BG == "BG_VERTE") \
             print("6eme CAS ACHAT ABSOLUE BOUGIE VERTE TRAVERSANTE FRONT MONTANT EMA15 DANS ZONE VENTE ULTIMATE_NINJA")
             ORDER="BUY"
             custom_info["SCENARIO"]="6eme CAS ACHAT ABSOLUE BOUGIE VERTE TRAVERSANTE FRONT MONTANT EMA15"
             print(ORDER)
             EXEC_ORDER(dataframe)
             #VAL_ACHAT=dataframe.close.loc[val_mask_idxmin]
             POINT_ENTRE_EMA200 = 1 #VEROUILAGE ACHAT ET VENTE NORMAL
             #exit()        
        """

        # 7eme CAS ACHAT AU DESSUS EMA200 and (VAL_EMA15_COURANT >= VAL_EMA200_COURANT)
        if (FRONT_MONTANT_EMA15 == 1) and  (int(EMA1L) >= int(VAL_EMA15_COURANT))   \
        and ((VAL_CLOSE_N2 <= VAL_EMA15_COURANT) or (VAL_CLOSE_N1 <= VAL_EMA15_COURANT)) \
        and (FRONT_MONTANT_COURT_EMA1H == 1 )  \
        and (FRONT_MONTANT_EMA200 >= 0 )  and (POINT_ENTRE_EMA200 == 0)  and (DERNIER_POINT_VENTE == 0) and ( ORDER != LAST_ORDER ) \
        and ((TYPE_BG_N2 == "BG_ROUGE") and (TYPE_BG_N1 == "BG_ROUGE")) and (TYPE_BG == "BG_VERTE") :
             print("\n7eme CAS ACHAT EMA15 > EMA200")
             ORDER="BUY"
             custom_info["SCENARIO"]="7eme CAS ACHAT EMA15 AU DESSUS EMA200"
             print(ORDER)
             EXEC_ORDER(dataframe)
             #VAL_ACHAT=dataframe.close.loc[val_mask_idxmin]
             POINT_ENTRE_EMA200 = 1 #VEROUILAGE ACHAT ET VENTE NORMAL
             ###exit()
             
        # 8eme CAS ACHAT EN DESSOUS EMA200    
        if (FRONT_MONTANT_EMA15 == 0) and (FRONT_MONTANT_COURT_EMA15 == 0 ) and  (int(EMA1H) < int(VAL_EMA15_COURANT))   \
        and (FRONT_MONTANT_COURT_EMA1H == 1 ) and (VAL_EMA15_COURANT < VAL_EMA200_COURANT) \
        and  VAL_CLOSE_N3 < VAL_EMA15_COURANT and (CUMUL_TAILLE_BG_N1_N2_N3 <= -250) \
        and (FRONT_MONTANT_EMA200 >= 0 )  and (POINT_ENTRE_EMA200 == 80)  and (DERNIER_POINT_VENTE == 0) and ( ORDER != LAST_ORDER ) \
        and ( (TYPE_BG_N3 == "BG_ROUGE") and (TYPE_BG_N2 == "BG_ROUGE") and (TYPE_BG_N1 == "BG_ROUGE") and (TYPE_BG == "BG_VERTE")) :
             print("\n8eme CAS ACHAT EMA15 EN DESSOUS EMA200 RRRV")
             ORDER="BUY"
             custom_info["SCENARIO"]="8eme CAS ACHAT EMA15 EN DESSOUS EMA200 RRRV"
             print(ORDER)
             EXEC_ORDER(dataframe)
             #VAL_ACHAT=dataframe.close.loc[val_mask_idxmin]
             POINT_ENTRE_EMA200 = 1 #VEROUILAGE ACHAT ET VENTE NORMAL
             ###exit()


            
        # 9eme CAS VENTE ABSOLUE BOUGIE VERTE TRAVERSANTE FRONT MONTANT SUR EMA200    and (FRONT_MONTANT_EMA15 == 1 ) 
        #if (float(VAL_CLOSE) > float(VAL_ACHAT)) and (FRONT_MONTANT_COURT_EMA15 == 0 ) \
        global ACHAT_DYNAMIQUE
        #global last_price
        #VAL_CLOSE=RECUP_LAST_PRICE(symbol) 
        VAL_CLOSE_ORG=dataframe.close.loc[val_mask_idxmin]
        #while True:
        j=1
        while j < 2 :
          print("9eme CAS ACHAT DYNAMIQUE ABSOLUE BOUGIE VERTE CROISSANTE : ",j)
          #dataframe=RECUPERATION_DE_LA_DERNIERE_TRAME()
          #dataframe=populate_indicators(dataframe)
          VAL_CLOSE_ORG=RECUP_LAST_PRICE_IN_FILE()
          time.sleep(1)
          VAL_CLOSE=RECUP_LAST_PRICE_IN_FILE()
          #VAL_EMA1H_PRECEDENT_COURT=dataframe.EMA1H.loc[val_mask_idxmin-1].astype(int)
          if VAL_CLOSE_ORG == "" :
              VAL_CLOSE_ORG=RECUP_LAST_PRICE_IN_FILE()
          if VAL_CLOSE == "" :
              VAL_CLOSE=RECUP_LAST_PRICE_IN_FILE()            
          print("\nVAL_CLOSE: {} VAL_CLOSE_ORG : {}".format(VAL_CLOSE,VAL_CLOSE_ORG))
          DIFF_CLOSE_VAL_CLOSE=int((float(VAL_CLOSE) - float(VAL_CLOSE_ORG))*MULTIP)
          FRONT_MONTANT_COURT_EMA1H_=float(VAL_CLOSE) - float(VAL_EMA1H_PRECEDENT_COURT) > 0
          print("\nVAL_CLOSE: {} VAL_CLOSE_ORG : {}".format(VAL_CLOSE,VAL_CLOSE_ORG))
          print("\nVAL_CLOSE: {} VAL_EMA1H_PRECEDENT_COURT : {}".format(VAL_CLOSE,float(VAL_EMA1H_PRECEDENT_COURT)))
          print("float(VAL_CLOSE) - float(VAL_CLOSE_ORG) : {}".format(DIFF_CLOSE_VAL_CLOSE))
          print("(FRONT_MONTANT_COURT_EMA1H == 1): ",(FRONT_MONTANT_COURT_EMA1H == 1))
          print("(FRONT_MONTANT_COURT_EMA1L == 1): ",(FRONT_MONTANT_COURT_EMA1L == 1))
          print("(FRONT_NEUTRE_EMA1L == 1): ",(int(FRONT_NEUTRE_EMA1L) == 1))
          print("(FRONT_NEUTRE_COURT_EMA15 == 1): ",(int(FRONT_NEUTRE_COURT_EMA15) == 1))
          print("(FRONT_MONTANT_EMA15 == 1): ",(int(FRONT_MONTANT_EMA15) == 1))
          print("(FRONT_MONTANT_EMA200 == 1): ",(int(FRONT_MONTANT_EMA200) == 1))
          print("(FRONT_NEUTRE_COURT_EMA15 == 1): ",(int(FRONT_NEUTRE_COURT_EMA15) == 1))
          print("(FRONT_MONTANT_COURT_EMA200 == 1): ",(FRONT_MONTANT_COURT_EMA200 == 1))
          print("(FRONT_NEUTRE_COURT_EMA200 == 1): ",(int(FRONT_NEUTRE_COURT_EMA200) == 1))
          print("(TYPE_BG = ",TYPE_BG)
          #print("TEST_ACHAT_REBOND_EMA1H:",TEST_ACHAT_REBOND_EMA1H)
          #print("float(VAL_CLOSE) - float(VAL_ACHAT)  :",float(VAL_CLOSE) - float(VAL_ACHAT))   
          #if (float(VAL_CLOSE) - float(VAL_CLOSE_ORG) >= 1)  :
          #if (DIFF_CLOSE_VAL_CLOSE >= 1) and (FRONT_MONTANT_COURT_EMA1H_ >= 0) or (TEST_ACHAT_REBOND_EMA1H == True):
          """    
          if ((DIFF_CLOSE_VAL_CLOSE >= 1) and (FRONT_MONTANT_COURT_EMA1H== 1) and (FRONT_MONTANT_COURT_EMA1L== 1)) \
            and (FRONT_MONTANT_COURT_EMA200 >= 0) | ((DIFF_CLOSE_VAL_CLOSE > 0)  and (FRONT_MONTANT_COURT_EMA1H) == 1) and (FRONT_MONTANT_COURT_EMA15 == 1) \
              or  (FRONT_MONTANT_COURT_EMA1L == 1) or ((TEST_ACHAT_REBOND_EMA1H == True) and (FRONT_MONTANT_COURT_EMA15 == 1)) \
              and (FRONT_MONTANT_COURT_EMA200 >= 0) :
              #or (TEST_ACHAT_REBOND_EMA1H == True) : and (FRONT_MONTANT_COURT_EMA1L== 1)
          """    
          if (DIFF_CLOSE_VAL_CLOSE >= 1) and ((FRONT_MONTANT_COURT_EMA15 == 1) or (FRONT_NEUTRE_COURT_EMA15 == 1))  or (COULEUR_VOLUME == "ROUGE") \
              and (FRONT_MONTANT_COURT_EMA1H== 1)  \
              and  (int(EMA1L) > int(VAL_EMA15_COURANT)) and (int(EMA1H) > int(VAL_EMA15_COURANT)) \
              and int(float(VAL_CLOSE)) >= int(VAL_EMA15_COURANT) and (FRONT_MONTANT_COURT_EMA200 == 1 ) \
              or (TEST_ACHAT_REBOND_EMA1H == True) :
              ACHAT="OK"
              break
          else:
              ACHAT="KO"
              #break
          j+=1
          #time.sleep(1)
        #VAL_CLOSE_ORG=dataframe.close.loc[val_mask_idxmin]
        #if (float(VAL_CLOSE) - float(VAL_CLOSE_N1) > 0) or (float(VAL_CLOSE_N1) - float(VAL_CLOSE_N2) > 0)   \
        #if (float(VAL_CLOSE) - float(VAL_CLOSE_ORG) > 0) or (float(VAL_CLOSE_N1) - float(VAL_CLOSE_N2) > 0)  \
        #and (FRONT_MONTANT_COURT_EMA15 == 1 ) and  (FRONT_MONTANT_EMA15 == 1) and  (FRONT_MONTANT_EMA1H == 1) \
        #if (float(VAL_CLOSE) - float(VAL_CLOSE_ORG) > 0)  and (FRONT_MONTANT_COURT_EMA1H == 1 ) \ and (TYPE_BG == "BG_VERTE")
        #and (FRONT_MONTANT_EMA15  == 1 ) and ((FRONT_NEUTRE_COURT_EMA200 == 1) or (FRONT_MONTANT_COURT_EMA200 == 1 ))\
        if  ACHAT=="OK"  \
        and (POINT_ENTRE_EMA200 == 0)  and (DERNIER_POINT_VENTE == 0)  and (ACHAT_DYNAMIQUE==0) and ( ORDER != LAST_ORDER ) : 
              print("9eme CAS ACHAT DYNAMIQUE ABSOLUE BOUGIE VERTE CROISSANTE")
              ORDER="BUY"
              custom_info["SCENARIO"]="9eme CAS ACHAT DYNAMIQUE ABSOLUE BOUGIE VERTE CROISSANTE"
              print(ORDER)
              EXEC_ORDER(dataframe)
              #VAL_ACHAT=dataframe.close.loc[val_mask_idxmin]
              POINT_ENTRE_EMA200 = 1 #VEROUILAGE ACHAT ET VENTE NORMAL
              ACHAT_DYNAMIQUE=1
              #time.sleep(20)
              #DERNIER_POINT_VENTE=1
              #exit()      
          
            #######################
        
        if (COULEUR_VOLUME == "ROUGE")  \
        and (FRONT_MONTANT_COURT_EMA15 == 1 ) and  (FRONT_MONTANT_COURT_EMA1H == 1 )\
        and (POINT_ENTRE_EMA200 == 1)  and (DERNIER_POINT_VENTE == 0) and ( ORDER != LAST_ORDER ) : 
             print("9eme NEW CAS ACHAT ABSOLUE BOUGIE VERTE CROISSANTE")
             ORDER="BUY"
             custom_info["SCENARIO"]="9eme CAS ACHAT ABSOLUE BOUGIE VERTE CROISSANTE"
             print(ORDER)
             EXEC_ORDER(dataframe)
             #VAL_ACHAT=dataframe.close.loc[val_mask_idxmin]
             POINT_ENTRE_EMA200 = 1 #VEROUILAGE ACHAT ET VENTE NORMAL
             #DERNIER_POINT_VENTE=1
             time.sleep(1)
             #exit()                      

        if (float(VAL_CLOSE) - float(VAL_CLOSE_N1) > 0) or (float(VAL_CLOSE_N1) - float(VAL_CLOSE_N2) > 0)   \
        and (FRONT_MONTANT_COURT_EMA15 == 1 ) and  (FRONT_MONTANT_COURT_EMA1H == 1 ) and (COULEUR_VOLUME == "VERT") \
        and (POINT_ENTRE_EMA200 == 1888)  and (DERNIER_POINT_VENTE == 0) and ( ORDER != LAST_ORDER ) : 
             print("9eme CAS ACHAT ABSOLUE BOUGIE VERTE CROISSANTE")
             ORDER="BUY"
             custom_info["SCENARIO"]="9eme CAS ACHAT ABSOLUE BOUGIE VERTE CROISSANTE"
             print(ORDER)
             EXEC_ORDER(dataframe)
             #VAL_ACHAT=dataframe.close.loc[val_mask_idxmin]
             POINT_ENTRE_EMA200 = 1 #VEROUILAGE ACHAT ET VENTE NORMAL
             #DERNIER_POINT_VENTE=1
             time.sleep(1)
             #exit()         
             

        ###### CAS VENTES ############################ 
        global VAL_VENTE
        VAL_VENTE=RECUP_LAST_PRICE_IN_FILE()

        # 1er CAS VENTE  AU DESSUS EMA200
        print("EMA1H:",VAL_EMA1H_COURANT)
        print("VAL_EMA200_COURANT:",VAL_EMA200_COURANT)
        if (FRONT_MONTANT_EMA15 == 1)  and  (int(EMA1L) > int(VAL_EMA15_COURANT)) and (int(EMA1H) > int(VAL_EMA15_COURANT)) and (EMA1L > VAL_EMA200_COURANT)  \
        and (VAL_EMA15_COURANT > VAL_EMA200_COURANT) and (FRONT_MONTANT_EMA200 == 1 ) and (float(VAL_CLOSE) > float(VAL_ACHAT)) \
        and (FRONT_MONTANT_EMA1H == 1) and (FRONT_MONTANT_EMA1L == 1)  and (TAILLE_BG > 2) \
        and (POINT_ENTRE_EMA200 == 10)  and (DERNIER_POINT_VENTE == 0) and ( ORDER != LAST_ORDER ) : 
            #and (SPEED_EMA15 >= 0) and (SPEED_EMA200 == 0)  and (FRONT_MONTANT_EMA15 == 1 ): #and (TYPE_BG_N1 == "BG_VERTE") \ and (FRONT_MONTANT_COURT_EMA1H == 1) or (SPEED_EMA1H >= 1) and ((SPEED_EMA1H == 0) ) 
            # and (TYPE_BG_N2 == "BG_VERTE") and (TYPE_BG_N1 == "BG_VERTE") and (TYPE_BG == "BG_VERTE")
            #and  (FRONT_MONTANT_COURT_EMA1L == 1 ) and  (FRONT_MONTANT_COURT_EMA1H == 1 ) \ and (TAILLE_BG >=20 )
             print("\n# 1er cas VENTE  EMA15 < EMA200 . EMA15 DESCENDANTE EMA1H < EMA15 et EMA1L < EMA15 ET DIFF_EMA200_CLOSE >= 50 ET EMA1H ET EMA15 SONT TOUTE MONTANTE ")
             print("EMA1H ET EMA1L AU DESSUS EMA15 FRONT MONTANT DANS ZONE VENTE ULTIMATE_NINJA BIS")
             ORDER="SELL"
             custom_info["SCENARIO"]="1er CAS VENTE AU DESSUS EMA200"
             print(ORDER)
             #LAST_ORDER="BUY"
             EXEC_ORDER(dataframe)
             VAL_ACHAT=dataframe.close.loc[val_mask_idxmin]
             #VAL_ACHAT=dataframe.close.loc[val_mask_idxmin]
             VAL_VENTE=RECUP_LAST_PRICE_IN_FILE()
             POINT_ENTRE_EMA200 = 0 #VEROUILAGE ACHAT ET VENTE NORMAL
             ###exit()
             
        # 2eme CAS VENTE AU DESSUS EMA200
        print("EMA1H:",VAL_EMA1H_COURANT)
        print("VAL_EMA200_COURANT:",VAL_EMA200_COURANT)
        if  (VAL_EMA15_COURANT > VAL_EMA200_COURANT) and (float(VAL_CLOSE) > float(VAL_ACHAT)) \
        and (int(EMA1H) > int(VAL_EMA15_COURANT)) \
        and (TYPE_BG_N3 == "BG_VERTE") and (TYPE_BG_N1 == "BG_VERTE") and (TYPE_BG == "BG_VERTE") and (TAILLE_BG > 100 ) and (CUMUL_TAILLE_BG_VERTE >= 180)  \
        and (POINT_ENTRE_EMA200 == 1)  and (DERNIER_POINT_VENTE == 0) and ( ORDER != LAST_ORDER ) : # and (SPEED_EMA1H == 0) : 
            #and (SPEED_EMA15 >= 0) and (SPEED_EMA200 == 0)  and (FRONT_MONTANT_EMA15 == 1 ): #and (TYPE_BG_N1 == "BG_VERTE") \ and (FRONT_MONTANT_COURT_EMA1H == 1) or (SPEED_EMA1H >= 1) and ((SPEED_EMA1H == 0) ) 
            # and (TYPE_BG_N2 == "BG_VERTE") and (TYPE_BG_N1 == "BG_VERTE") and (TYPE_BG == "BG_VERTE")
            #and  (FRONT_MONTANT_COURT_EMA1L == 1 ) and  (FRONT_MONTANT_COURT_EMA1H == 1 ) \ and (TAILLE_BG >=20 )
             print("\n# 2eme cas VENTE  EMA15 < EMA200 . EMA15 DESCENDANTE EMA1H < EMA15 et EMA1L < EMA15 ET DIFF_EMA200_CLOSE >= 50 ET EMA1H ET EMA15 SONT TOUTE MONTANTE ")
             print("EMA1H ET EMA1L AU DESSUS EMA15 FRONT MONTANT DANS ZONE VENTE ULTIMATE_NINJA BIS")
             ORDER="SELL"
             custom_info["SCENARIO"]="2eme CAS VENTE AU DESSUS EMA200"
             print(ORDER)
             #LAST_ORDER="BUY"
             EXEC_ORDER(dataframe)
             #VAL_ACHAT=dataframe.close.loc[val_mask_idxmin]
             POINT_ENTRE_EMA200 = 0 #VEROUILAGE ACHAT ET VENTE NORMAL
             #exit()         
         
        #"""   
        # 3eme CAS VENTE PARTOUT
        print("EMA1H:",VAL_EMA1H_COURANT)
        print("VAL_EMA200_COURANT:",VAL_EMA200_COURANT)
        #if (FRONT_MONTANT_EMA15 == 1)  and  (int(EMA1L) > int(VAL_EMA15_COURANT)) and (int(EMA1H) > int(VAL_EMA15_COURANT)) \
        #and (VAL_EMA15_COURANT > VAL_EMA200_COURANT) and (FRONT_MONTANT_EMA200 == 1 ) and (float(VAL_CLOSE) > float(VAL_ACHAT)) \
        #and (TYPE_BG_N1 == "BG_VERTE") and (TYPE_BG == "BG_VERTE") and (CUMUL_TAILLE_BG_N1_N2_N3 >= 15) \
        #and (TYPE_BG_N1 == "BG_VERTE") and (TYPE_BG == "BG_VERTE") and (CUMUL_TAILLE_BG_VERTE >= 15) \and (CUMUL_TAILLE_BG_N1_N2_N3 >= 18)  and (TAILLE_BG <= -10) 
        #(int(EMA1H) > int(VAL_EMA15_COURANT)) \
        #and (TYPE_BG_N2 == "BG_VERTE") and (TYPE_BG_N1 == "BG_VERTE") and (TYPE_BG == "BG_ROUGE") \
        if (float(VAL_CLOSE) > float(VAL_ACHAT)) \
        and ((TYPE_BG_N2 == "BG_VERTE") or (TYPE_BG_N1 == "BG_VERTE")) and (COULEUR_VOLUME == "BG_ROUGE") \
        and (POINT_ENTRE_EMA200 == 1)  and (DERNIER_POINT_VENTE == 0) and ( ORDER != LAST_ORDER ) : 
            #and (SPEED_EMA15 >= 0) and (SPEED_EMA200 == 0)  and (FRONT_MONTANT_EMA15 == 1 ): #and (TYPE_BG_N1 == "BG_VERTE") \ and (FRONT_MONTANT_COURT_EMA1H == 1) or (SPEED_EMA1H >= 1) and ((SPEED_EMA1H == 0) ) 
            # and (TYPE_BG_N2 == "BG_VERTE") and (TYPE_BG_N1 == "BG_VERTE") and (TYPE_BG == "BG_VERTE")
            #and  (FRONT_MONTANT_COURT_EMA1L == 1 ) and  (FRONT_MONTANT_COURT_EMA1H == 1 ) \ and (TAILLE_BG >=20 )
             print('\n# 3eme cas VENTE and (TYPE_BG_N2 == "BG_VERTE") and (TYPE_BG_N1 == "BG_VERTE") and (TYPE_BG == "BG_ROUGE") ')
             print("EMA1H ET EMA1L AU DESSUS EMA15 FRONT MONTANT DANS ZONE VENTE ULTIMATE_NINJA BIS")
             ORDER="SELL"
             custom_info["SCENARIO"]='3eme CAS VENTE PARTOUT \ (TYPE_BG_N2 == "BG_VERTE") and (TYPE_BG_N1 == "BG_VERTE") and (TYPE_BG == "BG_ROUGE") '
             print(ORDER)
             #LAST_ORDER="BUY"
             EXEC_ORDER(dataframe)
             #VAL_ACHAT=dataframe.close.loc[val_mask_idxmin]
             POINT_ENTRE_EMA200 = 0 #VEROUILAGE ACHAT ET VENTE NORMAL
            #### exit()   
       # """
        
        """
        print("TEST_VENTE_SOMMET_EMA1H:",TEST_VENTE_SOMMET_EMA1H)
        # 3eme CAS VENTE PARTOUT
        if (int(EMA1H) > int(VAL_EMA15_COURANT)) \
        and (float(VAL_CLOSE) > float(VAL_ACHAT)) \
        and (TEST_VENTE_SOMMET_EMA1H == True) \
        and (POINT_ENTRE_EMA200 == 1)  and (DERNIER_POINT_VENTE == 0) and ( ORDER != LAST_ORDER ) : 
             print('\n# 3eme cas VENTE and (TYPE_BG_N2 == "BG_VERTE") and (TYPE_BG_N1 == "BG_VERTE") and (TYPE_BG == "BG_ROUGE") ')
             print("EMA1H ET EMA1L AU DESSUS EMA15 FRONT MONTANT DANS ZONE VENTE ULTIMATE_NINJA BIS")
             ORDER="SELL"
             custom_info["SCENARIO"]='3eme CAS VENTE PARTOUT VVVROUGE '
             print(ORDER)
             #LAST_ORDER="BUY"
             EXEC_ORDER(dataframe)
             #VAL_ACHAT=dataframe.close.loc[val_mask_idxmin]
             POINT_ENTRE_EMA200 = 0 #VEROUILAGE ACHAT ET VENTE NORMAL
            #### exit()   
        """
        """

        print("TEST_VENTE_SOMMET_EMA1H:",TEST_VENTE_SOMMET_EMA1H)
        # 3eme CAS VENTE PARTOUT
        if (int(EMA1H) > int(VAL_EMA15_COURANT)) \
        and (VAL_EMA15_COURANT > VAL_EMA200_COURANT) and (int(EMA1H) >= int(VAL_EMA15_COURANT)) \
        and (float(VAL_CLOSE) > float(VAL_ACHAT)) \
        and (TEST_VENTE_SOMMET_EMA1H == True) \
        and (POINT_ENTRE_EMA200 == 1)  and (DERNIER_POINT_VENTE == 0) and ( ORDER != LAST_ORDER ) : 
             print('\n# 3eme cas VENTE and (TYPE_BG_N2 == "BG_VERTE") and (TYPE_BG_N1 == "BG_VERTE") and (TYPE_BG == "BG_ROUGE") ')
             print("EMA1H ET EMA1L AU DESSUS EMA15 FRONT MONTANT DANS ZONE VENTE ULTIMATE_NINJA BIS")
             ORDER="SELL"
             custom_info["SCENARIO"]='3eme CAS VENTE PARTOUT VVVROUGE '
             print(ORDER)
             #LAST_ORDER="BUY"
             EXEC_ORDER(dataframe)
             #VAL_ACHAT=dataframe.close.loc[val_mask_idxmin]
             POINT_ENTRE_EMA200 = 0 #VEROUILAGE ACHAT ET VENTE NORMAL
            #### exit()                
            """
 
             
        # 4eme CAS VENTE PARTOUT    
        #if (float(VAL_CLOSE) > float(VAL_ACHAT)) \
        if  OPEN >= VAL_EMA15_COURANT and  CLOSE <= VAL_EMA15_COURANT and (TYPE_BG == "BG_ROUGE") and (FRONT_MONTANT_EMA15 == 0 ) \
        and (FRONT_MONTANT_EMA200 == 0 ) \
        and (POINT_ENTRE_EMA200 == 1)  and (DERNIER_POINT_VENTE == 0) and ( ORDER != LAST_ORDER ) : 
            # and (SPEED_EMA1H == 0) :         
            #and OPEN >= VAL_EMA15_COURANT and  CLOSE <= VAL_EMA15_COURANT and (TYPE_BG == "BG_ROUGE") \
            #and (SPEED_EMA15 >= 0) and (SPEED_EMA200 == 0)  and (FRONT_MONTANT_EMA15 == 1 ): #and (TYPE_BG_N1 == "BG_VERTE") \ and (FRONT_MONTANT_COURT_EMA1H == 1) or (SPEED_EMA1H >= 1) and ((SPEED_EMA1H == 0) ) 
            # and (TYPE_BG_N2 == "BG_VERTE") and (TYPE_BG_N1 == "BG_VERTE") and (TYPE_BG == "BG_VERTE")
            #and  (FRONT_MONTANT_COURT_EMA1L == 1 ) and  (FRONT_MONTANT_COURT_EMA1H == 1 ) \ and (TAILLE_BG >=20 )
             print("4eme CAS VENTE ABSOLUE BOUGIE ROUGE TRAVERSANTE EMA15 DANS ZONE VENTE ULTIMATE_NINJA BIS")
             ORDER="SELL"
             custom_info["SCENARIO"]="4eme CAS VENTE ABSOLUE  BG_ROUGE PARTOUT"
             print(ORDER)
             #LAST_ORDER="BUY"
             EXEC_ORDER(dataframe)
             #VAL_ACHAT=dataframe.close.loc[val_mask_idxmin]
             POINT_ENTRE_EMA200 = 0 #VEROUILAGE ACHAT ET VENTE NORMAL
             DERNIER_POINT_VENTE=1
             #exit()  
             
        # 5eme CAS VENTE AU PARTOUT
        if  (int(custom_info["ACHAT_AU_DESSUS_EMA15"]) == 1) and (int(custom_info["ACHAT_EN_DESSOUS_EMA200"]) == 0) \
        and (FRONT_MONTANT_EMA1H == 0) and (FRONT_MONTANT_COURT_EMA1H == 0) \
        and  CLOSE <= VAL_EMA15_COURANT and (TYPE_BG == "BG_ROUGE") and (FRONT_MONTANT_COURT_EMA15 == 0 ) \
            and (POINT_ENTRE_EMA200 == 1)  and (DERNIER_POINT_VENTE == 0) and ( ORDER != LAST_ORDER ) : 
             print("5eme CAS FIN CYCLE  VENTE ABSOLUE BOUGIE ROUGE SOUS EMA15 ")
             ORDER="SELL"
             custom_info["SCENARIO"]="5eme CAS FIN CYCLE  VENTE ABSOLUE BOUGIE ROUGE SOUS EMA15"
             print(ORDER)
             #LAST_ORDER="BUY"
             EXEC_ORDER(dataframe)
             #VAL_ACHAT=dataframe.close.loc[val_mask_idxmin]
             POINT_ENTRE_EMA200 = 0 #VEROUILAGE ACHAT ET VENTE NORMAL
             DERNIER_POINT_VENTE=1
             #exit()         
            
        # 6eme CAS VENTE AU PARTOUT
        if (float(VAL_CLOSE) > float(VAL_ACHAT)) \
        and (TAILLE_BG >=300 ) and (TYPE_BG == "BG_VERTE") \
        and (POINT_ENTRE_EMA200 == 1)  and (DERNIER_POINT_VENTE == 0) and ( ORDER != LAST_ORDER ) : # and (SPEED_EMA1H == 0) : 
            #and (SPEED_EMA15 >= 0) and (SPEED_EMA200 == 0)  and (FRONT_MONTANT_EMA15 == 1 ): #and (TYPE_BG_N1 == "BG_VERTE") \ and (FRONT_MONTANT_COURT_EMA1H == 1) or (SPEED_EMA1H >= 1) and ((SPEED_EMA1H == 0) ) 
            # and (TYPE_BG_N2 == "BG_VERTE") and (TYPE_BG_N1 == "BG_VERTE") and (TYPE_BG == "BG_VERTE")
            #and  (FRONT_MONTANT_COURT_EMA1L == 1 ) and  (FRONT_MONTANT_COURT_EMA1H == 1 ) \ and (TAILLE_BG >=20 )
             print("DANS ZONE VENTE ULTIMATE_NINJA BIS 6eme CAS VENTE ABSOLUE PARTOUT BOUGIE VERTE INFINI TAILLE: ",TAILLE_BG)
             ORDER="SELL"
             custom_info["SCENARIO"]="6eme CAS VENTE ABSOLUE PARTOUT BOUGIE VERTE INFINI TAILLE: " + str(TAILLE_BG)
             print(ORDER)
             EXEC_ORDER(dataframe)
             #VAL_ACHAT=dataframe.close.loc[val_mask_idxmin]
             POINT_ENTRE_EMA200 = 0 #VEROUILAGE ACHAT ET VENTE NORMAL
             #exit()  
             
        # 7eme CAS VENTE ABSOLUE BOUGIE VERTE TRAVERSANTE FRONT MONTANT SUR EMA200            
        if (float(VAL_CLOSE) > float(VAL_ACHAT)) and (FRONT_MONTANT_COURT_EMA15 == 0 ) \
        and (int(custom_info["ACHAT_EN_DESSOUS_EMA200"]) == 1) \
        and OPEN <= EMA200 and  CLOSE >= EMA200 and (TYPE_BG_N1 == "BG_VERTE") and (TYPE_BG == "BG_VERTE") \
        and (POINT_ENTRE_EMA200 == 1)  and (DERNIER_POINT_VENTE == 0) and ( ORDER != LAST_ORDER ) : 
             print("7eme CAS VENTE ABSOLUE BOUGIE VERTE TRAVERSANTE FRONT MONTANT SUR EMA200")
             ORDER="SELL"
             custom_info["SCENARIO"]="7eme CAS VENTE ABSOLUE BOUGIE VERTE TRAVERSANTE FRONT MONTANT SUR EMA200"
             print(ORDER)
             EXEC_ORDER(dataframe)
             #VAL_ACHAT=dataframe.close.loc[val_mask_idxmin]
             POINT_ENTRE_EMA200 = 0 #VEROUILAGE ACHAT ET VENTE NORMAL
             #DERNIER_POINT_VENTE=1
             #exit()         
             
        #"""
        # 8eme CAS VENTE ABSOLUE BOUGIE VERTE TRAVERSANTE FRONT MONTANT SUR EMA200    and (FRONT_MONTANT_EMA15 == 1 ) and (FRONT_MONTANT_COURT_EMA15 <= 0 ) 
        #and (float(VAL_CLOSE) - float(VAL_CLOSE_N1) < 0) or (float(VAL_CLOSE_N1) - float(VAL_CLOSE_N2) < 0)   \
        if (float(VAL_CLOSE) > float(VAL_ACHAT)) \
        and ((float(VAL_CLOSE_N1) - float(VAL_CLOSE_N2) < 0) or (float(VAL_CLOSE) - float(VAL_CLOSE_N1) < 0))\
        and  ((FRONT_MONTANT_COURT_EMA1H == 1 ) or (FRONT_NEUTRE_EMA1H == 1 )) \
        and (POINT_ENTRE_EMA200 == 1888)  and (DERNIER_POINT_VENTE == 0) and ( ORDER != LAST_ORDER ) : 
             print("8eme CAS VENTE ABSOLUE BOUGIE VERTE DECROISSANTE")
             ORDER="SELL"
             custom_info["SCENARIO"]="8eme CAS VENTE ABSOLUE BOUGIE VERTE DECROISSANTE"
             print(ORDER)
             EXEC_ORDER(dataframe)
             #VAL_ACHAT=dataframe.close.loc[val_mask_idxmin]
             POINT_ENTRE_EMA200 = 0 #VEROUILAGE ACHAT ET VENTE NORMAL
             #DERNIER_POINT_VENTE=1
             #exit()         
       # """
             
        """CUMUL_TAILLE_BG_VERTE
        if  (FRONT_MONTANT_EMA1L == 1 ) and (FRONT_MONTANT_COURT_EMA1L == 1 ) and (FRONT_MONTANT_EMA1H == 1 ) and (FRONT_MONTANT_COURT_EMA1H == 1 )   \
            and (EMA1L >= VAL_EMA15_COURANT) and ( ORDER != LAST_ORDER ) and (POINT_ENTRE_EMA200 == 1) and (float(VAL_CLOSE) > float(VAL_ACHAT)) \
            and (VAL_EMA15_COURANT > VAL_EMA200_COURANT) and (SPEED_EMA1H == 0)  and (abs(DIFF_EMA200_EMA15) <= 20) and (TYPE_BG == "BG_VERTE")  and (TAILLE_BG >= 20 ) :
            # and (TYPE_BG_N2 == "BG_VERTE") (custom_info["ACHAT_EN_DESSOUS_EMA200"] == 0) and
            #print("POINT DE VENTE SOMMET EMA1H SUR ACCELERATION SPEED_EMA200 EMA1H == 0 : CONDITION VENTE \nDATE_COURANTE_VENTE: ",DATE_COURANTE_VENTE)
            print("\n# 3eme cas VENTE EMA1H DANS ZONE DE VENTE ULTIMATE_NINJA BIS :nd (SPEED_EMA1H == 0)  and (abs(DIFF_EMA200_EMA15) <= 30) and (TYPE_BG == BG_VERTE)  and (TAILLE_BG >= 20 )")
            #custom_info["HEURE_CROISEMENT_PAIR"]=DATE_COURANTE_VENTE
            ORDER="SELL"
            #LAST_ORDER="SELL"
            print(ORDER)
            EXEC_ORDER(dataframe)    
            POINT_ENTRE_EMA200 = 0 #DEVEROUILAGE ACHAT ET VENTE NORMAL  \ #and (VAL_EMA15_COURANT - VAL_EMA200_COURANT >= int(item) for item in LISTE_EMA15_EMA200) \
            FIRST_VENTE+=1
            #exit()         
        """
        print("SORTIE DANS ZONE ULTIMATE_NINJA BIS\n")
            
             
def TRAITEMENT_ACHAT(dataframe,val_mask_idxmin) :
        """
        if  (int (VAL_EMA1H_COURANT - VAL_EMA200_COURANT) > 0)  and (VAL_EMA1H_COURANT - VAL_EMA15_COURANT <= 38 )  and (POINT_ENTRE_EMA200 == 0 ) and (VAL_CLOSE >= VAL_EMA15_COURANT ) \
        and (int (VAL_EMA15_COURANT - VAL_EMA200_COURANT > 10)) and (VAL_EMA15_COURANT-VAL_EMA15_PRECEDENT > 0 ) and (VAL_EMA15_MAX - VAL_EMA15_COURANT >= 0) and (TYPE_EMA15 == "HAUT") \
        or (VAL_EMA1H_COURANT - VAL_EMA15_COURANT <= 5 ) and (int(VAL_EMA1H_COURANT) - int(VAL_EMA15_COURANT) > -5) and (VAL_EMA15_COURANT-VAL_EMA15_PRECEDENT > 0 ) \
        and (POINT_ENTRE_EMA200 == 0 ) and (int(VAL_EMA1H_COURANT) - int(VAL_EMA15_COURANT) > -5) and (VAL_EMA15_MAX - VAL_EMA15_COURANT >= 0) and (TYPE_EMA15 == "HAUT") \
        or (VAL_EMA15_COURANT-VAL_EMA15_PRECEDENT > 0 ) and (VAL_EMA1H_COURANT - VAL_EMA15_COURANT > 10 ) and (VAL_EMA1H_COURANT < VAL_EMA200_COURANT) \
        and (VAL_EMA1H_COURANT - VAL_EMA1H_PRECEDENT > 0) and (VAL_EMA15_MAX - VAL_EMA15_COURANT >= 0) and (TYPE_EMA15 == "HAUT")  :
        """

          #if (TYPE_EMA15 == "HAUT") and  (TYPE_BG == "BG_VERTE") and (VAL_EMA1H_COURANT - VAL_EMA15_COURANT > 10 ) :
        #if (FRONT_MONTANT_EMA200 == 1) and (FRONT_MONTANT_EMA15 == 0)  and (TYPE_BG == "BG_ROUGE") and (VAL_CLOSE <= VAL_EMA15_COURANT ) :
        global POINT_ENTRE_EMA200
        global FRONT_MONTANT_EMA200
        global FRONT_MONTANT_EMA15
        #global VAL_EMA200_MAX
        #global VAL_EMA200_idxmin_ORG
        global LISTE_ACHAT_VENTE
        global VAL_EMA15_COURANT
        global VAL_EMA15_PRECEDENT
        global VAL_EMA1H_COURANT
        global VAL_CLOSE
        global FRONT_NEUTRE_EMA200
        global FRONT_NEUTRE_EMA15
        global PT_RESISTANCE_HAUT_EMA1H_EMA15
        global ORDER
        #global LAST_ORDER
        global VAL_ACHAT
        global FIRST_VENTE
        global FLAG_BEST_NBR_TAILLE_BG
        
        print("\nENTRER DANS TRAITEMENT_ACHAT ")
        
        if (FIRST_VENTE == 0) :
            return
        """
        TEST_MODE_REEL=CALCUL_DATE_COURANTE(dataframe,val_mask_idxmin)
        if   TEST_MODE_REEL == 1 :
          val_mask_idxmin=last_index
        """
        """
        if FLAG_BEST_NBR_TAILLE_BG == 1 :
           val_mask_idxmin=DETECT_MODE_REEL(dataframe,val_mask_idxmin)
        """
         
        """
        last_index=len(dataframe)-1
        print("last_index=",last_index)
        if val_mask_idxmin >= last_index :
            val_mask_idxmin=last_index  
        """

        
        PT_RESISTANCE_HAUT_EMA1H_EMA15=0
        VAL_EMA1H_COURANT=dataframe.EMA1H.loc[val_mask_idxmin].astype(int)
        EMA1H=dataframe.EMA1H.loc[val_mask_idxmin].astype(int)
        EMA1L=dataframe.EMA1L.loc[val_mask_idxmin].astype(int)
        VAL_EMA15_COURANT=dataframe.EMA15.loc[val_mask_idxmin].astype(int)
        VAL_EMA200_COURANT=dataframe.EMA200.loc[val_mask_idxmin].astype(int)
        DIFF_EMA1L_EMA15=dataframe['DIFF_EMA1L_EMA15'].loc[val_mask_idxmin].astype(int)
        """
        if len(LISTE_ACHAT_VENTE) > 0 :
            print("LISTE_ACHAT_VENTE=\n",LISTE_ACHAT_VENTE)
            print("LEN LISTE_ACHAT_VENTE=",len(LISTE_ACHAT_VENTE))
            LAST_VENTE=LISTE_ACHAT_VENTE[["VENTE"]].iloc[-1].values
            print("LAST_VENTE=",LAST_VENTE)
        """
        #if  (FRONT_MONTANT_EMA200 == 1) and (FRONT_MONTANT_COURT_EMA15 == 1) and (EMA1H >= VAL_EMA15_COURANT) and ( ORDER != LAST_ORDER ) \
        #and (FRONT_MONTANT_EMA15 == 1) and (FRONT_MONTANT_EMA1H == 1)  and (VAL_EMA15_COURANT > VAL_EMA200_COURANT) and (POINT_ENTRE_EMA200 == 0) : #and  (TYPE_BG == "BG_ROUGE"):
        if  (FRONT_MONTANT_EMA200 == 0) and (FRONT_MONTANT_COURT_EMA200 == 1) and (FRONT_MONTANT_COURT_EMA15 == 1) and (EMA1L > VAL_EMA15_COURANT) and (EMA1H > VAL_EMA15_COURANT) and ( ORDER != LAST_ORDER ) \
        and (FRONT_MONTANT_COURT_EMA1L == 1) and (FRONT_MONTANT_COURT_EMA1H == 1)  and (VAL_EMA15_COURANT < VAL_EMA200_COURANT ) and (POINT_ENTRE_EMA200 == 0) : #and  (TYPE_BG == "BG_ROUGE"):
        #if (abs(VAL_EMA1H_COURANT - VAL_EMA15_COURANT) <= 1) and (FRONT_MONTANT_EMA15 == 0) and (VAL_EMA15_COURANT - VAL_EMA200_COURANT <= 1) and (POINT_ENTRE_EMA200 == 0) \
        ##OK# if ((VAL_EMA1H_COURANT > VAL_EMA15_COURANT) ) and (FRONT_MONTANT_EMA200 == 0) and (POINT_ENTRE_EMA200 == 0) : # and (FRONT_NEUTRE_EMA15 == 1) and (VAL_EMA15_COURANT <= VAL_EMA200_COURANT) and (POINT_ENTRE_EMA200 == 0) :
            """  
        if (abs(VAL_EMA1H_COURANT - VAL_EMA15_COURANT) <= 1) and (FRONT_MONTANT_EMA15 == 0) and (POINT_ENTRE_EMA200 == 0) and (not "m" in  interval) \
           or(VAL_EMA1H_COURANT - VAL_EMA15_COURANT == 0) and (VAL_EMA15_COURANT - VAL_EMA200_COURANT <= 1) and (POINT_ENTRE_EMA200 == 0) and ("m" in  interval) \
           or(VAL_EMA15_COURANT-VAL_EMA200_COURANT == 0) and (VAL_EMA15_COURANT-VAL_EMA15_PRECEDENT > 0) and (VAL_EMA200_COURANT-VAL_EMA200_idxmin_ORG > 0) and (POINT_ENTRE_EMA200 == 0)  :
            """  
            """  
            
            or (FRONT_MONTANT_EMA200 == 1) and (FRONT_MONTANT_EMA15 == 0) and (abs(VAL_EMA1H_COURANT - VAL_EMA15_COURANT) <= 1) \
               and  (POINT_ENTRE_EMA200 == 0) and (not "m" in  interval)\
            or (FRONT_MONTANT_EMA200 == 1) and (FRONT_MONTANT_EMA15 == 0) and (abs(VAL_EMA1H_COURANT - VAL_EMA15_COURANT) <= 1) and (VAL_EMA15_COURANT-VAL_EMA15_PRECEDENT >=0) \

            and (abs(VAL_EMA1H_COURANT - VAL_EMA15_COURANT) <= 10) and (POINT_ENTRE_EMA200 == 0) and ("m" in  interval) :
            """  
            """
            or(VAL_EMA15_COURANT-VAL_EMA200_COURANT == 0) and (VAL_EMA15_COURANT-VAL_EMA15_PRECEDENT <=0) \

           or(VAL_EMA15_COURANT-VAL_EMA15_PRECEDENT >0) and (VAL_EMA200_COURANT-VAL_EMA200_PRECEDENT > 0) and (POINT_ENTRE_EMA200 == 0) and ("m" in  interval) \
           or(VAL_EMA15_COURANT-VAL_EMA15_PRECEDENT >0) and (FRONT_NEUTRE_EMA200 == 1) and (POINT_ENTRE_EMA200 == 0) and ("m" in  interval)    : #and  (TAILLE_BG <= 10)  :
            """
            print("\n !!!!! POINT ENTRE EMA200 !!!!! EMA200 CROISSANTE OK OK OK")
            print("VAL_EMA200_MAX - VAL_EMA200_idxmin_ORG =",VAL_EMA200_MAX - VAL_EMA200_idxmin_ORG)
            print("VAL_EMA200_MAX - VAL_EMA200_COURANT =",VAL_EMA200_MAX - VAL_EMA200_COURANT)
            print("\nDataframe MASK EMA200 MIN=\n",dataframe[["date","EMA200"]].loc[val_mask_idxmin_ORG])
            #POINT_ENTRE_EMA200=1
            global MASK_POINT_ENTRE_EMA15
            MASK_POINT_ENTRE_EMA15=val_mask_idxmin_ORG
            global mask_POINT_ACHAT
            mask_POINT_ACHAT=(dataframe.date >= dataframe.loc[MASK_POINT_ENTRE_EMA15].date) #and (dataframe.date <= dataframe.loc[val_mask_idxmin].date)
            print("val_mask_idxmin_ORG=",val_mask_idxmin_ORG)
            print("POINT_ENTRER_EMA200=",POINT_ENTRE_EMA200)
            print("POINT_ACHAT OK OK OK\n")
            #VAL_ACHAT=VAL_EMA1H_COURANT
            VAL_ACHAT=dataframe.close.loc[val_mask_idxmin]
            VAL_DATE_ACHAT=dataframe.date.loc[val_mask_idxmin]
            ORDER="BUY"
            print(ORDER)
            #LAST_ORDER="BUY"
            EXEC_ORDER(dataframe)
            #time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(x)))
            DATE=VAL_DATE_ACHAT.strftime("ACHAT: %Y-%m-%d %H:%M:%S")
            #print("DATE=",DATE)
            """
            LISTE_ACHAT.append(DATE+" PRIX:"+VAL_ACHAT)
            LISTE_GLOBALE.append(DATE+" PRIX:"+VAL_ACHAT)
            """
            VAL_VENTE=""
            DATE_VENTE=""
            DATE_PD=VAL_DATE_ACHAT.strftime("%Y-%m-%d %H:%M:%S")
            date=[{'DATE_ACHAT': DATE_PD,'ACHAT':VAL_ACHAT,'DATE_VENTE':DATE_VENTE,'VENTE':VAL_VENTE,'GAIN':"",'CUMUL':""}]
            #df = pd.DataFrame(data=data,columns=['DATE','ACHAT','VENTE'])
            #LISTE_ACHAT_VENTE = pd.DataFrame(date)
            LISTE_ACHAT_VENTE = LISTE_ACHAT_VENTE.append(date,ignore_index=True)
            print("LISTE_ACHAT_VENTE=\n",LISTE_ACHAT_VENTE)
            print("LEN LISTE_ACHAT_VENTE=",len(LISTE_ACHAT_VENTE))
            #if FLAG_BEST_NBR_TAILLE_BG == 1 :
               # time.sleep(5)
            #print("VAL_ACHAT=",VAL_ACHAT)
            """
            print("LISTE_ACHAT=",LISTE_ACHAT)
            print("LISTE_GLOBALE=",LISTE_GLOBALE)
            """
            #print("SORTIE DANS TRAITEMENT_ACHAT\n")
        print("SORTIE DANS TRAITEMENT_ACHAT\n")
            
            
def TRAITEMENT_VENTE(dataframe,val_mask_idxmin) :
        global POINT_ENTRE_EMA200
        global PT_RESISTANCE_HAUT_EMA1H_EMA15
        global NBR_PREC
        global NBR_PREC_LONG
        global VAL_NBR_PREC_LONG
        global ORDER
        #global LAST_ORDER
        global FLAG_BEST_NBR_TAILLE_BG
        print("\nENTRER DANS TRAITEMENT_VENTE ")


        """
        TEST_MODE_REEL=CALCUL_DATE_COURANTE(dataframe,val_mask_idxmin)
        if   TEST_MODE_REEL == 1 :
          val_mask_idxmin=last_index
        """
        """
        if FLAG_BEST_NBR_TAILLE_BG == 1 :
           val_mask_idxmin=DETECT_MODE_REEL(dataframe,val_mask_idxmin)
        """
        if ( POINT_ENTRE_EMA200 == 1 ) : 
            """
            last_index=len(dataframe)-1
            print("last_index=",last_index)
            if val_mask_idxmin >= last_index :
                val_mask_idxmin=last_index  
            """
           
            #CALCULE MAX EMA1H
            VAL_CLOSE=dataframe.close.loc[val_mask_idxmin]
            VAL_ACHAT=VAL_CLOSE
            VAL_ACHAT_INT=int(float(VAL_ACHAT)*MULTIP)
            #print("VAL_ACHAT_INT=",VAL_ACHAT_INT)
            
            if val_mask_idxmin == 0 :
                nbr_dec=0
            else :
                nbr_dec=1
               
            ##mask_EMA15 = (dataframe.date >=  dataframe.loc[MASK_POINT_ENTRE_EMA15].date ) and (dataframe.date <= dataframe.loc[val_mask_idxmin].date)
            #val_mask_EMA1H_idxmax=dataframe['EMA1H'].loc[mask_POINT_ACHAT].idxmax()
            val_mask_EMA1H_idxmax=dataframe['EMA1H'].idxmax()
            VAL_EMA1L_COURANT=dataframe.EMA1L.loc[val_mask_idxmin].astype(int)
            VAL_EMA1L_PRECEDENT=dataframe.EMA1L.loc[val_mask_idxmin-nbr_dec].astype(int)
            VAL_EMA1L_PRECEDENT_LONG=dataframe.EMA1L.loc[val_mask_idxmin-NBR_PREC_LONG].astype(int)
            VAL_EMA1H_COURANT=dataframe.EMA1H.loc[val_mask_idxmin].astype(int)
            VAL_EMA1H_PRECEDENT=dataframe.EMA1H.loc[val_mask_idxmin-nbr_dec].astype(int)
            VAL_EMA1H_PRECEDENT_LONG=dataframe.EMA1H.loc[val_mask_idxmin-NBR_PREC_LONG].astype(int)
            VAL_EMA1H_MAX=dataframe.EMA1H.loc[val_mask_EMA1H_idxmax].astype(int)
            EMA1H=dataframe.EMA1H.loc[val_mask_idxmin].astype(int)
            EMA1L=dataframe.EMA1L.loc[val_mask_idxmin].astype(int)
            VAL_HIGH=dataframe.EMA1H_ORG.loc[val_mask_EMA1H_idxmax]
            VAL_EMA15_PRECEDENT_LONG=dataframe.EMA15.loc[val_mask_idxmin-NBR_PREC_LONG].astype(int)
            VAL_EMA15_PRECEDENT=dataframe.EMA15.loc[val_mask_idxmin-NBR_PREC].astype(int)
            DIFF_EMA1L_EMA15=dataframe['DIFF_EMA1L_EMA15'].loc[val_mask_idxmin].astype(int)
            print("\nDataframe MASK EMA1H =\n",dataframe[["date","EMA1H"]].loc[val_mask_idxmin])
            print("VAL_EMA1H_COURANT=",VAL_EMA1H_COURANT)
            print("\nVAL_EMA1H_MAX=\n",dataframe.loc[val_mask_EMA1H_idxmax])
            print("\nVAL_EMA1H_MAX-VAL_EMA1H_COURANT=",VAL_EMA1H_MAX-VAL_EMA1H_COURANT)
            high=dataframe.high.loc[val_mask_idxmin]
            print("high=",float(high))
            print("VAL_HIGH=",VAL_HIGH)
            print("VAL_ACHAT=",VAL_ACHAT)
            print("EMA1H=",EMA1H)
            print("VAL_ACHAT=",VAL_ACHAT)
            print("VAL_ACHAT_INT=",VAL_ACHAT_INT)
            print("VAL_CLOSE=",VAL_CLOSE)
            print("VAL_CLOSE_INT=",VAL_CLOSE_INT)
            print("DIFF_EMA1L_EMA15=",DIFF_EMA1L_EMA15)
            print("VAL_EMA200_COURANT=",VAL_EMA200_COURANT)
            print("VAL_EMA1H_COURANT=",VAL_EMA1H_COURANT)
            print("VAL_EMA15_COURANT=",VAL_EMA15_COURANT)
            print("VAL_EMA15_PRECEDENT=",VAL_EMA15_PRECEDENT)
            print("VAL_EMA1H_PRECEDENT=",VAL_EMA1H_PRECEDENT)
            DIFF_EMA15_EMA200=abs(int(VAL_EMA15_COURANT)  - int(VAL_EMA200_COURANT))
            print("FONCTION DE VENTE")
            print("FRONT_MONTANT_EMA200=",FRONT_MONTANT_EMA200)
            print("FRONT_MONTANT_EMA15=",FRONT_MONTANT_EMA15)
            print("FRONT_MONTANT_EMA1L=",FRONT_MONTANT_EMA1L)
            print("FRONT_MONTANT_EMA1H=",FRONT_MONTANT_EMA1H)
            print("TAILLE_BG=",TAILLE_BG)
            print("DIFF_EMA15_EMA200=",DIFF_EMA15_EMA200)
            """
            if (abs(VAL_EMA1H_COURANT - VAL_EMA1H_PRECEDENT) >= 20 ) and (float(VAL_CLOSE) > float(VAL_ACHAT)*1.01) and (int(VAL_EMA1H_COURANT) - int(VAL_EMA15_COURANT) >= 150) \
             and (int(VAL_EMA1H_COURANT) > int(VAL_EMA200_COURANT)) and (TAILLE_BG >= 20 ) and (int(VAL_CLOSE_INT) > int(VAL_EMA200_COURANT)) and (VAL_EMA15_COURANT-VAL_EMA15_PRECEDENT > 0 ) :
             #or(FRONT_MONTANT_EMA200 == 1) and (FRONT_MONTANT_EMA15 == 0) and (TYPE_BG == "BG_ROUGE") and (VAL_EMA15_COURANT-VAL_EMA15_PRECEDENT < 0 ) :
            """
            """
            #if (FRONT_MONTANT_EMA200 == 1) and (FRONT_MONTANT_EMA15 == 0) and (TYPE_BG == "BG_ROUGE") and (VAL_EMA15_COURANT-VAL_EMA15_PRECEDENT < 0 ) \
            if (FRONT_MONTANT_EMA200 == 1) and (TYPE_BG == "BG_ROUGE") and (VAL_EMA15_COURANT-VAL_EMA15_PRECEDENT < 0 ) \
            and (float(VAL_CLOSE) > float(VAL_ACHAT)*1.01) and (TYPE_BG == "BG_VERT") : 
            """
            #if (FRONT_MONTANT_EMA200 == 1) and (FRONT_MONTANT_EMA15 == 0) and (VAL_EMA15_COURANT-VAL_EMA15_PRECEDENT <= 6 ) and (float(VAL_CLOSE) > float(VAL_ACHAT)*1.01) : # and (int(VAL_EMA1H_COURANT) - int(VAL_EMA15_COURANT) >= 150) :
            #if  (FRONT_MONTANT_EMA15 == 0) and  (TAILLE_BG >= 25) :
            #if  (FRONT_MONTANT_EMA15 == 0) and  (TAILLE_BG >= 25) and (float(VAL_CLOSE) > float(VAL_ACHAT)) :
            #if  (float(VAL_CLOSE) > (float(VAL_ACHAT)*2.55)) and (TAILLE_BG >= 50) :
            #if  (TAILLE_BG >= 20) and  (float(VAL_CLOSE) > (float(VAL_ACHAT)*1.25)) :
            #if  (float(VAL_CLOSE_INT) > float(VAL_ACHAT_INT)) :
            #if  (FRONT_MONTANT_EMA15 == 1) :
                
            #NBR_TAILLE_BG=0
            #NBR_TAILLE_BG=36
            #NBR_TAILLE_BG=40
            #NBR_TAILLE_BG=50
            #NBR_TAILLE_BG=60
            ###NBR_TAILLE_BG=70 #WABIUSDT
            #NBR_TAILLE_BG=100
            print("NBR_TAILLE_BG=",NBR_TAILLE_BG)
            LISTE_EMA15_EMA200 = [20,30,40,50,60,70,100,200]
            DIFF_EMA1H_EMA1L=(int(VAL_EMA1H_COURANT) - int(EMA1L))
            #print("\nENTRER DANS TRAITEMENT_VENTE ")
            
            if (VAL_EMA1H_COURANT - VAL_EMA15_PRECEDENT == 0 ) :
                PT_RESISTANCE_HAUT_EMA1H_EMA15=VAL_EMA1H_COURANT
                print("PT_RESISTANCE_HAUT_EMA1H_EMA15=",PT_RESISTANCE_HAUT_EMA1H_EMA15)
                #time.sleep(5) and (int(EMA1H - EMA1L) == 3)   and (int(DIFF_EMA1L_EMA15) > 7) (FRONT_MONTANT_EMA200 == 1) and # and ( ORDER != LAST_ORDER ) and (VAL_CLOSE > VAL_ACHAT) \
            #DATE_COURANTE_VENTE = DATE_COURANTE - pd.Timedelta(minutes=val_minute)
            #if (FRONT_MONTANT_EMA1H == 1 )  and (FRONT_MONTANT_COURT_EMA1H == 0 ) and (DATE_COURANTE_VENTE == VAL_EMA1H_DATE_MAX) :                    
            if  ((FRONT_MONTANT_EMA15 == 1) and (EMA1L > VAL_EMA15_COURANT) and (VAL_EMA15_COURANT > VAL_EMA200_COURANT) and (FRONT_MONTANT_EMA1L == 1) and (FRONT_MONTANT_EMA1H == 1) 
                 and (FRONT_MONTANT_COURT_EMA1L == 0) and (FRONT_MONTANT_COURT_EMA1H == 0) and (TAILLE_BG > 20)) :# and  (TYPE_BG == "BG_VERTE")) :
                #and (DIFF_EMA1H_EMA1L >= int(item) for item in LISTE_EMA15_EMA200)) :
                #   # and (VAL_CLOSE > VAL_ACHAT) : and (TAILLE_BG >= NBR_TAILLE_BG) and (FRONT_MONTANT_COURT_EMA1L == 1) and (FRONT_MONTANT_COURT_EMA1H == 1) 
            #if (FRONT_MONTANT_EMA200 == 1) and (FRONT_MONTANT_EMA15 == 0) and (int(VAL_EMA1H_COURANT) - int(VAL_EMA15_COURANT) >= 5) and (VAL_CLOSE > VAL_ACHAT) \
              #  and (TAILLE_BG >= NBR_TAILLE_BG) and (int(VAL_EMA15_COURANT) - int(VAL_EMA200_COURANT) >0) and (not "m" in  interval) \
              #  or(int(VAL_EMA1H_COURANT) - int(VAL_EMA200_COURANT) >= 10)  and (TAILLE_BG >= NBR_TAILLE_BG) and ("m" in  interval) \
              #  or (VAL_EMA1H_COURANT - PT_RESISTANCE_HAUT_EMA1H_EMA15 > 2 ) and (PT_RESISTANCE_HAUT_EMA1H_EMA15 > 0 )  and (TAILLE_BG >= NBR_TAILLE_BG) and ("m" in  interval) :
        
                #(VAL_EMA15_COURANT-VAL_EMA15_PRECEDENT <=0)
                # (int(VAL_EMA1H_COURANT) - int(VAL_EMA200_COURANT) >= 10) and ("m" in  interval) :
                print("OK OK OK POINT_VENTE OK OK OK")
                print("VAL_EMA1H_COURANT=",VAL_EMA1H_COURANT)
                print("VAL_EMA1H_ACHAT=",VAL_ACHAT)
                print("FRONT_MONTANT_EMA15=",FRONT_MONTANT_EMA15)
                #POINT_ENTRE_EMA200 = 0
                ORDER="SELL"
                print(ORDER)
                #LAST_ORDER="SELL"
                EXEC_ORDER(dataframe)
                print("DANS VENTE LISTE_ACHAT_VENTE=\n",LISTE_ACHAT_VENTE)
                VAL_VENTE=dataframe.close.loc[val_mask_idxmin]
                VAL_DATE_VENTE=dataframe.date.loc[val_mask_idxmin]
                DATE=VAL_DATE_VENTE.strftime("VENTE: %Y-%m-%d %H:%M:%S")
                """
                LISTE_VENTE.append(DATE+" PRIX:"+VAL_VENTE)
                LISTE_GLOBALE.append(DATE+" PRIX:"+VAL_VENTE)
                print("LISTE_VENTE=",LISTE_VENTE)
                print("LISTE_GLOBALE=",LISTE_GLOBALE)
                """
                LEN=len(LISTE_ACHAT_VENTE)
                print("LISTE_ACHAT_VENTE=\n",LISTE_ACHAT_VENTE.tail(LEN))
                print("LEN LISTE_ACHAT_VENTE=",len(LISTE_ACHAT_VENTE))
                #print("LISTE_ACHAT_VENTE=\n",LISTE_ACHAT_VENTE)
                #LISTE_ACHAT_VENTE[["DATE_VENTE","VENTE"]].tail(LEN)=VAL_DATE_VENTE,VAL_VENTE
                #LISTE_ACHAT_VENTE[["DATE_VENTE"]].replace("VIDE",VAL_DATE_VENTE)
                LISTE_ACHAT_VENTE[["DATE_VENTE"]]=LISTE_ACHAT_VENTE[["DATE_VENTE"]].replace("",VAL_DATE_VENTE)
                LISTE_ACHAT_VENTE[["VENTE"]]=LISTE_ACHAT_VENTE[["VENTE"]].replace("",VAL_VENTE)
                print("LEN LISTE_ACHAT_VENTE=",len(LISTE_ACHAT_VENTE))
                print("LISTE_ACHAT_VENTE=\n",LISTE_ACHAT_VENTE)
                #LISTE_ACHAT_VENTE["GAIN"]=LISTE_ACHAT_VENTE[["VENTE"]].sub(LISTE_ACHAT_VENTE[["ACHAT"]])
                #GAIN=int((float(LISTE_ACHAT_VENTE.VENTE[0])-float(LISTE_ACHAT_VENTE.ACHAT[0]))*MULTIP)
                LISTE_ACHAT_VENTE["GAIN"]=LISTE_ACHAT_VENTE.VENTE.astype(float).sub(LISTE_ACHAT_VENTE.ACHAT.astype(float), axis = 0)
                #GAIN=LISTE_ACHAT_VENTE[["VENTE"]].sub(LISTE_ACHAT_VENTE[["ACHAT"]])
                #print("GAIN=",GAIN)
                #LISTE_ACHAT_VENTE["GAIN"]=LISTE_ACHAT_VENTE["GAIN"].replace("",GAIN)
                LISTE_ACHAT_VENTE["CUMUL"]=LISTE_ACHAT_VENTE["GAIN"].cumsum()
                LAST_CUMUL=LISTE_ACHAT_VENTE.CUMUL.values.astype(float)
                #GAIN= int(str(LISTE_ACHAT_VENTE.GAIN.values*MULTIP/10).split(".")[0].split("[")[1])
                #print("GAIN=",GAIN)
                #LISTE_ACHAT_VENTE['GAIN'].iloc[-1]= GAIN
                # np.round(mins.DEMA40,decimals = 6)
                LISTE_ACHAT_VENTE['GAIN']= LISTE_ACHAT_VENTE['GAIN'].apply(lambda x : (x*MULTIP)/100)
                LISTE_ACHAT_VENTE['GAIN']= LISTE_ACHAT_VENTE['GAIN'].apply(lambda x : (np.round(x,decimals = 1)*10)).astype(int)
                #LISTE_ACHAT_VENTE['GAIN']= LISTE_ACHAT_VENTE['GAIN'].astype(str)
                #LISTE_ACHAT_VENTE['GAIN']= LISTE_ACHAT_VENTE['GAIN'].apply(lambda x : (x.split(".")[0].split("[")[1]))
                #LISTE_ACHAT_VENTE['GAIN']= LISTE_ACHAT_VENTE['GAIN'].astype(int)
                

                #.apply(lambda x : (x*MULTIP/10)).astype(str).split(".")[0]
                #LISTE_ACHAT_VENTE['CUMUL']= LISTE_ACHAT_VENTE.CUMUL.apply(lambda x : (x*MULTIP)/100).astype(int)
                

                #LISTE_ACHAT_VENTE["CUMUL"]=LISTE_ACHAT_VENTE["GAIN"].sum()
                print("LISTE_ACHAT_VENTE=\n",LISTE_ACHAT_VENTE)
                #if FLAG_BEST_NBR_TAILLE_BG == 1 :
                    #time.sleep(5)
                #LAST_CUMUL="{0:f}".format(LAST_CUMUL)
                #print("LAST_CUMUL=",LAST_CUMUL)
                #LAST_LISTE_ACHAT_VENTE=LISTE_ACHAT_VENTE.tail(-1)  
                #print("LAST_LISTE_ACHAT_VENTE=\n",LAST_LISTE_ACHAT_VENTE)                              
                """
                DATE_PD=VAL_DATE_ACHAT.strftime("%Y-%m-%d %H:%M:%S")
                date=[{'DATE_ACHAT': DATE_PD,'ACHAT':VAL_ACHAT,'DATE_VENTE':DATE_VENTE,'VENTE':VAL_VENTE,'GAIN':"",'CUMUL':""}]
                #df = pd.DataFrame(data=data,columns=['DATE','ACHAT','VENTE'])
                #LISTE_ACHAT_VENTE = pd.DataFrame(date)
                LISTE_ACHAT_VENTE = LISTE_ACHAT_VENTE.append(date,ignore_index=True)
                print("LISTE_ACHAT_VENTE=\n",LISTE_ACHAT_VENTE)
                """
                #print("SORTIE DANS TRAITEMENT_VENTE\n")
        print("SORTIE DANS TRAITEMENT_VENTE\n")
            
            
def TRAITEMENT_DERNIER_VENTE(dataframe,val_mask_idxmin) :
        global POINT_ENTRE_EMA200
        global MASK_POINT_ENTRE_EMA15
        global VAL_EMA15_PRECEDENT
        #global VAL_ACHAT
        global VAL_CLOSE
        global POINT_ENTRE_EMA200
        global ORDER
        global DERNIER_POINT_VENTE
        global LAST_FRONT_NEUTRE_EMA15
        global LAST_ORDER
        global custom_info
        global MODE_GAIN
        global FLAG_BEST_NBR_TAILLE_BG
        global NBR_PREC_LONG
        global VAL_NBR_PREC_LONG
        global VAL_EMA200_DATE_MAX
        global dataframe_date
        global MULTIP
        global FRONT_MONTANT_EMA200
        global FRONT_MONTANT_COURT_EMA1H
        global FRONT_MONTANT_COURT_EMA1L
        global FRONT_NEUTRE_COURT_EMA15
        global FRONT_MONTANT_EMA15
        global FRONT_MONTANT_EMA1L
        global FRONT_MONTANT_EMA1H
        global DIFF_VAL_CLOSE_INF_VAL_CLOSE_N1
        
        
       
        print("\nENTRER DANS TRAITEMENT_DERNIER_VENTE")

        """
        if FLAG_BEST_NBR_TAILLE_BG == 1 :
           val_mask_idxmin=DETECT_MODE_REEL(dataframe,val_mask_idxmin)
        """
        
        """
        last_index=len(dataframe)-1
        print("last_index=",last_index)
        if val_mask_idxmin >= last_index :
            val_mask_idxmin=last_index  
        """
                    
        VAL_EMA200_COURANT=dataframe.EMA200.loc[val_mask_idxmin].astype(int)
        VAL_EMA15_COURANT=dataframe.EMA15.loc[val_mask_idxmin].astype(int)
        VAL_EMA1H_COURANT=dataframe.EMA1H.loc[val_mask_idxmin].astype(int)

        EMA1L=dataframe.EMA1L.loc[val_mask_idxmin].astype(int)
        EMA1H=dataframe.EMA1H.loc[val_mask_idxmin].astype(int)
        #global VAL_EMA15_MAX
        if (POINT_ENTRE_EMA200 == 1) : # and  (VAL_EMA1H_COURANT - VAL_EMA15_COURANT < 0 ) :
            #print("\nENTRER DANS TRAITEMENT_DERNIER_VENTE")
 
            DIFF_EMA200_EMA15=dataframe.DIFF_EMA200_EMA15.loc[val_mask_idxmin].astype(int)

            #EMA1L=dataframe.EMA1L.loc[val_mask_idxmin].astype(int)

            print("DIFF_EMA200_EMA15=",DIFF_EMA200_EMA15)
            print("TYPE_BG=",TYPE_BG)
            ##NBR_TAILLE_BG=36
            #NBR_TAILLE_BG=40
            #NBR_TAILLE_BG=100
        #if (FRONT_MONTANT_EMA200 == 1) and (FRONT_MONTANT_EMA15 == 1 )  and (FRONT_MONTANT_EMA1H == 1 ) and (FRONT_MONTANT_COURT_EMA1H == 0 ) \
           #and (TYPE_BG == "BG_ROUGE")   :
            """   
            if  (VAL_EMA15_COURANT >= VAL_EMA200_COURANT ) and (DATE_COURANT >= DATE_MAX) and (DIFF_EMA200_EMA15 == 0)  and ( POINT_ENTRE_EMA200 == 1 ) \
                and (float(VAL_CLOSE) > float(VAL_ACHAT)*1.01) and (DERNIER_POINT_VENTE == 0):
            """        
            print("FRONT_MONTANT_EMA200:",FRONT_MONTANT_EMA200)
            print("EMA1L >= VAL_EMA15_COURANT:",EMA1L >= VAL_EMA15_COURANT)
            print("EMA1H > VAL_EMA15_COURANT:",EMA1H > VAL_EMA15_COURANT)
            print("FRONT_MONTANT_COURT_EMA1L == 0:",FRONT_MONTANT_COURT_EMA1L == 0)
            print("FRONT_MONTANT_COURT_EMA1H == 0:",FRONT_MONTANT_COURT_EMA1H == 0)
            print("FRONT_NEUTRE_COURT_EMA15 == 1:",FRONT_NEUTRE_COURT_EMA15 == 1)
            print("FRONT_MONTANT_EMA15:",FRONT_MONTANT_EMA15 == 1)
            print("FRONT_MONTANT_EMA1H:",FRONT_MONTANT_EMA1H == 1)
            print("FRONT_MONTANT_EMA1L == 1:",FRONT_MONTANT_EMA1L == 1)
            print("abs(DIFF_EMA200_EMA15) >= 10:",abs(int(DIFF_EMA200_EMA15)) >= 90)
            """
            if  (FRONT_MONTANT_EMA200 == 1)  and (EMA1H > VAL_EMA15_COURANT) and ( ORDER != LAST_ORDER ) \
                and (FRONT_MONTANT_COURT_EMA1L == 0)  and (FRONT_MONTANT_COURT_EMA1H == 0)  and (POINT_ENTRE_EMA200 == 1) \
                and (abs(DIFF_EMA200_EMA15) >= 10) \
                    | (LAST_FRONT_NEUTRE_EMA15 > 0) and (LAST_FRONT_NEUTRE_EMA15 > VAL_EMA15_COURANT ) and (FRONT_MONTANT_EMA200 == 1)  and (EMA1H <= VAL_EMA15_COURANT) and ( ORDER != LAST_ORDER ) \
                        and (FRONT_MONTANT_COURT_EMA1L == 0)  and (FRONT_MONTANT_COURT_EMA1H == 0)  and (POINT_ENTRE_EMA200 == 1) : #and (float(VAL_CLOSE) > float(VAL_ACHAT)) :
            """
            global VAL_ACHAT_INITIALE   
            if custom_info["VAL_ACHAT_INITIALE"] == "" :
                custom_info["VAL_ACHAT_INITIALE"]=0

            # VAL_ACHAT_INITIALE=(custom_info["VAL_ACHAT_INITIALE"])
            # VAL_ACHAT_INITIALE=int(float(VAL_ACHAT_INITIALE)*MULTIP)

            print("LAST_ORDER=",LAST_ORDER)
            print("VAL_ACHAT_INITIALE=",VAL_ACHAT_INITIALE)

            global GAIN_RELATIF
            global GAIN   
            global GAIN_ABSOLUE
            global GAIN_ABSOLUE_RELATIF
            if GAIN_ABSOLUE == "" :
                GAIN_ABSOLUE=0
                
            if ((LAST_ORDER == "BUY")  and ( float(VAL_ACHAT_INITIALE) > 0)) :
                """
                LAST_CLOSE=dataframe.close.loc[val_mask_idxmin]
                LAST_CLOSE=(float(LAST_CLOSE)*MULTIP)/100
                LAST_CLOSE=np.round(LAST_CLOSE,decimals = 1)
                LAST_CLOSE=int(LAST_CLOSE)
                """
                LAST_CLOSE=dataframe['CLOSE'].loc[val_mask_idxmin].astype(int)
                RECUP_LAST_PRICE_IN_FILE()
                LAST_CLOSE=PRIX
                GAIN_ABSOLUEF=(float(LAST_CLOSE) - float(VAL_ACHAT_INITIALE))
                GAIN_ABSOLUE=np.round(GAIN_ABSOLUE,decimals = 8)
                # GAIN_ABSOLUE=(int(LAST_CLOSE) - int(VAL_ACHAT_INITIALE))
                print("LAST_CLOSE:",LAST_CLOSE)
                print("VAL_ACHAT_INITIALE:",VAL_ACHAT_INITIALE)
                print("GAIN_ABSOLUE:",GAIN_ABSOLUE)
                print("GAIN_ABSOLUE_RELATIF:",GAIN_ABSOLUE_RELATIF)
                if LAST_CLOSE == VAL_ACHAT_INITIALE :
                    return
                if "VAL_ACHAT" in custom_info  and (POINT_ENTRE_EMA200 == 1)  and (DERNIER_POINT_VENTE == 0) and ( ORDER != LAST_ORDER ):
                    VAL_ACHAT=custom_info["VAL_ACHAT"] 
                    VAL_ACHAT=(float(VAL_ACHAT)*MULTIP)
                    LAST_CLOSE=(float(LAST_CLOSE)*MULTIP)
                    #print("VAL_ACHAT ORG: ",VAL_ACHAT)
                    #VAL_ACHAT=(float(VAL_ACHAT)*MULTIP)/100
                    #VAL_ACHAT=np.round(VAL_ACHAT,decimals = 1)
                    # VAL_ACHAT=float(VAL_ACHAT)      
                    print("VAL_ACHAT: ",VAL_ACHAT)
                    # GAIN=(float(LAST_CLOSE) - float(VAL_ACHAT))
                    CINQ_POUR_CENT_VAL_ACHAT=(VAL_ACHAT)*0.98   
                    print("CINQ_POUR_CENT_VAL_ACHAT: ",CINQ_POUR_CENT_VAL_ACHAT)
                    #CINQ_POUR_CENT_VAL_ACHAT=(float(CINQ_POUR_CENT_VAL_ACHAT)*MULTIP)/100
                    #CINQ_POUR_CENT_VAL_ACHAT=np.round(CINQ_POUR_CENT_VAL_ACHAT,decimals = 1)
                    # CINQ_POUR_CENT_VAL_ACHAT=int(CINQ_POUR_CENT_VAL_ACHAT)  
                    # print("CINQ_POUR_CENT_VAL_ACHAT: ",CINQ_POUR_CENT_VAL_ACHAT)
                    # MULTIP=len(str(LAST_CLOSE))
                    # print("MULTIP:",MULTIP)
                    # CINQ_POUR_CENT_VAL_ACHAT=CALCULE_TAILLE_BOUGIE(CINQ_POUR_CENT_VAL_ACHAT,MULTIP) 
                    print("CINQ_POUR_CENT_VAL_ACHAT: ",CINQ_POUR_CENT_VAL_ACHAT)
                    # DATE_COURANTE=dataframe_date.date.loc[val_mask_idxmin]
                    #exit()
                   # if   (FRONT_MONTANT_EMA15 == 1 ) and (FRONT_MONTANT_COURT_EMA15 == 0 )  and (VAL_EMA15_COURANT >= VAL_EMA200_COURANT)  :#(FRONT_MONTANT_EMA200 == 1)  and and ( ORDER != LAST_ORDER ) :
                    if   ((VAL_ACHAT) <= (CINQ_POUR_CENT_VAL_ACHAT) ):
                            print("POINT DE VENTE MOINS 5%")                    
                            ORDER="SELL"
                            custom_info["SCENARIO"]="POINT DE VENTE MOINS 5% "
                            print(ORDER)
                            #LAST_ORDER="BUY"
                            EXEC_ORDER(dataframe)
                            VAL_ACHAT=dataframe.close.loc[val_mask_idxmin]
                            POINT_ENTRE_EMA200 = 0 #VEROUILAGE ACHAT ET VENTE NORMAL
                            
                    TAKE_GAIN_ABSOLUE=1200
                    global DIFF_GAIN_ABSOLUE
                    global GAIN_RELATIF
                    global NBR_CUMUL    
                    # if (int(GAIN_ABSOLUE) >= int(TAKE_GAIN_ABSOLUE)) and "VAL_ACHAT_INITIALE" in custom_info :

                    if "VAL_ACHAT_INITIALE" in custom_info :
                        custom_info["NBR_CUMUL"]=NBR_CUMUL
                        # custom_info["POINT_DE_VENTE_GAIN_ABSOLUE"]=GAIN_ABSOLUE
                        # print("POINT_DE_VENTE_GAIN_ABSOLUE: ",custom_info["POINT_DE_VENTE_GAIN_ABSOLUE"])
                        print("NBR_CUMUL=",NBR_CUMUL)
                        print("custom_info : NBR_CUMUL=",custom_info["NBR_CUMUL"])
                        if  NBR_CUMUL == 0 :
                            DIFF_GAIN_ABSOLUE = GAIN_ABSOLUE
                            # custom_info["DIFF_GAIN_ABSOLUE"]=DIFF_GAIN_ABSOLUE
                            NBR_CUMUL=1
                        else:
                            DIFF_GAIN_ABSOLUE=float(DIFF_GAIN_ABSOLUE)-float(GAIN_ABSOLUE) 
                            NBR_CUMUL=0
                            
                        DIFF_GAIN_ABSOLUE=np.round(DIFF_GAIN_ABSOLUE,decimals = 8)
                        print("GAIN_RELATIF=",GAIN_RELATIF)
                        print("DIFF_GAIN_ABSOLUE=",DIFF_GAIN_ABSOLUE)
                        custom_info["DIFF_GAIN_ABSOLUE"]=DIFF_GAIN_ABSOLUE
                        # GAIN_ABSOLUE=0
                        # custom_info["GAIN_ABSOLUE"]=GAIN_ABSOLUE
                        # if (float(DIFF_GAIN_ABSOLUE) < 0 and float(GAIN_RELATIF < 0)) :

                        if ( float(GAIN_RELATIF < 0) and ( DIFF_VAL_CLOSE_INF_VAL_CLOSE_N1 == True)) :
                            print("POINT DE VENTE GAIN_ABSOLUE")   
                            # LAST_ORDER="BUY"
                            ORDER="SELL"
                            custom_info["SCENARIO"]="POINT DE VENTE GAIN_ABSOLUE"
                            print(ORDER)
                            EXEC_ORDER(dataframe)
                            POINT_ENTRE_EMA200 = 0 #VEROUILAGE ACHAT ET VENTE NORMAL

                            # custom_info["POINT_DE_VENTE_GAIN_ABSOLUE"]=GAIN_ABSOLUE
                            # print("POINT_DE_VENTE_GAIN_ABSOLUE: ",custom_info["POINT_DE_VENTE_GAIN_ABSOLUE"])
                            # LAST_ORDER="SELL"
                        # exit()
                        # VAL_ACHAT=dataframe.close.loc[val_mask_idxmin]
                        #POINT_ENTRE_EMA200 = 0 #VEROUILAGE ACHAT ET VENTE NORMAL     
                        
                    # global POINT_SOMMET_HAUT_EMA200
                    # #if  (FRONT_MONTANT_EMA200 == 0 )   and (VAL_EMA15_COURANT < VAL_EMA200_COURANT) and (GAIN < 0)  and (int(VAL_ACHAT) <= int(CINQ_POUR_CENT_VAL_ACHAT)):
                    # if  (FRONT_MONTANT_EMA200 == 0 )   and (VAL_EMA15_COURANT < VAL_EMA200_COURANT) and (GAIN < 0)  and (POINT_SOMMET_HAUT_EMA200 == 1 ):
                    # #if  (FRONT_MONTANT_EMA200 == 0 )   and (GAIN < 0)  and (POINT_SOMMET_HAUT_EMA200 == 1 ):
                    #         print("POINT DE VENTE ABSOLUE EMA200: SIGNAL VENTE TOUTES COURBES")                    
                    #         #POINT_ENTRE_EMA200=0
                    #         print("POINT_ENTRE_EMA1H=1")
                    #         print("OK OK OK DERNIER_POINT_VENTE DANS TRAITEMENT_DERNIER_VENTE OK OK OK")
                    #         ORDER="SELL"
                    #         custom_info["SCENARIO"]="POINT DE VENTE ABSOLUE EMA200: SIGNAL VENTE TOUTES COURBES"
                    #         print(ORDER)
                    #         #LAST_ORDER="BUY"
                    #         EXEC_ORDER(dataframe)
                    #         VAL_ACHAT=dataframe.close.loc[val_mask_idxmin]
                    #         #POINT_ENTRE_EMA200 = 0 #VEROUILAGE ACHAT ET VENTE NORMAL
                    #         #DERNIER_POINT_VENTE=1
                    #         time.sleep(10)
                        
            #print("SORTIE DANS TRAITEMENT_DERNIER_VENTE\n")
        print("SORTIE DANS TRAITEMENT_DERNIER_VENTE\n")


def TRAITEMENT_SOMMET(dataframe,val_mask_idxmin) :
        print("\nENTRER DANS SOMMET:")
        #global VAL_EMA15_MAX
        global VAL_EMA15_PRECEDENT_LONG
        global VAL_EMA15_PRECEDENT
        global VAL_EMA15_PRECEDENT_COURT
        global VAL_EMA200_PRECEDENT
        global POINT_ENTRE_EMA200
        global GAIN_SOMMET
        global FLAG_BEST_NBR_TAILLE_BG
        global FRONT_MONTANT_EMA15
        global FRONT_MONTANT_EMA1H
        global FRONT_MONTANT_EMA1L
        global FRONT_MONTANT_EMA200
        global TYPE_FRONT_EMA15
        global TYPE_FRONT_EMA1L
        global TYPE_FRONT_EMA1H
        global TYPE_FRONT_EMA200
        global TYPE_FRONT_COURT_EMA15
        global TYPE_FRONT_COURT_EMA1L
        global TYPE_FRONT_COURT_EMA1H
        global TYPE_FRONT_COURT_EMA200
        global VAL_NBR_PREC_LONG
        global LAST_CROISEMENT_EMA200_GOLDEN_CROSS_EMA15

      
        """
        TEST_MODE_REEL=CALCUL_DATE_COURANTE(dataframe,val_mask_idxmin)
        if   TEST_MODE_REEL == 1 :
          val_mask_idxmin=last_index
        """
        """
        if FLAG_BEST_NBR_TAILLE_BG == 1 :
           val_mask_idxmin=DETECT_MODE_REEL(dataframe,val_mask_idxmin)
        """
        
        """
        last_index=len(dataframe)-1
        print("last_index=",last_index)
        if val_mask_idxmin >= last_index :
            val_mask_idxmin=last_index  
        """
            
        #global VAL_EMA200_PRECEDENT_LONG
        if val_mask_idxmin == 0 :
            nbr_dec=0
        else :
            nbr_dec=1
            
        # if val_mask_idxmin >= VAL_NBR_PREC_LONG :
        #     NBR_PREC_LONG=VAL_NBR_PREC_LONG
        # else :
        #     NBR_PREC_LONG=0
            
        NBR_PREC_LONG=VAL_NBR_PREC_LONG
 
        MASK_POINT_ENTRE_EMA15=val_mask_idxmin
        #mask_EMA15 = (dataframe.date >=  dataframe.loc[MASK_POINT_ENTRE_EMA15].date ) and (dataframe.date <= dataframe.loc[val_mask_idxmin].date)
        mask_EMA15 = (dataframe.date >=  dataframe.loc[MASK_POINT_ENTRE_EMA15].date ) #and (dataframe.date <= dataframe.loc[val_mask_idxmin].date)

        val_mask_EMA15_idxmax=dataframe['EMA15'].loc[mask_EMA15].idxmax()
        VAL_EMA15_MAX=dataframe.EMA15.loc[val_mask_EMA15_idxmax].astype(int)
        VAL_EMA15_PRECEDENT=dataframe.EMA15.loc[val_mask_idxmin-nbr_dec].astype(int)
        #VAL_EMA15_PRECEDENT_LONG=int(LAST_CROISEMENT_EMA200_GOLDEN_CROSS_EMA15.EMA15.astype(int))
        ##VAL_EMA15_PRECEDENT_LONG=dataframe.EMA15.loc[val_mask_idxmin-NBR_PREC_LONG].astype(int)
        
        #mask_ORG=(dataframe.date >= dataframe.loc[val_mask_idxmin_ORG].date) and (dataframe.date <= dataframe.iloc[-1].date)
        mask_ORG=(dataframe.date >= dataframe.loc[val_mask_idxmin_ORG].date) #and (dataframe.date <= dataframe.iloc[-1].date)

        val_mask_EMA200_idxmax=dataframe['EMA200'].loc[mask_ORG].idxmax()
        VAL_EMA200_MAX=dataframe.EMA200.loc[val_mask_EMA200_idxmax].astype(int)
        ##VAL_EMA15_PRECEDENT_COURT=dataframe.EMA15.loc[val_mask_idxmin-nbr_dec].astype(int)
        ##VAL_EMA15_COURANT=dataframe.EMA15.loc[val_mask_idxmin].astype(int)
        VAL_EMA200_COURANT=dataframe.EMA200.loc[val_mask_idxmin].astype(int)
        VAL_EMA200_PRECEDENT=dataframe.EMA200.loc[val_mask_idxmin-nbr_dec].astype(int)

        print("\nval_mask_EMA200_idxmax=",val_mask_EMA200_idxmax) 
        print("\nVAL_EMA200_MAX=",VAL_EMA200_MAX)    
        EMA200_MAX=dataframe.loc[val_mask_EMA200_idxmax]
        print("\nEMA200_MAX=\n",EMA200_MAX)          
        print("\nINDEX COURANT=",val_mask_idxmin)
        TRAME_COURANTE=dataframe.loc[val_mask_idxmin]
        print("TRAME_COURANTE=\n",TRAME_COURANTE)
        print("VAL_EMA15_PRECEDENT_COURT=",VAL_EMA15_PRECEDENT_COURT)
        print("VAL_EMA15_COURANT=",VAL_EMA15_COURANT)
        print("VAL_EMA200_COURANT=",VAL_EMA200_COURANT)
        """
        print("VAL_EMA200_MAX - VAL_EMA200_idxmin_ORG =",VAL_EMA200_MAX - VAL_EMA200_idxmin_ORG)
        print("VAL_EMA200_MAX - VAL_EMA200_COURANT =",VAL_EMA200_MAX - VAL_EMA200_COURANT)
        print("\nDataframe MASK EMA200 MIN=\n",dataframe[["date","EMA200"]].loc[val_mask_idxmin_ORG])
        print("\nDataframe MASK EMA200 MAX=\n",dataframe[["date","EMA200"]].loc[val_mask_idxmax_ORG])
        print("INDEX idxmin=",val_mask_ORG_idxmin)
        print("INDEX idxmax=",val_mask_ORG_idxmax)
        """
        EMA1L=dataframe.EMA1L.loc[val_mask_idxmin].astype(int)
        EMA1H=dataframe.EMA1H.loc[val_mask_idxmin].astype(int)
        #VAL_EMA1H_COURANT=dataframe.EMA1H.loc[val_mask_idxmin].astype(int)
        EMA15=dataframe.EMA15.loc[val_mask_idxmin].astype(int)
        DIFF_EMA200_EMA15=dataframe.DIFF_EMA200_EMA15.loc[val_mask_idxmin].astype(int)
        if (POINT_ENTRE_EMA200 == 1) and ( "VAL_ACHAT" in custom_info) : #and (LAST_ORDER == "BUY") : #and ( "VAL_ACHAT" in custom_info):
           VAL_VENTE=dataframe.close.loc[val_mask_idxmin]
           VAL_VENTE=(float(VAL_VENTE)*MULTIP)/100
           VAL_VENTE=np.round(VAL_VENTE,decimals = 1)
           #VAL_VENTE=int(VAL_VENTE)      
           VAL_ACHAT=float(custom_info["VAL_ACHAT"])
           VAL_ACHAT=(float(VAL_ACHAT)*MULTIP)/100
           VAL_ACHAT=np.round(VAL_ACHAT,decimals = 1)
           #VAL_ACHAT=int(VAL_ACHAT) 
           GAIN_SOMMET=(VAL_VENTE - VAL_ACHAT)
           print("GAIN_SOMMET=",(GAIN_SOMMET))

        print(TYPE_FRONT_EMA200)
        print(TYPE_FRONT_COURT_EMA15)
        print(TYPE_FRONT_EMA1L)
        print(TYPE_FRONT_EMA1H)
        print(TYPE_FRONT_EMA15)
        print("VAL_EMA15_COURANT-EMA1L)=",(EMA15-EMA1L))
        print("(VAL_EMA15_COURANT-EMA1L <= 10 )=",(EMA15-EMA1L <= 10 ))
        print("DIFF_EMA200_EMA15=",abs(DIFF_EMA200_EMA15))

        if (VAL_EMA15_MAX-VAL_EMA15_COURANT == 0 ) and (VAL_EMA15_COURANT-VAL_EMA15_PRECEDENT == 0 )  :
            print("\nINDEX COURANT=\n",dataframe.loc[val_mask_idxmin])
            if VAL_EMA15_COURANT-VAL_EMA15_PRECEDENT_LONG < 0 :
                TYPE_EMA15="BAS"
                
        if (FRONT_MONTANT_EMA200 == 1) and (FRONT_MONTANT_EMA15 == 1 )  and (FRONT_MONTANT_COURT_EMA15 == 0 ) and (FRONT_MONTANT_EMA1H == 1 ) and (FRONT_MONTANT_COURT_EMA1H == 0 ) \
           and (VAL_EMA15_COURANT-EMA1L <= 10 ) and (FRONT_NEUTRE_COURT_EMA200 == 1) and (TYPE_BG == "BG_VERTE") :
                TYPE_EMA15="HAUT"
                print("POINT HAUT EMA15 ON QUITTE LA COURBE")
                #exit()

        if (VAL_EMA200_MAX-VAL_EMA200_COURANT == 0 ) and (VAL_EMA200_COURANT-VAL_EMA200_PRECEDENT == 0 )  :
            print("\nINDEX COURANT=\n",dataframe.loc[val_mask_idxmin])
            if VAL_EMA200_COURANT-VAL_EMA200_PRECEDENT_LONG < 0 :
                TYPE="BAS"
                print("POINT BAS ON QUITTE LA COURBE")
        """        
        if  (VAL_EMA200_MAX-VAL_EMA200_COURANT == 0 ) and (FRONT_MONTANT_EMA15 == 1 )  and (FRONT_MONTANT_COURT_EMA15 == 0 ) and (FRONT_MONTANT_EMA200 == 1 ) \
        and (FRONT_NEUTRE_COURT_EMA200 == 1) : #  and (FRONT_MONTANT_COURT_EMA200 == 1 ) :  
        """        
        VAL_EMA1H_COURANT=dataframe.EMA1H.loc[val_mask_idxmin].astype(int)
        EMA1L=dataframe.EMA1L.loc[val_mask_idxmin].astype(int)

        #if (val_mask_idxmin > val_mask_EMA200_idxmax ) and (FLAG_BEST_NBR_TAILLE_BG == 1) :    
        if (FRONT_NEUTRE_EMA200 == 1) and abs(VAL_EMA1H_COURANT - VAL_EMA200_COURANT <= 1 ) and abs(EMA1L - VAL_EMA200_COURANT <= 1 ) :
            TYPE="HAUT_INTERMEDIARE_EMA200"
            #if (VAL_EMA15_PRECEDENT_COURT == 0 ) and (VAL_EMA15_COURANT >= VAL_EMA200_COURANT):
            if (VAL_EMA15_COURANT >= VAL_EMA200_COURANT) or  (FRONT_MONTANT_COURT_EMA200 == 0) and (VAL_EMA15_COURANT <= VAL_EMA200_COURANT) :
                TYPE="HAUT_FINALE_EMA200"
                print("POINT HAUT ON QUITTE LA COURBE")
                print("\n SOMMET EMA200 ",TYPE)
                print("VAL_EMA200_COURANT=",VAL_EMA200_COURANT)
                print("VAL_EMA1H_COURANT=",VAL_EMA1H_COURANT)
                print("VAL_EMA200_PRECEDENT=",VAL_EMA200_PRECEDENT)
                print("VAL_EMA200_PRECEDENT_LONG=",VAL_EMA200_PRECEDENT_LONG)
                print("VAL_EMA200_COURANT-VAL_EMA200_PRECEDENT=",VAL_EMA200_COURANT-VAL_EMA200_PRECEDENT)
                print("VAL_EMA200_COURANT-VAL_EMA200_PRECEDENT_LONG=",VAL_EMA200_COURANT-VAL_EMA200_PRECEDENT_LONG)
                print("VAL_EMA1H_COURANT-VAL_EMA200_COURANT=",VAL_EMA1H_COURANT-VAL_EMA200_COURANT)
                #POINT_ENTRE_EMA200=0
                #DERNIER_POINT_VENTE=1
               # exit()
                
        if  (VAL_EMA200_MAX-VAL_EMA200_COURANT <  0) :
               print("\n EMA200 DECROISSANTE")
        print("SORTIE DE SOMMET\n")

def convert_currency(val):
    """
    Convert the string number value to a float
     - Remove $
     - Remove commas
     - Convert to float type
    """
    new_val = val.replace(',','').replace('$', '')
    return float(new_val)

def CALCUL_DATE_COURANTE(dataframe,val_mask_idxmin):
    global DATE_DU_PASSE
    DATE_COURANTE=dataframe.date.loc[val_mask_idxmin]
    DATE_COURANTE=DATE_COURANTE.strftime("%Y-%m-%d %H:%M:%S")
    DATE_COURANTE=DATE_COURANTE[:-3]
    from datetime import datetime, timedelta
    now=datetime.utcnow()
    new_hour=now  #+ timedelta(hours=2)   
    new_hour=new_hour.strftime("%Y-%m-%d %H:%M:%S")
    new_hour=new_hour.split(".")[0]
    new_hour=new_hour[:-6]
    if (DATE_DU_PASSE == 0) :
        print("new_hour :",new_hour)
        print("DATE_COURANTE :",DATE_COURANTE)
    if  new_hour in str(DATE_COURANTE) :
       #print("IMPORTE df: \n",dataframe.tail())
       print("VALIDATION MODE REEL")
       return 1
    # else:
    #    if (DATE_DU_PASSE == 0) :
    #        print("DATE DU PASSE : PAS DE MODE REEL")
    #        DATE_DU_PASSE=1
    #    return 0
def CALCULE_TAILLE_BOUGIE(TAILLE_BG,MULTIP) :
      # print("ENTRER DANS CALCULE_TAILLE_BOUGIE:")
      # TAILLE_BG=-0.00012608000000000064
      # TAILLE_BG=-9.35e-05
     
        import numpy as np
        TAILLE_BG=np.round(float(TAILLE_BG),decimals = MULTIP)
        if "e-" in str(TAILLE_BG) :
            # TAILLE_BG=str(TAILLE_BG).split(".")[0]
            TAILLE_BG=(str(TAILLE_BG).split("e-")[0])
            # return TAILLE_BG
        if float(TAILLE_BG) != 0 :
            TAILLE_BG=int(str(TAILLE_BG).replace("0","").replace(".",""))
        # print("TAILLE_BG:",TAILLE_BG)
        # print("SORTIR DANS CALCULE_TAILLE_BOUGIE:")
        return TAILLE_BG


def TRAITEMENT_BOUGIE(dataframe,val_mask_idxmin) :
    global MULTIP 
    global TAILLE_BG
    global TAILLE_BG_N1
    global TAILLE_BG_N2
    global TAILLE_BG_N3
    global TYPE_BG
    global TYPE_BG_N1
    global TYPE_BG_N2
    global TYPE_BG_N3
    global TYPE_BG_N4
    global VAL_OPEN
    global VAL_CLOSE
    global VAL_OPEN_N1
    global VAL_CLOSE_N1
    global VAL_OPEN_N2
    global VAL_CLOSE_N2    
    global VAL_OPEN_N3
    global VAL_CLOSE_N3
    global CUMUL_TAILLE_BG_ROUGE
    global CUMUL_TAILLE_BG_VERTE
    global CUMUL_TAILLE_BG_N1_N2_N3
    global CUMUL_TAILLE_BG_N1_N2
    global FLAG_BEST_NBR_TAILLE_BG
    global FRONT_MONTANT_COURT_EMA1H
    global FRONT_MONTANT_COURT_EMA1H_N1
    global FRONT_MONTANT_COURT_EMA1H_N2
    global FRONT_MONTANT_COURT_EMA1H_N3 
    global FRONT_MONTANT_COURT_EMA1H_N4  
    import numpy as np
    global GAIN1
    
    print("\nENTRER DANS TRAITEMENT_BOUGIE:")
    try:

        last_index=len(dataframe)-1
        val_mask_idxmin = last_index
        
        if val_mask_idxmin <= 3 :
           RANG1=0
           RANG2=0
           RANG3=0
    
        else:
           k=1
           RANG1=1+k
           RANG2=2+k
           RANG3=3+k
    
       # if FLAG_BEST_NBR_TAILLE_BG == 1 :
            #val_mask_idxmin+=1
            
        #if val_mask_idxmin == last_index :
           #val_mask_idxmin=val_mask_idxmin-1
        
        print("val_mask_idxmin:",val_mask_idxmin)
        VAL_OPEN=(float(dataframe['open'].iloc[val_mask_idxmin]))
        VAL_CLOSE=(float(dataframe['close'].iloc[val_mask_idxmin]))
        VAL_OPEN_N1=(float(dataframe['open'].iloc[val_mask_idxmin-RANG1]))
        VAL_CLOSE_N1=(float(dataframe['close'].iloc[val_mask_idxmin-RANG1-k]))
        VAL_OPEN_N2=(float(dataframe['open'].iloc[val_mask_idxmin-RANG2]))
        VAL_CLOSE_N2=(float(dataframe['close'].iloc[val_mask_idxmin-RANG2-k-1]))
        VAL_OPEN_N3=(float(dataframe['open'].iloc[val_mask_idxmin-RANG3]))
        VAL_CLOSE_N3=(float(dataframe['close'].iloc[val_mask_idxmin-RANG3-k-1]))
        
        # VAL_OPEN=(format(VAL_OPEN,'.8f'))
        # VAL_CLOSE=(format(VAL_CLOSE,'.8f'))
        # VAL_OPEN_N1=(format(VAL_OPEN_N1,'.8f'))
        # VAL_CLOSE_N1=(format(VAL_CLOSE_N1,'.8f'))
        # VAL_OPEN_N2=(format(VAL_OPEN_N2,'.8f'))
        # VAL_CLOSE_N2=(format(VAL_CLOSE_N2,'.8f'))
        # VAL_OPEN_N3=(format(VAL_OPEN_N3,'.8f'))
        # VAL_CLOSE_N3=(format(VAL_CLOSE_N3,'.8f'))


    
        
        VAL_CLOSE_INT=VAL_CLOSE
        MULTIP=len(str(VAL_CLOSE))
        print("MULTIP:",MULTIP)
        
        print("VAL_OPEN=",VAL_OPEN)
        print("VAL_CLOSE=",VAL_CLOSE)
        TAILLE_BG=float(VAL_CLOSE)-float(VAL_OPEN)
        # print("TAILLE_BG BEFORE:",TAILLE_BG)
        # TAILLE_BG=format(TAILLE_BG,'.8f')
        # print("TAILLE_BG MODIF:",TAILLE_BG)
        TAILLE_BG=CALCULE_TAILLE_BOUGIE(TAILLE_BG,MULTIP) 
        print("TAILLE_BG:",TAILLE_BG)
    
        # # TAILLE_BG=round(TAILLE_BG,MULTIP)
        # TAILLE_BG=-0.00012608000000000064
        # TAILLE_BG=-9.35e-05
        # TAILLE_BG=np.round(TAILLE_BG,decimals = MULTIP)
        # if "e-" in str(TAILLE_BG) :
        #     TAILLE_BG=str(TAILLE_BG).split(".")[0]
        # TAILLE_BG=int(str(TAILLE_BG).replace("0","").replace(".",""))
        # print("TAILLE_BG:",TAILLE_BG)
        
        print("VAL_OPEN_N1=",VAL_OPEN_N1)
        print("VAL_CLOSE_N1=",VAL_CLOSE_N1)
        TAILLE_BG_N1=float(VAL_CLOSE_N1)-float(VAL_OPEN_N1)
        TAILLE_BG_N1=CALCULE_TAILLE_BOUGIE(TAILLE_BG_N1,MULTIP) 
        print("TAILLE_BG_N1=",TAILLE_BG_N1)
        
        print("VAL_OPEN_N2=",VAL_OPEN_N2)
        print("VAL_CLOSE_N2=",VAL_CLOSE_N2)
        TAILLE_BG_N2=float(VAL_CLOSE_N2)-float(VAL_OPEN_N2)
        TAILLE_BG_N2=CALCULE_TAILLE_BOUGIE(TAILLE_BG_N2,MULTIP) 
        print("TAILLE_BG_N2=",TAILLE_BG_N2)
    
        print("VAL_OPEN_N3=",VAL_OPEN_N3)
        print("VAL_CLOSE_N3=",VAL_CLOSE_N3)
        TAILLE_BG_N3=float(VAL_CLOSE_N3)-float(VAL_OPEN_N3)
        TAILLE_BG_N3=CALCULE_TAILLE_BOUGIE(TAILLE_BG_N3,MULTIP) 
        print("TAILLE_BG_N3=",TAILLE_BG_N3)  
        
        # exit()
        
        #"""
        
        if TAILLE_BG > 0  :
            TYPE_BG="BG_VERTE"
            print("TYPE_BG:",TYPE_BG)
    
        if TAILLE_BG_N1 > 0 :
            TYPE_BG_N1="BG_VERTE"
            print("TYPE_BG_N1:",TYPE_BG_N1)
            # TYPE_BG=TYPE_BG_N1
            # TAILLE_BG=TAILLE_BG_N1
    
        if TAILLE_BG_N2 > 0 :
            TYPE_BG_N2="BG_VERTE"
            print("TYPE_BG_N2:",TYPE_BG_N2)
            
        if TAILLE_BG_N3 > 0 :
            TYPE_BG_N3="BG_VERTE"
            print("TYPE_BG_N3:",TYPE_BG_N3)
            
        if TAILLE_BG <= 0 :
            TYPE_BG="BG_ROUGE"
        if TAILLE_BG_N1 <= 0 :
            TYPE_BG_N1="BG_ROUGE"
        if TAILLE_BG_N2 <= 0 :
            TYPE_BG_N2="BG_ROUGE"
        if TAILLE_BG_N3 <= 0 :
            TYPE_BG_N3="BG_ROUGE"
            
            
        # if (( FRONT_MONTANT_EMA1L == 1) and  ( FRONT_MONTANT_EMA1H == 1)) :
        #   TYPE_BG="BG_VERTE"
        # else :
        #   TYPE_BG="BG_ROUGE"            
            
        # if GAIN1 > 0 or (( FRONT_MONTANT_EMA1L == 1) or  ( FRONT_MONTANT_EMA1H == 1)):
        #   TYPE_BG="BG_VERTE"
         
        # if GAIN1 < 0 :
        #   TYPE_BG="BG_ROUGE"            
            
        # VAL_OPEN=(format(VAL_OPEN,'.8f'))
        # VAL_CLOSE=(format(VAL_CLOSE,'.8f'))
        # VAL_OPEN_N1=(format(VAL_OPEN_N1,'.8f'))
        # VAL_CLOSE_N1=(format(VAL_CLOSE_N1,'.8f'))
        # VAL_OPEN_N2=(format(VAL_OPEN_N2,'.8f'))
        # VAL_CLOSE_N2=(format(VAL_CLOSE_N2,'.8f'))
        # VAL_OPEN_N3=(format(VAL_OPEN_N3,'.8f'))
        # VAL_CLOSE_N3=(format(VAL_CLOSE_N3,'.8f'))

        #""" 
        
        #NEW TEST      
        """ 
        if (FRONT_MONTANT_COURT_EMA1H == 1):
            TYPE_BG="BG_VERTE"
        else:
            TYPE_BG="BG_ROUGE"
        print("FRONT_MONTANT_COURT_EMA1H:",FRONT_MONTANT_COURT_EMA1H)
        print("TYPE_BG:",TYPE_BG)
        """ 
        """
        if (FRONT_MONTANT_COURT_EMA1H_N1 > 0) and TAILLE_BG >= 0 :
            TYPE_BG_N1="BG_VERTE"
        else:
            TYPE_BG_N1="BG_ROUGE"
        TYPE_BG=TYPE_BG_N1
        print("FRONT_MONTANT_COURT_EMA1H_N1:",FRONT_MONTANT_COURT_EMA1H_N1)
        #print("TYPE_BG_N1:",TYPE_BG_N1)
            
        if (FRONT_MONTANT_COURT_EMA1H_N2 > 0) and TAILLE_BG_N1 >= 0 :
            TYPE_BG_N2="BG_VERTE"
        else:
            TYPE_BG_N2="BG_ROUGE"
        TYPE_BG_N1=TYPE_BG_N2
        print("FRONT_MONTANT_COURT_EMA1H_N2:",FRONT_MONTANT_COURT_EMA1H_N2)
        #print("TYPE_BG_N2:",TYPE_BG_N2)
        print("TYPE_BG_N1:",TYPE_BG_N1)
        
            
        if (FRONT_MONTANT_COURT_EMA1H_N3 > 0) and TAILLE_BG_N2 >= 0 :
            TYPE_BG_N3="BG_VERTE"
        else:
            TYPE_BG_N3="BG_ROUGE"  
        TYPE_BG_N2=TYPE_BG_N3
        print("FRONT_MONTANT_COURT_EMA1H_N3:",FRONT_MONTANT_COURT_EMA1H_N3)
        #print("TYPE_BG_N3:",TYPE_BG_N3)
        print("TYPE_BG_N2:",TYPE_BG_N2)
               
        if (FRONT_MONTANT_COURT_EMA1H_N4 > 0) and TAILLE_BG_N3 >= 0 :
            TYPE_BG_N4="BG_VERTE"
        else:
            TYPE_BG_N4="BG_ROUGE"   
        TYPE_BG_N3=TYPE_BG_N4
        print("FRONT_MONTANT_COURT_EMA1H_N4:",FRONT_MONTANT_COURT_EMA1H_N4)
        #print("TYPE_BG_N4:",TYPE_BG_N4)
        print("TYPE_BG_N3:",TYPE_BG_N3)
        """
    
        global CUMUL_TAILLE_BG_VERTE 
        global CUMUL_TAILLE_BG_ROUGE
    
        CUMUL_TAILLE_BG_VERTE=0
        CUMUL_TAILLE_BG=(int(TAILLE_BG+TAILLE_BG_N1+TAILLE_BG_N2+TAILLE_BG_N3)) 
        CUMUL_TAILLE_BG_N1_N2=(int(TAILLE_BG_N1+TAILLE_BG_N2))
        CUMUL_TAILLE_BG_N1_N2_N3=(int(TAILLE_BG_N1+TAILLE_BG_N2+TAILLE_BG_N3))
    
    
        #if TYPE_BG=="BG_VERTE" and  TYPE_BG_N1=="BG_VERTE" and  TYPE_BG_N2=="BG_VERTE" :
        if CUMUL_TAILLE_BG > 0:
            CUMUL_TAILLE_BG_VERTE=CUMUL_TAILLE_BG 
            CUMUL_TAILLE_BG_ROUGE=0
        else:    
            CUMUL_TAILLE_BG_ROUGE=CUMUL_TAILLE_BG 
            CUMUL_TAILLE_BG_VERTE=0
        #exit()
    except Exception as j:
        pass
    print("SORTIE DANS TRAITEMENT_BOUGIE")
    
def MAIN(dataframe) :
  # try:
     global FIRST_INIT_TRAITEMENT_REELLE
     FIRST_INIT_TRAITEMENT_REELLE=""
     global i
     i=0     
     while True : #index_courant <= last_index :
        global VAL_CLOSE_INT
        global TAILLE_BG
        global TAILLE_BG_N1
        global TAILLE_BG_N2
        global TAILLE_BG_N3
        global TYPE_BG
        global TYPE_BG_N1
        global TYPE_BG_N2
        global TYPE_BG_N3
        global VAL_OPEN
        global VAL_CLOSE
        global VAL_OPEN_N1
        global VAL_CLOSE_N1
        global VAL_OPEN_N2
        global VAL_CLOSE_N2    
        global VAL_OPEN_N3
        global VAL_CLOSE_N3
        global LEN_LISTE_ACHAT_VENTE
        global FLAG_BEST_NBR_TAILLE_BG
        global val_mask_idxmin
        global last_index
        global NBR_TAILLE_BG
        global LAST_DATE_VENTE
        global TRAITEMENT_REELLE
        global DERNIER_POINT_VENTE
        global GAIN
        global GAIN_RELATIF
        global GAIN_ABSOLUE
        global MODE_GAIN
        global COMPTEUR_BUY_INITIAL
        global COMPTEUR_BUY_SELL
        global COMPTEUR_SELL
        global COMPTEUR_TEMPORELLE
        global NBR_COMPTEUR_TEMPORELLE
        global PREVIOUS_MODE
        global DERNIERE_VENTE_GAIN_ABSOLUE
        global custom_info
        global ORDER
        global LAST_ORDER
        global FLAG_SIMULATION_GLOBAL
        global VAL_ACHAT_INITIALE
        global MODE_GAIN
        global NBR_CUMUL
        global MULTIP 
        global CUMUL_TAILLE_BG_ROUGE
        global CUMUL_TAILLE_BG_VERTE
        global CUMUL_TAILLE_BG_N1_N2_N3
        global CUMUL_TAILLE_BG_N1_N2
        global LAST_CROISEMENT_EMA200_GOLDEN_CROSS_EMA15_INDEX
        global DEB_SIMULATION
        global dataframe_date

        signal.signal(signal.SIGINT, PKILL)
        signal.signal(signal.SIGTERM, PKILL)
        if FLAG_BEST_NBR_TAILLE_BG == 1 :
            dataframe=RECUPERATION_DE_LA_DERNIERE_TRAME()
            dataframe=populate_indicators(dataframe)
            
            
        #"""
        ###val_mask_idxmin=DETECT_MODE_REEL(dataframe,val_mask_idxmin)
        last_index=len(dataframe)-1
        print("last_index=",last_index)
        if val_mask_idxmin >= last_index :
            val_mask_idxmin=last_index   
        # du dernier index 
        #last_index=len(dataframe)-1
       # """
        #dataframe=RECUPERATION_DE_LA_DERNIERE_TRAME()
        """
        TEST_MODE_REEL=CALCUL_DATE_COURANTE(dataframe,val_mask_idxmin)
        if   TEST_MODE_REEL == 1 :
          val_mask_idxmin=last_index
        """      
        
        #last_index=dataframe.index[-1]
        last_index=len(dataframe)-1
        if val_mask_idxmin == last_index :
           #val_mask_idxmin=val_mask_idxmin-1
           FLAG_BEST_NBR_TAILLE_BG=1
           
        #FLAG_BEST_NBR_TAILLE_BG=1
        
        #MODE SIMULATION ACTIF
        TRAITEMENT_REELLE="SIMULATION"
        #SIMULATION FORCE QUELQUE SOIT LE MODE DE VENTE
        FLAG_SIMULATION_GLOBAL=1

        if (val_mask_idxmin != last_index) or (FLAG_BEST_NBR_TAILLE_BG == 1):
              
            VAL_EMA1H_COURANT=dataframe.EMA1H.loc[val_mask_idxmin].astype(int)
            VAL_EMA200_COURANT=dataframe.EMA200.loc[val_mask_idxmin].astype(int)
            if (TYPE == "HAUT_FINALE_EMA200") and ( int(VAL_EMA1H_COURANT - VAL_EMA200_COURANT) <= -50) :
                print("\nPOINT HAUT ON QUITTE LA COURBE")

            if FLAG_BEST_NBR_TAILLE_BG == 0 or TRAITEMENT_REELLE == "SIMULATION" :
                global  FLAG_SIMULATION
                FLAG_SIMULATION=1
            else:
                FLAG_SIMULATION=0
            #DERNIER_POINT_VENTE=1
            DERNIER_POINT_VENTE=0

            # try:  
            while True :
               # while True :
                RECUP_LAST_PRICE_IN_FILE()
                TRAITEMENT_ANTI_FLUCTUATION(dataframe,val_mask_idxmin)
                # SYNCHRONISATION_INDICE(dataframe,val_mask_idxmin)
                DETECTION_FRONT(dataframe,val_mask_idxmin)
                TRAITEMENT_BOUGIE(dataframe,val_mask_idxmin)
                # TRAITEMENT_SOMMET(dataframe,val_mask_idxmin)
                # TRAITEMENT_DERNIER_VENTE(dataframe,val_mask_idxmin)
                ULTIMATE_NINJA_NEW(dataframe,val_mask_idxmin)
                #DETECT_LAST_SELL(dataframe,val_mask_idxmin)
                

                if (int(VAL_EMA1H_COURANT) >= int(VAL_EMA15_COURANT)) :
                    DERNIER_POINT_VENTE=0
                    
                #if (DERNIER_POINT_VENTE == 0): # or (FRONT_NEUTRE_COURT_EMA200 == 1) :
                    #ULTIMATE_NINJA(dataframe,val_mask_idxmin)
                    #ULTIMATE_NINJA_BIS(dataframe,val_mask_idxmin)
                    #ULTIMATE_NINJA_NEW(dataframe,val_mask_idxmin)
                    #DETECT_LAST_SELL(dataframe,val_mask_idxmin)
               # else:
                   # DETECT_LAST_SELL(dataframe,val_mask_idxmin)
                #"""
                    #TRANSITION_ACHAT_VENTE(dataframe,val_mask_idxmin)
                    #TRAITEMENT_ACHAT(dataframe,val_mask_idxmin)
                    #TRAITEMENT_VENTE(dataframe,val_mask_idxmin)            
                #"""
            
                if FLAG_BEST_NBR_TAILLE_BG == 0 :
                    print("FLAG_BEST_NBR_TAILLE_BG=0") 
                    break          
                #"""
                if FLAG_BEST_NBR_TAILLE_BG == 1 :
                    #custom_info["ORDER"] 
                    print("LAST_ORDER=",LAST_ORDER) 
                    #if LAST_ORDER != custom_info["ORDER"] :
                    #if (COMPTEUR_TEMPORELLE == 2) or (LAST_ORDER == custom_info["ORDER"] ) :
                    NBR_COMPTEUR_TEMPORELLE=0
                    if (COMPTEUR_TEMPORELLE == NBR_COMPTEUR_TEMPORELLE)  :
                        COMPTEUR_TEMPORELLE=0
                        break     
                    COMPTEUR_TEMPORELLE+=1
                    print("COMPTEUR T{}={}".format(COMPTEUR_TEMPORELLE,val_mask_idxmin))
                    val_mask_idxmin-=1
                    print("RECUL COMPTEUR T1=",val_mask_idxmin)
                #"""
            # #"""
            # except Exception as j:
            #     pass
            #   print(f'\nError TRAITEMENT ACHAT VENTE : {j}')
            #   time.sleep(1)
            # #"""            
        """
        if FLAG_BEST_NBR_TAILLE_BG == 0 :
            print("FLAG_BEST_NBR_TAILLE_BG=",FLAG_BEST_NBR_TAILLE_BG)
            exit()  
        """
        """
        if FLAG_BEST_NBR_TAILLE_BG == 1 :
            print('custom_info["ORDER"]=',custom_info["ORDER"]) 
            LAST_ORDER=custom_info["LAST_ORDER"]
            print("LAST_ORDER=",LAST_ORDER) 
            exit()
        #exit()
        """
        
        #SIMULATION FORCE QUELQUE SOIT LE MODE DE VENTE
        #FLAG_SIMULATION_GLOBAL=1
        #Quand on atteind la BOUGIE COURANTE ON SORT ON CALCULE LA MEILLEUR TAILLE DE BOUGIE
        #UNE FOIS  CALCULE LA MEILLEUR TAILLE DE BOUGIE ON BOUCLE A L'INFINIE SUR LA DERNIER BOUGIE
        #if (val_mask_idxmin == last_index) and (FLAG_BEST_NBR_TAILLE_BG == 0) :
           #FLAG_BEST_NBR_TAILLE_BG=1
           
        if FLAG_BEST_NBR_TAILLE_BG == 0 :
            print("\nAPPEL DE LA NOUVELLE BOUGIE DANS SIMULATION  SYMBOL:{} ".format(symbol))
            print("\nFLAG_BEST_NBR_TAILLE_BG=",FLAG_BEST_NBR_TAILLE_BG)
            print("val_mask_idxmin=",val_mask_idxmin)
            val_mask_idxmin+=1
            """
            if val_mask_idxmin == last_index :
                val_mask_idxmin=val_mask_idxmin-1
            else:
                val_mask_idxmin+=1
            """
            print("last_index=",last_index)
            print("DANS SIMULATION df: \n",dataframe.tail())
            #DEB_SIMULATION=1
            FIRST_INIT_TRAITEMENT_REELLE=0
        else:
            #APPEL DE LA NOUVELLE BOUGIE DANS REELE
            print("\n SYMBOL:{} !!!! TRAITEMENT REELLE !!!! TRAITEMENT REELLE  APPEL DE LA NOUVELLE BOUGIE REELLE !!!! TRAITEMENT REELLE FIRST_INIT_TRAITEMENT_REELLE: {}".format(symbol,FIRST_INIT_TRAITEMENT_REELLE))
            print("\nFLAG_BEST_NBR_TAILLE_BG=",FLAG_BEST_NBR_TAILLE_BG)
            print("NBR_TAILLE_BG",NBR_TAILLE_BG)
            print("DANS  TRAITEMENT REELLE last_index=",last_index)
            global val_mask_idxmin_ORG
            val_mask_idxmin=last_index

            #MODE SIMULATION ACTIF
            TRAITEMENT_REELLE="SIMULATION"
            #SIMULATION FORCE QUELQUE SOIT LE MODE DE VENTE
            FLAG_SIMULATION_GLOBAL=1
            
            if FIRST_INIT_TRAITEMENT_REELLE == 0 :
            #if DEB_SIMULATION == 1 :
               #if LAST_ORDER =="BUY" :
                   #LAST_ORDER="SELL"
               """    
               if  ("MODE_GAIN" in  custom_info) :
                if (not "GAIN NEGATIF" in custom_info["MODE_GAIN"]) :                   
                   custom_info={}
               """    
               DEB_SIMULATION=0
               last_index=len(dataframe)-1
               val_mask_idxmin=last_index
               # COMPTEUR_BUY_INITIAL=0
               COMPTEUR_SELL=0
               DERNIER_POINT_VENTE=0 #INITIALISATION DES PARAMETRETRE D'ACHAT EN MODE REEL
               #custom_info={}
               custom_info["ACHAT_EN_DESSOUS_EMA200"]=2
               custom_info["CUMUL_GAIN_ABSOLUE"]=0
               custom_info["POINT_DE_VENTE_GAIN_ABSOLUE"]=0
               # custom_info["CUMUL_GAIN_RELATIF"]=0
               #POINT_DE_VENTE_GAIN_ABSOLUE=0
               FIRST_INIT_TRAITEMENT_REELLE=1
               GAIN=0
               # GAIN_RELATIF=0
               GAIN_ABSOLUE=0
               #VAL_ACHAT_INITIALE=0
               MODE_GAIN="GAIN_ABSOLUE"
               custom_info["MODE_GAIN"]=MODE_GAIN
               custom_info["VAL_ACHAT_INITIALE"]=""
               #VAL_ACHAT_INITIALE=0
               # ORDER="ORDER"
               # LAST_ORDER="SELL"
               NBR_CUMUL=0
               """               
               custom_info["POINT_DE_VENTE_GAIN_ABSOLUE"]=""
               POINT_DE_VENTE_GAIN_ABSOLUE=0
 
               COMPTEUR_BUY_SELL=0
               PREVIOUS_MODE=""
               DERNIERE_VENTE_GAIN_ABSOLUE=0
               """
               
            """
            while True :
                RESTART_ONE_PAIR(symbol,timeframe)
                dataframe=RECUPERATION_DE_LA_DERNIERE_TRAME()
                last_index=len(dataframe)-1
                DATE_COURANTE=dataframe.date.loc[last_index]
                DATE_COURANTE=DATE_COURANTE.strftime("%Y-%m-%d %H:%M:%S")
                DATE_COURANTE=DATE_COURANTE[:-3]
                from datetime import datetime, timedelta
                now=datetime.utcnow()
                new_hour=now  + timedelta(hours=2)   
                new_hour=new_hour.strftime("%Y-%m-%d %H:%M:%S")
                new_hour=new_hour.split(".")[0]
                new_hour=new_hour[:-3]
                print("new_hour :",new_hour)
                print("DATE_COURANTE :",DATE_COURANTE)
                if  new_hour in str(DATE_COURANTE) :
                   print("IMPORTE df: \n",dataframe.tail())
                   break
                time.sleep(2)
            """
            #Chargement de la derniere donnée 

            """
            dataframe=RECUPERATION_DE_LA_DERNIERE_TRAME()
            dataframe=populate_indicators(dataframe)
            val_mask_idxmin=DETECT_MODE_REEL(dataframe,val_mask_idxmin)
            last_index=len(dataframe)-1
            print("last_index=",last_index)
            if val_mask_idxmin >= last_index :
                val_mask_idxmin=last_index   
            # du dernier index 
            last_index=len(dataframe)-1
            """
 
            print("\nLAST_DATE_VENTE=",LAST_DATE_VENTE)
            #mask = (dataframe.loc[LAST_DATE_VENTE].date  <= dataframe.date <=  dataframe.loc[last_index].date )
            if  LAST_DATE_VENTE == "" :
                mask = (dataframe_date.date <=  dataframe_date.loc[last_index].date )
            else:
                mask = (dataframe_date.date >= LAST_DATE_VENTE) and (dataframe_date.date <=  dataframe_date.loc[last_index].date )
    
            #val_mask_idxmin_ORG=dataframe['EMA200'].loc[mask].idxmin()
            if val_mask_idxmin_ORG < 0 :
                val_mask_idxmin_ORG=0
                
               
            print("\nval_mask_idxmin_ORG=",val_mask_idxmin_ORG)
            print("last_index=",last_index)
            #print("DFINFO: \n",dataframe.info())
            print("dataframe :\n",dataframe.tail())
            #print("\ndataframe GOLDEN CROSS INDEX ILOC idx_EMA200_EMA15 > EMA15 :",LAST_CROISEMENT_EMA200_GOLDEN_CROSS_EMA15_INDEX)
            print("\nINDEX ORIGINE DANS TRAITEMENT REELLE=\n",dataframe.loc[val_mask_idxmin_ORG])
            print("\nINDEX COURANT DANS TRAITEMENT REELLE=\n",dataframe.loc[val_mask_idxmin])
            print("SYMBOL : {} INTERVAL:{} TRAITEMENT_REELLE={} et FLAG_BEST_NBR_TAILLE_BG={}".format(symbol,interval,TRAITEMENT_REELLE,FLAG_BEST_NBR_TAILLE_BG))
            """
            if  (TRAITEMENT_REELLE == 1)  and (FLAG_BEST_NBR_TAILLE_BG == 1) and ("m" in  interval) and ( LEN_LISTE_ACHAT_VENTE != 0) :
                CALCULE_BEST_BG()
            #NBR_TAILLE_BG_MAX=100
            """
            if "1m" in  interval :  
                DECALAGE=0
                #RESTART_ONE_PAIR(symbol,timeframe)
                #time.sleep(0.5)
            else:
                DECALAGE=0
    
            print("AVANT CALCULE TAILLE BOUGIE last_index=",last_index)
            #DATE_PRECEDENTE=dataframe.date.loc[last_index]
            """
            from datetime import datetime, timedelta
            now=datetime.utcnow()
            new_hour=now  + timedelta(hours=2)   
            new_hour=new_hour.strftime("%Y-%m-%d %H:%M:%S")
            new_hour=new_hour.split(".")[0]
            new_hour=new_hour[:-3]+":00"
            new_hour=datetime.strptime(new_hour, '%Y-%m-%d %H:%M:%S')
            DATE_ACTUELLE= new_hour  + pd.Timedelta(minutes=val_minute)
            DATE_FUTUR_RESTART = DATE_ACTUELLE + pd.Timedelta(minutes=val_minute+3) - pd.Timedelta(seconds=2)
            """
         
            #DETECT_LAST_SELL(dataframe,val_mask_idxmin)
            #time.sleep(10)
            
            #print("DATE_PRECEDENTE: {}".format(DATE_PRECEDENTE))
            #exit()
            if (val_mask_idxmin == last_index) :
                DATE_PRECEDENTE=dataframe_date.date.loc[last_index]
                DATE_FUTUR = DATE_PRECEDENTE + pd.Timedelta(minutes=val_minute)
                DATE_FUTUR_RESTART = DATE_PRECEDENTE + pd.Timedelta(minutes=val_minute+DECALAGE) - pd.Timedelta(seconds=2)
                # start_time = dataframe.date.iloc[-1] - pd.Timedelta(minutes=nbr_interval)
                #DATE_FUTUR=DATE_FUTUR.strftime("%Y-%m-%d %H:%M:%S")
                print("DATE_PRECEDENTE: {} et DATE_FUTUR {} et DATE_FUTUR_RESTART {} et i= {}:".format(DATE_PRECEDENTE,DATE_FUTUR,DATE_FUTUR_RESTART,i))
                #exit()
                
                # RESTART_ONE_PAIR(symbol,timeframe)
                #while True :
                try:
                    #print("dataframe.date.iloc[-1].time()=",dataframe.date.iloc[-1].time())
                    dataframe=RECUPERATION_DE_LA_DERNIERE_TRAME()
                    if len(dataframe) > 0 :
                        last_index=len(dataframe)-1
                        DATE_COURANTE=dataframe_date.date.loc[last_index]
                        #DATE_COURANTE=DATE_COURANTE.strftime("DATE_COURANTE: %Y-%m-%d %H:%M:%S")
                        if i == 0 :
                            print("DANS WHILE TRUE DATE_PRECEDENTE: {} et DATE_COURANTE {} et i= {}:".format(DATE_PRECEDENTE,DATE_COURANTE,i))

                        if DATE_PRECEDENTE != DATE_COURANTE :
                            dataframe=populate_indicators(dataframe)
                            #last_index=dataframe.index[-1]
                            val_mask_idxmin=last_index 
                            mask = (dataframe_date.date <=  dataframe_date.loc[last_index].date )
                            val_mask_idxmin_ORG=dataframe['EMA200'].loc[mask].idxmin()
                            print("\nSORTIE WHILE TRUE DATE_PRECEDENTE: {} et DATE_COURANTE: {} DIFFERENTE".format(DATE_PRECEDENTE,DATE_COURANTE))
                            break
                        
                        CHECK_NEW_BG(DATE_FUTUR)
                        #if RESULT_CHECK_NEW_BG != "1" :
                        if i == 0 :
                            print("last_index=",last_index)
                            print("IMPORTE df: \n",dataframe.tail())
                            print("ATTENTE DE LA NOUVELLE BOUGIE DANS {} {} \n RESULT_CHECK_NEW_BG:{}".format(nbr_interval,TEMP,RESULT_CHECK_NEW_BG))
                            i=1
                            #time.sleep(1)
                     
                        #from datetime import datetime, timedelta
                        now=datetime.now()
                        new_hour=now  #+ timedelta(hours=2)   
                        new_hour=new_hour.strftime("%Y-%m-%d %H:%M:%S")
                        new_hour=new_hour.split(".")[0]
                        seconde=new_hour[-2:]
                        new_hour=new_hour[:-3]
                        #print("SECONDE :",seconde)
                        
                        """
                        while  seconde <= "35" :
                            print("SECONDE :",seconde)
                            # if DERNIER_POINT_VENTE==1:
                              # break
                            DETECT_LAST_SELL(dataframe,val_mask_idxmin)
                            time.sleep(15)
                            break
                        """
                            #exit()
                        """
                        print("DATE_FUTUR {} :".format(DATE_FUTUR))
                        print("new_hour :",new_hour)
                        print("SECONDE :",seconde)
                        print("TRONC new_hour :",new_hour[:-3]+":00")
                        """
                        #if new_hour[:-3]+":00" in str(DATE_FUTUR) :
                        # if new_hour in str(DATE_FUTUR) :
                        # if (seconde == "55") and (i == 0) :
                        #     print("RESTART_ONE_PAIR : new_hour :",new_hour)
                        #     DETECT_MODE_REEL(dataframe,val_mask_idxmin)
                        #     #RESTART_ONE_PAIR(symbol,timeframe)
                        #     #time.sleep(0.5)
                             
                        if  new_hour in str(DATE_FUTUR_RESTART) :
                            #print("RELANCE TIMER BOUGIE :",interval)
                            print("RESTART_ONE_PAIR : new_hour :",new_hour)
                            print("RESTART_ONE_PAIR : DATE_FUTUR_RESTART :",DATE_FUTUR_RESTART)
                            ####DETECT_MODE_REEL(dataframe,val_mask_idxmin)
                            #RESTART_ONE_PAIR(symbol,timeframe)
                            #time.sleep(0.5)
                            DATE_FUTUR_RESTART = DATE_PRECEDENTE + pd.Timedelta(minutes=val_minute+3) - pd.Timedelta(seconds=2)
                            #time.sleep(59)
                            #RESTART_ONE_PAIR(symbol,timeframe)
                            #time.sleep(20)
                          
                        #APPEL ROUTINE EXECUTION DES ORDRES ACHAT ET VENTE    
                        #EXEC_ORDER (dataframe)
                            

            #"""
                except Exception as i:
                  print(f'\nError INDEX : {i}')
                  #RESTART_ONE_PAIR(symbol,timeframe)
                  #time.sleep(0.5)
            #"""
# #"""
  # except Exception as j:
  #      pass
#     print(f'\nError GLOBAL  MAIN  : {j}')
#     #RESTART_ONE_PAIR(symbol,timeframe)
#     #time.sleep(0.5)
# #"""         


 
         
# def DETECT_LAST_SELL(dataframe,val_mask_idxmin):
#     #global VAL_ACHAT
#     global POINT_ENTRE_EMA200
#     global DERNIER_POINT_VENTE
#     global ORDER
#     global DIFF_DYNAMIQUE_VAL_CLOSE_VAL_CLOSE_ORG
#     global MULTIP
#     global CLOSE_LAST_INDEX_ORG
#     global last_price
#     global LIST_LAST_VAL_CLOSE_VAL_ACHAT
#     global VARIATION_PRIX
#     global LEN_2_ELEMENT
#     global DIFF_CLOSE_VAL_CLOSE_N2
#     global DIFF_CLOSE_VAL_CLOSE
#     global df_VAL_CLOSE_VAL_ACHAT
#     global COULEUR_VOLUME
    
#     print("\nENTRER DANS DETECT_LAST_SELL et POINT_ENTRE_EMA200 : ",POINT_ENTRE_EMA200)
#     DATE_COURANTE=dataframe.date.iloc[-1]
# #if (POINT_ENTRE_EMA200 == 1) or ( DIFF_DYNAMIQUE_VAL_CLOSE_VAL_CLOSE_ORG == True):
#     if (int(POINT_ENTRE_EMA200) == 1) :
#         #VAL_CLOSE=RECUP_LAST_PRICE(symbol)  
#         #df.set_index('date', inplace=True)
#         #VAL_ACHAT=custom_info["VAL_ACHAT"] 
#         VAL_ACHAT=custom_info["VAL_ACHAT_ORG"]
#         #VAL_CLOSE=RECUP_LAST_PRICE_IN_FILE()
#         VAL_CLOSE_ORG=dataframe.close.loc[val_mask_idxmin]
#         global VAL_EMA1H_PRECEDENT_COURT

#         while True:
#           VAL_CLOSE_ORG=RECUP_LAST_PRICE_IN_FILE()
#           time.sleep(1)
#           VAL_CLOSE=RECUP_LAST_PRICE_IN_FILE()
#           FRONT_MONTANT_COURT_EMA1H=float(VAL_CLOSE) - float(VAL_EMA1H_PRECEDENT_COURT) > 0
#           DIFF_CLOSE_VAL_CLOSE=int((float(VAL_CLOSE) - float(VAL_CLOSE_ORG))*MULTIP)
#           DIFF_CLOSE_VAL_ACHAT=int((float(VAL_CLOSE) - float(VAL_ACHAT))*MULTIP)
#           GAIN_ABSOLUE_PRECEDENT=int(custom_info["GAIN_ABSOLUE_PRECEDENT"])
#           DIFF_GAIN_ABSOLUE=(DIFF_CLOSE_VAL_ACHAT-GAIN_ABSOLUE_PRECEDENT) < 0
#           print("\nDANS DETECT_LAST_SELL")
#           print("VAL_ACHAT:{} VAL_CLOSE: {} VAL_CLOSE_ORG : {}".format(VAL_ACHAT,VAL_CLOSE,VAL_CLOSE_ORG))
#           print("float(VAL_CLOSE) - float(VAL_CLOSE_ORG) : {}".format(DIFF_CLOSE_VAL_CLOSE))
#           print("float(VAL_CLOSE) - float(VAL_ACHAT)  : {}".format(DIFF_CLOSE_VAL_ACHAT))  
#           print("DIFF_GAIN_ABSOLUE : {}".format(DIFF_GAIN_ABSOLUE))  
#           print("(FRONT_MONTANT_COURT_EMA15 == 0): ",(FRONT_MONTANT_COURT_EMA15 == 0))
#           #if (float(VAL_CLOSE) - float(VAL_CLOSE_ORG) < 0) and float(VAL_CLOSE) - float(VAL_ACHAT) > 0 :
#           #if (DIFF_CLOSE_VAL_CLOSE < 0) and (DIFF_CLOSE_VAL_ACHAT > 0) :
#           #if (DIFF_CLOSE_VAL_CLOSE < -3) and (FRONT_MONTANT_COURT_EMA1H >= 0) and (FRONT_MONTANT_COURT_EMA200 >= 0) :
#           if (DIFF_CLOSE_VAL_CLOSE < -3) or (FRONT_MONTANT_COURT_EMA15 == 0) or (COULEUR_VOLUME == "VERT") :
#               VENTE="OK"
#               if (FRONT_MONTANT_COURT_EMA15 == 0) :
#                   custom_info["POINT_DE_VENTE_GAIN_ABSOLUE"]="POINT_DE_VENTE_GAIN_ABSOLUE"
#               break
#         #VAL_ACHAT=CLOSE_LAST_INDEX_ORG
#         DIFF_CLOSE_VAL_CLOSE_OLD=DIFF_CLOSE_VAL_CLOSE
#         DIFF_CLOSE_VAL_CLOSE=int((float(VAL_CLOSE) - float(VAL_CLOSE_ORG))*MULTIP)
#         DIFF_CLOSE_VAL_ACHAT=int((float(VAL_CLOSE) - float(VAL_ACHAT))*MULTIP)
#         """
#         print("float(VAL_ACHAT):", float(VAL_ACHAT))
#         print("float(VAL_CLOSE_ORG):", float(VAL_CLOSE_ORG))
#         print("DATE_COURANTE:",DATE_COURANTE)
#         print("DIFF_CLOSE_VAL_ACHAT:",DIFF_CLOSE_VAL_ACHAT)
#         """
#         print("len(LIST_LAST_VAL_CLOSE_VAL_ACHAT['LAST_VAL_CLOSE_VAL_ACHAT']):",len(LIST_LAST_VAL_CLOSE_VAL_ACHAT['LAST_VAL_CLOSE_VAL_ACHAT']))
#         #LIST_LAST_VAL_CLOSE_VAL_ACHAT['LAST_VAL_CLOSE_VAL_ACHAT'].loc[len(LIST_LAST_VAL_CLOSE_VAL_ACHAT['LAST_VAL_CLOSE_VAL_ACHAT'])]=[DATE_COURANTE,DIFF_CLOSE_VAL_CLOSE]
#         if LEN_2_ELEMENT == 0 :
#             LEN_INIT=len(LIST_LAST_VAL_CLOSE_VAL_ACHAT['LAST_VAL_CLOSE_VAL_ACHAT'])
#             LIST_LAST_VAL_CLOSE_VAL_ACHAT['LAST_VAL_CLOSE_VAL_ACHAT'].loc[LEN_INIT]=[DATE_COURANTE,DIFF_CLOSE_VAL_CLOSE]
#         else:
#             LEN_INIT=LEN_2_ELEMENT #LEN_2_ELEMENT --> 1
#             # Entre LA DERNIERE DONNEE RECUE ( Indice 1 ) à la Fin du Tableau
#             LIST_LAST_VAL_CLOSE_VAL_ACHAT['LAST_VAL_CLOSE_VAL_ACHAT'].loc[LEN_INIT]=[DATE_COURANTE,DIFF_CLOSE_VAL_CLOSE] 

#         df_VAL_CLOSE_VAL_ACHAT=LIST_LAST_VAL_CLOSE_VAL_ACHAT['LAST_VAL_CLOSE_VAL_ACHAT']
#         df_VAL_CLOSE_VAL_ACHAT=df_VAL_CLOSE_VAL_ACHAT.set_index('DATE_COURANTE')
#         print("df_VAL_CLOSE_VAL_ACHAT:\n",df_VAL_CLOSE_VAL_ACHAT)
#         print("LEN df_VAL_CLOSE_VAL_ACHAT:",len(df_VAL_CLOSE_VAL_ACHAT))
#         #exit() 
#         LEN=len(df_VAL_CLOSE_VAL_ACHAT)-1
#         """
#         if LEN_2_ELEMENT == 0 :
#             LEN=len(df_VAL_CLOSE_VAL_ACHAT)-1
#         else:
#             LEN=len(df_VAL_CLOSE_VAL_ACHAT)
#         """

#         print("LEN_INIT :",LEN_INIT)
#         print("LEN :",LEN)
#         print("LASTE PRICE:", float(VAL_CLOSE))
#         print("float(VAL_ACHAT):", float(VAL_ACHAT))
#         print("float(VAL_CLOSE_ORG):", float(VAL_CLOSE_ORG))
#         print("DATE_COURANTE:",DATE_COURANTE)
#         print("DIFF_CLOSE_VAL_ACHAT:",DIFF_CLOSE_VAL_ACHAT)

#         if len(df_VAL_CLOSE_VAL_ACHAT) > 1 : ##.values.astype(int)[0]
#             if LEN_2_ELEMENT == 0 :
#                 DIFF_CLOSE_VAL_CLOSE_N2=df_VAL_CLOSE_VAL_ACHAT.DIFF_CLOSE_VAL_CLOSE[LEN-1]
#                 DIFF_CLOSE_VAL_CLOSE=df_VAL_CLOSE_VAL_ACHAT.DIFF_CLOSE_VAL_CLOSE[LEN-2]
#             else:
#                 # ---> DEPLACE l Indice 1 dans le PASSE (Indice 0 ) dans  au Debut du Tableau dans DIFF_CLOSE_VAL_CLOSE_N2
#                 #DIFF_CLOSE_VAL_CLOSE_N2=DIFF_CLOSE_VAL_CLOSE  
#                 df_VAL_CLOSE_VAL_ACHAT.DIFF_CLOSE_VAL_CLOSE[0]=DIFF_CLOSE_VAL_CLOSE_OLD
#                 DIFF_CLOSE_VAL_CLOSE_N2=df_VAL_CLOSE_VAL_ACHAT.DIFF_CLOSE_VAL_CLOSE[0] 
                
#                 #COPIE  LA DERNIERE DONNEE RECUE ( Indice 1 ) ---> Dans DIFF_CLOSE_VAL_CLOSE
#                 DIFF_CLOSE_VAL_CLOSE=df_VAL_CLOSE_VAL_ACHAT.DIFF_CLOSE_VAL_CLOSE[LEN_2_ELEMENT]  #LEN_2_ELEMENT --> 1

       
#             print("DIFF_CLOSE_VAL_CLOSE_N1:",DIFF_CLOSE_VAL_CLOSE_N2)
#             print("DIFF_CLOSE_VAL_CLOSE:",DIFF_CLOSE_VAL_CLOSE)
#             """
#                 DIFF_VARIATION_PRIX_VAL_CLOSE_N2=int(DIFF_CLOSE_VAL_CLOSE_N2) >= 0 
#                 DIFF_VARIATION_PRIX_VAL_CLOSE=int(DIFF_CLOSE_VAL_CLOSE) < 0
#                 VARIATION_PRIX=(DIFF_VARIATION_PRIX_VAL_CLOSE == True) and (DIFF_VARIATION_PRIX_VAL_CLOSE_N2 == True)
#             """
#             #DIFF_VARIATION_PRIX_VAL_CLOSE_N2=abs(int(DIFF_CLOSE_VAL_CLOSE) + int(DIFF_CLOSE_VAL_CLOSE_N2)) > abs(int(DIFF_CLOSE_VAL_CLOSE_N2))
#             #DIFF_VARIATION_PRIX_VAL_CLOSE=abs(int(DIFF_CLOSE_VAL_CLOSE) + int(DIFF_CLOSE_VAL_CLOSE_N2)) > abs(int(DIFF_CLOSE_VAL_CLOSE)) 
#             DIFF_VARIATION_PRIX_VAL_CLOSE=(int(DIFF_CLOSE_VAL_CLOSE) > int(DIFF_CLOSE_VAL_CLOSE_N2))

#             VARIATION_PRIX=(DIFF_VARIATION_PRIX_VAL_CLOSE == True)  and (int(DIFF_CLOSE_VAL_CLOSE) != 0 ) and  (int(DIFF_CLOSE_VAL_CLOSE_N2) != 0 )
#             #print("DIFF_VARIATION_PRIX_VAL_CLOSE_N2:",DIFF_VARIATION_PRIX_VAL_CLOSE_N2)
#             print("DIFF_VARIATION_PRIX_VAL_CLOSE:",DIFF_VARIATION_PRIX_VAL_CLOSE)
#             print("VARIATION_PRIX:",VARIATION_PRIX)
#             #LIST_LAST_VAL_CLOSE_VAL_ACHAT = {'LAST_VAL_CLOSE_VAL_ACHAT': pd.DataFrame(columns=['DATE_COURANTE', 'DIFF_CLOSE_VAL_CLOSE'])}
#             LEN_2_ELEMENT=1
#             #exit()
#         #else:
#             #VARIATION_PRIX=False
#             #print("df_VAL_CLOSE_VAL_ACHAT:\n",df_VAL_CLOSE_VAL_ACHAT)
#         #exit()
#         #DIFF_VAL_CLOSE_VAL_CLOSE_ORG=(float(VAL_CLOSE) - float(VAL_CLOSE_ORG) <= -1) and ((float(VAL_CLOSE) - float(VAL_ACHAT) > 0) or (float(VAL_CLOSE) - float(VAL_ACHAT) < 0))
#         #DIFF_VAL_CLOSE_VAL_CLOSE_ORG=(VARIATION_PRIX == True) and (float(VAL_CLOSE) >= float(VAL_ACHAT) ) and (int(DIFF_CLOSE_VAL_CLOSE) < 0)
#         DIFF_VAL_CLOSE_VAL_CLOSE_ORG=(VARIATION_PRIX == True)   
#         #DIFF_DYNAMIQUE_VAL_CLOSE_VAL_CLOSE_ORG=DIFF_VAL_CLOSE_VAL_CLOSE_ORG or  (float(VAL_CLOSE) < float(VAL_ACHAT))
#         DIFF_DYNAMIQUE_VAL_CLOSE_VAL_CLOSE_ORG=(DIFF_VAL_CLOSE_VAL_CLOSE_ORG and  (float(VAL_CLOSE) - float(VAL_ACHAT) > 0)) 
#         #DIFF_DYNAMIQUE_VAL_CLOSE_VAL_CLOSE_ORG=DIFF_VAL_CLOSE_VAL_CLOSE_ORG < 0 and DIFF_VAL_CLOSE_VAL_CLOSE_ORG < -10
#         print("float(VAL_CLOSE) - float(VAL_CLOSE_ORG) < 0 :",float(VAL_CLOSE) - float(VAL_CLOSE_ORG) < 0)
#         #print("float(VAL_CLOSE) - float(VAL_CLOSE_ORG) < -10 :",float(VAL_CLOSE) - float(VAL_CLOSE_ORG) < -10)
#         print("float(VAL_CLOSE) - float(DIFF_CLOSE_VAL_ACHAT) : {}".format(DIFF_CLOSE_VAL_ACHAT))
#         print("float(VAL_CLOSE) - float(VAL_ACHAT) > 0 :",float(VAL_CLOSE) - float(VAL_ACHAT) > 0)   
#         print("float(VAL_CLOSE) - float(VAL_ACHAT) < 0 :",float(VAL_CLOSE) - float(VAL_ACHAT) < 0)   
#         print("float(VAL_CLOSE) - float(VAL_CLOSE_ORG) : {}".format(DIFF_CLOSE_VAL_CLOSE))
#         print("(float(VAL_CLOSE) < float(VAL_CLOSE_ORG) ) :",float(VAL_CLOSE) < float(VAL_CLOSE_ORG) )
#         print("DIFF_DYNAMIQUE_VAL_CLOSE_VAL_CLOSE_ORG :", DIFF_DYNAMIQUE_VAL_CLOSE_VAL_CLOSE_ORG )
#         if DIFF_DYNAMIQUE_VAL_CLOSE_VAL_CLOSE_ORG == True :
#              print("!!!!!!!!!!!!! CHUTE DES PRIX BOUGIE ROUGE DECROISSANTE : {} !!!!!!!!!!!!!".format(VAL_CLOSE))

#         # 8eme CAS VENTE ABSOLUE BOUGIE VERTE TRAVERSANTE FRONT MONTANT SUR EMA200    and (FRONT_MONTANT_EMA15 == 1 ) and (FRONT_MONTANT_COURT_EMA15 <= 0 ) 
#         #and (float(VAL_CLOSE) - float(VAL_CLOSE_N1) < 0) or (float(VAL_CLOSE_N1) - float(VAL_CLOSE_N2) < 0)   \
#         #if (float(VAL_CLOSE) - float(VAL_CLOSE_ORG) < 0)  and (POINT_ENTRE_EMA200 == 1):
#         #if (float(VAL_CLOSE) < float(VAL_CLOSE_ORG) ) and float(VAL_CLOSE) > float(VAL_ACHAT) and (POINT_ENTRE_EMA200 == 1):
#         #if DIFF_DYNAMIQUE_VAL_CLOSE_VAL_CLOSE_ORG == True and float(VAL_CLOSE) > float(VAL_ACHAT) and (POINT_ENTRE_EMA200 == 1):
#         #if ((DIFF_DYNAMIQUE_VAL_CLOSE_VAL_CLOSE_ORG == True)  and (POINT_ENTRE_EMA200 == 1) and  (float(VAL_CLOSE) < float(VAL_ACHAT)) 
#            # and  (float(VAL_CLOSE) >  float(VAL_ACHAT))  
#         """
#         if ( ((float(VAL_CLOSE) - float(VAL_CLOSE_ORG)) < 0 and float(VAL_CLOSE) - float(VAL_ACHAT) > 0 
#             and float(VAL_CLOSE) < float(VAL_CLOSE_ORG))) : 
#         #and (FRONT_MONTANT_COURT_EMA1H == 1 ) and (POINT_ENTRE_EMA200 == 1) \
#         #and  ((FRONT_MONTANT_COURT_EMA1H == 1 ) or (FRONT_NEUTRE_EMA1H == 1 )) :
#         """
#         if VENTE == "OK" and  COULEUR_VOLUME== "ROUGE" and  (float(VAL_CLOSE)  - float(VAL_ACHAT) > -1) :
#              print("VENTE DYNAMIQUE BOUGIE VERTE DECROISSANTE")
#              ORDER="SELL"
#              custom_info["SCENARIO"]="DETECT_LAST_SELL VENTE DYNAMIQUE BOUGIE VERTE DECROISSANTE"
#              print(ORDER)
#              EXEC_ORDER(dataframe)
#              VAL_ACHAT=dataframe.close.loc[val_mask_idxmin]
#              POINT_ENTRE_EMA200 = 0 #VEROUILAGE ACHAT ET VENTE NORMAL
#              #DERNIER_POINT_VENTE=1
#              VENTE=""
             

#         print("SORTIE DANS DETECT_LAST_SELL\n")
#         time.sleep(4)
#              #exit()                 

#def DETECT_LAST_SELL_OLD(dataframe,val_mask_idxmin):
def DETECT_LAST_SELL(dataframe,val_mask_idxmin):

    global VAL_ACHAT
    global POINT_ENTRE_EMA200
    global DERNIER_POINT_VENTE
    global ORDER
    global DIFF_DYNAMIQUE_VAL_CLOSE_VAL_CLOSE_ORG
    global MULTIP
    global CLOSE_LAST_INDEX_ORG
    global last_price
    global LIST_LAST_VAL_CLOSE_VAL_ACHAT
    global VARIATION_PRIX
    global LEN_2_ELEMENT
    global DIFF_CLOSE_VAL_CLOSE_N2
    global DIFF_CLOSE_VAL_CLOSE
    global df_VAL_CLOSE_VAL_ACHAT
    global COULEUR_VOLUME
    
    print("\nENTRER DANS DETECT_LAST_SELL et POINT_ENTRE_EMA200 : ",POINT_ENTRE_EMA200)
    DATE_COURANTE=dataframe.date.iloc[-1]
    #VAL_CLOSE=RECUP_LAST_PRICE_IN_FILE()

    if (COULEUR_VOLUME == "ROUGE")  and (POINT_ENTRE_EMA200 == 1) and  float(last_price) > float(VAL_ACHAT) : 
         print("VENTE DYNAMIQUE BOUGIE VERTE DECROISSANTE")
         ORDER="SELL"
         custom_info["SCENARIO"]="DETECT_LAST_SELL VENTE DYNAMIQUE BOUGIE VERTE DECROISSANTE"
         print(ORDER)
         EXEC_ORDER(dataframe)
         #VAL_ACHAT=dataframe.close.loc[val_mask_idxmin]
         POINT_ENTRE_EMA200 = 0 #VEROUILAGE ACHAT ET VENTE NORMAL
         #DERNIER_POINT_VENTE=1
         VENTE=""
         
    print("SORTIE DANS DETECT_LAST_SELL\n")
    #time.sleep(2)
         #exit()                 

             

            
def DETECT_MODE_REEL(dataframe,val_mask_idxmin):
    global DATE_DU_PASSE
    DATE_DU_PASSE=0
    while True :
        val_mask_idxmin_ORG=val_mask_idxmin
        last_index=len(dataframe)-1
        val_mask_idxmin=last_index
        TEST_MODE_REEL=CALCUL_DATE_COURANTE(dataframe,val_mask_idxmin)
        if   TEST_MODE_REEL == 1 :
          val_mask_idxmin=last_index
          break
        else:
          RESTART_ONE_PAIR(symbol,timeframe)
          #time.sleep(1)
          dataframe=RECUPERATION_DE_LA_DERNIERE_TRAME()
          dataframe=populate_indicators(dataframe)          
    return val_mask_idxmin
    
def check_string (string):
    print("string:",string)
    print("Entrer check_string")
    j=0
    string=str(string)
    for i in range(len(string)) :
        if string[-i-1] != "0"  :
          print(string[-i-1])
        else:
          j=i+1   
    if  string[0] == "0" :
        print(string[0])
    print("j:",j)   
    print(string[:j])
    if j == 0 :
        print(string)
        print("Sortie check_string")
        return float(string)
    else:
        print(string[:j])
        print("Sortie check_string")
        return float(string[:j])

# def check_gain(string):
#     if "-" in str(string) :
#         nbr=str(string).split("-")[1]
#         nbr=int(nbr)
#         string=format(string,".8f")
#         deb=string.split(".")[0]
#         fin=string.split(".")[1]
#         len_deb=len(deb)+1
#         gain=string[:nbr+len_deb]
#         gain=float(gain)
#         gain=int(gain * 10**nbr)
#         print("gain:",gain)
#         return gain

# def check_gain(string):
#     if "-" in str(string) :
#         gain=str(string).split(".")[0]
#         gain=int(gain)
#         print("gain:",gain)
#         return gain
    
def check_gain(string):
    if string == "" or string == 0:
        return 0 
    
    if "e-" in str(string) :
        gain=str(string).split(".")[0]
    else:
      j=0
      k=0
      gain=str(string).split(".")[0]

      if abs(int(gain)) == 0 :
       while True:
        # print("j:",j)
        #print("k:",k)
        gain=np.round(string,j)
        gain=str(gain).split(".")[1]
        gain=str(gain).replace(".", "")
        gain=int(gain)

        if gain != 0 and k==1 :
            break
        if gain != 0 and k==0 :
            k=1        
        j+=1+k
        
      if "-" in str(string) :
            gain=-int(gain)
      print("gain:",gain)
      return gain 

def calcule_gain(cumul_gain):
    #import numpy as np
    MISE=1000
    gain=np.round(float(cumul_gain),2)
    # VAL_ACHAT=float(custom_info["VAL_ACHAT"])
    # VAL_ACHAT=1.06
    VAL_ACHAT=custom_info["VAL_ACHAT"]
    CUMUL_GAIN_EURO=(MISE/float(VAL_ACHAT))*gain
    CUMUL_GAIN_EURO=(MISE/VAL_ACHAT)*gain
    print("CUMUL_GAIN_EURO:",CUMUL_GAIN_EURO)
    return CUMUL_GAIN_EURO    

def calcule_perte(cumul_perte):
    #import numpy as np
    MISE=1000
    gain=np.round(float(cumul_perte),2)
    VAL_ACHAT=custom_info["VAL_ACHAT"]
    CUMUL_PERTE_EURO=(MISE/float(VAL_ACHAT))*gain
    print("CUMUL_PERTE_EURO:",CUMUL_PERTE_EURO)
    return CUMUL_PERTE_EURO    
           
def EXEC_ORDER (dataframe):
    global ORDER
    global LAST_ORDER
    global COMPTEUR_BUY_SELL
    global COMPTEUR_SELL
    global GAIN
    global GAIN_RELATIF
    global GAIN_ABSOLUE
    global GAIN_ABSOLUE_OLD
    global DERNIER_POINT_VENTE
    global POINT_ENTRE_EMA200
    global COMPTEUR_BUY_INITIAL
    global VAL_ACHAT_INITIALE
    global FLAG_SIMULATION
    global PREVIOUS_MODE
    global MODE_GAIN
    global GAIN_NEGATIF
    global FLAG_DERNIERE_VENTE_GAIN_ABSOLUE
    global DERNIERE_VENTE_GAIN_ABSOLUE
    global FLAG_SIMULATION_GLOBAL
    global POINT_DE_VENTE_GAIN_ABSOLUE
    global val_mask_idxmin
    global DATE_COURANTE
    global FIRST_VENTE
    global NBR_CUMUL
    global CUMUL_GAIN_OLD
    global TYPE_FRONT_EMA200
    global TYPE_FRONT_EMA1H
    global NBR_COMPTEUR_TEMPORELLE
    global DIFF_DYNAMIQUE_VAL_CLOSE_VAL_CLOSE_ORG
    global ACHAT_DYNAMIQUE
    global VENTE_DYNAMIQUE
    global CLOSE_LAST_INDEX
    global CLOSE_LAST_INDEX_ORG
    global COMPTEUR_PERTE
    global TRAITEMENT_REELLE
    global FIRST_ACHAT
    global last_price
    global CUMUL_GAIN_RELATIF
    global PRIX
    
    signal.signal(signal.SIGINT, PKILL)
    signal.signal(signal.SIGTERM, PKILL)
    print("\nENTRER DANS EXEC_ORDER \n ORDER: {}  LAST_ORDER: {}  FLAG_SIMULATION : {} FLAG_SIMULATION_GLOBAL: {} COMPTEUR_BUY_INITIAL: {}  DIFF_DYNAMIQUE_VAL_CLOSE_VAL_CLOSE_ORG: {}"
          .format(ORDER,LAST_ORDER,FLAG_SIMULATION,FLAG_SIMULATION_GLOBAL,COMPTEUR_BUY_INITIAL,DIFF_DYNAMIQUE_VAL_CLOSE_VAL_CLOSE_ORG))
    time.sleep(0.1)

    #print("\nENTRER DANS EXEC_ORDER ORDER: {} ".format(ORDER))
    if (ORDER != "") and ( ORDER == "BUY" ) and (LAST_ORDER != "BUY"): #and (COMPTEUR_BUY_SELL < 1 )  : #  and ( LAST_ORDER == "SELL" ) : #and (POINT_ENTRE_EMA200 == 0 ) :
              #VAL_ACHAT=RECUP_LAST_PRICE_IN_FILE()
              RECUP_LAST_PRICE_IN_BINANCE(dataframe)
              VAL_ACHAT=PRIX
              #VAL_ACHAT=last_price
              #VAL_ACHAT=RECUP_LAST_PRICE_IN_FILE()
              custom_info["VAL_ACHAT_ORG"] = VAL_ACHAT
              last_index=len(dataframe)-1
              #CLOSE=int(float(VAL_ACHAT)*MULTIP)
              # CLOSE=check_string(PRIX)
              CLOSE=PRIX
              CLOSE_LAST_INDEX= dataframe['CLOSE'].iloc[last_index] #.astype(int)
              #CLOSE_LAST_INDEX_ORG= dataframe['close'].iloc[-1]
              CLOSE_LAST_INDEX_ORG= dataframe['close'].iloc[last_index]

              """
              CLOSE= dataframe['CLOSE'].loc[val_mask_idxmin].astype(int)
              CLOSE_LAST_INDEX= dataframe['CLOSE'].iloc[last_index].astype(int)
              CLOSE_LAST_INDEX_ORG= dataframe['close'].iloc[-1]
              """
              custom_info["symbol"]=symbol
              custom_info["PAIR"]=symbol  
              custom_info["DATAFRAME_PAIR"]=symbol             
              custom_info["CLOSE"]=CLOSE
              custom_info["CLOSE_LAST_INDEX"]=CLOSE_LAST_INDEX
              # custom_info["couleur"]=TYPE_BG
              custom_info["TYPE_CROISEMENT_EMA200"]=TYPE_FRONT_EMA200
              custom_info["TYPE_CROISEMENT_EMA1H"]=TYPE_FRONT_EMA1H
              custom_info["TYPE_CROISEMENT"]=TYPE_FRONT_EMA15
              custom_info["MODE_FUTUR"]="NEANT"
              #custom_info["HEURE_CROISEMENT_PAIR"]=dataframe.date.loc[val_mask_idxmin]
              custom_info["TIMEFRAME"]=interval 
              custom_info["TYPE"] = "MARKET"
              #custom_info["TYPE"] = "LIMIT"
        #ROUTINE EXECUTION REELE DES ORDRES ACHAT ET VENTE
    #if (TRAITEMENT_REELLE == 1) or (ORDER != "") and ( ORDER == LAST_ORDER ) :
    #if (ORDER != "") and ( ORDER == "BUY" ) and (LAST_ORDER != "BUY"): #and (COMPTEUR_BUY_SELL < 1 )  : #  and ( LAST_ORDER == "SELL" ) : #and (POINT_ENTRE_EMA200 == 0 ) :

              if ( LAST_ORDER == ORDER ) :
                   # exit()              
                    return        
        
              DIFF_EMA200_EMA15=dataframe.DIFF_EMA200_EMA15.loc[val_mask_idxmin].astype(int)
              print("DIFF_EMA200_EMA15=",DIFF_EMA200_EMA15)
              
              if (DIFF_EMA200_EMA15 > 0 ):
                  custom_info["ACHAT_EN_DESSOUS_EMA200"] = 1
              else :
                  custom_info["ACHAT_EN_DESSOUS_EMA200"] = 0
             
              DIFF_EMA1H_EMA15=dataframe.DIFF_EMA1H_EMA15.loc[val_mask_idxmin].astype(int)
              print("DIFF_EMA1H_EMA15=",DIFF_EMA1H_EMA15)
              
              if (DIFF_EMA1H_EMA15 >= 0 ):
                  custom_info["ACHAT_AU_DESSUS_EMA15"] = 1
              else :
                  custom_info["ACHAT_AU_DESSUS_EMA15"] = 0                  
           
              #if ("GAIN NEGATIF" in MODE_GAIN):
                  #LAST_ORDER="BUY"
                 # return
          
              #if COMPTEUR_BUY_SELL < 1 :
                  #COMPTEUR_BUY_SELL=+1
              # if ORDER == "BUY" :
              
              ENV_MSG="ENV_MSG_"+ORDER
              if FLAG_SIMULATION == 1 or  TRAITEMENT_REELLE == "SIMULATION":
                  #last_index=dataframe.index[-1]
                last_index=len(dataframe)-1
                DIFF_last_index_val_mask_idxmin=last_index-val_mask_idxmin <= nbr_interval
                if  TRAITEMENT_REELLE == "SIMULATION" and DIFF_last_index_val_mask_idxmin :
                    custom_info[ENV_MSG]="FLAG_SIMULATION_TRAITEMENT_REELLE"
                    #val_mask_idxmin=DETECT_MODE_REEL(dataframe,val_mask_idxmin)
                    last_index=len(dataframe)-1
                    print("last_index=",last_index)
                    if val_mask_idxmin >= last_index :
                        val_mask_idxmin=last_index  
                else :
                    custom_info[ENV_MSG]="FLAG_SIMULATION"
              else:
               custom_info[ENV_MSG]="OUI"
               #val_mask_idxmin=DETECT_MODE_REEL(dataframe,val_mask_idxmin)
               last_index=len(dataframe)-1
               print("last_index=",last_index)
               if val_mask_idxmin >= last_index :
                   val_mask_idxmin=last_index  
               
              #custom_info["HEURE_CROISEMENT_PAIR"]=dataframe.date.loc[val_mask_idxmin]
              custom_info["PATH_EMA200_DEMA40_EMA15"]=PATH_EMA200_DEMA40_EMA15
              # LAST_ORDER="BUY"
              # LAST_ORDER=ORDER
              # print("LAST_ORDER=",LAST_ORDER)   
              print("APPEL TRADING ORDER=",ORDER)
              custom_info["ORDER"] = ORDER
              # ORDER="" 
              """
              VAL_ACHAT=dataframe.close.loc[val_mask_idxmin]
              VAL_ACHAT=(float(VAL_ACHAT)*MULTIP)/100
              VAL_ACHAT=np.round(VAL_ACHAT,decimals = 1)
              VAL_ACHAT=int(VAL_ACHAT)
              """
              #CLOSE= dataframe['CLOSE'].loc[val_mask_idxmin].astype(int)
              #VAL_ACHAT=CLOSE
              #VAL_ACHAT=RECUP_LAST_PRICE_IN_FILE()
              # VAL_ACHAT=check_string(VAL_ACHAT)
              # exit()
              custom_info["VAL_ACHAT"]=VAL_ACHAT
              custom_info["DATE_ACHAT"]=datetime.now()

              # VAL_ACHAT=int(float(VAL_ACHAT)*MULTIP)

              if COMPTEUR_BUY_INITIAL == 0 : #and int(custom_info["VAL_ACHAT_INITIALE"]) == 0 :
                 # VAL_ACHAT_INITIALE = int(VAL_ACHAT)
                 custom_info["VAL_ACHAT_INITIALE"] = VAL_ACHAT
                 COMPTEUR_BUY_INITIAL=1 
                 FIRST_ACHAT=1
                 FLAG_SIMULATION=1
                 MODE_GAIN="!!!! DEBUT D EXECUTION DU BOT  !!! \n !!! ACTIVATION MODE SIMULTATION !!!"
                 PREVIOUS_MODE=MODE_GAIN
                 custom_info["MODE_GAIN"]=MODE_GAIN
                 TRAITEMENT_REELLE == "SIMULATION"                 
              else:
                  custom_info["GAIN_ABSOLUE_PRECEDENT"]=custom_info["GAIN_ABSOLUE"]
                 
              if (FLAG_SIMULATION == 0) and (FLAG_SIMULATION_GLOBAL == 0) and ( MODE_GAIN == "GAIN_RELATIF") :
                 CALL_TRADING(dataframe)
              if (FLAG_SIMULATION == 0) and (FLAG_SIMULATION_GLOBAL == 0) and ( MODE_GAIN == "GAIN_ABSOLUE") : #and (POINT_DE_VENTE_GAIN_ABSOLUE == 1) :
                 POINT_DE_VENTE_GAIN_ABSOLUE=0
                 CALL_TRADING(dataframe)     
              
              custom_info["LAST_ORDER"]=LAST_ORDER
              COMPTEUR_BUY_SELL=int(COMPTEUR_BUY_SELL+1)
              custom_info["COMPTEUR_BUY_SELL"]=COMPTEUR_BUY_SELL
              print("COMPTEUR_BUY_INITIAL=",COMPTEUR_BUY_INITIAL)
              CALL_TELEGRAMME()       
              LAST_ORDER=ORDER
              print("LAST_ORDER=",LAST_ORDER) 
              ORDER="" 
              #custom_info["LAST_ORDER"]=LAST_ORDER
              #POINT_ENTRE_EMA200=1
              #DERNIER_POINT_VENTE=1
              if VENTE_DYNAMIQUE==1 :
               VENTE_DYNAMIQUE=0
              time.sleep(2)
              """
              #DERTERMINATION DU POINT D ACHAT
              if (DIFF_EMA200_EMA15 > 0 ):
                  custom_info["ACHAT_EN_DESSOUS_EMA200"] = 1
              else :
                  custom_info["ACHAT_EN_DESSOUS_EMA200"] = 0
              """
        
    #if (ORDER == "SELL") and (LAST_ORDER == "BUY")  and ( ORDER == LAST_ORDER ) and (TRAITEMENT_REELLE == 1) :
    if (ORDER == "SELL") and (LAST_ORDER == "BUY") or (DIFF_DYNAMIQUE_VAL_CLOSE_VAL_CLOSE_ORG == True) :
       #if COMPTEUR_BUY_SELL <= 1 :
           #COMPTEUR_BUY_SELL=-1
           ORDER="SELL"
           ENV_MSG="ENV_MSG_"+ORDER
           if FLAG_SIMULATION == 1 or  TRAITEMENT_REELLE == "SIMULATION":
             last_index=len(dataframe)-1
             if  TRAITEMENT_REELLE == "SIMULATION"  :
                 custom_info[ENV_MSG]="FLAG_SIMULATION_TRAITEMENT_REELLE"
                 #val_mask_idxmin=DETECT_MODE_REEL(dataframe,val_mask_idxmin)
                 last_index=len(dataframe)-1
                 print("last_index=",last_index)
                 if val_mask_idxmin >= last_index :
                     val_mask_idxmin=last_index  
             else :
                 custom_info[ENV_MSG]="FLAG_SIMULATION"
           else:
               custom_info[ENV_MSG]="OUI"
               #val_mask_idxmin=DETECT_MODE_REEL(dataframe,val_mask_idxmin)  
               last_index=len(dataframe)-1
               print("last_index=",last_index)
               if val_mask_idxmin >= last_index :
                   val_mask_idxmin=last_index  

           custom_info["PATH_EMA200_DEMA40_EMA15"]=PATH_EMA200_DEMA40_EMA15
           # LAST_ORDER="SELL"
           # LAST_ORDER=ORDER
           # print("LAST_ORDER=",LAST_ORDER) 
           print("APPEL TRADING ORDER=",ORDER)  
           custom_info["ORDER"] = ORDER
           # ORDER="" 
           #VAL_VENTE=dataframe.close.loc[val_mask_idxmin]
           # while True :
           #     #VAL_VENTE=RECUP_LAST_PRICE_IN_FILE()
           #     RECUP_LAST_PRICE_IN_BINANCE(dataframe)
           #     VAL_VENTE=PRIX
               
           #     if (float(VAL_VENTE)) > 0 :
           #         break
           VAL_VENTE=PRIX
           custom_info["DATE_VENTE"]=datetime.now()
           # VAL_VENTE=(float(VAL_VENTE)*MULTIP)
           # VAL_VENTE=np.round(VAL_VENTE,decimals = 1)
           # VAL_VENTE=float(VAL_VENTE)
           print("VAL_VENTE=",VAL_VENTE)
           VAL_ACHAT=custom_info["VAL_ACHAT"]
           # VAL_ACHAT=int(float(VAL_ACHAT)*MULTIP)
           VAL_ACHAT_INITIALE=(custom_info["VAL_ACHAT_INITIALE"])
           # VAL_ACHAT_INITIALE=int(float(VAL_ACHAT_INITIALE)*MULTIP)
           
           # VAL_VENTE=check_string(VAL_VENTE)
           # VAL_ACHAT_INITIALE=check_string(VAL_ACHAT_INITIALE)
           # VAL_ACHAT=check_string(VAL_ACHAT)

           # VAL_VENTE=VAL_VENTE.replace(".","")
           # VAL_ACHAT_INITIALE=str(VAL_ACHAT_INITIALE).replace(".","")
           # VAL_ACHAT=str(VAL_ACHAT).replace(".","")


           if VAL_ACHAT_INITIALE == "" :
               VAL_ACHAT_INITIALE=0
               
           if VAL_ACHAT == "" :
               VAL_ACHAT=0
               
           print("VAL_ACHAT_INITIALE=",VAL_ACHAT_INITIALE)
           print("VAL_ACHAT=",VAL_ACHAT)
           
           #ACHAT_ABSOLUE
           GAIN_ABSOLUE=(float(VAL_VENTE) - float(VAL_ACHAT_INITIALE))
           # GAIN_ABSOLUE=check_gain(GAIN_ABSOLUE)
           # GAIN_ABSOLUE=np.round(GAIN_ABSOLUE,decimals = 2)
           # GAIN_ABSOLUE=np.round(GAIN_ABSOLUE)
           # GAIN_ABSOLUE=round(GAIN_ABSOLUE)
           GAIN_ABSOLUE=np.round(GAIN_ABSOLUE,decimals = 8)
           # GAIN_ABSOLUE=int(float(GAIN_ABSOLUE)*MULTIP)
           custom_info["GAIN_ABSOLUE"]=GAIN_ABSOLUE
           GAIN_ABSOLUE=float(GAIN_ABSOLUE)

           #if abs(GAIN) >= 0 :
           GAIN_RELATIF=(float(VAL_VENTE) - float(VAL_ACHAT))
           # GAIN_RELATIF=check_gain(GAIN_RELATIF)
           # GAIN_RELATIF=np.round(GAIN_RELATIF)
           # GAIN_RELATIF=round(GAIN_RELATIF)
           GAIN_RELATIF=np.round(GAIN_RELATIF,decimals = 8)
           # GAIN_RELATIF=int(float(GAIN_RELATIF)*MULTIP)
           custom_info["GAIN_RELATIF"]=GAIN_RELATIF
           GAIN_RELATIF=float(GAIN_RELATIF)


           custom_info["CLOSE"]=PRIX
           custom_info["CLOSE_LAST_INDEX"]=VAL_VENTE
           
           # if not "." in str(GAIN_ABSOLUE) and "0" in str(GAIN_ABSOLUE) :
           #    GAIN_ABSOLUE=str(GAIN_ABSOLUE).replace("0","")

           # if not "." in str(GAIN_RELATIF) and "0" in  str(GAIN_RELATIF) :
           #     GAIN_RELATIF= str(GAIN_RELATIF).replace("0","")   
              
           if (GAIN_RELATIF >= 0):
               if COMPTEUR_SELL == 0 :
                  # CUMUL_GAIN_RELATIF=GAIN_RELATIF
                  custom_info["CUMUL_GAIN_RELATIF"]=CUMUL_GAIN_RELATIF+GAIN_RELATIF
                  # CUMUL_GAIN_RELATIF_OLD=CUMUL_GAIN_RELATIF
               else:
                  CUMUL_GAIN_RELATIF=float(custom_info["CUMUL_GAIN_RELATIF"])
                  # CUMUL_GAIN_R
                  ELATIF_OLD=float(custom_info["CUMUL_GAIN_RELATIF"])
                  CUMUL_GAIN_RELATIF=CUMUL_GAIN_RELATIF+float(GAIN_RELATIF)
                  # CUMUL_GAIN_RELATIF=np.round(CUMUL_GAIN_RELATIF,decimals =len(str(MULTIP)))
                  custom_info["CUMUL_GAIN_RELATIF"]=CUMUL_GAIN_RELATIF
    
                  # CUMUL_GAIN_RELATIF=np.round(CUMUL_GAIN_RELATIF,decimals =len(str(MULTIP)))

              
           
           custom_info["GAIN_ABSOLUE"]=format(GAIN_ABSOLUE,'.8f') 
           custom_info["GAIN_RELATIF"]=format(GAIN_RELATIF,'.8f')

           # GAIN_ABSOLUE=int(GAIN_ABSOLUE)
           # GAIN_RELATIF=int(GAIN_RELATIF)

           if (GAIN_RELATIF < 0):
              if COMPTEUR_PERTE == 0 :
                 custom_info["CUMUL_PERTE_RELATIF"]=GAIN_RELATIF
              else:
                  custom_info["CUMUL_PERTE_RELATIF"]=float(custom_info["CUMUL_PERTE_RELATIF"])+GAIN_RELATIF
              CUMUL_PERTE_RELATIF=float(custom_info["CUMUL_PERTE_RELATIF"])
              CUMUL_PERTE_EURO=calcule_perte(CUMUL_PERTE_RELATIF)
              custom_info["CUMUL_PERTE_EURO"]=CUMUL_PERTE_EURO
              custom_info["CUMUL_PERTE_EURO"]=format(CUMUL_PERTE_EURO,'.8f')
              print("!!!!!!! CUMUL_PERTE_EURO=",CUMUL_PERTE_EURO)
              COMPTEUR_PERTE+=1
               
           COMPTEUR_SELL=1    
           #print("GAIN=",GAIN)
           print("GAIN_ABSOLUE=",format(GAIN_ABSOLUE,'.8f'))
           print("GAIN_RELATIF=",format(GAIN_RELATIF,'.8f'))
           if "CUMUL_GAIN_RELATIF" in custom_info :
               print("CUMUL_GAIN_RELATIF=",custom_info["CUMUL_GAIN_RELATIF"])
               
           if (GAIN_RELATIF > 0):               
               CUMUL_GAIN_EURO=calcule_gain(CUMUL_GAIN_RELATIF)
               custom_info["CUMUL_GAIN_EURO"]=CUMUL_GAIN_EURO


           if (GAIN_RELATIF < 0) or (GAIN_ABSOLUE < 0) and (FLAG_DERNIERE_VENTE_GAIN_ABSOLUE == 0) : # or ("GAIN NEGATIF" in PREVIOUS_MODE) :
               FLAG_SIMULATION=1
               MODE_GAIN="!!!! GAIN NEGATIF !!! \n !!! ACTIVATION MODE SIMULTATION !!!"
               PREVIOUS_MODE=MODE_GAIN
               custom_info["MODE_GAIN"]=MODE_GAIN
               TRAITEMENT_REELLE == "SIMULATION"
           #else:
               #MODE_GAIN=""
               #custom_info["MODE_GAIN"]=MODE_GAIN
               
           if (int(CUMUL_GAIN_RELATIF) > float(GAIN_ABSOLUE)) and (float(CUMUL_GAIN_RELATIF) > 0) and (FLAG_DERNIERE_VENTE_GAIN_ABSOLUE == 0) : #and (PREVIOUS_MODE == "") : # and (MODE_GAIN != "GAIN NEGATIF ACTIVATION MODE SIMULTATION") :
               MODE_GAIN="GAIN_RELATIF"
               custom_info["MODE_GAIN"]=MODE_GAIN
                
           if (int(GAIN_ABSOLUE) >= float(CUMUL_GAIN_RELATIF)) and (float(GAIN_ABSOLUE) > 0) and (FLAG_DERNIERE_VENTE_GAIN_ABSOLUE == 0) : # and (PREVIOUS_MODE == "") : # and (MODE_GAIN != "GAIN NEGATIF ACTIVATION MODE SIMULTATION") :
               MODE_GAIN="GAIN_ABSOLUE"    
               custom_info["MODE_GAIN"]=MODE_GAIN
           
           print("custom_info[MODE_GAIN]=",custom_info["MODE_GAIN"])
    


           #if not "POINT_DE_VENTE_GAIN_ABSOLUE" in custom_info:

           #if int(GAIN_ABSOLUE_OLD) > 0 :
           """
           if custom_info["POINT_DE_VENTE_GAIN_ABSOLUE"] != "" : 
               custom_info["CUMUL_GAIN_ABSOLUE"]=GAIN_ABSOLUE_OLD
               print("GAIN_ABSOLUE_OLD=",GAIN_ABSOLUE_OLD)
               time.sleep(4)
           """

           """
           TAKE_GAIN_ABSOLUE=1200
           if (GAIN_ABSOLUE >= TAKE_GAIN_ABSOLUE)  :
               custom_info["NBR_CUMUL"]=NBR_CUMUL
               custom_info["POINT_DE_VENTE_GAIN_ABSOLUE"]=GAIN_ABSOLUE
               print("POINT_DE_VENTE_GAIN_ABSOLUE: ",custom_info["POINT_DE_VENTE_GAIN_ABSOLUE"])
               print("NBR_CUMUL=",NBR_CUMUL)
               print("custom_info : NBR_CUMUL=",custom_info["NBR_CUMUL"])
               global CUMUL_GAIN_ABSOLUE
               if NBR_CUMUL == 0:
                   CUMUL_GAIN_ABSOLUE=int(GAIN_ABSOLUE) 
                   NBR_CUMUL=1
               else:
                   CUMUL_GAIN_ABSOLUE=int(CUMUL_GAIN_ABSOLUE)+int(GAIN_ABSOLUE) 
               print("CUMUL_GAIN_ABSOLUE=",CUMUL_GAIN_ABSOLUE)
               custom_info["CUMUL_GAIN_ABSOLUE"]=CUMUL_GAIN_ABSOLUE
               GAIN_ABSOLUE=0
               FIRST_VENTE = 0
             """
               
        
           """ 
           if (GAIN_NEGATIF >= 2) and (MODE_GAIN == "GAIN_RELATIF") and (FLAG_DERNIERE_VENTE_GAIN_ABSOLUE == 0):
             DERNIER_POINT_VENTE=1
             DERNIERE_VENTE_GAIN_RELATIVE=int(VAL_VENTE)
           """  
           """  
           if (GAIN_NEGATIF >= 2) and (GAIN_ABSOLUE < 0 ) and (MODE_GAIN == "GAIN_ABSOLUE") and (FLAG_DERNIERE_VENTE_GAIN_ABSOLUE == 0):
             #DERNIER_POINT_VENTE=1
             DERNIERE_VENTE_GAIN_ABSOLUE=GAIN_ABSOLUE 
             FLAG_DERNIERE_VENTE_GAIN_ABSOLUE=1
             GAIN_NEGATIF=0
  
           if (FLAG_DERNIERE_VENTE_GAIN_ABSOLUE == 1) and (GAIN_ABSOLUE  > DERNIERE_VENTE_GAIN_ABSOLUE)  :
             FLAG_DERNIERE_VENTE_GAIN_ABSOLUE=0
             BASCULE_MODE_GA_GR="GAIN_ABSOLUE  > DERNIERE_VENTE_GAIN_ABSOLUE : \n {} > {}".format(GAIN_ABSOLUE, DERNIERE_VENTE_GAIN_ABSOLUE)
             custom_info["BASCULE_MODE_GA_GR"]=BASCULE_MODE_GA_GR
           """  
             
           """  
           if (FLAG_SIMULATION == 1) and (FLAG_SIMULATION_GLOBAL == 1) and (GAIN == 0 ):   
              DERNIER_POINT_VENTE=1
              return  
           """  

               
           #if (FLAG_DERNIERE_VENTE_GAIN_ABSOLUE == 0):
           if (GAIN_RELATIF != "") or  (DIFF_DYNAMIQUE_VAL_CLOSE_VAL_CLOSE_ORG == True)  or DERNIER_POINT_VENTE==1  :
            if (FLAG_SIMULATION == 0) and (FLAG_SIMULATION_GLOBAL == 0) and ( MODE_GAIN == "GAIN_RELATIF") and (DIFF_DYNAMIQUE_VAL_CLOSE_VAL_CLOSE_ORG == True):
               CALL_TRADING(dataframe)
            if (FLAG_SIMULATION == 0) and (FLAG_SIMULATION_GLOBAL == 0) and ( MODE_GAIN == "GAIN_ABSOLUE") : #and (POINT_DE_VENTE_GAIN_ABSOLUE == 1) :
                if (GAIN_ABSOLUE > CUMUL_GAIN_RELATIF) and (GAIN_RELATIF >= 1) and custom_info["SCENARIO"] == "3eme CAS VENTE PARTOUT VVVROUGE" :
                    FLAG_VENTE_GAIN_ABSOLUE=1
                    custom_info["FLAG_VENTE_GAIN_ABSOLUE"]=FLAG_VENTE_GAIN_ABSOLUE
                    CALL_TRADING(dataframe)   
               
            if ("GAIN NEGATIF" in PREVIOUS_MODE) and (GAIN_RELATIF > 0) or (GAIN_ABSOLUE > 0):
                PREVIOUS_MODE=""
            
            print("COMPTEUR_BUY_INITIAL=",COMPTEUR_BUY_INITIAL)
            if DIFF_DYNAMIQUE_VAL_CLOSE_VAL_CLOSE_ORG == True :
                 print("!!!!!!!!!!!!! DANS EXEC_ORDER CHUTE DES PRIX BOUGIE ROUGE DECROISSANTE !!!!!!!!!!!!!".format(RECUP_LAST_PRICE_IN_FILE()))
                 time.sleep(1)
                 
            # ((int(custom_info["ACHAT_AU_DESSUS_EMA15"]) == 1) and (int(custom_info["ACHAT_EN_DESSOUS_EMA200"]) == 0))
            if (GAIN_RELATIF != "") : #or (DIFF_DYNAMIQUE_VAL_CLOSE_VAL_CLOSE_ORG == True)  : # or DERNIER_POINT_VENTE==1  :
              #or  (custom_info["SCENARIO"]=="VENTE DYNAMIQUE BOUGIE VERTE DECROISSANTE" ):
                # LAST_ORDER="SELL"
                custom_info["LAST_ORDER"]=LAST_ORDER
                
                CALL_TELEGRAMME()
                LAST_ORDER=ORDER
                print("DANS EXEC ORDER VENTE LAST_ORDER=",LAST_ORDER) 
                ORDER="" 
                #POINT_ENTRE_EMA200=0
                custom_info["SCENARIO"]=""
                if (GAIN_RELATIF > 0) :
                   TRAITEMENT_REELLE=0

                if ACHAT_DYNAMIQUE==1 :
                   ACHAT_DYNAMIQUE=0

            #else:
                 #custom_info["CUMUL_GAIN_RELATIF"]=CUMUL_GAIN_RELATIF_OLD
                 #ORDER=""

                
            """
            else :
                if (int(custom_info["ACHAT_AU_DESSUS_EMA15"]) == 1) and (int(custom_info["ACHAT_EN_DESSOUS_EMA200"]) == 0) :
                    LAST_ORDER="SELL"
                    CALL_TELEGRAMME()
                    ORDER="" 
                    custom_info["LAST_ORDER"]=LAST_ORDER
            
            custom_info["ACHAT_AU_DESSUS_EMA15"]=2
            custom_info["ACHAT_EN_DESSOUS_EMA200"]=2
            
            """
            
            """
            CALL_TELEGRAMME()
            ORDER="" 
            custom_info["LAST_ORDER"]=LAST_ORDER
            """
            
    """
        if (FLAG_BEST_NBR_TAILLE_BG == 1) and (GAIN == 0):   
           DERNIER_POINT_VENTE=1
           if "m" in  interval :
               time.sleep(60)
    """
    #POINT_ENTRE_EMA200=0
    #print("LAST_ORDER=",LAST_ORDER) 
    print("\nSORTIE DE EXEC_ORDER ")

 
def CALL_TRADING (dataframe):
    print("\nCALL_TRADING TRADING ACHAT VENTE")
    print("self.timeframe",timeframe)
	   #print("self.custom_info",self.custom_info)

    import sys
    #sys.path.insert(1,PATH)
    from TRADINGV2 import TRADINGV2
    n = TRADINGV2(custom_info,timeframe)
    n.ACHAT_VENTE(dataframe)
	   #self.custom_info["LAST_ORDER"]=LAST_ORDER
	   #return LAST_ORDER   
       
def CALL_TELEGRAMME ():
    print("CALL_TELEGRAMME")
    import sys
    #sys.path.insert(1,PATH)
    from TELEGRAMME import TELEGRAMME
    n = TELEGRAMME(custom_info,timeframe)
    n.SEND_TELEGRAMME()  

def CHECK_NEW_BG(DATE_FUTUR): 
        import os
        global RESULT_CHECK_NEW_BG
        global PATH_EMA200_DEMA40_EMA15
        DATE_FUTUR=DATE_FUTUR.strftime("%Y-%m-%d %H:%M:%S")
        BOT="BOT_EMA200_DEMA40_EMA15"
        TYPE_DEMA="DEMA40"
        PATH_EMA200_DEMA40_EMA15="/root/BOT/freqtrade/user_data/strategies/FTX_BOT/"+BOT
        PATH=PATH_EMA200_DEMA40_EMA15
        custom_info["PATH_EMA200_DEMA40_EMA15"]=PATH_EMA200_DEMA40_EMA15
        PATH=PATH+"/LISTE_TRADING/"+symbol
        SYMBOL_CSV=PATH+"/"+symbol+"_"+timeframe+".csv"
        #print("SYMBOL_CSV: ",SYMBOL_CSV)
        CMD_CHECK_NEW_BG="/usr/bin/egrep -ci '"+str(DATE_FUTUR)+"' "+str(SYMBOL_CSV)
        #print("CMD_CHECK_NEW_BG=",CMD_CHECK_NEW_BG)
        stream = os.popen(CMD_CHECK_NEW_BG) 
        RESULT_CHECK_NEW_BG= stream.read().strip()
                    
          
def TEST_FICHIER_VIDE(FICHIER) :           
        cmd_test_fichier_vide="ls -1 "+FICHIER+" > /dev/null 2>and1;echo $?"
        print("cmd_test_fichier_vide=",cmd_test_fichier_vide)
        import os
        stream = os.popen(cmd_test_fichier_vide)
        #global TEST_FICHIER_VIDE
        TEST_FICHIER_VIDE= stream.read().strip()
        print("Dans TEST_FICHIER_VIDE  :",TEST_FICHIER_VIDE)
        return int(TEST_FICHIER_VIDE)
            
def RECUPERATION_DE_LA_DERNIERE_TRAME()  : #-> dataFrame:
    try:
        #RECUPERATION DE LA DERNIERE TRAME
        global SYMBOL_CSV
        dataframe=pd.DataFrame()
        BOT="BOT_EMA200_DEMA40_EMA15"
        TYPE_DEMA="DEMA40"
        PATH_EMA200_DEMA40_EMA15="/root/BOT/freqtrade/user_data/strategies/FTX_BOT/"+BOT
        PATH=PATH_EMA200_DEMA40_EMA15
        PATH=PATH+"/LISTE_TRADING/"+symbol
        SYMBOL_CSV=PATH+"/"+symbol+"_"+timeframe+".csv"
        global i
        if i == 0 :
            print("\nRECUPERATION DE LA DERNIERE TRAME")
            print("SYMBOL_CSV: ",SYMBOL_CSV)
            print("NBR_TAILLE_BG=",NBR_TAILLE_BG)
            #i=1

        col_names = ['date',
                     'open',
                     'high',
                     'low',
                     'close',
                     'volume']
        
        #if os.stat(SYMBOL_CSV).st_size == 0 :
        #FICHIER_VIDE=TEST_FICHIER_VIDE(SYMBOL_CSV)
        #if FICHIER_VIDE != 0 :
        while True :
            df=pd.read_csv(SYMBOL_CSV,names=col_names, skiprows=[0])
            df['date']=pd.to_datetime(df['date'])
            df.date= df.date.apply(lambda d: d + pd.Timedelta(hours=TIMEDELTA))
            df = pd.DataFrame(df)
            print("\n DANS RECUPERATION_DE_LA_DERNIERE_TRAME len (df): ",len (df))
            if len (df) > 0  :  
                break
            else:
                RESTART_ONE_PAIR(symbol,timeframe)
                # time.sleep(2)
        #print("IMPORTE df: \n",df.tail())
        #print("IMPORTE df: \n",df.info())
        #print("1 ER df.info(): \n",df.info())
        #df['date'] = df.date.apply(lambda d: datetime.datetime.fromtimestamp(int(d)) + pd.Timedelta(hours=2) + pd.Timedelta(seconds=1))
        #print("\nResult Lambda: \n",df.date)
        #print("IMPORTE DATAFRAME CREATE INDICATOR : \n",dataframe[['date','DEMA40','EMA15','DIFF_DEMA40_EMA15']])
        return df
    except Exception as f:
        if  "'str' object has no attribute 'date'" in f.args :
            print(f'\nError: DANS CREATE INDICATOR RECUPERATION DE LA DERNIERE TRAME ERREUR DE LECTURE DU FICHIER: {f}')
            

          

def RESTART_ONE_PAIR(PAIR,timeframe): 
    try:
        import os
        import subprocess
        #PKILL(15,"OTHER")
        # CMD_PS="ps -ef|egrep -i \""+PAIR+"|THREAD_PTT_ftx\"|grep -v grep|awk '{print $2}'"
        # CMD_PS="ps -ef|egrep -i " +PAIR+"|egrep -i THREAD_PTT_ftx|grep -v grep|awk '{print $2}'"
        # BREAK=0
        # print("CMD_PS=",CMD_PS)
        # stream = os.popen(CMD_PS) 
        # time.sleep(1)
        # pid=stream.read().strip()
        # print ("PID=",pid)
        # if  (pid != "") : 
        #     pid=int(pid)
        #     os.kill(pid, 9) 
        #     CMD_KILL="/usr/bin/pkill -f \"THREAD_PTT_ftx.py "+PAIR+" "+timeframe +"\" 2> /dev/null"
        #     stream = os.popen(CMD_KILL) 
        #     time.sleep(2)
        #     print("CMD_KILL=",pid)
        # CMD_KILL="/usr/bin/pkill -f \"THREAD_PTT_ftx.py "+PAIR+" "+timeframe +"\" 2> /dev/null"
        # #print(CMD_KILL)
        # stream = os.popen(CMD_KILL)
        BOT="BOT_EMA200_DEMA40_EMA15"
        PATH_EMA200_DEMA40_EMA15="/root/BOT/freqtrade/user_data/strategies/FTX_BOT/"+BOT
        RESTART_PAIR=PATH_EMA200_DEMA40_EMA15+"/TOOLS/CREATE_ALL_TIMEFRAME_PEER_SYMBOL.sh "+PAIR+" "+timeframe +" |at now 2> /dev/null"
        #RESTART_PAIR="/root/BOT/freqtrade/.env/bin/python3.8 "+PATH_EMA200_DEMA40_EMA15+"/TOOLS/THREAD_PTT_ftx.py "+PAIR+" "+timeframe +" |at now 2> /dev/null"
        #os.popen(RESTART_PAIR)
        #time.sleep(1)
        os.popen(RESTART_PAIR) 
        #time.sleep(1)
    except Exception as i:
        pass
     #print(f'\nError dans RESTART_ONE_PAIR : {i}') 
     # time.sleep(0)
     #(PAIR,timeframe)      

def RESTART_ONE_PAIR_ORG(PAIR,timeframe): 
    import subprocess
    #CMD_ARG= "-Aforgrep" +PAIR+"|egrep -i THREAD_PTT_ftx"
    CMD_ARG = "-Af"
    subprocess = subprocess.Popen(['ps', CMD_ARG], stdout=subprocess.PIPE)
    output, error = subprocess.communicate()
    #print(output)
    target_process = PAIR
    for line in output.splitlines():
        if (target_process in str(line)) and ("THREAD_PTT_ftx" in str(line)) :
            pid = int(line.split(None, 1)[0])
            os.kill(pid, 9)     
            print("\nRESTART_PAIR=",PAIR)
            
    BOT="BOT_EMA200_DEMA40_EMA15"
    PATH_EMA200_DEMA40_EMA15="/root/BOT/freqtrade/user_data/strategies/FTX_BOT/"+BOT
    RESTART_PAIR=PATH_EMA200_DEMA40_EMA15+"/TOOLS/CREATE_ALL_TIMEFRAME_PEER_SYMBOL.sh "
    CMD_ARG=PAIR+" "+timeframe+" orat now and "
    subprocess = subprocess.Popen([RESTART_PAIR, CMD_ARG], stdout=subprocess.PIPE)
    output, error = subprocess.communicate()
    print(output)

     
def CALCULE_BEST_BG() :
    global NBR_TAILLE_BG
    global LAST_DATE_VENTE
    global LISTE_ACHAT_VENTE
    global FLAG_BEST_NBR_TAILLE_BG
    global PATH_EMA200_DEMA40_EMA15

    BOT="BOT_EMA200_DEMA40_EMA15"
    PATH_EMA200_DEMA40_EMA15="/root/BOT/freqtrade/user_data/strategies/FTX_BOT/"+BOT
    custom_info["PATH_EMA200_DEMA40_EMA15"]=PATH_EMA200_DEMA40_EMA15
    PATH=PATH_EMA200_DEMA40_EMA15

    #DEBUT PORGRAMME
    #TEST_BEST_BG=pd.DataFrame(columns=['LAST_LISTE_ACHAT_VENTE'])
    #NBR_TAILLE_BG_MAX=100
    liste = []
    print("\n ENTRER DANS CALCULE_BEST_BG")
    print("NBR_TAILLE_BG_MAX=",NBR_TAILLE_BG_MAX)
    print("NBRDEC=",NBRDEC)
    LEN_LISTE_ACHAT_VENTE=len(LISTE_ACHAT_VENTE)
    print("LEN_LISTE_ACHAT_VENTE=",LEN_LISTE_ACHAT_VENTE)

    if ( LEN_LISTE_ACHAT_VENTE == 0) :
    #if LEN_LISTE_ACHAT_VENTE.empty:
        print('LISTE_ACHAT_VENTE is empty!')
        FLAG_BEST_NBR_TAILLE_BG=1
        NBR_TAILLE_BG=int(NBR_TAILLE_DEFAULT_BG_1M)
        print("FIN DE LA SIMULATION FLAG_BEST_NBR_TAILLE_BG == 1")
        return
    
    LAST_INDEX_LISTE_ACHAT_VENTE=LISTE_ACHAT_VENTE.index[-1]
    LAST_LIGNE_GAIN=LISTE_ACHAT_VENTE.GAIN.iloc[-1]
    print("LAST_LIGNE_GAIN=",LAST_LIGNE_GAIN)
    if LAST_LIGNE_GAIN == 0.000000000  :
       LISTE_ACHAT_VENTE=LISTE_ACHAT_VENTE.drop(LAST_INDEX_LISTE_ACHAT_VENTE)
       print("DROP LAST_LISTE_ACHAT_VENTE=\n",LISTE_ACHAT_VENTE)

    LAST_LISTE_ACHAT_VENTE_CUMUL=LISTE_ACHAT_VENTE.CUMUL.iloc[-1]
    LAST_LISTE_ACHAT_VENTE=LISTE_ACHAT_VENTE.iloc[-1]
    DATE_VENTE=LISTE_ACHAT_VENTE.DATE_VENTE.iloc[-1]


    if (LAST_LISTE_ACHAT_VENTE_CUMUL == "") and ( LEN_LISTE_ACHAT_VENTE > 1 ):
       LAST_LISTE_ACHAT_VENTE_CUMUL=LISTE_ACHAT_VENTE.CUMUL.iloc[-2]
       LAST_LISTE_ACHAT_VENTE=LISTE_ACHAT_VENTE.iloc[-2]
       DATE_VENTE=LISTE_ACHAT_VENTE.DATE_VENTE.iloc[-2]
       
    if (LAST_LISTE_ACHAT_VENTE_CUMUL != "")  and ( LEN_LISTE_ACHAT_VENTE > 0 ):
        DATE_VENTE=DATE_VENTE.strftime("%Y-%m-%d %H:%M:%S")
        print("LAST_LISTE_ACHAT_VENTE_CUMUL={0:f}".format(LAST_LISTE_ACHAT_VENTE_CUMUL))   
        print("LAST_LISTE_ACHAT_VENTE=\n",LAST_LISTE_ACHAT_VENTE)
        #data = {'LAST_LISTE_ACHAT_VENTE':[LAST_LISTE_ACHAT_VENTE]}
        #data = {'CUMUL':[LAST_LISTE_ACHAT_VENTE]}
        global TEST_BEST_BG
        #TEST_BEST_BG=pd.DataFrame(columns=['NBR_TAILLE_BG','CUMUL'])
        #data = [NBR_TAILLE_BG,LAST_LISTE_ACHAT_VENTE_CUMUL]
        data = {'NBR_TAILLE_BG':NBR_TAILLE_BG,'CUMUL':LAST_LISTE_ACHAT_VENTE_CUMUL}
        ###TEST_BEST_BG=pd.DataFrame(data)
        ##data = [LAST_LISTE_ACHAT_VENTE]
        TEST_BEST_BG=TEST_BEST_BG.append(data,ignore_index=True)
        TEST_BEST_BG['NBR_TAILLE_BG']= TEST_BEST_BG.NBR_TAILLE_BG.apply(lambda x : x).astype(int)
        TEST_BEST_BG['CUMUL']= TEST_BEST_BG.CUMUL.apply(lambda x : x).astype(float)
        #TEST_BEST_BG=TEST_BEST_BG.append(data,ignore_index=True)
          ##print("TEST_BEST_BG=",TEST_BEST_BG[0].values)
        
        #TEST_BEST_BG=pd.DataFrame(columns=['LAST_LISTE_ACHAT_VENTE'])
        #TEST_BEST_BG=TEST_BEST_BG.append(data,ignore_index=True)
        print("TEST_BEST_BG=\n",TEST_BEST_BG)
        TRIE_BEST_BG=TEST_BEST_BG.sort_values(by = ['NBR_TAILLE_BG','CUMUL'])
        #TRIE_BEST_BG=TEST_BEST_BG.sort_values(by = ['CUMUL'])
        print("TRIE TEST_BEST_BG=\n",TRIE_BEST_BG)
        LAST_INDEX=TEST_BEST_BG.index[-1]
        print("LAST_INDEX=",LAST_INDEX)
        #LAST_LIGNE_BEST_BG=TRIE_BEST_BG.CUMUL.iloc[-1][0]
        LAST_LIGNE_BEST_BG=len(TRIE_BEST_BG.CUMUL)-1

        #print("TRIE_BEST_BG.NBR_TAILLE_BG.iloc[-1][0]=",TRIE_BEST_BG.NBR_TAILLE_BG.iloc[-1][0])

        if LAST_INDEX > 0 :
            if (TRIE_BEST_BG.CUMUL.iloc[-1] == TRIE_BEST_BG.CUMUL.iloc[-2]) and (TRIE_BEST_BG.NBR_TAILLE_BG.iloc[-1] == TRIE_BEST_BG.NBR_TAILLE_BG.iloc[-2])  :
               print("TRIE TEST_BEST_BG={}\n".format(TRIE_BEST_BG))
               TRIE_BEST_BG=TRIE_BEST_BG.drop(LAST_INDEX)
               TEST_BEST_BG=TEST_BEST_BG.drop(LAST_INDEX)
               #print("TRIE TEST_BEST_BG=\n",TRIE_BEST_BG)

        print("TRIE TEST_BEST_BG=\n",TRIE_BEST_BG)
        #LAST_LIGNE_BEST_BG=LAST_LISTE_ACHAT_VENTE.CUMUL.iloc[-1][0]
        LAST_LIGNE_BEST_BG=LAST_LISTE_ACHAT_VENTE.CUMUL
        LAST_DATE_VENTE=LAST_LISTE_ACHAT_VENTE.DATE_VENTE.strftime("%Y-%m-%d %H:%M:%S")
        LAST_BEST_PROFIT=LAST_LIGNE_BEST_BG
        #LAST_BEST_PROFIT=LAST_LIGNE_BEST_BG.CUMUL
        print("LAST LIGNE BEST_BG=",LAST_LIGNE_BEST_BG)
        print("\nLAST_DATE_VENTE=",LAST_DATE_VENTE)
        print("\nLAST_BEST_PROFIT ={}".format(LAST_BEST_PROFIT))
        LEN_LISTE_ACHAT_VENTE=len(LISTE_ACHAT_VENTE)
        print("LEN_LISTE_ACHAT_VENTE=",LEN_LISTE_ACHAT_VENTE)
    
        print("TRIE TEST_BEST_BG=\n",TRIE_BEST_BG)
        print("LAST LIGNE BEST_BG=\n",TRIE_BEST_BG.iloc[-1])
        print("\nBEST PROFIT ={0:f}".format(TRIE_BEST_BG.CUMUL.iloc[-1]))
        #print("\nBEST PROFIT ={0:f}".format(TRIE_BEST_BG.CUMUL.iloc[-1][0]))
        BEST_NBR_TAILLE_BG=TRIE_BEST_BG.NBR_TAILLE_BG.iloc[-1]
        print("BEST TAILLE BG=",BEST_NBR_TAILLE_BG)
        #NBR_TAILLE_BG=NBR_TAILLE_BG+NBRDEC
        print("NBR_TAILLE_BG= ",NBR_TAILLE_BG)
        print("NBR_TAILLE_BG_MAX= ",NBR_TAILLE_BG_MAX)
        if (NBR_TAILLE_BG == NBR_TAILLE_BG_MAX) : #or (LEN_LISTE_ACHAT_VENTE == 1) : # or("1m" in  interval) or (LEN_LISTE_ACHAT_VENTE == 1) :
           NBR_TAILLE_BG=BEST_NBR_TAILLE_BG
           FLAG_BEST_NBR_TAILLE_BG=1
           print("FIN DE LA SIMULATION FLAG_BEST_NBR_TAILLE_BG == 1")

        NBR_TAILLE_BG=NBR_TAILLE_BG+NBRDEC
        print("INCREMENTATION TAILLE_BG= ",NBR_TAILLE_BG)
        
        time.sleep(1)
    else:
        if (NBR_TAILLE_BG < NBR_TAILLE_BG_MAX) :
            NBR_TAILLE_BG=NBR_TAILLE_BG+NBRDEC
            print("INCREMENTATION TAILLE_BG= ",NBR_TAILLE_BG)
            time.sleep(1)
        else:
            NBR_TAILLE_BG=NBR_TAILLE_DEFAULT_BG_1M
            FLAG_BEST_NBR_TAILLE_BG=1
            print("FIN DE LA SIMULATION FLAG_BEST_NBR_TAILLE_BG = ",NBR_TAILLE_BG)
            time.sleep(1)

##################DEBUT TRAITEMENT####################
TEST_BEST_BG=pd.DataFrame()
global NBR_TAILLE_BG
NBR_TAILLE_BG=0
global NBR_TAILLE_DEFAULT_BG_1M
global FLAG_BEST_NBR_TAILLE_BG
global TRAITEMENT_REELLE
global TIMEDELTA
global NBRDEC
global POINT_ENTRE_EMA200
global PT_RESISTANCE_HAUT_EMA1H_EMA15
global LAST_DATE_VENTE
global NBR_TAILLE_BG_MAX
global custom_info
global FLAG_SIMULATION
global PATH_EMA200_DEMA40_EMA15
global LAST_ORDER
global ORDER
global FIRST_VENTE
global COMPTEUR_BUY_SELL
global GAIN_RELATIF
global COMPTEUR_BUY_INITIAL
global COMPTEUR_SELL
COMPTEUR_SELL=0
global COMPTEUR_TEMPORELLE
COMPTEUR_TEMPORELLE=0
global VAL_ACHAT
global CUMUL_GAIN_OLD
CUMUL_GAIN_OLD=0
global NBR_CUMUL
NBR_CUMUL=0
global GAIN_ABSOLUE
GAIN_ABSOLUE=0
global GAIN_ABSOLUE_OLD
GAIN_ABSOLUE_OLD=0
global VAL_ACHAT_INITIALE
VAL_ACHAT_INITIALE=0
VAL_ACHAT=0
global PREVIOUS_MODE
PREVIOUS_MODE=""
global MODE_GAIN
MODE_GAIN=""
global GAIN_NEGATIF
GAIN_NEGATIF=0
global LAST_FRONT_NEUTRE_EMA15
LAST_FRONT_NEUTRE_EMA15=0
global FLAG_DERNIERE_VENTE_GAIN_ABSOLUE
FLAG_DERNIERE_VENTE_GAIN_ABSOLUE=0
global DERNIERE_VENTE_GAIN_ABSOLUE
#global POINT_DE_VENTE_GAIN_ABSOLUE
#POINT_DE_VENTE_GAIN_ABSOLUE=0
global FLAG_SIMULATION_GLOBAL
FLAG_SIMULATION_GLOBAL=1
GAIN_RELATIF=0
COMPTEUR_BUY_INITIAL=0
COMPTEUR_BUY_SELL=0
FIRST_VENTE=0
global VAL_NBR_PREC_LONG
# VAL_NBR_PREC_LONG=100
VAL_NBR_PREC_LONG=20
global POINT_SOMMET_HAUT_EMA200
POINT_SOMMET_HAUT_EMA200=0
global DIFF_DYNAMIQUE_VAL_CLOSE_VAL_CLOSE_ORG
DIFF_DYNAMIQUE_VAL_CLOSE_VAL_CLOSE_ORG=False
global ACHAT_DYNAMIQUE
global VENTE_DYNAMIQUE
ACHAT_DYNAMIQUE=0
VENTE_DYNAMIQUE=0
global last_price
last_price=0
global CLOSE_LAST_INDEX_ORG
CLOSE_LAST_INDEX_ORG=0
global LIST_LAST_VAL_CLOSE_VAL_ACHAT
LIST_LAST_VAL_CLOSE_VAL_ACHAT = {'LAST_VAL_CLOSE_VAL_ACHAT': pd.DataFrame(columns=['DATE_COURANTE', 'DIFF_CLOSE_VAL_CLOSE'])}
global VARIATION_PRIX
VARIATION_PRIX=False
global LEN_2_ELEMENT
LEN_2_ELEMENT=0
global DIFF_CLOSE_VAL_CLOSE
DIFF_CLOSE_VAL_CLOSE=0
global COULEUR_VOLUME
COULEUR_VOLUME=""
global DATE_HEURE
DATE_HEURE=""
global VOLUME_ASK
global PRICE_ASK
global VOLUME_BID
global PRICE_BID
VOLUME_ASK=0
PRICE_ASK=0
VOLUME_BID=0
PRICE_BID=0
global NEW_EMA1H
NEW_EMA1H=0
global NEW_EMA1L
NEW_EMA1L=0
global NEW_LAST_PRICE
NEW_LAST_PRICE=0
global FIRST_ACHAT
FIRST_ACHAT=0
# global NBR_LAST_PRICE
# NBR_LAST_PRICE=0
# global OLD_LAST_PRICE
# OLD_LAST_PRICE=""
global SEUIL
SEUIL=0
global PRIX
PRIX=0
global NBR_Diff_last_price_OLD_LAST_PRICE
NBR_Diff_last_price_OLD_LAST_PRICE=0
global DERNIERE_VENTE_POSITIVE
DERNIERE_VENTE_POSITIVE=0
global COMPTEUR_ACHAT_VENTE
COMPTEUR_ACHAT_VENTE=0
global COMPTEUR_VENTE_RELATIVE
COMPTEUR_VENTE_RELATIVE=0
global GAIN_OLD
global GAIN1
GAIN_OLD=0
GAIN1=0
global Diff_VAL_ACHAT_GAIN1_MOINS_VAL_ACHAT
Diff_VAL_ACHAT_GAIN1_MOINS_VAL_ACHAT=0
global OLD_DATE_HEURE
global OLD_Diff_VOLUME_VWAP_LAST_PRICE_OLD_LAST_PRICE
OLD_DATE_HEURE=""
OLD_Diff_VOLUME_VWAP_LAST_PRICE_OLD_LAST_PRICE=0
global Diff_VOLUME_VWAP_Diff_VOLUME_VWAP_OLD
Diff_VOLUME_VWAP_Diff_VOLUME_VWAP_OLD=0
global CUMUL_GAIN_ABSOLUE
CUMUL_GAIN_ABSOLUE=0
global COMPTEUR_NEGATIF
COMPTEUR_NEGATIF=0
global COMPTEUR_GAIN_ZERO
COMPTEUR_GAIN_ZERO=0
global DIFF_GAIN_ABSOLUE
DIFF_GAIN_ABSOLUE=0
global last_price_file
last_price_file=0
global NEW_HIGH_PRICE
NEW_HIGH_PRICE=0
global NEW_OPEN_PRICE
NEW_OPEN_PRICE=0
global TAILLE_BG_BIS
TAILLE_BG_BIS=0
global TYPE_BG_BIS
TYPE_BG_BIS="NEANT"
global CUMUL_GAIN_RELATIF
CUMUL_GAIN_RELATIF=0
global DIFF_VAL_CLOSE_INF_VAL_CLOSE_N1
DIFF_VAL_CLOSE_INF_VAL_CLOSE_N1 =""
global TIME_DEB_CYCLE_ACHAT
global TIME_DEB_ACHAT
global QUANTITE_ACHAT
QUANTITE_ACHAT=0
global QUANTITE_VENTE
QUANTITE_VENTE=0
global PRICE_VOLUME_ASK
PRICE_VOLUME_ASK=0
global PRICE_VOLUME_BID
PRICE_VOLUME_BID=0
global SPREAD
SPREAD=0
global DIFF_NEW_HIGH_PRICE_SUP_NEW_OPEN_PRICE
DIFF_NEW_HIGH_PRICE_SUP_NEW_OPEN_PRICE=False
global LAST_PRICE
LAST_PRICE=0
global DATE_VENTE_FUTUR
DATE_VENTE_FUTUR=""
global TEMPS
TEMPS=2
global CYCLE_COURT
CYCLE_COURT=False
global GAIN_ABSOLUE_RELATIF
GAIN_ABSOLUE_RELATIF=0
global DIFF_SAR_SUP_PRIX
DIFF_SAR_SUP_PRIX=""
global DIFF_SAR_SUP_EMA15
DIFF_SAR_SUP_EMA15=""
global DIFF_SAR_SUP_OPEN
DIFF_SAR_SUP_OPEN=""
global COMPTEUR_DIFF_GAIN1_EGAL
COMPTEUR_DIFF_GAIN1_EGAL=0
global NBR_COMPTEUR_DIFF_GAIN1
NBR_COMPTEUR_DIFF_GAIN1=0
global DIFF_GAIN1_INF_GAIN_OLD
DIFF_GAIN1_INF_GAIN_OLD=0




custom_info={}
custom_info["MODE_GAIN"]=MODE_GAIN
custom_info["VAL_ACHAT_INITIALE"]=0
custom_info["NBR_CUMUL"]=""
custom_info["symbol"]=symbol
custom_info["SCENARIO"]=""

BOT="BOT_EMA200_DEMA40_EMA15"
PATH_EMA200_DEMA40_EMA15="/root/BOT/freqtrade/user_data/strategies/FTX_BOT/"+BOT
custom_info["PATH_EMA200_DEMA40_EMA15"]=PATH_EMA200_DEMA40_EMA15
custom_info["MODE_TRADING"]="OK" 
#custom_info["MODE_TRADING"]="KO" 
#custom_info["MODE_FUTUR"]="OK"  
custom_info["MODE_FUTUR"]="KO"  
custom_info["MSG_ALERTE"]=""
#custom_info["MSG_ALERTE"]="ALERTE"
custom_info["ACHAT_EN_DESSOUS_EMA200"]=2
custom_info["ACHAT_AU_DESSUS_EMA15"]=2
custom_info["ORDER"]=""
custom_info["LAST_ORDER"]=""
custom_info["GAIN_ABSOLUE_PRECEDENT"]=0
custom_info["CUMUL_GAIN_ABSOLUE"]=0
custom_info["CUMUL_PERTE_RELATIF"]=0
custom_info["CUMUL_GAIN_RELATIF"]=0
custom_info["CUMUL_GAIN_EURO"]=0
custom_info["CUMUL_PERTE_EURO"]=0
global COMPTEUR_PERTE
COMPTEUR_PERTE=0
ORDER="ORDER"
LAST_ORDER="LAST_ORDER"
PATH=PATH_EMA200_DEMA40_EMA15
FLAG_SIMULATION=0
LAST_DATE_VENTE=""
POINT_ENTRE_EMA200=0
#TIMEDELTA=2
#TIMEDELTA=1
TIMEDELTA=0
#TRAITEMENT_REELLE=0
TRAITEMENT_REELLE="DEBUT TRADE EN SIMULATION"
FLAG_BEST_NBR_TAILLE_BG=0 
NBR_TAILLE_BG_MAX=200
NBR_TAILLE_DEFAULT_BG_1M=40
NBR_TAILLE_BG_MAX=200
NBRDEC=10  


if "1m" in  interval :
    NBR_TAILLE_BG_MAX=int(NBR_TAILLE_BG_MAX/10)
    NBRDEC=int(NBRDEC/10)
RESTART_ONE_PAIR(symbol,timeframe)
#time.sleep(2)      
dataframe=populate_indicators_INIT()
#RESTART_ONE_PAIR(symbol,timeframe)
#time.sleep(2)


while True :
    INIT(dataframe)
    MAIN(dataframe)
    global LISTE_ACHAT_VENTE
    LEN_LISTE_ACHAT_VENTE=len(LISTE_ACHAT_VENTE)
    print("LEN_LISTE_ACHAT_VENTE=",LEN_LISTE_ACHAT_VENTE)
    if ( LEN_LISTE_ACHAT_VENTE != 0)  :
        LAST_LISTE_ACHAT_VENTE=LISTE_ACHAT_VENTE.CUMUL.iloc[-1]
 
    if FLAG_BEST_NBR_TAILLE_BG == 0 :
       CALCULE_BEST_BG()    
    """
    if (FLAG_BEST_NBR_TAILLE_BG == 0) :
      if (LAST_LISTE_ACHAT_VENTE != "") and ( LEN_LISTE_ACHAT_VENTE != 0)  :
         CALCULE_BEST_BG()
      
      else:
          NBR_TAILLE_BG=6
          FLAG_BEST_NBR_TAILLE_BG=1
          print("MODE MINUTE")
          #ON QUITTE LA COURBE
      """
