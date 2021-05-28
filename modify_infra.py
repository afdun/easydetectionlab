import os
import sys
import json
import ast
import tkinter as tk
from tkinter import filedialog

# Contain the path to the saves
current_path_save = "Saves/rien1.json" # A CHANGER AVEC GUI
current_path_auto_save = "Saves/autoSave.json"

# Values to check the input of the user
yes = {'ou','o', 'oui', ''}
no = {'non','n', 'no'}

# GUI
root = tk.Tk()
root.withdraw()

def load_infra():
    # Read file of the current infrastructure
    with open(current_path_save, "r") as outputFile:
	    contentFile = outputFile.read()
    # Clean file content
    strContentFile = str(contentFile).replace("\\n","").replace("'", "").replace(" ","")
    # Update auto save file
    with open(current_path_auto_save, "w") as outputFile:
	    outputFile.write(strContentFile)

def read_infra():
    json_file = {}
    with open(current_path_auto_save, "r") as outputFile:
	    contentFile = outputFile.read()
    # Clean file content
    strContentFile = str(contentFile).replace("\\n","").replace("'", "").replace(" ","")
    # Transform string to dict
    try:
        res = ast.literal_eval(strContentFile)
        # Add to the json_file variable to generate new Vagrantfile
        for i in res:
            json_file[i] = res.get(i)
    except SyntaxError:
        print("\nProblème de syntaxe dans le fichier json. Merci de charger une nouvelle infrastructure ou modifier la syntaxe.")
        #METTRE UN EXIT SOIT DEMANDER DE CHARGER NEW INFRA GUI
    return json_file

def update_infra(json_file):
    # Update the auto save file with modifications
    with open(current_path_auto_save, "w") as outputFile:
	    outputFile.write(json.dumps(json_file, indent=2))

def choose_box_configuration():
    # PRENDRE EN COMPTE LE CAS OU L'USER CLIQUE SUR "CANCEL" -> CHEMIN VIDE CRASH
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

def add_boxes():
    #
    json_file = read_infra()
    #
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
    #return json_file
    update_infra(json_file)

def delete_boxes():
    #
    json_file = read_infra()
    #
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
    #return json_file
    update_infra(json_file)
   
def save_infra():
    global current_path_save
    #
    json_file = read_infra()
    #
    #Choose the name and location for the save
    input("Le nom de la sauvegarde ainsi que le chemin absolu du dossier dans lequel vous voulez sauvegarder l'infrastructure (chemin/nom-répertoire-parent/nom-fichier) va vous être demandé. ENTER pour ouvrir l'interface de choix.")
    destinationSave = filedialog.asksaveasfilename(defaultextension='.json', filetypes=[("json files", '*.json')], title="Choisir nom et emplacement du fichier")
    print("Chemin choisi : " + destinationSave)
    current_path_save = destinationSave
    with open(destinationSave, "w") as outputFile:
	    outputFile.write(json.dumps(json_file, indent=2))
    #return json_file

def destroy_infra():
    global current_path_save
    if current_path_save != "":
        not_valid = True
        while not_valid:
            print("Le fichier : " + current_path_save + " va être supprimé. Entrer 'o' pour confirmer ou 'n' pour annuler")
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
        #DEMANDER DE CHARGER UN NOUVEAU FICHIER D'INFRA GUI SINON CA NE MARCHE PLUS
    else:
        print("Erreur, vous n'avez pas encore sauvegardé d'infrastructure.")
    #return json_file

def save_file(txt_edit):
    text = txt_edit.get(1.0, tk.END)
    text = str(text).replace("\\n","").replace(" ","")
    res = ast.literal_eval(text)
    #
    update_infra(res)
    #
    save_infra()
    #

def disable_event():
    pass

def exit_program(editor):
    #editor.destroy()
    #editor.quit()
    #editor.withdraw()
    return 1


def edit_infra():
    # PROBLEME -> TERMINAL BLOQUE SI ON FERME FENETRE EDITEUR + CHOIX SAUVEGARDE
    #
    json_file = read_infra()
    #
    editor = tk.Tk()
    editor.title("Modifier la configuration")
    #editor.protocol("WM_DELETE_WINDOW", disable_event)

    editor.rowconfigure(0, minsize=900, weight=1)
    editor.columnconfigure(1, minsize=900, weight=1)

    txt_edit = tk.Text(editor)
    fr_buttons = tk.Frame(editor)
    btn_save = tk.Button(fr_buttons, text="Sauvegarder", command=lambda: save_file(txt_edit))
    btn_quit = tk.Button(fr_buttons, text="Quitter", command=editor.destroy)#lambda:exit_program(editor))

    btn_save.grid(row=0, column=0, sticky="ew", padx=5, pady=5)
    btn_quit.grid(row=1, column=0, sticky="ew", padx=5)

    fr_buttons.grid(row=0, column=0, sticky="ns")
    txt_edit.grid(row=0, column=1, sticky="nsew")

    txt_edit.delete(1.0, tk.END)
    txt_edit.insert(tk.END, json.dumps(json_file, indent=2))

    editor.mainloop()
    #return json_file

def quit_program():
    print("Fermeture du programme")
    exit()

def menu(arg):
    switcher = {
        1: add_boxes,
        2: delete_boxes,
        3: save_infra,
        4: destroy_infra,
        5: edit_infra,
        6: quit_program
    }
    # Get and execute the right function from the dict
    f = switcher.get(arg)
    f()
    #json_file = f(json_file)
    #return json_file

def modify_infra():
    print("\n-----------------------------------------------------------")
    print("-------------- MODIFIER INFRASTRUCTURE -----------------------")
    print("------------------------------------------------------------\n")    

    # REMPLACER PAR FENETRE GUI DEMANDANT DE CHOISIR FICHIER
    load_infra()

    while True:
        print()
        print("Choisissez une option")
        print("1 - Ajouter une/des box à l'infrastructure existante")
        print("2 - Supprimer une/des box de l'infrastructure existante")
        print("3 - Sauvegarder l'infrastructure existante")
        print("4 - Détruire l'infrastructure existante")
        print("5 - Editer infrastructure existante")
        print("6 - Quitter le programme")
        choice = input()
        try:
            if int(choice) <= 6 and int(choice) >= 1:
                # Call the adequate function
                #json_file = menu(int(choice), json_file)
                menu(int(choice))
                #print(json_file)
            else:
                sys.stdout.write("Merci d'entrer une option valide\n")
        except ValueError:
            print("Merci d'entrer une option valide\n")

modify_infra()

"""
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
"""