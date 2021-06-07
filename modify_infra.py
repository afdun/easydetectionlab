import os
import sys
import shutil
import json
import ast
import tkinter as tk
from tkinter import filedialog
from compiler import convertJSONtoVAGRANTFILE, setVAGRANTFILE
from decompiler import convertVAGRANTFILEtoJSON, setJSON

# Global variables that contains the path to the saves
current_path_save = ""
current_path_auto_save = "Saves/autoSave/autoSave.json"
current_path_auto_save_tmp = "Saves/autoSave/autoSaveTmp.json"

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
        print("Voulez-vous :\n1. Installer Detection Lab\n2. Vérifier configuration requise\n3. Charger l'infrastructure par défaut\n4. Importer une infrastructure existante\n5. Quitter")
        choice = input().lower()
        if choice == '1': #Install DetectionLab
            os.system("git clone https://github.com/clong/DetectionLab.git")
        elif choice == '2': # Check required configuration
            input("Soyez sûr que DETECTIONLAB/DetectionLab/Vagrant/prepare.sh ait bien les droits d'exécution (chmod u+x prepare.sh). ENTER pour continuer")
            os.system("./DETECTIONLAB/DetectionLab/Vagrant/prepare.sh")
            print()
        elif choice == '3': # Default infrastructure
            print("\nChargement de l'infrastructure par défaut.")
            current_path_save = "Saves/DefaultInfrastructure.json"
            not_valid = False
        elif choice == '4': # Import file
            while not_valid_2:
                print("\nVoulez-vous :\n1. Charger un Vagrant file\n2. Charger un fichier JSON")
                choice = input().lower()
                if choice == '1': # Vagrant File
                    path = choose_box_configuration() # Select file
                    if path != "null":
                        json_text = convertVAGRANTFILEtoJSON(path)
                        setJSON(current_path_auto_save, json_text) # save in file
                        current_path_save = current_path_auto_save # change current path
                    else: # No file selected
                        print("\nAucun fichier sélectionné.\n")
                        return choose_current_infra()
                    not_valid_2 = False
                elif choice == '2': # JSON File
                    configFile = choose_box_configuration() # Select file
                    if configFile != "null":
                        current_path_save = configFile
                    else: # No file selected
                        print("\nAucun fichier sélectionné.\n")
                        return choose_current_infra()
                    not_valid_2 = False
                else:
                    sys.stdout.write("Merci de répondre par '1' ou '2'\n\n")
            not_valid = False
        elif choice == '5': # Quit the program
            exit()
        else:
            sys.stdout.write("Merci de répondre par un chiffre entre 1 et 5\n\n")


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

def update_infra(path, json_file):
    """
    Update the auto save file with the new value of the JSON dictionary.
    1. Open the file
    2. Check syntax
    3. Create JSON dictionary

    @param `path`: The location to save the content of the JSON ditionary

    @param `json_file`: Dictionary containing the current infrastructure

    @return: No return
    """
   
    with open(path, "w") as outputFile: # Update the auto save file with json_file modifications
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
    input("\nSélectionner le fichier à importer. ENTER pour ouvrir l'interface de choix.")
    try: # Choose a file location
        configFile = filedialog.askopenfilename(title = "Choisir le fichier à ouvrir")
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

