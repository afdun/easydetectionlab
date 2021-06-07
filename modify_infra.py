import os
import sys
import shutil
import json
import ast
import tkinter as tk
from tkinter import filedialog

#TO DO
# AJOUTER OPTION VAGRANT DEBUT dans choose_current_infra -> Amaury
# fonction launch_infra -> Amaury
# COMMENTAIRES launch_infra, get_input, copytree, create_new_box -> Amaury
# PREPARE.SH -> à check
# CREER FICHIER JSON INFRA PAR DEFAUT ET CHANGER VALEUR dans choose_current_infra -> Amaury a le fichier

# Global variables that contains the path to the saves
current_path_save = ""
current_path_auto_save = "Saves/autoSave/autoSave.json"

# Values to check the input of the user
yes = {'ou','o', 'oui', '', 'yes', 'y'}
no = {'non','n', 'no'}

# GUI
root = tk.Tk()
root.withdraw()

def choose_current_infra():
    """
    Choose the file that contains the infrastructure (JSON or Vagrant File) that we want to load.

    @param: No parameters

    @return `function choose_current_infra`: Only if no file was selected. A file must be selected for the next parts to work.
    """

    global current_path_save
    not_valid = True
    not_valid_2 = True
    while not_valid:
        print("Voulez-vous :\n1.Installer Detection Lab\n2.Vérifier configuration requise\n3. Charger l'infrastructure par défaut\n4. Importer un fichier\n5. Quitter")
        choice = input().lower()
        if choice == '1': #Install DetectionLab
            os.system("git clone https://github.com/clong/DetectionLab.git")
            not_valid = False
        elif choice == '2': # Check required configuration
            os.system("./DetectionLab/Vagrant/prepare.sh")
            print()
            not_valid = False
        elif choice == '3': # Default infrastructure
            print("\nChargement de l'infrastructure par défaut.")
            #CHANGER AVEC LE NOM DU FICHIER AVEC L'INFRA PAR DEFAUT
            current_path_save = "Saves/rien1.json"
            not_valid = False
        elif choice == '4': # Import file
            while not_valid_2:
                print("\nVoulez-vous :\n1. Charger un Vagrant file ?\n2. Charger un fichier JSON ?")
                choice = input().lower()
                if choice == '1': # Vagrant File
                    # FONCTION VAGRANT TO JSON -> AMAURY
                    not_valid_2 = False
                elif choice == '2': # JSON File
                    configFile = choose_box_configuration() # Choose file
                    if configFile != "null":
                        current_path_save = configFile
                    else: # No file was selected
                        print("\nAucun fichier sélectionné.\n")
                        return choose_current_infra()
                    not_valid_2 = False
                else:
                    sys.stdout.write("Merci de répondre par '1' ou '2'\n\n")
            not_valid = False
        elif choice == '5': # Quit the program
            exit()
        else:
            sys.stdout.write("Merci de répondre par '1' ou '2'\n\n")


def load_infra():
    """
    Load the infrastructure file that was chosen by the user.
    1. Open the file
    2. Check syntax
    3. Create the auto save file

    @param: No parameters

    @return: No return
    """
    
    with open(current_path_save, "r") as outputFile: # Read file of the chosen infrastructure
	    contentFile = outputFile.read()
    strContentFile = str(contentFile).replace("\\n","").replace("'", "").replace(" ","") # Clean file content

    try: #Check the syntax of the file
        res = ast.literal_eval(strContentFile) # Convert it to JSON
    except SyntaxError:
        print("\nProblème de syntaxe dans le fichier json. Merci de charger une nouvelle infrastructure ou de modifier la syntaxe de votre fichier.")
        return modify_infra() # Error: Back to main menu

    with open(current_path_auto_save, "w") as outputFile: # Create auto save file
	    outputFile.write(strContentFile)

