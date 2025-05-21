# Dossier de Tests pour le Prototype Modulable  

Ce dossier contient les fichiers de code python pour faire fonctionner les énigmes de la mallette avec la librairie PySimpleGUI. 
Pour faire fonctionner le programme, il faut activer l'application de programmation python 'thonny' en mode sudo avec la commande 'sudo thonny', puis faire rouler le fichier 'main.py'. 
Le fichier 'main.py' dépend des librairies dans l'environnement virtuel de 'venv'.

Voici comment créer cette environnement virtuel et ajouter les librairies:
Créer un environnement virtuel avec la commande 'python3 -m venv path/to/venv.'
Activé l'environnement virtuel avec la commande 'source .venv/bin/activate' dans CMD
Ajouter une librairie à l'environnement virtuel avec la commande 'python3 -m pip install XYZ' dans CMD (XYZ est la librairie désiré)
Répéter la commande précédente avec la liste de librairie suivante :

'smbus2'

'rpi_ws281x'

'Adafruit-Blinka'

pour l'installation de la dernière version de PysimpleGUI : 'python -m pip install --upgrade --extra-index-url https://PysimpleGUI.net/install PySimpleGUI'



Le reste des import du main.py est des librairie de base ou des librairie fait par nous.
Voici la liste des librairies custom qui faut mettre dans le même répertoire de main.py :
'moduleDEL'
'Class_Croco'
'Class_SW'
'Class_POT'
'MazeModule'

# Contient
- 'venv' l'environnement virtuel
- 'Class_Croco.py' le module d'énigme d'équation
- 'Class_SW.py' le module d'affichage de l'état des switches
- 'Class_POT.py' le module d'énigme de sine wave
- 'I2c_COMM.py' le module de communication i2c entre le pi et le esp32
- 'main.py' le programme principale
- 'MazeModule.py' le module d'énigme du labyrinthe (NON FONCTIONNEL)
- 'moduleDEL.py' le module de controle des DEL
- 'monautostart.desktop' fichier qui permet l'ouverture du programme lors du boot, doit être placé dans /etc/xdg/autostart/
- 'README.md'

# Création d'un fichier exécutable
Activer votre environnement virtuel si ce n'est pas déjà fait :

'source path/to/venv/bin/activate'

Assurez-vous que votre environnement virtuel est à jour :

'sudo apt update'
'sudo apt install python3-venv'

Essayez d’installer PyInstaller :

'pip install -U pyinstaller'

Installer les bibliothèques nécessaires :

- 'pip install zmq flask requests'
- 'pip install paho-mqtt'
- 'pip install pyzmq'

Créer l'exécutable pour chacun des programmes que vous voulez compiler :

- 'pyinstaller --onefile mon_programme.py'

Note 1 : Si vous avez oublié d’ajouter une librairie, il suffit de l’installer puis de relancer la commande pyinstaller --onefile.

Note 2 : il est à noter qu'après que le fichier exécutable soit créer, il peut être placer à n'importe quel endroit et encore être fonctionnel. Ceci peut aider si les chemins sont trop longs.
