# FlexEval #

FlexEval is a software that aim to help you create a web-based evaluation platform.

# How to install
Installation require pip3.
You can find the procedure to install it here: https://docs.python.org/fr/3.6/installing/index.html

```
pip3 install -r requirements.txt
```

# Launching the webserver

## Launching a local instance
```
python3 run.py absolute_path_to_instance
```
absolute_path_to_instance correspond to the absolute path to our instance's repository.
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
@inproceedings{
}
```
