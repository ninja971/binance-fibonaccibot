#FONCTION PRODUCTION DETECTION POINT ORIGINE 
from pandas import DataFrame
from functools import reduce
import pandas as pd
import arrow
import talib.abstract as ta
import requests
import datetime
import numpy as np
import sys
from pprint import pprint
import json
import time
import pytz
import os



class TELEGRAMME():

    def __init__(self, custom_info,timeframe):
       self.custom_info = custom_info
       self.timeframe = timeframe
       self.CLOSE = self.custom_info["CLOSE"]
       self.CLOSE_LAST_INDEX = self.custom_info["CLOSE_LAST_INDEX"]
       self.PAIR=self.custom_info["PAIR"]
       self.ORDER=self.custom_info["ORDER"]
       self.LAST_ORDER=self.custom_info["LAST_ORDER"]
       self.PATH_EMA200_DEMA40_EMA15=self.custom_info["PATH_EMA200_DEMA40_EMA15"]
       self.PATH=self.PATH_EMA200_DEMA40_EMA15
       PAIR=self.custom_info["DATAFRAME_PAIR"]
       self.PATH=self.PATH+"/LISTE_TRADING/"+PAIR
       self.COMPTEUR_BUY_SELL=self.custom_info["COMPTEUR_BUY_SELL"]
       CUMUL_PERTE_RELATIF=self.custom_info["CUMUL_PERTE_RELATIF"]

       
       
    def WRITE_FILE(self,FICHIER,TEST_FIRST_SEND_MSG):
    # ENTRE DANS  WRITE_FILE FICHIER /root/BOT/freqtrade/TEST_FIRST_SEND_PAIR = et MSG = NEO/BTC_0.000909
    #    import sys
    #    from pprint import pprint
        # We open the log file in writting mode
        print("ENTRE DANS  WRITE_FILE FICHIER {} = et MSG = {}".format(FICHIER,TEST_FIRST_SEND_MSG))
        fichier = open(FICHIER, "a")
        fichier.write("\n"+TEST_FIRST_SEND_MSG)
        fichier.close()




    def TEST_SEND_PAIR(self,FICHIER,TEST_FIRST_SEND_MSG):
        import os
        cmd_TOUCH_FILE="touch "+FICHIER
        print("cmd_TOUCH_FILE=",FICHIER)
        import os
        stream = os.popen(cmd_TOUCH_FILE)
        """
        if os.stat(FICHIER).st_size == 0 :
            FICHIER = open(FICHIER,"w")
            FICHIER.close()
        """
        print("ENTRE DANS TEST_SEND_PAIR FICHIER  = ",FICHIER)
        chaine = TEST_FIRST_SEND_MSG
        print("chaine =",chaine)
        ENV_MSG="NON"
        val_chaine=0
        fichier = open(FICHIER,"r")
        for ligne in fichier:
         #print("ligne =",ligne)
         if chaine  in ligne:
           val_chaine=1
        fichier.close()

        print("TROUVE_PAIR=",val_chaine)
        if not  val_chaine == 1 :
           self.WRITE_FILE(FICHIER, TEST_FIRST_SEND_MSG)
           ENV_MSG="OUI"

        if os.stat(FICHIER).st_size == 0 :
           fichier.close()
           self.WRITE_FILE(FICHIER, TEST_FIRST_SEND_MSG)
           ENV_MSG="OUI"
        print("DANS TEST_SEND_PAIR ENV_MSG=",ENV_MSG)
        #exit()
        return ENV_MSG
         #fichier.close()
         #exit()



    def SEND_TELEGRAMME(self) :
     try:  
        PAIR=self.PAIR
        ORDER=self.ORDER
        CLOSE=self.CLOSE
        CLOSE_LAST_INDEX=self.CLOSE_LAST_INDEX
        LAST_ORDER=self.LAST_ORDER
        #print("ENTRER DANS TELEGRAMME TEST CROSSING ORDER=",ORDER," PAIR=",PAIR)
        # CLOSE=(format(CLOSE,'.8f'))
        print("\nENTRER DANS TELEGRAMME TEST CROSSING ORDER={} LAST_ORDER={} et PAIR={} et CLOSE={}".format(ORDER,LAST_ORDER,PAIR,CLOSE))
        if PAIR == "" or ORDER == "" :
           return
        #if PAIR != "" and ORDER != "" and LAST_ORDER == ORDER or ORDER == "ORDRE_TRAITER" :
        #   return
        if ORDER == "NO_TRADING" :
           return
        if "MSG_ALERTE" in self.custom_info  :
            if self.custom_info["MSG_ALERTE"] == "ALERTE" :
               return       
            else:
                self.custom_info["MSG_ALERTE"]=""
        
       #df = pd.DataFrame.from_dict(metadata, orient = 'index').iloc[0].iloc[0]
        #print("metadata=",df)
        # CLOSE=str(CLOSE)
        # CLOSE=(format(CLOSE,'.8f'))
        print("CLOSE=",CLOSE)
        CLOSE_LAST_INDEX=str(CLOSE_LAST_INDEX)
        print("CLOSE_LAST_INDEX=",CLOSE_LAST_INDEX)
        print(datetime.datetime.today().strftime("%Y-%m-%d %H:%M:%S"))
        HEURE_LOCALE=datetime.datetime.today().strftime("%Y-%m-%d %H:%M:%S")
        #df2 = dataframe['date'].apply(lambda x: pd.to_datetime(x).tz_convert('Europe/Paris'))
        #HEURE_UTC_2=pd.to_datetime(HEURE_LOCALE).tz_localize('Europe/Paris').tz_convert(None)
        HEURE_UTC_2=pd.to_datetime(HEURE_LOCALE).tz_localize('Europe/Paris').tz_convert('Europe/Paris')
        HEURE_UTC_2=HEURE_UTC_2.strftime("%Y-%m-%d %H:%M:%S")
        print("HEURE_UTC_2=",HEURE_UTC_2)
        #VAL_CROSSING_DATE_TIME=HEURE_LOCALE
        #HEURE_CROISEMENT_PAIR="HEURE_CROISEMENT"+PAIR
        HEURE_CROISEMENT=self.custom_info["HEURE_CROISEMENT_PAIR"]
        VAL_CROSSING_DATE_TIME=str(HEURE_CROISEMENT)
        print("VAL_CROSSING_DATE_TIME=",VAL_CROSSING_DATE_TIME)
        #TEST_FIRST_SEND_MSG=PAIR+"_"+str(VAL_CROSSING_DATE_TIME)
        ORDER=ORDER.upper()
        ENV_MSG="ENV_MSG_"+ORDER
        ENV_MSG_FILE=""
        VAL_ENV_MSG=self.custom_info[ENV_MSG]
        if ( not "FLAG_SIMULATION" in VAL_ENV_MSG ) :
            TEST_FIRST_SEND_MSG=PAIR+"_"+str(CLOSE)
            #FICHIER="/root/BOT/freqtrade/TEST_FIRST_SEND_PAIR"
            FICHIER=self.PATH+"/FIRST_SEND_PAIR_"+self.PAIR
            ENV_MSG_FILE=self.TEST_SEND_PAIR(FICHIER,TEST_FIRST_SEND_MSG)
            print("ENV_MSG ",ENV_MSG,"ENV_MSG_FILE=",ENV_MSG_FILE)
            if  ENV_MSG_FILE == "NON" :
                return
        #self.VARIABLE_GLOBALE(ENV_MSG,VAL_ENV_MSG)
        #PAIR  = PAIR.replace("/","").strip()
        #DATAFRAME_PAIR="DATAFRAME_"+PAIR
        #Cross_buy=self.custom_info[DATAFRAME_PAIR]
        couleur=self.custom_info["couleur"].upper()
        TYPE_CROISEMENT=self.custom_info["TYPE_CROISEMENT"]
        TYPE_CROISEMENT_EMA200=self.custom_info["TYPE_CROISEMENT_EMA200"]
        TYPE_CROISEMENT_EMA1H=self.custom_info["TYPE_CROISEMENT_EMA1H"]

        timeframe=self.custom_info["TIMEFRAME"]

        #df1['newdate'] = df1['date'].apply(lambda x: pd.to_datetime(x).tz_localize('Europe/Paris').tz_convert(None))
        #MSG = ORDER+" HEURE UTC 2 "+ HEURE_UTC_2 + " CROISEMENT "+ couleur +" EN " + TYPE_CROISEMENT
        MSG ="TIMEFRAME: "+timeframe+ "\nSCENARIO: " + str(self.custom_info["SCENARIO"])+ "\n"+ORDER+ " SUR "+ couleur +" EN \n" + str(TYPE_CROISEMENT_EMA200) +" \n " + str(TYPE_CROISEMENT) \
        +" \n " + str(TYPE_CROISEMENT_EMA1H) + "\nPOUR L'ORDRE DE TYPE : " + str(self.custom_info["TYPE"])
        # MSG ="TIMEFRAME: "+timeframe+ "\nSCENARIO: " + str(self.custom_info["SCENARIO"])+ "\n"+ORDER+ " SUR "+ couleur + "\nPOUR L'ORDRE DE TYPE : " + str(self.custom_info["TYPE"])        
        #MSG = ORDER+ " CROISEMENT "+ couleur +" EN " + TYPE_CROISEMENT_EMA200 +" EN  MODE " + TYPE_CROISEMENT +"\nPOUR L'ORDRE DE TYPE : " + str(self.custom_info["TYPE"])
        #MSG = ORDER+" HEURE LOCAL = " + HEURE_LOCALE + " HEURE UTC 2 "+ HEURE_UTC_2 +" CROISEMENT "+ couleur +" EN " + TYPE_CROISEMENT
        MSG_GAIN ="" 
        print("VAL_ENV_MSG=",VAL_ENV_MSG)
        self.custom_info["ETAPE"]="VIDE"
        
        if (VAL_ENV_MSG == "OUI" or  VAL_ENV_MSG == "FLAG_SIMULATION" or  VAL_ENV_MSG == "FLAG_SIMULATION_TRAITEMENT_REELLE"  ) or (VAL_ENV_MSG == "OUI" and ENV_MSG_FILE  == "OUI" ) :
           if (VAL_ENV_MSG == "FLAG_SIMULATION" ) :
               MSG="!!!! MODE SIMULATION !!!! \n"+MSG
           if (VAL_ENV_MSG == "FLAG_SIMULATION_TRAITEMENT_REELLE" ) :
               MSG="!!!! FLAG_SIMULATION_TRAITEMENT_REELLE !!!! \n"+MSG
           if ORDER == "SELL" or ORDER == "BUY" :
            if  ("VAL_ACHAT_INITIALE" in  self.custom_info) :
                  #if ("GAIN NEGATIF" in self.custom_info["MODE_GAIN"]) :
              if (self.custom_info["MODE_GAIN"] != "") :
                     VAL_ACHAT_INITIALE=self.custom_info["VAL_ACHAT_INITIALE"]
                     VAL_ACHAT_INITIALE=(format(VAL_ACHAT_INITIALE,'.8f'))
                     VAL_CROSSING_DATE_TIME=VAL_CROSSING_DATE_TIME+"\nACHAT INITIALE: " + str(VAL_ACHAT_INITIALE)
                     VAL_ACHAT=self.custom_info["VAL_ACHAT"]
                     VAL_ACHAT=(format(VAL_ACHAT,'.8f'))
                     VAL_CROSSING_DATE_TIME=VAL_CROSSING_DATE_TIME+"\nACHAT RELATIF: " + str(VAL_ACHAT)   
                     print("1_VAL_CROSSING_DATE_TIME")

                       
                  # #if ("VAL_ACHAT_RELATIF" in self.custom_info) :
                  #    VAL_CROSSING_DATE_TIME=VAL_CROSSING_DATE_TIME+"\nACHAT INITIALE: " + str(self.custom_info["VAL_ACHAT_INITIALE"]) 
                  # #if ("VAL_ACHAT_RELATIF" in self.custom_info) :
                  #    VAL_CROSSING_DATE_TIME=VAL_CROSSING_DATE_TIME+"\nACHAT RELATIF: " + str(self.custom_info["VAL_ACHAT"])      
              if ORDER == "SELL" :
                  if (self.custom_info["MODE_GAIN"] != "") :
                   CUMUL_GAIN_RELATIF=self.custom_info["CUMUL_GAIN_RELATIF"]
                   CUMUL_GAIN_RELATIF=(format(CUMUL_GAIN_RELATIF,'.8f'))
                   CUMUL_GAIN_EURO=self.custom_info["CUMUL_GAIN_EURO"]
                   CUMUL_GAIN_EURO=(format(CUMUL_GAIN_EURO,'.8f'))
                   if "CUMUL_PERTE_EURO" in self.custom_info :
                       CUMUL_PERTE_EURO=self.custom_info["CUMUL_PERTE_EURO"]
                       print("DANS TELEGRAMME CUMUL_PERTE_EURO:",CUMUL_PERTE_EURO)
                       # CUMUL_PERTE_EURO=(format(CUMUL_PERTE_EURO,'.8f'))
                   print("2_CUMUL_GAIN_EURO")


                   MSG_GAIN ="\n MODE GAIN: " + str(self.custom_info["MODE_GAIN"]) +"\nGAIN ABSOLUE: " + str(self.custom_info["GAIN_ABSOLUE"]) +"\nGAIN RELATIF: " + str(self.custom_info["GAIN_RELATIF"]) \
                   +"\nCUMUL_GAIN RELATIF: " + str(CUMUL_GAIN_RELATIF) +"\nCUMUL_GAIN_EURO: " + str(CUMUL_GAIN_EURO)
                   if "CUMUL_PERTE_EURO" in self.custom_info :
                       MSG_GAIN = MSG_GAIN +"\nCUMUL_PERTE_EURO: " + str(CUMUL_PERTE_EURO)
                   # MSG_GAIN = MSG_GAIN +"\nDIFF GAIN ABSOLUE : " + str(self.custom_info["DIFF_GAIN_ABSOLUE"])    
                   print("3_MSG_GAIN")  
                   
                   # if "BASCULE_MODE_GA_GR" in self.custom_info :
                   #     if self.custom_info["BASCULE_MODE_GA_GR"] != "" :
                   #         MSG_GAIN = MSG_GAIN +"\nBASCULE MODE GAIN ABSOLUE VERS GAIN RELATF : \n" + str(self.custom_info["BASCULE_MODE_GA_GR"])
                   #         self.custom_info["BASCULE_MODE_GA_GR"]=""
    
                  if "POINT_DE_VENTE_GAIN_ABSOLUE" in self.custom_info :
                       print("3_POINT_DE_VENTE_GAIN_ABSOLUE")  
                       if self.custom_info["POINT_DE_VENTE_GAIN_ABSOLUE"] != "" :
                           MSG_GAIN = MSG_GAIN +"\n TAKE PROFIT : " + str(self.custom_info["POINT_DE_VENTE_GAIN_ABSOLUE"])                      
                           self.custom_info["POINT_DE_VENTE_GAIN_ABSOLUE"]=""
                          
                  if "CUMUL_PERTE_RELATIF" in self.custom_info :
                       print("3_CUMUL_PERTE_RELATIF")  
                       if self.custom_info["CUMUL_PERTE_RELATIF"] != "" :
                           MSG_GAIN = MSG_GAIN +"\n CUMUL_PERTE_RELATIF :" + str(self.custom_info["CUMUL_PERTE_RELATIF"])                      

                          # """
                          # if "CUMUL_GAIN_ABSOLUE" in self.custom_info :
                          #   #if self.custom_info["CUMUL_GAIN_ABSOLUE"] != "" :
                          #     MSG_GAIN = MSG_GAIN +"\n CUMUL GAIN ABSOLUE : \n" + str(self.custom_info["CUMUL_GAIN_ABSOLUE"])    
                          #     print("CUMUL_GAIN_ABSOLUE: ",self.custom_info["CUMUL_GAIN_ABSOLUE"])
                          #     #exit()
                          # """
                              
           # #"""              
           # if "CUMUL_GAIN_ABSOLUE" in self.custom_info :
           #     if self.custom_info["CUMUL_GAIN_ABSOLUE"] != "" :
           #         MSG_GAIN = MSG_GAIN +"\nCUMUL GAIN ABSOLUE : " + str(self.custom_info["CUMUL_GAIN_ABSOLUE"])    
                   #self.custom_info["CUMUL_GAIN_ABSOLUE"]=""
                   #self.custom_info["NBR_CUMUL"]="" 

               #print(MSG_GAIN,"=",MSG_GAIN)
               #print("CUMUL_GAIN_ABSOLUE: ",self.custom_info["CUMUL_GAIN_ABSOLUE"])
               #exit()
           #"""     
           
           if (ORDER == "BUY") and ("ACHAT_EN_DESSOUS_EMA200" in  self.custom_info) :
               if (self.custom_info["ACHAT_EN_DESSOUS_EMA200"] == 1 ):  
                  MSG=MSG+"\n!!!! ACHAT_EN_DESSOUS_EMA200 !!!!"
           
           # if (ORDER == "BUY") and ("MODE_GAIN" in  self.custom_info) :
           #     if ("GAIN NEGATIF" in self.custom_info["MODE_GAIN"]) :
           #         VAL_ACHAT_INITIALE=self.custom_info["VAL_ACHAT_INITIALE"]
           #         VAL_ACHAT_INITIALE=(format(VAL_ACHAT_INITIALE,'.8f'))
           #         VAL_CROSSING_DATE_TIME=VAL_CROSSING_DATE_TIME+"\nACHAT INITIALE: " + str(VAL_ACHAT_INITIALE)
           #         if ("VAL_ACHAT_RELATIF" in self.custom_info) :
           #             VAL_ACHAT=self.custom_info["VAL_ACHAT"]
           #             VAL_ACHAT=(format(VAL_ACHAT,'.8f'))
           #             VAL_CROSSING_DATE_TIME=VAL_CROSSING_DATE_TIME+"\nACHAT RELATIF: " + str(VAL_ACHAT)   
           #         if (self.custom_info["MODE_GAIN"] != "") :
           #             MSG_GAIN ="\n MODE GAIN: " + str(self.custom_info["MODE_GAIN"])  
                       
           if (ORDER == "BUY"):
               TYPE="\nACHAT N° : "
           else:
               TYPE="\nVENTE N° : "
           
           print("4_TELEGRAM_JMB")
           self.custom_info["ETAPE"]="4_TELEGRAM_JMB"
     
           TELEGRAM_JMB="https://api.telegram.org/bot1703103353:AAFTnMpkee5ea_2hfVEYPprgi7D5kn-A57s/sendMessage?chat_id=1884218992=&text="
           TELEGRAM_SARAH="https://api.telegram.org/bot5116065198:AAHfOuF3QfT5w26MvAt0tw8726znZK7kruc/sendMessage?chat_id=2032377684=&text="
           
           #VAR= TELEGRAM_JMB + MSG + "\nDATE="+VAL_CROSSING_DATE_TIME+"\nPAIR = " + PAIR + " CLOSE= " + CLOSE + " CLOSE_LAST_INDEX= " + CLOSE_LAST_INDEX + MSG_GAIN
           #VAR="https://api.telegram.org/bot1703103353:AAFTnMpkee5ea_2hfVEYPprgi7D5kn-A57s/sendMessage?chat_id=1884218992=&text=" + MSG + "metadata = " + df
           #r = requests.get(VAR)
           #VAR_SARAH="https://api.telegram.org/bot5116065198:AAHfOuF3QfT5w26MvAt0tw8726znZK7kruc/sendMessage?chat_id=2032377684=&text=" + MSG + "\nDATE="+VAL_CROSSING_DATE_TIME+"\nPAIR = " + PAIR + " CLOSE= " + CLOSE + " CLOSE_LAST_INDEX= " + CLOSE_LAST_INDEX + MSG_GAIN
           for TELEGRAM in TELEGRAM_JMB, TELEGRAM_SARAH :
               #VAR= TELEGRAM + MSG + TYPE + str(self.COMPTEUR_BUY_SELL) + "\nDATE="+VAL_CROSSING_DATE_TIME+"\nPAIR = " + PAIR + " CLOSE= " + CLOSE + " CLOSE_LAST_INDEX= " + CLOSE_LAST_INDEX + MSG_GAIN
               VAR= TELEGRAM + MSG + TYPE + str(self.COMPTEUR_BUY_SELL) + "\nDATE="+VAL_CROSSING_DATE_TIME+"\nPAIR = " + str(PAIR) + " CLOSE= " + str(CLOSE) + MSG_GAIN
               r = requests.get(VAR) 
               # self.custom_info["LAST_ORDER"] = self.custom_info["ORDER"]
               self.custom_info["ORDER"] = "ORDRE_TRAITER"
               
        print("\nSORTIE DANS TELEGRAMME TEST CROSSING ORDER={} LAST_ORDER={} et PAIR={}".format(ORDER,LAST_ORDER,PAIR))
        
     except Exception as j:
         pass