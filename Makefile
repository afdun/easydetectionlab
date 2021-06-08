all: 
	@echo "Liste des commandes :"
	@echo "---------------------"
	@echo "make run                         : exécution du programme"
	@echo "make vagrant opt='option'        : exécution de vagrant avec l'option voulu "
	@echo "make clean                       : suppression de DetectionLab, de la documentation et des fichiers temporaires"
	@echo "make doc                         : génération de la documentation"
	@echo "make readme                      : affichage du README"
run: 
	@python3 modify_infra.py

vagrant:
	@echo "Commandes Vagrant disponibles : "
	@cd DETECTIONLAB/DetectionLab/Vagrant/
	@vagrant -opt $(opt)

clean:
	@rm -rf doc/ __pycache__/ Saves/autoSave/* DETECTIONLAB/DetectionLab/
	@echo "Nettoyage réalisé avec succès !"

doc:
	@pdoc3 --html compiler.py decompiler.py modify_infra.py -o doc
	@echo "Documentation générée dans doc/"

readme:
	@cat README.md

	
