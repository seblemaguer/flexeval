# FlexEval #

FlexEval is a software that aim to help you create a web-based evaluation platform.

# How to install
Installation require pip3.
You can find the procedure to install it here: https://docs.python.org/fr/3.6/installing/index.html

```
pip3 install .
```

# Launching the webserver

## Launching a local instance
```
python3 run.py absolute_path_to_instance
```
absolute_path_to_instance correspond to the absolute path to your instance's repository.
The server's IP and PORT are defined by default: http://127.0.0.1:8080.
For any information concerning run.py, you can get some help with the following flag -h.

```
python3 run.py -h
```

Please consider the following example:
```
python3 run.py C:\Users\User\Documents\FlexEval\examples\test_dev
```

In order to build your instance you need to create an instance respository, you can find help on how to do it by clicking [here](INSTANCE.md).


## Application Factory

You are not satisfy with run.py ?
A FlexEval's application is built using the application factory pattern.
More information concerning application factory [here](https://flask.palletsprojects.com/en/1.1.x/patterns/appfactories/).


# How to cite

```bibtex
@inproceedings{fayet:hal-02768500,
  TITLE = {{FlexEval, cr{\'e}ation de sites web l{\'e}gers pour des campagnes de tests perceptifs multim{\'e}dias}},
  AUTHOR = {Fayet, C{\'e}dric and Blond, Alexis and Coulombel, Gr{\'e}goire and Simon, Claude and Lolive, Damien and Lecorv{\'e}, Gw{\'e}nol{\'e} and Chevelu, Jonathan and Le Maguer, S{\'e}bastien},
  URL = {https://hal.archives-ouvertes.fr/hal-02768500},
  BOOKTITLE = {{6e conf{\'e}rence conjointe Journ{\'e}es d'{\'E}tudes sur la Parole (JEP, 31e {\'e}dition), Traitement Automatique des Langues Naturelles (TALN, 27e {\'e}dition), Rencontre des {\'E}tudiants Chercheurs en Informatique pour le Traitement Automatique des Langues (R{\'E}CITAL, 22e {\'e}dition)}},
  ADDRESS = {Nancy, France},
  EDITOR = {Benzitoun, Christophe and Braud, Chlo{\'e} and Huber, Laurine and Langlois, David and Ouni, Slim and Pogodalla, Sylvain and Schneider, St{\'e}phane},
  PUBLISHER = {{ATALA}},
  PAGES = {22-25},
  YEAR = {2020}
}
```
