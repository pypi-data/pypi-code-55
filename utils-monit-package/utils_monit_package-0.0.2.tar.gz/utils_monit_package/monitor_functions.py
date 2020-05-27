import os

# Definiamo la funzione per gestire l'allarme timeout
def Segnalazione_Errore(E_msg,E_obj,E_app):
    cmd = 'opcmsg a=' + E_app + ' o=' + E_obj + ' msg_t=' + E_msg
    os.system(cmd)
    #sys.exit()
 

def Scrittura_Log(LogFile,Step,Step_Time,Stato,Sentinella,Adesso,Servizio):
    sfile = open(LogFile,"a")
    riga_to_insert = Sentinella + "," + Adesso + "," + Step + "," + Stato + "," + str(Step_Time) + ".0,00000," + Servizio + "\n"
    sfile.write(riga_to_insert)
    sfile.close()