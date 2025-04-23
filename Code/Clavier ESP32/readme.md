Pour entrer dans le mode programmation du clavier esp32 :
Appuyer sur le bouton RESET
En restant appuyé, appuyer sur le potentiomètre
Puis relacher le bouton RESET
Un répertoire devrait s'ouvrir sur l'ordinateur

Pour programmer votre clavier esp32:
Remplacer le fichier code.py dans le répertoire avec le fichier code.py sur le git
Le fichier important est code.py qui peut être modifié selon les informations sur : https://github.com/KMKfw/kmk_firmware

La souris est déjà configuré, mais voici comment configurer la souris avec le clavier esp32:
Dans le fichier code.py
1 - Ajouter la ligne "from kmk.modules.mouse_keys import MouseKeys" dans "# Keys"
2 - Ajouter la ligne "mouse = MouseKeys()" dans "#KEYBOARD SETUP"
3 - Ajouter "mouse" dans la liste de module "keyboard.modules = [encoder_handler, tapdance, mouse]"
Optionnel - mettre :
"mousekeys = MouseKeys(
    max_speed = 10,
    acc_interval = 20, # Delta ms to apply acceleration
    move_step = 1
)" pour ajuster la vitesse

La configuration actuelle des 12 touches:
[A]         [MS_UP]     [MS_UP]     [BSPACE]
[MS_LEFT]   [MB_LMB]    [MS_RIGHT]  ['+']
[MS_DOWN]   [MS_DOWN]   [keypad_3]  ['-']

 
 