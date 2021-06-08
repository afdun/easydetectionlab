# Easy Detection Lab

## Table des matières

* [Description](#description)
* [Prérequis](#prérequis)
* [Pré-installation](#pré-installation)
* [Commandes du Makefile](#commandes-du-makefile)
* [Installation](#installation)
* [Utilisation](#utilisation)
* [Crédits](#crédits)

## Description

Ce projet est un fork de [Detection Lab](https://github.com/clong/DetectionLab) de Chris Long.

L'objectif de ce projet est de faciliter l'ajout de nouvelles boxes et la modification d'une infrastructure existante.


## Prérequis

Voici quelques prérequis :
* 55GB+ d'espace disque disponible recommandé
* 16GB+ de RAM hautement recommandé
* Vagrant 2.2.9+ (une archive est disponible dans le dossier DETECTIONLAB)
* Virtualbox 6.0+ recommandé
* Python 3.0+
* Tkinter 8.6+ recommandé (`sudo apt-get install python3-tk`)
* Pdoc3 0.9+ recommandé (`pip3 install pdoc3`)

## Pré-installation

Utiliser `git clone https://github.com/afdun/easydetectionlab` pour cloner le projet dans votre répertoire personnel.
Il ne devrait pas y avoir besoin d'utiliser `sudo`.

## Commandes du Makefile

Pour afficher les différentes commandes disponibles, faire un `make` dans le dossier easydetectionlab cloné. Les commandes suivantes s'afficheront :
```
make run             : exécution du programme
make clean           : suppression de la documentation et des fichiers temporaires
make clear           : clean + suppression de DetectionLab
make doc             : génération de la documentation
make readme          : affichage du README
```

## Installation

Pour installer Detection Lab, il faut lancer le programme grâce au `make run`. Puis sélectionner l'option 1 "**Installer Detection Lab**".

![Menu au lancement du programme](https://user-images.githubusercontent.com/34754768/121226373-c751c900-c88a-11eb-942f-b2882e13f062.png)

![Installation du GitHub Detection Lab](https://user-images.githubusercontent.com/34754768/121226451-de90b680-c88a-11eb-896a-4b2f71286742.png)

Avant d'aller plus loin, ne pas hésiter à vérifier sa configuration de vagrant. Pour cela, sélectionner l'option 2 "**Vérifier configuration requise**" du menu initial.

![Message d’information avant le lancement de la commande](https://user-images.githubusercontent.com/34754768/121226757-33343180-c88b-11eb-87e6-19d94bd09630.png)


## Utilisation

### Importer une infrastructure

Quel que soit l'usage voulu, il faut charger une infrastructure. Deux options s'offrent à l'utilisateur.
* L'option n°3 "**Charger l’infrastructure par défaut**" permet d'importer le fichier JSON contenant l’infrastructure par défaut (placé dans Saves/autoSave).
* L'option n°4 "**Importer une infrastructure existante**" va demander à l’utilisateur de choisir entre l’import d’un fichier VagrantFile ou d’un fichier JSON.


![Choix du type de fichier à importer](https://user-images.githubusercontent.com/34754768/121227075-7a222700-c88b-11eb-9ab1-e090133239ee.png)


![Choix du fichier à importer](https://user-images.githubusercontent.com/34754768/121226872-4d6e0f80-c88b-11eb-9c98-bc40b2b64ba3.png)


![Validation du fichier](https://user-images.githubusercontent.com/34754768/121227271-ab025c00-c88b-11eb-844a-87ba324425e2.png)


Attention, la syntaxe du VagrantFile importé doit respecter un format précis en raison de sa transformation ultérieure en JSON. 
* Ainsi, le fichier doit contenir un `Vagrant.configure("2") do |config|` et un `end` englobant le reste de la configuration. 
* Les lignes de déclaration de variables sont autorisées en dehors de ces balises mais seulement au début du fichier.
* Pour définir une machine virtuelle, utiliser `config.vm.define "NOM-VM" do |cfg|`.
* En dehors de cette dernière, les autres lignes de configuration devront avoir `cfg` et non `config` au début.
* Définir un `provider` sera nécessaire pour paramétrer la VM. Pour le moment, seul `virtualbox` sera lu.
* L'indentation d'un VagrantFile se fait avec deux espaces.


### Editer une infrastructure

#### Menu d'édition

Après avoir choisi l'infrastructure à éditer, le menu d'édition apparaîtra.

![Menu d’édition](https://user-images.githubusercontent.com/34754768/121227356-bf465900-c88b-11eb-9d49-9bfdbc11de5f.png)

Là encore, plusieurs options sont possibles.


#### Option 1 : Ajouter une/des box à l’infrastructure existante

Cette option va permettre de déplacer les fichiers de la box à ajouter. Premièrement, il faudra choisir le dossier de départ et le dossier d’arrivée des fichiers.


![Choix du dossier de la box à ajouter](https://user-images.githubusercontent.com/34754768/121227652-19dfb500-c88c-11eb-96d5-a6e749263680.png)


![Choix du dossier contenant les boxes Vagrant officielles](https://user-images.githubusercontent.com/34754768/121227667-1e0bd280-c88c-11eb-885f-6d0db551f450.png)


Ensuite, le nom et la version de la nouvelle box vont être demandés à l’utilisateur, puis il devra confirmer ses différents choix avant de continuer.

![Validation des informations entrées](https://user-images.githubusercontent.com/34754768/121227677-2237f000-c88c-11eb-9781-4c510b6da5f3.png)


Enfin, si tout s’est bien passé, le message de validation s’affichera. Sinon, un message d’erreur le remplacera.

![Message apparaissant à la fin de l’ajout d’une box](https://user-images.githubusercontent.com/34754768/121227688-26640d80-c88c-11eb-88be-6b585eb65f33.png)



#### Option 2 : Supprimer une/des boxes de l’infrastructure existante

Cette option va permettre de choisir les boxes à supprimer parmi les boxes existantes de l’infrastructure.

![Suppression de boxes](https://user-images.githubusercontent.com/34754768/121227723-311ea280-c88c-11eb-933b-096c86ad99f9.png)



#### Option 3 : Sauvegarder l’infrastructure existante

L’utilisateur va choisir un nom et un emplacement de fichier pour sauvegarder l’infrastructure actuelle.

![Choix du nom et de l’emplacement de la sauvegarde](https://user-images.githubusercontent.com/34754768/121227753-3845b080-c88c-11eb-8192-cfd2a0bf1467.png)



#### Option 4 : Détruire l’infrastructure existante

Cette option va demander une confirmation avant de supprimer la dernière sauvegarde.

![Message de confirmation avant suppression](https://user-images.githubusercontent.com/34754768/121227784-43004580-c88c-11eb-9a73-1888087a96e7.png)


#### Option 5 : Editer infrastructure existante

Cette option va ouvrir une interface graphique affichant à gauche l’aperçu de l’infrastructure en JSON, et à droite l’aperçu du VagrantFile généré.

![Fenêtre d’édition de l’infrastructure actuelle](https://user-images.githubusercontent.com/34754768/121227817-4b588080-c88c-11eb-8043-9f3dbf8c69a9.png)


Le texte dans la fenêtre de gauche peut être modifié et compilé pour avoir le nouvel aperçu VagrantFile. Si la syntaxe est correcte, l’utilisateur pourra observer la modification. Si un problème de syntaxe apparaît, une erreur sera affichée, et les modifications seront perdues si l’utilisateur clique sur le bouton "Terminer".


![Aperçu de la compilation JSON vers VagrantFile](https://user-images.githubusercontent.com/34754768/121227864-58756f80-c88c-11eb-829e-5f2c37677195.png)


![Message d’erreur s’il y a un problème de syntaxe](https://user-images.githubusercontent.com/34754768/121227893-61664100-c88c-11eb-9c89-5b34ea6095b2.png)


Attention, le JSON doit respecter un format précis du fait de sa conversion en VagrantFile. Ne pas hésiter à consulter les exemples dans le dossier Saves ou à en créer en utilisant directement le décompilateur (voir partie adéquate).


#### Option 6 : Afficher l’infrastructure existante

Cette option va ouvrir une interface graphique affichant à gauche l’aperçu de l’infrastructure actuelle en JSON, et à droite l’aperçu du VagrantFile généré sans possibilité de modification.

![Fenêtre d’aperçu de l’infrastructure actuelle](https://user-images.githubusercontent.com/34754768/121227911-675c2200-c88c-11eb-8f82-f5c5b0cbd6e7.png)


#### Option 7 : Valider l’infrastructure

Option permettant de vérifier la syntaxe de l’infrastructure actuelle. S’il n’y a pas de problème, un fichier Vagrantfile sera généré et le message de validation sera affiché. Le programme se fermera ensuite automatiquement.

![Message de validation de la création du VagrantFile](https://user-images.githubusercontent.com/34754768/121227951-7511a780-c88c-11eb-9650-22e19a839a42.png)


#### Option 8 : Quitter le programme
Option qui permet de terminer le programme.


## Traducteurs

### Traducteur JSON vers VagrantFile

Le fichier `compiler.py` permet de convertir un JSON au format VagrantFile.
N'étant pas voué à être utilisé ainsi, il faudra faire les entrées en brut pour le moment.
Dans le main à la fin du fichier, il suffit de renseigner les chemins du fichier JSON et du fichier Vagrant à générer.
Ensuite, lancer le programme avec `python3 compiler.py`. Par défaut, le VagrantFile généré se trouve dans le dossier tmp.

### Traducteur VagrantFile vers JSON

Le fichier `decompiler.py` permet de convertir un VagrantFile au format JSON.
N'étant pas voué à être utilisé ainsi, il faudra faire les entrées en brut pour le moment.
Dans le main à la fin du fichier, il suffit de renseigner les chemins du fichier Vagrant et du fichier JSON à générer.
Ensuite, lancer le programme avec `python3 decompiler.py`. Par défaut, le JSON généré se trouve dans le dossier tmp.

## Crédits

Programme conçu par Audrey et Amaury dans le cadre d'un projet de fin d'études.
