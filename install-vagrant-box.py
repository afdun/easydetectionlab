import os
import sys
import shutil
import tkinter as tk
from tkinter import filedialog

root = tk.Tk()
root.withdraw()

def saisie(question,option="False",erreur="Veuillez entrer le format attendu de données !"):
    saisieEntree = input(question)

    if saisieEntree == "" or eval(option):
        print(erreur)
        return saisie(question, option, erreur)
    else:
        return saisieEntree

def saisieNouvelleBox():

    """ Choix du dossier de départ """
    input("Le chemin absolu du dossier contenant les fichiers de la box à intégrer (chemin/nom-répertoire-parent) va vous être demandé. ENTER pour ouvrir l'interface de choix.")
    cheminDepart = filedialog.askdirectory()
    print("Chemin choisi : "+cheminDepart)

    """ Choix du dossier d'arrivée """
    input("Le chemin absolu du dossier contenant les boxes vagrant officielles (chemin/) va vous être demandé. ENTER pour ouvrir l'interface de choix.")
    cheminArrivee = filedialog.askdirectory()
    print("Chemin choisi : "+cheminArrivee)

    """ Saisie du constructeur de la box """
    constructeur = saisie("Constructeur (ex: hashicorp/bionic64) : ","saisieEntree.count('/') != 1","Le constructeur doit contenir un slash séparant l'auteur du nom de version de la box.")

    """ Saisie de la version de la box """
    versionBox = saisie("Version de la box : ")
    
    """ Formatage nom de la box """
    cheminArrivee += "/"+constructeur.replace("/","-VAGRANTSLASH-")
    
    """ Confirmation des saisies """
    os.system("clear")
    confirmation = input("Configuration à valider :\nDépart :"+cheminDepart+"\nArrivée : "+cheminArrivee+"\nVersion : "+versionBox+"\nConfirmation ? (y/n) ")
    if confirmation.lower() != "y":
        print("Annulation des données rentrées précédemment...")
        print("Relance du processus de saisie...")
        return saisieNouvelleBox()
    else:
        return (cheminDepart,cheminArrivee,versionBox)

def copytree(src, dst, symlinks=False, ignore=None):
    for item in os.listdir(src):
        s = os.path.join(src, item)
        d = os.path.join(dst, item)
        if os.path.isdir(s):
            shutil.copytree(s, d, symlinks, ignore)
        else:
            shutil.copy2(s, d)
            
def creationNouvelleBox(cheminDepart,cheminArrivee,version):
    print("Création de l'arborescence... ",end="")
    cheminArrivee += "/"+version+"/virtualbox"
    os.makedirs(cheminArrivee)
    print("ok")
    print("Déplacement des fichiers... ",end="")
    copytree(cheminDepart,cheminArrivee)
    print("ok")
    os.listdir(cheminArrivee)
    
def menu():
    os.system("clear")
    print("Bienvenue dans le programme de gestion de Vagrant en ligne de commande.")
    print("Crédits : Amaury & Audrey")
    print("\nMenu principal :")
    print("\n1. Installation de DetectionLab")
    print("\n2. Importation d'une nouvelle box vagrant")
    print("\n3. Lancement d'un Vagrantfile")
    print("\n4. Destruction des VM")
    print("\n5. Désinstallation de DetectionLab")
    print("\n0. Quitter")
    return saisie("\nEntrez l'option voulu : ","(saisieEntree!='0' and saisieEntree!='1' and saisieEntree!='2' and saisieEntree!='3' and saisieEntree!='4' and saisieEntree!='5')","Veuillez entrer un chiffre entre 0 et 5 !")

"""
Installation de DetectionLab
Installation d'une infra depuis zéro
Installation de l'infra par défaut
Ajout d'une box à l'infra actuelle
Suppression d'une vm
Suppression de toute l'infra actuelle
Suppression de DetectionLab

"""

def main():
    
    menuChoix = int(menu())
    if menuChoix == 0:
        print("Vous allez quitter le programme.")
        print("Merci d'avoir utilisé l'interface de gestion de Vagrant en ligne de commande.")
        print("A bientôt !")
        sys.exit()
    elif menuChoix == 1:
        print("Fonction en travaux...")
    elif menuChoix == 2:
        (cheminDepart,cheminArrivee,version) = saisieNouvelleBox()
        creationNouvelleBox(cheminDepart,cheminArrivee,version)
    else:
        print("Fonction en travaux...")
    input("ENTER pour retourner au menu.")
    main()
    

"""
config.vm.define "logger" do |cfg|
    cfg.vm.box = "bento/ubuntu-18.04"
    cfg.vm.hostname = "logger"
    cfg.vm.provision :shell, path: "logger_bootstrap.sh"
    cfg.vm.network :private_network, ip: "192.168.38.105", gateway: "192.168.38.1", dns: "8.8.8.8"

    cfg.vm.provider "virtualbox" do |vb, override|
      vb.gui = true
      vb.name = "logger"
      vb.customize ["modifyvm", :id, "--memory", 1024]
      vb.customize ["modifyvm", :id, "--cpus", 1]
      vb.customize ["modifyvm", :id, "--vram", "32"]
      vb.customize ["modifyvm", :id, "--nicpromisc2", "allow-all"]
      vb.customize ["modifyvm", :id, "--clipboard", "bidirectional"]
      vb.customize ["modifyvm", :id, "--natdnshostresolver1", "on"]
      vb.customize ["setextradata", "global", "GUI/SuppressMessages", "all" ]
    end
    
{ logger: {
cfg: {
  box: "bento/ubuntu-18.04",
  hostname: "logger",
  provision: [(shell, "logger_bootstrap.sh")],
  network: [(":private_network"), ("ip", "192.168.38.105"), ("gateway","192.168.38.1"), ("dns","8.8.8.8")],
  provider: "virtualbox",
  vb: {
  gui: true,
  name: "logger",
  customize: [["modifyvm", :id, "--memory", 1024],
  ["modifyvm", :id, "--cpus", 1],
  ["modifyvm", :id, "--vram", "32"],
  ["modifyvm", :id, "--nicpromisc2", "allow-all"],
  ["modifyvm", :id, "--clipboard", "bidirectional"],
  ["modifyvm", :id, "--natdnshostresolver1", "on"],
  ["setextradata", "global", "GUI/SuppressMessages", "all" ]]
  }
}
} ,
amaurymangedeslimaces:{
    
}
}
"""


if __name__ == "__main__":
    main()
