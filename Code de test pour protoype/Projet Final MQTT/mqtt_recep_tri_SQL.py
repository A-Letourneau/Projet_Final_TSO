import paho.mqtt.client as paho
import json
import sqlite3

"""
Exemple de Json
{
  "Id": 1,
  "NomRaspPI": "RASP_PI_MASTER",
  "NomESP32": "ESP_BOUTON",
  "Timestamp": 123456789,
  "NumeroDeEssai": 2,
  "TempsDepuisLeDebut": "1m30",
  "EtapeDeEnigme": 4,
  "TempsDepuisLaDerniereEtape": "0m30",
  "EtapeReussi": 1,
  "MalletteReussi": 1,
  "JsonRecu" : '{"BTN_1" : 1, "POT_2" : 12.34}'
}
"""
sqliteFile = 'DB_Mallette.sqlite'

curID = 0

##########################################################################
def on_subscribe(client, userdata, mid, granted_qos):
    print("Subscribed: "+str(mid)+" "+str(granted_qos))

##########################################################################
def on_message(client, userdata, msg):
    # Création d'un curseur pour exécuter des commandes SQL
    conn = sqlite3.connect(sqliteFile)
    cur = conn.cursor()
    #Crée 3 tables pour enregistrer les data
    cur.execute(
        '''CREATE TABLE IF NOT EXISTS DataMallette (
            Id                         INTEGER PRIMARY KEY,
            Timestamp                  INTEGER,
            NomRaspPI                  TEXT,
            NomESP32                   TEXT,
            NumeroDeEssai              INTEGER,
            EtapeDeEnigme              INTEGER,
            TempsDepuisLaDerniereEtape TEXT,
            TempsDepuisLeDebut         TEXT,
            EtapeReussi                INTEGER,
            MalletteReussi             INTEGER,
            JsonRecu                   TEXT
        );'''
                )

    reception = str(msg.payload.decode('utf-8')) 

    print(reception)

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

    cur.execute('''
    INSERT INTO DataMallette (Id, Timestamp, NomRaspPI, NomESP32,  NumeroDeEssai, EtapeDeEnigme, TempsDepuisLaDerniereEtape, TempsDepuisLeDebut, EtapeReussi, MalletteReussi, JsonRecu)
    VALUES (:Id, :Timestamp, :NomRaspPI, :NomESP32, :NumeroDeEssai, :EtapeDeEnigme, :TempsDepuisLaDerniereEtape, :TempsDepuisLeDebut, :EtapeReussi, :MalletteReussi, :JsonRecu)
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
