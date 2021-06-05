import os
import sys
import json
import ast
import tkinter as tk
from tkinter import filedialog

# Contain the path to the saves
current_path_save = ""
current_path_auto_save = "Saves/autoSave/autoSave.json"

# Values to check the input of the user
yes = {'ou','o', 'oui', ''}
no = {'non','n', 'no'}

# GUI
root = tk.Tk()
#root.withdraw()

def choose_current_infra():
    global current_path_save
    print("Merci de sélectionner le fichier contenant l'infrastructure à charger. Sinon, l'infrastructure par défaut sera sélectionnée.\n")
    configFile = choose_box_configuration()
    if configFile != "null":
        current_path_save = configFile
    else:
        print("Aucun fichier sélectionné. Chargement de l'infrastructure par défaut.")
        #CHANGER AVEC LE NOM DU FICHIER AVEC L'INFRA PAR DEFAUT
        current_path_save = "Saves/rien1.json"

def load_infra():
    # Read file of the current infrastructure
    with open(current_path_save, "r") as outputFile:
	    contentFile = outputFile.read()
    # Clean file content
    strContentFile = str(contentFile).replace("\\n","").replace("'", "").replace(" ","")
    #Check the syntax of the file
    try:
        res = ast.literal_eval(strContentFile)
    except SyntaxError:
        print("\nProblème de syntaxe dans le fichier json. Merci de charger une nouvelle infrastructure ou de modifier la syntaxe de votre fichier.")
        return modify_infra()
    # Create auto save file
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
        print("\nProblème de syntaxe dans le fichier json. Merci de charger une nouvelle infrastructure ou de modifier la syntaxe.")
        return modify_infra() # A CHANGER PEUT ETRE ?
    return json_file

def update_infra(json_file):
    # Update the auto save file with modifications
    with open(current_path_auto_save, "w") as outputFile:
	    outputFile.write(json.dumps(json_file, indent=2))

def choose_box_configuration():
    error = False
    #Choose the configuration file to open
    input("Le chemin absolu du dossier contenant le fichier de configuration à intégrer (chemin/nom-répertoire-parent/nom-fichier) va vous être demandé. ENTER pour ouvrir l'interface de choix.")
    try:
        configFile = filedialog.askopenfilename(filetypes = [("JSON file", ".json")])
        print("Fichier choisi : " + configFile)
    except:
        error = True

    if error == False and configFile != "":
        #Confirm location entered
        os.system("clear")
        confirmation = input("Fichier à valider : " + configFile + "\nConfirmation ? (y/n) ")
        if confirmation.lower() != "y":
            print("Annulation des données rentrées précédemment...")
            print("Relance du processus de saisie...")
            return choose_box_configuration()
        else:
            return configFile
    else:
        print("Aucun fichier sélectionné. Infrastructure non modifiée.")
        return "null"

def add_boxes():
    json_file = read_infra()
    configFile = choose_box_configuration()
    if configFile != "null":
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
        update_infra(json_file)

def delete_boxes():
    json_file = read_infra()
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
    update_infra(json_file)
   
def save_infra():
    global current_path_save
    json_file = read_infra()
    #Choose the name and location for the save
    #input("Le nom de la sauvegarde ainsi que le chemin absolu du dossier dans lequel vous voulez sauvegarder l'infrastructure (chemin/nom-répertoire-parent/nom-fichier) va vous être demandé. ENTER pour ouvrir l'interface de choix.")
    destinationSave = filedialog.asksaveasfilename(defaultextension='.json', filetypes=[("json files", '*.json')], title="Choisir nom et emplacement du fichier")
    print("Chemin choisi : " + destinationSave)
    current_path_save = destinationSave
    with open(destinationSave, "w") as outputFile:
	    outputFile.write(json.dumps(json_file, indent=2))

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
            elif choice in no:
                not_valid = False
            else:
                sys.stdout.write("Merci de répondre par 'oui' ou 'non'\n\n")
        modify_infra()
    else:
        print("Erreur, vous n'avez pas encore sauvegardé d'infrastructure.")

def compile_vagrant(txt_edit,txt_edit_vagrant):
    # Read text from the left panel of the editor 
    text = txt_edit.get(1.0, tk.END)
    txt_edit_vagrant.delete(1.0, tk.END)
    # Compile in Vagrant file and show in the right panel of the editor
    txt_edit_vagrant.insert(tk.END, text.upper())
    # Auto Save with the right syntax
    text = str(text).replace("\\n","").replace(" ","")
    res = ast.literal_eval(text)
    update_infra(res)

def edit_infra():
    json_file = read_infra()

    editor = tk.Toplevel(root)
    editor.title("Modifier la configuration")

    editor.rowconfigure(0, minsize=800, weight=1)
    editor.columnconfigure(1, minsize=600, weight=1)
    editor.columnconfigure(2, minsize=600, weight=1)

    txt_edit = tk.Text(editor)
    txt_edit_vagrant = tk.Text(editor)
    fr_buttons = tk.Frame(editor)
    btn_compile = tk.Button(fr_buttons, text="Compiler", command=lambda: compile_vagrant(txt_edit,txt_edit_vagrant))
    btn_quit = tk.Button(fr_buttons, text="Terminer", command=lambda: editor.destroy())

    btn_compile.grid(row=0, column=0, sticky="ew", padx=5, pady=5)
    btn_quit.grid(row=1, column=0, sticky="ew", padx=5)

    fr_buttons.grid(row=0, column=0, sticky="ns")
    txt_edit.grid(row=0, column=1, sticky="nsew")
    txt_edit_vagrant.grid(row=0, column=2, sticky="nsew")

    txt_edit.delete(1.0, tk.END)
    txt_edit.insert(tk.END, json.dumps(json_file, indent=2))
    #editor.mainloop()

def launch_infra():
    print("Lancer infra")

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
        6: launch_infra,
        7: quit_program
    }
    # Get and execute the right function from the dict
    f = switcher.get(arg)
    f()

def modify_infra():
    print("\n-----------------------------------------------------------")
    print("-------------- MODIFIER INFRASTRUCTURE -----------------------")
    print("------------------------------------------------------------\n")    

    choose_current_infra()
    load_infra()

    while True:
        print()
        print("Choisissez une option")
        print("1 - Ajouter une/des box à l'infrastructure existante")
        print("2 - Supprimer une/des box de l'infrastructure existante")
        print("3 - Sauvegarder l'infrastructure existante")
        print("4 - Détruire l'infrastructure existante")
        print("5 - Editer infrastructure existante")
        print("6 - Lancer infrastructure")
        print("7 - Quitter le programme")
        choice = input()
        try:
            if int(choice) <= 7 and int(choice) >= 1:
                # Call the adequate function
                menu(int(choice))
            else:
                sys.stdout.write("Merci d'entrer une option valide\n")
        except ValueError:
            print("Merci d'entrer une option valide\n")

modify_infra()