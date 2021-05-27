import os
import sys
import json
import ast
import tkinter as tk
from tkinter import filedialog
from common_functions import add_boxes

# Contain the path to the saved file
current_path_save = ""

# Values to check the input of the user
yes = {'ou','o', 'oui', ''}
no = {'non','n', 'no'}

# GUI
root = tk.Tk()
root.withdraw()

def delete_boxes(json_file):
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

    #for key, value in json_file.items():
    #    print(key)
    return json_file
   
def save_infra(json_file):
    global current_path_save
    #Choose the name and location for the save
    input("Le nom de la sauvegarde ainsi que le chemin absolu du dossier dans lequel vous voulez sauvegarder l'infrastructure (chemin/nom-répertoire-parent/nom-fichier) va vous être demandé. ENTER pour ouvrir l'interface de choix.")
    destinationSave = filedialog.asksaveasfilename(defaultextension='.json', filetypes=[("json files", '*.json')], title="Choisir nom et emplacement du fichier")
    print("Chemin choisi : " + destinationSave)
    current_path_save = destinationSave
    with open(destinationSave, "w") as fichier:
	    fichier.write(json.dumps(json_file, indent=2))
    return json_file

def destroy_infra(json_file):
    global current_path_save
    if current_path_save != "":
        not_valid = True
        while not_valid:
            print("Le fichier correspondant au chemin : " + current_path_save + " va être supprimé. Entrer 'o' pour confirmer ou 'n' pour annuler")
            choice = input().lower()
            if choice in yes:
                os.remove(current_path_save)
                not_valid = False
                # New infrastructure
                json_file = {}
                # Reset value of the current path
                current_path_save = ""
            elif choice in no:
                not_valid = False
            else:
                sys.stdout.write("Merci de répondre par 'oui' ou 'non'\n\n")
    else:
        print("Erreur, vous n'avez pas encore sauvegardé d'infrastructure.")
    return json_file

def quit_program(json_file):
    print("Fermeture du programme")
    exit()

def menu(arg, json_file):
    switcher = {
        1: add_boxes,
        2: delete_boxes,
        3: save_infra,
        4: destroy_infra,
        5: quit_program
    }
    # Get and execute the right function from the dict
    f = switcher.get(arg)
    json_file = f(json_file)
    return json_file

def modify_infra(json_file):
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
                json_file = menu(int(choice), json_file)
            else:
                sys.stdout.write("Merci d'entrer une option valide\n")
        except ValueError:
            print("Merci d'entrer une option valide\n")

# Test variable
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

modify_infra(json_file)