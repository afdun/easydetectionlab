import os
import sys
import json
import ast
import tkinter as tk
from tkinter import filedialog

# Values to check the input of the user
yes = {'ou','o', 'oui', ''}
no = {'non','n', 'no'}

# GUI
root = tk.Tk()
root.withdraw()

def choose_box_configuration():
    #Choose the configuration file to open
    input("Le chemin absolu du dossier contenant le fichier de configuration de/des box à intégrer (chemin/nom-répertoire-parent/nom-fichier) va vous être demandé. ENTER pour ouvrir l'interface de choix.")
    configFile = filedialog.askopenfilename(filetypes = [("JSON file", ".json")])
    print("Fichier choisi : " + configFile)
    
    #Confirm location entered
    os.system("clear")
    confirmation = input("Fichier à valider : " + configFile + "\nConfirmation ? (y/n) ")
    if confirmation.lower() != "y":
        print("Annulation des données rentrées précédemment...")
        print("Relance du processus de saisie...")
        return chooseBoxConfiguration()
    else:
        return configFile

def add_boxes(json_file):
    configFile = choose_box_configuration()
    with open(configFile, "r") as fichier:
	    contentFile = fichier.read()
    # Clean file content
    strContentFile = str(contentFile).replace("\\n","").replace("'", "").replace(" ","")
    # Transform string to dict
    try:
        res = ast.literal_eval(strContentFile)
        # Add to the json_file variable to generate new Vagrantfile
        for i in res:
            json_file[i] = res.get(i)
        print("\nInfrastructure modifiée avec succès.")
    except SyntaxError:
        print("\nProblème de syntaxe dans le fichier json importé. Infrastructure non modifiée.")
    return json_file