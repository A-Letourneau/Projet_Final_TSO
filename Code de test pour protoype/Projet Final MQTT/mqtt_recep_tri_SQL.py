import paho.mqtt.client as paho
import json
import sqlite3
import time

"""
Exemple de Json recu
{
  "NomEsp32": "enigmeTest1",
  "JsonData": '{ "sw1": "0", "sw2": "0", "btn1": "0" }'
}
Exemple de Json complet
{
  "Id": 1,
  "NomRaspPI": "RASP_PI_MASTER",
  "NomEsp32": "ESP_BOUTON",
  "timestamp": 123456789,
  "NumeroDeEssai": 2,
  "TempsDepuisLeDebut": "1m30",
  "EtapeDeEnigme": 4,
  "TempsDepuisLaDerniereEtape": "0m30",
  "EtapeReussi": 1,
  "MalletteReussi": 1,
  "JsonData" : '{"BTN_1" : 1, "POT_2" : 12.34}'
}
"""
sqliteFile = 'DB_Mallette.sqlite'
nameOfPI = "PI_MASTER"
curID = 0

##########################################################################
def on_subscribe(client, userdata, mid, granted_qos):
    print("Subscribed: "+str(mid)+" "+str(granted_qos))

##########################################################################
def on_message(client, userdata, msg):
    # Création d'un curseur pour exécuter des commandes SQL
    conn = sqlite3.connect(sqliteFile)
    cur = conn.cursor()
    #Crée tables pour enregistrer les data
    cur.execute( '''CREATE TABLE IF NOT EXISTS DataMallette (
            Id                         INTEGER PRIMARY KEY,
            timestamp                  INTEGER,
            NomRaspPI                  TEXT,
            NomEsp32                   TEXT,
            NumeroDeEssai              INTEGER,
            EtapeDeEnigme              INTEGER,
            TempsDepuisLaDerniereEtape TEXT,
            TempsDepuisLeDebut         TEXT,
            EtapeReussi                INTEGER,
            MalletteReussi             INTEGER,
            JsonData                   TEXT)''')

    reception = str(msg.payload.decode('utf-8')) 

    #print(reception)
    
    try:        #DEbug des erreur du Json
        dictReceived = json.loads(reception) #Transforme le message recu en json
        #print(listDictPlain)
    except json.JSONDecodeError as e:
        print("Erreur au niveau du la convertion du json")
    

    #Trouve le ID le plus grand des table 
    currentIdNb = 'Select MAX(Id) FROM DataMallette'
    cur.execute(currentIdNb)
    currentIdNb = cur.fetchone()
    if isinstance(currentIdNb[0], int): # S'il y a pas d'ID
        curID = currentIdNb[0] + 1
    else :
        curID = 1

    dictReceived['Id'] = curID
    dictReceived['NomRaspPI'] = nameOfPI
    dictReceived["timestamp"] = int(time.time())
    dictReceived["NumeroDeEssai"] = 3
    dictReceived["EtapeDeEnigme"] = 2

    try:
        findStartTimeQuery = 'Select MIN(timestamp) FROM DataMallette WHERE NumeroDeEssai = {nbEssai}'.format(nbEssai=dictReceived["NumeroDeEssai"])
        cur.execute(findStartTimeQuery)
        findStartTimeQuery = cur.fetchone()
        if isinstance(findStartTimeQuery[0], int): # Si c'est la premiere donne
            print(findStartTimeQuery[0])
            dictReceived["TempsDepuisLeDebut"] = int(time.time()) - findStartTimeQuery[0]
            print(dictReceived["TempsDepuisLeDebut"])
        else :
            print("Premiere donnee Debut")
            dictReceived["TempsDepuisLeDebut"] = 0
    except:
        dictReceived["TempsDepuisLeDebut"] = 0


    dictReceived["TempsDepuisLeDebut"] = str(dictReceived["TempsDepuisLeDebut"])

    try:
        findStartTimeQuery = 'Select MIN(timestamp) FROM DataMallette WHERE EtapeDeEnigme = {nbEssai}'.format(nbEssai=dictReceived["EtapeDeEnigme"])
        cur.execute(findStartTimeQuery)
        findStartTimeQuery = cur.fetchone()
        if isinstance(findStartTimeQuery[0], int): 
            dictReceived["TempsDepuisLaDerniereEtape"] = int(time.time()) - findStartTimeQuery[0]
        else :  #Si c'est la premiere donnee
            print("Premiere donnee Etape")
            dictReceived["TempsDepuisLaDerniereEtape"] = 0
    except:
        dictReceived["TempsDepuisLaDerniereEtape"] = 0

    dictReceived["TempsDepuisLaDerniereEtape"] = str(dictReceived["TempsDepuisLaDerniereEtape"])

    dictReceived["EtapeReussi"] = 0
    dictReceived["MalletteReussi"] = 0
    dictReceived["JsonData"] = str(dictReceived["JsonData"])
    dictReceived["JsonData"] = dictReceived["JsonData"].replace("\'", "\"")
    print(dictReceived)
    #print(type(dictReceived["JsonData"]))

    cur.execute('''
    INSERT INTO DataMallette (Id, timestamp, NomRaspPI, NomEsp32,  NumeroDeEssai, EtapeDeEnigme, TempsDepuisLaDerniereEtape, TempsDepuisLeDebut, EtapeReussi, MalletteReussi, JsonData)
    VALUES (:Id, :timestamp, :NomRaspPI, :NomEsp32, :NumeroDeEssai, :EtapeDeEnigme, :TempsDepuisLaDerniereEtape, :TempsDepuisLeDebut, :EtapeReussi, :MalletteReussi, :JsonData)
    ''', dictReceived)

    conn.commit()
    # Fermeture de la connexion
    conn.close()
#Fin de def on_message


client = paho.Client(client_id="PC_RECEIVER_TSO_AL_123")
client.on_subscribe = on_subscribe
client.on_message = on_message
client.username_pw_set("projetTSO","LesProjets2025SontCool!!!")
client.connect('cgs.altecoop.ca', 1883, 60)
client.subscribe('CegepSherbrooke/projet/tso/Mallette')

client.loop_forever()
