# Mallette d'Évasion

## Description du Projet
La **Mallette d'Évasion** est un projet réalisé dans le cadre du cours **247-67P-SH Projet de fin d'études** en génie électrique. Il s'agit d'un système électronique basé sur un **Raspberry Pi 4** et plusieurs **ESP32-C3**, intégrant divers capteurs et composants pour résoudre des énigmes interactives.

## Concepteurs
- **Louis Boisvert**
- **Alexis Letourneau**

## Date
- **30 janvier 2025**

## Technologies Utilisées
- **Raspberry Pi 4 Model B (4GB)**
- **ESP32-C3-DEVKITC-02**
- **I2C (SDA/SCL)**
- **Boutons et interrupteurs**
- **Bandes de DEL**
- **Potentiomètres**
- **Pinces crocodiles**
- **PCB personnalisé**

## Schémas Principaux
1. **Raspberry_Pi** : Gestion centrale du système
2. **Schéma_Bloc** : Vue d'ensemble des connexions
3. **Énigme1_Interrupteur** : Activation d'un mécanisme via interrupteurs
4. **Énigme2_Pince_Banane** : Détection de contacts avec pinces crocodiles
5. **Énigme3_Potentiomètre** : Réglage d'une valeur par potentiomètres

## Fonctionnalités
- **Communication entre Raspberry Pi et ESP32 via I2C**
- **Gestion des entrées/sorties GPIO pour les énigmes**
- **Alimentation 3.3V et 5V pour les composants**
- **Intégration de multiples résistances et condensateurs pour stabilisation**
- **Utilisation de buffers 74HC1G125GV pour sécuriser les signaux**

## Instructions d'Utilisation
1. **Alimenter le système** : Assurez-vous que le Raspberry Pi et les ESP32 sont correctement branchés.
2. **Vérifier les connexions I2C** : Assurez-vous que les broches SDA et SCL sont bien connectées.
3. **Démarrer les énigmes** : Interagir avec les boutons, interrupteurs, pinces et potentiomètres pour progresser.

## Développement et Déploiement
- **Code source** : À stocker sur le Raspberry Pi
- **Configuration des GPIO** : À vérifier dans le script de contrôle
- **Tests** : Vérifier chaque énigme séparément avant l'intégration complète

## Améliorations Possibles
- Ajout d'un affichage LCD ou OLED pour des indices visuels
- Intégration de modules audio pour une meilleure immersion
- Optimisation du code pour améliorer la réactivité

## Licence
Ce projet est réalisé dans le cadre académique et son utilisation est limitée à des fins éducatives.

