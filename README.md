# PercepEval #

## How to install the webserver ?

Installation require pip3.
You can find the procedure to install it here: https://docs.python.org/fr/3.6/installing/index.html

```
pip3 install -r requirements.txt
```

## Launching the webserver

```
python3 run.py name_instance IP PORT
```

name_instance correspond to the name given to our instance's repository.
This repository need to be in the following repository: [here](instances/).

If access to our websevice is not via http://IP:PORT/, you need to provide our url via the optinal parameter public_url.
Please consider the following example:
```
python3 run.py name_instance IP PORT -p https://monsupersite.com/tests/
```

For any information concerning run.py, you can get some help with the following flag -h.
```
python3 run.py -h
```

-------------------------------------------------