def read_infra():
    """
    Read the auto save file and convert it to a JSON dictionary.
    1. Open the file
    2. Check syntax
    3. Create JSON dictionary

    @param: No parameters

    @return `json_file`: Dictionary containing the current infrastructure 
    """

    json_file = {}
    with open(current_path_auto_save, "r") as outputFile: # Read auto save file
	    contentFile = outputFile.read()
    strContentFile = str(contentFile).replace("\\n","").replace("'", "").replace(" ","") # Clean file content

    try: # Transform string to dict
        res = ast.literal_eval(strContentFile) # Convert it to JSON
        for i in res: 
            json_file[i] = res.get(i) # Add entry to dictionary variable
    except SyntaxError:
        print("\nProblème de syntaxe dans le fichier json. Merci de charger une nouvelle infrastructure ou de modifier la syntaxe.")
        return modify_infra() # Error: Back to main menu
    return json_file

def update_infra(json_file):
    """
    Update the auto save file with the new value of the JSON dictionary.
    1. Open the file
    2. Check syntax
    3. Create JSON dictionary

    @param `json_file`: Dictionary containing the current infrastructure

    @return: No return
    """
   
    with open(current_path_auto_save, "w") as outputFile: # Update the auto save file with json_file modifications
	    outputFile.write(json.dumps(json_file, indent=2))

def choose_box_configuration():
    """
    Choose the box configuration file to open.

    @param: No parameters

    @return `function choose_box_configuration`: call to the function in case the user was wrong in his input
    
    @return `configFile`: the path to the configuration file to open
    
    @return `null`: means that an error occured in the function and that the code will stop
    """

    error = False
    #Choose the configuration file to open
    input("\nLe chemin absolu du dossier contenant le fichier de configuration à intégrer (chemin/nom-répertoire-parent/nom-fichier) va vous être demandé. ENTER pour ouvrir l'interface de choix.")
    try: # Choose a file location
        configFile = filedialog.askopenfilename(filetypes = [("JSON file", ".json")], title = "Choisir le fichier à ouvrir")
        print("\nFichier choisi : " + configFile)
    except:
        error = True

    if error == False and configFile != "": # File location selected
        os.system("clear")
        confirmation = input("Fichier à valider : " + configFile + "\nConfirmation ? (y/n) ") # Confirm location entered
        if confirmation.lower() not in yes:
            print("\nAnnulation des données rentrées précédemment...")
            print("Relance du processus de saisie...\n")
            return choose_box_configuration() # New entry request
        else:
            return configFile
    else: # No file location selected
        print("\nAucun fichier sélectionné. Infrastructure non modifiée.")
        return "null"

# DEMANDER A AMAURY
def get_input(question, option="False",error="Veuillez entrer le format attendu de données !"):
    """
    

    @param `question`:  
    
    @param `option`: 
    
    @param `error`: 
    
    @return `function get_input`: 
    
    @return `entry_input`: 
    """

    entry_input = input(question)
    if entry_input == "" or eval(option):
        print("\n"+error)
        return get_input(question, option, error)
    else:
        return entry_input

