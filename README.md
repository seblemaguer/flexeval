# FlexEval

FlexEval is a software that aim to help you create a web-based evaluation platform.

## How to install

Installation require pip3.
You can find the procedure to install it here: https://docs.python.org/fr/3.6/installing/index.html

```sh
pip3 install .
```

## Launching the webserver

### Launching a local instance

```sh
python3 run.py absolute_path_to_instance
```
absolute_path_to_instance correspond to the absolute path to your instance's repository.
The server's IP and PORT are defined by default: http://127.0.0.1:8080.
For any information concerning run.py, you can get some help with the following flag -h.

```sh
python3 run.py -h
```

Please consider the following example:

```sh
python3 run.py C:\Users\User\Documents\FlexEval\examples\test_dev
```

## Contributing

Please don't forget to install `pre-commit` to ensure your commits will respect the constraints of the toolkit:
  1. install the package `pre-commit`: `pip install pre-commit`
  2. install the git hooks: `pre-commit install`