def get_input(question, option="False",error="Veuillez entrer le format attendu de données !"):
    """
    Function asking a customizable question to the user, checking his answer according to customizable 
    expected options and displaying a customizable error message if necessary.

    @param `question`: string with the custom question  
    
    @param `option`: string with the custom format of expected response
    
    @param `error`: string with the custom error message
    
    @return `get_input`: function recall if input error
    
    @return `entry_input`: string with the response if no input error
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
        input("\nSélectionner le dossier contenant les fichiers de la box à importer. ENTER pour ouvrir l'interface de choix.")
        start_path = filedialog.askdirectory() #Enter new box repository
        print("\nChemin choisi : "+start_path)

        input("\nSélectionner le dossier contenant les boxes vagrant officielles. ENTER pour ouvrir l'interface de choix.")
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

def copytree(src, dst, symlinks=False, ignore=None):
    """
    Function copying a json to another.

    @param `src`: string with the source path
    
    @param `dst`: string with the destination path
    
    @param `symlinks`: boolean (True if symbolic links are activated else False)
    
    @param `ignore`: callable that will receive as its arguments the directory being visited by copytree(), and a list of its contents
    
    @return: No return
    """

    for item in os.listdir(src):
        s = os.path.join(src, item)
        d = os.path.join(dst, item)
        if os.path.isdir(s):
            shutil.copytree(s, d, symlinks, ignore) # Copy if it is a directory
        else:
            shutil.copy2(s, d) # Copy if it is a file

def create_new_box(start_path,end_path,version):
    """
    Create the tree structure for the new Vagrant box and move files to the Vagrant boxes repository.

    @param `start_path`: location of the new box to add
    
    @param `end_path`: location of the other vagrant boxes
    
    @param `version`: version of the new box to add
    
    @return: No return
    """

    print("\nCréation de l'arborescence... ",end="")
    end_path += "/"+version+"/virtualbox" # Complete the file path
    os.makedirs(end_path) # Create all directories
    print("ok")
    print("Déplacement des fichiers... ",end="")
    copytree(start_path,end_path) # Move all files to end path
    print("ok")
    # os.listdir(end_path) # ls -l (debug only)

def add_boxes():
    """
    Add a new box to the current Vagrant boxes folder.

    @param: No parameters
    
    @return: No return
    """

    (start_path,end_path,version) = enter_new_box() # Enter information about the new box to add
    if(start_path == "null"): # Problem in the file location selection: stop
        print("Pas de modifications effectuées.")
    else:
        create_new_box(start_path,end_path,version) # Create new box

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
        if key != "intro": # We don't want to delete this key
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
    update_infra(current_path_auto_save, json_file) # save new infrastructure
   
def save_infra():
    """
    Save the current infrastructure as a JSON file at a chosen location.

    @param: No parameters
    
    @return: No return
    """

    global current_path_save
    error = False
    json_file = read_infra() # current infrastructure
    input("\nChoisissez le nom et l'emplacement de la sauvegarde. ENTER pour ouvrir l'interface de choix.")
    
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
    text = str(text).replace("\\n","").replace(" ","") # Clean file content
    txt_edit_vagrant.delete(1.0, tk.END) # Delete any existing content

    try: # Check the syntax of the JSON text
        res = ast.literal_eval(text) # Convert it to JSON
        update_infra(current_path_auto_save_tmp, res) # Save current infrastructure in tmp file
        txt_edit_vagrant.insert(tk.END, convertJSONtoVAGRANTFILE(current_path_auto_save_tmp)) # Compile in Vagrant file and show in the right panel of the editor        
    except SyntaxError:
        txt_edit_vagrant.insert(tk.END, "Erreur de syntaxe. Impossible de transformer en Vagrant File.") # Error message

def exit_editor(editor, txt_edit):
    """
    Check if the current JSON representation has the right syntax before exiting. If not, the changes will be discarded.

    @param `editor`: Tkinter window to close
    @param `txt_edit`: Text tkinter widget that contains the JSON representation
    
    @return: No return
    """

    text = txt_edit.get(1.0, tk.END) # Read text from the left panel of the editor 
    text = str(text).replace("\\n","").replace(" ","") # Clean file content
    try: # Check the syntax of the JSON text
        res = ast.literal_eval(text) # Convert it to JSON
        update_infra(current_path_auto_save, res) # Save current infrastructure in save file
    except SyntaxError:
        print("\nErreur de syntaxe dans le fichier modifié. Les modifications ne sont pas prises en compte.\nChoisissez une option :")
    editor.destroy()

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

    editor.protocol("WM_DELETE_WINDOW", True)

    txt_edit = tk.Text(editor) # JSON editor
    txt_edit_vagrant = tk.Text(editor) # Vagrant file representation
    fr_buttons = tk.Frame(editor)
    btn_compile = tk.Button(fr_buttons, text="Compiler", command=lambda: compile_vagrant(txt_edit,txt_edit_vagrant))
    btn_quit = tk.Button(fr_buttons, text="Terminer", command=lambda: exit_editor(editor, txt_edit))

    btn_compile.grid(row=0, column=0, sticky="ew", padx=5, pady=5)
    btn_quit.grid(row=1, column=0, sticky="ew", padx=5)

    fr_buttons.grid(row=0, column=0, sticky="ns")
    txt_edit.grid(row=0, column=1, sticky="nsew")
    txt_edit_vagrant.grid(row=0, column=2, sticky="nsew")

    txt_edit.insert(tk.END, json.dumps(json_file, indent=2)) # insert the content of the current infrastructure
    txt_edit_vagrant.insert(tk.END, convertJSONtoVAGRANTFILE(current_path_auto_save)) # insert the content of the current infrastructure

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
    txt_edit_vagrant.insert(tk.END, convertJSONtoVAGRANTFILE(current_path_auto_save)) # insert the content of the current infrastructure

def check_infra():
    """
    Check the syntax of the JSON file before transformation in Vagrant File.
    1. Convert JSON to Vagrant representation
    2. Create Vagrant File
    3. Exit the program

    @param: No parameters
    
    @return: No return
    """

    vagrantText = convertJSONtoVAGRANTFILE(current_path_auto_save) # Convert to Vagrant File representation
    result = setVAGRANTFILE("VagrantFile", vagrantText) # Create Vagrant File
    print("\nVotre fichier Vagrant File a bien été validé et créé.\n")
    print("Après la fermeture de ce programme, vous pourrez utiliser les commandes suivantes depuis l'emplacement 'DETECTIONLAB/DetectionLab/Vagrant' pour intéragir avec elle :")
    print("'Vagrant up' pour la lancer\n'Vagrant restart' pour la redémarrer\n'Vagrant stop' pour la stopper")
    exit()

def quit_program():
    """
    Exit the program.

    @param: No parameters
    
    @return: No return
    """

    print("\nFermeture du programme")
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
        7: check_infra,
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
        print("7 - Valider infrastructure")
        print("8 - Quitter le programme")
        choice = input()
        try:
            if int(choice) <= 8 and int(choice) >= 1:
                menu(int(choice)) # Call the adequate function
            else:
                sys.stdout.write("Merci d'entrer une option valide\n")
        except ValueError:
            print("Merci d'entrer une option valide\n")

if __name__ == "__main__":
    modify_infra()