def enter_new_box():
    """
    Enter the details needed to create the new vagrant box tree structure.
    1. Select path containing new box to add
    2. Select path containing the other Vagrant boxes
    3. Enter information about the new box (name, version)

    @param: No parameters
    
    @return `function enter_new_box`: call to the function in case the user was wrong in his input
    
    @return `(start_path,end_path,box_version)`: information needed to create tree structure
    
    @return `null`: means that an error occured in the function and that the code will stop
    """

    error = False
    try:
        input("\nLe chemin absolu du dossier contenant les fichiers de la box à intégrer (chemin/nom-répertoire-parent) va vous être demandé. ENTER pour ouvrir l'interface de choix.")
        start_path = filedialog.askdirectory() #Enter new box repository
        print("\nChemin choisi : "+start_path)

        input("\nLe chemin absolu du dossier contenant les boxes vagrant officielles (chemin/) va vous être demandé. ENTER pour ouvrir l'interface de choix.")
        end_path = filedialog.askdirectory() #Enter Vagrant boxes repository
        print("\nChemin choisi : "+end_path)
    except:
        error = True

    if error == False and start_path != "" and end_path != "": # Both file locations selected
        constructor = get_input("\nConstructeur (ex: hashicorp/bionic64) : ","entry_input.count('/') != 1",
            "Le constructeur doit contenir un slash séparant l'auteur du nom de version de la box.") # Enter box constructor
        box_version = get_input("\nVersion de la box : ") # Enter box version
        end_path += "/"+constructor.replace("/","-VAGRANTSLASH-") # Name formatting
        
        os.system("clear")
        confirmation = input("Configuration à valider :\nDépart :"+start_path+"\nArrivée : "+end_path+"\nVersion : "+box_version+"\nConfirmation ? (y/n) ")
        if confirmation.lower() not in yes: # Confirm entries
            print("\nAnnulation des données rentrées précédemment...")
            print("Relance du processus de saisie...\n")
            return enter_new_box() # New entry request
        else:
            return (start_path,end_path,box_version)
    else: # Files location not selected
        print("\nAucun fichier sélectionné. Infrastructure non modifiée.")
        return ("null", "null", "null")

# DEMANDER A AMAURY
def copytree(src, dst, symlinks=False, ignore=None):
    """
    

    @param `src`: 
    
    @param `dst`:
    
    @param `symlinks`:
    
    @param `ignore`:
    
    @return: No return
    """

    for item in os.listdir(src):
        s = os.path.join(src, item)
        d = os.path.join(dst, item)
        if os.path.isdir(s):
            shutil.copytree(s, d, symlinks, ignore)
        else:
            shutil.copy2(s, d)

# DEMANDER A AMAURY
def create_new_box(start_path,end_path,version):
    """
    Create the tree structure for the new Vagrant box and move files to the Vagrant boxes repository.

    @param `start_path`: location of the new box to add
    
    @param `end_path`: location of the other vagrant boxes
    
    @param `version`: version of the new box to add
    
    @return: No return
    """

    print("\nCréation de l'arborescence... ",end="")
    end_path += "/"+version+"/virtualbox" # ?
    os.makedirs(end_path) # ?
    print("ok")
    print("Déplacement des fichiers... ",end="")
    copytree(start_path,end_path) # ?
    print("ok")
    os.listdir(end_path) # ?

def add_boxes():
    """
    Add a new box to the current infrastructure.
    1. If not already imported, move the new box to the current Vagrant box repository
    2. Choose the configuration file for the new box

    @param: No parameters
    
    @return: No return
    """

    error = False
    not_valid = True
    #Choose new box if not already imported
    while not_valid:
        print("\nVotre box est-elle déjà présente dans le fichier des boxes Vagrant ? o pour oui, n pour non")
        choice = input().lower()
        if choice in yes: # Box already imported
            not_valid = False
        elif choice in no: # Box not imported
            (start_path,end_path,version) = enter_new_box() # Enter information about the new box to add
            if(start_path == "null"): # Problem in the file location selection: stop
                error = True
            else:
                create_new_box(start_path,end_path,version) # Create new box
            not_valid = False
        else:
            sys.stdout.write("Merci de répondre par 'oui' ou 'non'\n\n")

    # Choose new box configuration file
    if error == False:
        json_file = read_infra() # current infrastructure
        configFile = choose_box_configuration() # choose new box configuration file
        if configFile != "null": # no error in location selection
            with open(configFile, "r") as fichier:
                contentFile = fichier.read()
            strContentFile = str(contentFile).replace("\\n","").replace("'", "").replace(" ","") # Clean file content
            try: # Transform string to dict
                res = ast.literal_eval(strContentFile) # Convert it to JSON
                for i in res:
                    json_file[i] = res.get(i) # Add entry to dictionary variable
                print("\nInfrastructure modifiée avec succès.")
                update_infra(json_file) # save new infrastructure
            except SyntaxError:
                print("\nProblème de syntaxe dans le fichier json importé. Infrastructure non modifiée.")

