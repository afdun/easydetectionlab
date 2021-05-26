import os
import sys
import json
import ast
import tkinter as tk
from tkinter import filedialog

#Test variable
json_file = {
    "logger": 
    {
    "cfg": 
        {
        "box": "bento/ubuntu-18.04",
        "hostname": "logger",
        "provision": [("shell", "logger_bootstrap.sh")],
        "network": [(":private_network"), ("ip", "192.168.38.105"), ("gateway","192.168.38.1"), ("dns","8.8.8.8")],
        "provider": "virtualbox", "vb": 
            {
            "gui": "true",
            "name": "logger",
            "customize": [["modifyvm", ":id", "--memory", 1024],
            ["modifyvm", ":id", "--cpus", 1],
            ["modifyvm", ":id", "--vram", "32"],
            ["modifyvm", ":id", "--nicpromisc2", "allow-all"],
            ["modifyvm", ":id", "--clipboard", "bidirectional"],
            ["modifyvm", ":id", "--natdnshostresolver1", "on"],
            ["setextradata", "global", "GUI/SuppressMessages", "all" ]]
            }
        }
    },
    "TESTamaury":
    {
        "cfg": 
        {
        "box": "splunk/ubuntu-20",
        "hostname": "logger",
        "provision": [("shell", "logger_bootstrap.sh")],
        "network": [(":private_network"), ("ip", "192.168.38.106"), ("gateway","192.168.38.1"), ("dns","8.8.8.8")],
        "provider": "virtualbox", "vb": 
            {
            "gui": "true",
            "name": "logger",
            "customize": [["modifyvm", ":id", "--memory", 1024],
            ["modifyvm", ":id", "--cpus", 1],
            ["modifyvm", ":id", "--vram", "32"],
            ["modifyvm", ":id", "--nicpromisc2", "allow-all"],
            ["modifyvm", ":id", "--clipboard", "bidirectional"],
            ["modifyvm", ":id", "--natdnshostresolver1", "on"],
            ["setextradata", "global", "GUI/SuppressMessages", "all" ]]
            }
        }
    },
    "TEST":
    {
        "cfg": 
        {
        "box": "hashicorp/ubuntu-18.04",
        "hostname": "logger",
        "provision": [("shell", "logger_bootstrap.sh")],
        "network": [(":private_network"), ("ip", "192.168.38.107"), ("gateway","192.168.38.1"), ("dns","8.8.8.8")],
        "provider": "virtualbox", "vb": 
            {
            "gui": "true",
            "name": "logger",
            "customize": [["modifyvm", ":id", "--memory", 1024],
            ["modifyvm", ":id", "--cpus", 1],
            ["modifyvm", ":id", "--vram", "32"],
            ["modifyvm", ":id", "--nicpromisc2", "allow-all"],
            ["modifyvm", ":id", "--clipboard", "bidirectional"],
            ["modifyvm", ":id", "--natdnshostresolver1", "on"],
            ["setextradata", "global", "GUI/SuppressMessages", "all" ]]
            }
        }
    }
}

"""
for i in json_file:
    print(i)
    print(json_file.get(i))
print()
"""

# Values to check the input of the user
yes = {'ou','o', 'oui', ''}
no = {'non','n', 'no'}

# GUI
root = tk.Tk()
root.withdraw()

def choose_box_configuration():
    #Choose the configuration file to open
    input("Le chemin absolu du dossier contenant le fichier de configuration de la box à intégrer (chemin/nom-répertoire-parent/nom-fichier) va vous être demandé. ENTER pour ouvrir l'interface de choix.")
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

def add_boxes():
    configFile = choose_box_configuration()
    with open(configFile, "r") as fichier:
	    contentFile = fichier.read()
    # Clean file content
    strContentFile = str(contentFile).replace("\\n","").replace("'", "").replace(" ","")
    # Transform string to dict
    res = ast.literal_eval(strContentFile)
    # Add to the json_file variable to generate new Vagrantfile
    for i in res:
        json_file[i] = res.get(i)

def delete_boxes():
    existing_boxes = []
    for key, value in json_file.items():
        existing_boxes.append(key)

    for box in existing_boxes:
        not_valid = True
        while not_valid:
            print("Voulez-vous supprimer la box \"" + box + "\" ? o pour oui, n pour non")
            choice = input().lower()
            if choice in yes:
                json_file.pop(box)
                not_valid = False
            elif choice in no:
                not_valid = False
            else:
                sys.stdout.write("Merci de répondre par 'oui' ou 'non'\n\n")

    for key, value in json_file.items():
        print(key)

"""
def check_file_name(file_name):
    alphaLow = "abcdefghijklmnopqrstuvwxyz"
    alphaUp = alphaLow.upper()
    num = "1234567890"
    charAllowed = alphaLow+alphaUp+num
    for a in file_name:
        if a not in charAllowed:
            return False
    return True
"""
   
def save_infra():
    #Choose the name and location for the save
    input("Le nom de la sauvegarde ainsi que le chemin absolu du dossier dans lequel vous voulez sauvegarder l'infrastructure (chemin/nom-répertoire-parent/nom-fichier) va vous être demandé. ENTER pour ouvrir l'interface de choix.")
    destinationSave = filedialog.asksaveasfilename(defaultextension='.json', filetypes=[("json files", '*.json')], title="Choisir nom et emplacement du fichier")
    print("Chemin choisi : " + destinationSave)
    with open(destinationSave, "w") as fichier:
	    fichier.write(json.dumps(json_file, indent=2))

def destroy_infra():
    print("TODO destroy_infra")
    #Trouver la ligne de commande à taper ici du style
    #os.system("cd attack_range_local;source venv/bin/activate;python3 attack_range_local.py -a build")

def quit_program():
    print("Fermeture du programme")
    exit()

def menu(arg):
    switcher = {
        1: add_boxes,
        2: delete_boxes,
        3: save_infra,
        4: destroy_infra,
        5: quit_program
    }
    # Get and execute the right function from the dict
    f = switcher.get(arg)
    f()

def modify_infra():
    print("\n-----------------------------------------------------------")
    print("-------------- MODIFIER INFRASTRUCTURE -----------------------")
    print("------------------------------------------------------------\n")

    while True:
        print()
        print("Choisissez une option")
        print("1 - Ajouter une/des box à l'infrastructure existante")
        print("2 - Supprimer une/des box de l'infrastructure existante")
        print("3 - Sauvegarder l'infrastructure existante")
        print("4 - Détruire l'infrastructure existante")
        print("5 - Quitter le programme")
        choice = input()
        try:
            if int(choice) <= 5 and int(choice) >= 1:
                # Call the adequate function
                menu(int(choice))
            else:
                sys.stdout.write("Merci d'entrer une option valide\n")
        except ValueError:
            print("Merci d'entrer une option valide\n")

modify_infra()

