IMPROVEMENT

Pour mettre en place un système permettant d'éviter les déséquilibrage, il faudrait prévoir une table contenant les transactions en cours dans la BDD en SQLite. Cette table n'aurait cependant pas d'intérêt lors de la récupération des données.

Cette table serait ainsi décrite de la façon suivante: 
	- id 			INT AUTO INCREMENT
	- date 			DATE
	- user 			CHAR
	- sample_index 	INT
	- systemX		INT

Il faut donc prévoir la création de cette table lors de la génération de la plateforme
Donc dans la fonction : generator.py - create_db()

Le système fonctionenrait de la façon suivante :
	- lorsque l'on récupère une "étape de test"
	- on stocke son contenu dans la table de transaction
	- lorsque la réponse a été fournie, on recherche cette transaction dans la table et on la supprime

Si une autre étape de test est demandé avant d'avoir la réponse, il faut compter le nombre de fois où le système est présent dans la table de transaction pour savoir si on le choisit ou non. Il faut ainsi modifier la façon de sélectionner les échantillons dans la méthode get_test_sample() de model.py.

La suppression de la transaction serait intéressante dans la fonction insert_data() vu que l'on a toute les informations nécessaires qui nous sont données en paramètre.


Le système de TimeOut de l'information serait cependant trop complexe (si possible) à mettre en place. Une autre solution consiste à vérifier, lorsque quelqu'un effectue une nouvelle étape, si les informations contenues dans la table des transactions sont encore valide. Pour cela il faut utiliser la date de la transaction et choisir un timeout (pourquoi pas dans le fichier de configuration)