def delete_boxes():
    """
    Delete box(es) from the current infrastructure.
    1. Select the box(es) to delete
    2. Delete entries from the JSON dictionary

    @param: No parameters
    
    @return: No return
    """

    json_file = read_infra() # current infrastructure
    existing_boxes = []
    for key, value in json_file.items():
        existing_boxes.append(key) # list of current boxes
    for box in existing_boxes:
        not_valid = True
        while not_valid:
            print("\nVoulez-vous supprimer la box \"" + box + "\" ? o pour oui, n pour non")
            choice = input().lower()
            if choice in yes: # delete entry
                json_file.pop(box)
                not_valid = False
            elif choice in no:
                not_valid = False
            else:
                sys.stdout.write("\nMerci de répondre par 'oui' ou 'non'\n\n")
    update_infra(json_file) # save new infrastructure
   
def save_infra():
    """
    Save the current infrastructure as a JSON file at a chosen location.

    @param: No parameters
    
    @return: No return
    """

    global current_path_save
    error = False
    json_file = read_infra() # current infrastructure
    input("\nLe nom de la sauvegarde ainsi que le chemin absolu du dossier dans lequel vous voulez sauvegarder l'infrastructure (chemin/nom-répertoire-parent/nom-fichier) va vous être demandé. ENTER pour ouvrir l'interface de choix.")
    
    try: # choose the name and location for the save
        destinationSave = filedialog.asksaveasfilename(defaultextension='.json', filetypes=[("json files", '*.json')], title="Choisir nom et emplacement du fichier")
        print("\nChemin choisi : " + destinationSave)
    except:
        error = True

    if error == False and destinationSave != "": # file location selected
        current_path_save = destinationSave # change global variable
        with open(destinationSave, "w") as outputFile: # save file
	        outputFile.write(json.dumps(json_file, indent=2))
    else: # no file location selected
        print("\nAucun chemin sélectionné. Infrastructure non sauvegardée.")

def destroy_infra():
    """
    The latest save file is deleted.

    @param: No parameters
    
    @return: No return
    """

    global current_path_save
    if current_path_save != "":
        not_valid = True
        while not_valid:
            print("\nLe fichier : " + current_path_save + " va être supprimé. Entrer 'o' pour confirmer ou 'n' pour annuler")
            choice = input().lower() # confirmation to delete the save
            if choice in yes:
                os.remove(current_path_save) # remove file
                not_valid = False
                modify_infra() # no infrastructure left, back to menu
            elif choice in no:
                not_valid = False
            else:
                sys.stdout.write("Merci de répondre par 'oui' ou 'non'\n\n")
    else:
        print("\nErreur, vous n'avez pas encore sauvegardé d'infrastructure.")

def compile_vagrant(txt_edit,txt_edit_vagrant):
    """
    In the tkinter window, transform JSON representation into Vagrant file representation.

    @param `txt_edit`: Text tkinter widget that contains the JSON representation
    
    @param `txt_edit_vagrant`: Text tkinter widget that contains the Vagrant file representation
    
    @return: No return
    """

    text = txt_edit.get(1.0, tk.END) # Read text from the left panel of the editor 
    txt_edit_vagrant.delete(1.0, tk.END) # Delete any existing content
    txt_edit_vagrant.insert(tk.END, text.upper()) # Compile in Vagrant file and show in the right panel of the editor
    
    text = str(text).replace("\\n","").replace(" ","") # Clean file content
    res = ast.literal_eval(text) # Transform in JSON format
    update_infra(res) # Save current infrastructure

