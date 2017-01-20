# Subjective test web platform
***
## Utilisation du test
script de test : `test.sh rm`

lancement de l'application : `python platform.py`

templates utilisés : `template.tpl`, `completed.tpl`, `index.tpl`


## Module python utilisés
- argparse
- bottle
- csv
- date
- itertools
- json
- model
- operator
- os
- pprint
- random
- re
- request
- SessionMiddleware
- shutil
- sqlite3
- sys


## Notes sur le script de test
Celui-ci peut êtr lancé avec l'option 'rm' ou sans. Cete option permet de supprimer préalablement l'ensemble du dossier `tests`.

---
## Utilisation sans script de test
Il possible de lancer une génération sans utiliser le script de test en exécutant le script python `generator.py`.
Ce dernier accepte les arguments suivants :

| court | long              | description                                                                           | requis |
| ----- | ----------------- | ------------------------------------------------------------------------------------- | ------ |
| `-j`  | `--json`          | fichier JSON                                                                          | oui    |
| `-t`  | `--main-tpl`      | modèle principal                                                                      | oui    |
| `-i`  | `--index-tpl`     | modèle pour la page d'index                                                           | oui    |
| `-c`  | `--completed-tpl` | modèle pour la page de fin de test                                                    | oui    |
| `-s`  | `--systems`       | liste des fichiers CSV des systèmes                                                   | oui    |
| `-n`  | `--name`          | booléen décirvant si le nom est écrit après le chemin du système (par défaut : faux)  | non    |
| `-v`  | `--verbose`       | mode verbeux                                                                          | non    |
|       | `--csv-delimiter` | définit le délimiteur CSV utilisé (par défaut : ';')                                  | non    |


---
Dans platform.py, ne pas oublier de changer la valeur de `myapp.APP_PREFIX`.
Ici c'est la valeur '/perceptualTestA' (comme indiqué dans l'exemple de config apache ci-dessous)

---
Configuration WSGI avec Apache :
- ajouter le mod_wsgi
  libapache2-mod-wsgi
  
- dans le virtualhost :
	# Cette directive peut être ajoutée autant de fois que nécessaire
	WSGIScriptAlias /perceptualTestA /var/www/apps/perceptualTestA/platform.py

		<Directory /var/www/apps>
			Require all granted
		</Directory>