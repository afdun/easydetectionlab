import os
import sys

#add
#supp
#del
#save

"""
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
    "TESTamaurymangedeslimaces":
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
    "TESTamaurymangedeslimaces":
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

# input retourne une chaîne vide pour "Entrée"
yes = {'ou','o', 'oui', ''}
no = {'non','n', 'no'}

def add_boxes():
    print("add boxes") 

def delete_boxes():
    print("delete boxes")
    existing_boxes = []

    for key, value in json_file.items():
        existing_boxes.append(key)        

    for box in existing_boxes:
        not_valid = True
        #print(box)
        while not_valid:
            print("Voulez-vous supprimer la box \"" + box + "\" ? o pour oui, n pour non")
            choice = input().lower()
            if choice in yes:
                json_file.pop(box)
                not_valid = False
            elif choice in no:
                #print(box + " ne sera pas supprimée\n")
                not_valid = False
            else:
                sys.stdout.write("Merci de répondre par 'oui' ou 'non'\n\n")

    for key, value in json_file.items():
        print(key)

def check_file_name(file_name):
    characters = [" ", "é", "è", "/", "\"", "à", "ù", "'"]
    for a in file_name:
        if a in characters:
            return False
    return True
    
def save_infra():
    #sauvegarder la variable json_file dans un fichier .json dans un certain répertoire -> voir avec Amaury
    print("save infra")
    print("Comment voulez-vous nommer la sauvegarde ? (attention à ne pas mettre d'espace ou de caractères spéciaux)")
    not_valid = True
    while(not_valid):
        file_name = input()
        if check_file_name(file_name):
            not_valid = False
            #est-ce qu'on check si le fichier existe déjà ? lui demande s'il veut vraiment écraser ?
        else:
            print("Nom de fichier incorrect, ne pas mettre d'espace ou de caractères spéciaux")
    
    with open(file_name+".json", "w") as fichier:
	    fichier.write(str(json_file))
    
def destroy_infra():
    print("destroy_infra")
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