def edit_infra():
    """
    Open a tkinter window that allows the user to change dynamically the current infrastructure.
    1. Edit the JSON file of the current infrastructure
    2. Transform into Vagrant file representation

    @param: No parameters
   
    @return: No return
    """

    json_file = read_infra() # current infrastructure

    editor = tk.Toplevel(root) # new window
    editor.title("Modifier la configuration")

    editor.rowconfigure(0, minsize=800, weight=1)
    editor.columnconfigure(1, minsize=600, weight=1)
    editor.columnconfigure(2, minsize=600, weight=1)

    txt_edit = tk.Text(editor) # JSON editor
    txt_edit_vagrant = tk.Text(editor) # Vagrant file representation
    fr_buttons = tk.Frame(editor)
    btn_compile = tk.Button(fr_buttons, text="Compiler", command=lambda: compile_vagrant(txt_edit,txt_edit_vagrant))
    btn_quit = tk.Button(fr_buttons, text="Terminer", command=lambda: editor.destroy())

    btn_compile.grid(row=0, column=0, sticky="ew", padx=5, pady=5)
    btn_quit.grid(row=1, column=0, sticky="ew", padx=5)

    fr_buttons.grid(row=0, column=0, sticky="ns")
    txt_edit.grid(row=0, column=1, sticky="nsew")
    txt_edit_vagrant.grid(row=0, column=2, sticky="nsew")

    txt_edit.delete(1.0, tk.END) # delete any existing content
    txt_edit.insert(tk.END, json.dumps(json_file, indent=2)) # insert the content of the current infrastructure

def display_infra():
    """
    Open a tkinter window that displays the content of the current infrastructure.

    @param: No parameters
    
    @return: No return
    """

    json_file = read_infra() # current infrastructure

    editor = tk.Toplevel(root) # new window
    editor.title("Infrastructure actuelle")

    editor.rowconfigure(0, minsize=800, weight=1)
    editor.columnconfigure(0, minsize=600, weight=1)
    editor.columnconfigure(1, minsize=600, weight=1)

    txt_edit = tk.Text(editor) # JSON editor
    txt_edit_vagrant = tk.Text(editor) # Vagrant file representation

    txt_edit.grid(row=0, column=0, sticky="nsew")
    txt_edit_vagrant.grid(row=0, column=1, sticky="nsew")

    txt_edit.insert(tk.END, json.dumps(json_file, indent=2)) # insert the content of the current infrastructure
    txt_edit_vagrant.insert(tk.END, json.dumps(json_file, indent=2).upper()) # insert the content of the current infrastructure

# A FINIR DEMANDER A AMAURY
def launch_infra():
    """
    

    @param: No parameters
    
    @return: No return
    """

    print("Lancer infra")

def quit_program():
    """
    Exit the program.

    @param: No parameters
    
    @return: No return
    """

    print("Fermeture du programme")
    exit()

def menu(arg):
    """
    Select the function to execute.

    @param `arg`: The number of the function to call
    
    @return: No return
    """

    switcher = {
        1: add_boxes,
        2: delete_boxes,
        3: save_infra,
        4: destroy_infra,
        5: edit_infra,
        6: display_infra,
        7: launch_infra,
        8: quit_program
    }
    f = switcher.get(arg) # Get the right function from the dictionary
    f() # execute the function

def modify_infra():
    """
    Main function which presents the menu and calls the different functions.

    @param: No parameters
    
    @return: No return
    """

    print("\n-----------------------------------------------------------")
    print("-------------- MODIFIER INFRASTRUCTURE -----------------------")
    print("------------------------------------------------------------\n")    

    choose_current_infra()
    load_infra()

    while True:
        print()
        print("Choisissez une option :")
        print("1 - Ajouter une/des box à l'infrastructure existante")
        print("2 - Supprimer une/des box de l'infrastructure existante")
        print("3 - Sauvegarder l'infrastructure existante")
        print("4 - Détruire l'infrastructure existante")
        print("5 - Editer infrastructure existante")
        print("6 - Afficher infrastructure existante")
        print("7 - Lancer infrastructure")
        print("8 - Quitter le programme")
        choice = input()
        try:
            if int(choice) <= 8 and int(choice) >= 1:
                menu(int(choice)) # Call the adequate function
            else:
                sys.stdout.write("Merci d'entrer une option valide\n")
        except ValueError:
            print("Merci d'entrer une option valide\n")

modify_infra()
