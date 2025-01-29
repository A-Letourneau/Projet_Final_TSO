from tabulate import tabulate
import sqlite3
import os
import time

csvFile = 'Database_CSV_Sensors.sqlite'
path = 'Database_CSV_Sensors.sqlite'
listFieldnames = ['MAX __id','gateway', 'timestamp', 'type', 'mac', 'bleNo', 'bleName', 'rssi', 'battery', 'Xaxis', 'Yaxis', 'Zaxis', 'rawData']
class class_id:
    idNb_S1 = 0
    idNb_E8 = 0
    idNb_Other = 0
    idNb_cls = 10  #Refresh rate de l'affichage
class userInterface:
    choice = '0'
    mac = ''

idNb = class_id
user = userInterface

#Define des choix du user
showE8 = '1'
showS1 = '2'
showOther = '3'
oneE8 = '4'
oneS1 = '5'
refreshRate = 1000

#Interface graphique pour l'usager
print("1 - Show all E8 sensors")
print("2 - Show all S1 sensors")
print("3 - Show all other sensors")
print("4 - Show one E8 sensor")
print("5 - Show one S1 sensor")

user.choice = input("Choose an option : ")

if user.choice == '4' or user.choice == '5':
    user.mac = input("Enter MAC ADR : ")

while 1:
    # Création d'un curseur pour exécuter des commandes SQL
    conn = sqlite3.connect(csvFile)
    cur = conn.cursor()


    #Les instructions pour filtrer les database SQL en leurs type
    typeE8FromMACADR = f"Select mac FROM my_sensors WHERE type = 'E8'"
    typeS1FromMACADR = f"Select mac FROM my_sensors WHERE type = 'S1'"
    typeOtherFromMACADR  = "SELECT mac FROM my_sensors WHERE NOT type = 'E8' AND NOT type = 'S1'"

    #Recoit la liste de tout les mac adr associé au type E8
    cur.execute(typeE8FromMACADR)
    typeE8FromMACADR = cur.fetchall()
    #Recoit la liste de tout les mac adr associé au type S1
    cur.execute(typeS1FromMACADR)
    typeS1FromMACADR = cur.fetchall()
    #Recoit la liste de tout les mac adr associé au autre type
    cur.execute(typeOtherFromMACADR)
    typeS1FromMACADR = cur.fetchall()

    #Init des la configuration des tabulations
    listForTabulate = []
    tempString = ''
    tempCasting = ()

    #Série de if pour mettre la bonne information dans listForTabulate
    if user.choice == oneE8:
        if user.mac != '':
            tempString = """SELECT MAX(__id), *
                            FROM Data_XYZ_SensorV2
                            WHERE mac = '{mac}';"""

            cur.execute(tempString.format(mac = user.mac))

            tempCasting = cur.fetchall()
            tempCasting = list(tempCasting[0])
            tempCasting.pop(0)
            listForTabulate.append(tempCasting)

    if user.choice == oneS1:
        if user.mac != '':
            tempString = """SELECT MAX(__id), *
                            FROM Data_S1
                            WHERE mac = '{mac}';"""

            cur.execute(tempString.format(mac = user.mac))

            tempCasting = cur.fetchall()
            tempCasting = list(tempCasting[0])
            tempCasting.pop(0)
            listForTabulate.append(tempCasting)

    if user.choice == showE8:
        for mac in typeE8FromMACADR:
            if mac[0] != '':
                tempString = """SELECT MAX(__id), *
                                FROM Data_XYZ_SensorV2
                                WHERE mac = '{mac}';"""

                cur.execute(tempString.format(mac = mac[0]))

                tempCasting = cur.fetchall()
                tempCasting = list(tempCasting[0])
                tempCasting.pop(0)
                listForTabulate.append(tempCasting)

    if user.choice == showS1:
        for mac in typeS1FromMACADR:
            if mac[0] != '':
                tempString = """SELECT MAX(__id), *
                                FROM Data_S1
                                WHERE mac = '{mac}';"""

                cur.execute(tempString.format(mac = mac[0]))

                tempCasting = cur.fetchall()
                tempCasting = list(tempCasting[0])
                tempCasting.pop(0)
                listForTabulate.append(tempCasting)

    if user.choice == showOther:
        for mac in typeOtherFromMACADR:
            if mac[0] != '' and mac[0] == "''';":
                tempString = """SELECT MAX(__id), *
                                FROM Data_Other
                                WHERE mac = '{mac}';"""
                print(mac)
                cur.execute(tempString.format(mac = mac[0]))
                
                tempCasting = cur.fetchall()
                tempCasting = list(tempCasting[0])
                tempCasting.pop(0)
                listForTabulate.append(tempCasting)

    #Refresh la tabulation a chaque 1s
    os.system('cls')
    print(tabulate(listForTabulate, headers=listFieldnames, tablefmt='grid'))
    time.sleep(3)







