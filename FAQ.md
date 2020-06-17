# Frequently Asked Questions

## General

### What is the minimal code to collect evaluations?

Standard basic tests (AB, MOS, MUSHRA) are **available** and you can **use** them **without** having to write **additional code**.
In this case, in order to specify your **own test**, you **only need** to fill in:
* the test configuration file (***structure.json***)
* the systems file (***tests.json***)

In **addition**, you will need to **provide**:
* for each system, the ***.csv*** file containing the **access paths** to the samples media files
* the **sample media files**
 

### Is there examples somewhere?

Yes, you can find  examples in the ***examples/test_dev*** folder.
* the current _structure.json_ file **aggregates** several **possible scenes** for a **variety of tests**. You can specify the configuration of your **own test** by **choosing a sequence of scenes** that suit you.
* the current _tests.json_ file contains **entries** for **many** tests (ab, mos, mushra). You can **add entries** to this file in order to specify the **systems** used in your **own test**.
* **for each system**, you find the **.csv correponding file**, located in the ***examples/test_dev/systems*** folder.
* the **sample media files** are located in the ***examples/test_dev/systems/files***  folder

## Administration

### What if I do not include an admin module in my website?

It is possible to have **no admin module** in the website. To do this, **simply** provide an **empty list** of "**mods**" in the "**admin**" entry of the *structure.json* configuration file. The application works well with **no administration menu** in the **admin panel**.
Here is an example of configuration for the "admin" entry  in the ***structure.json*** file:
```
...
"admin":{
    "entrypoint":{"mod":"admin_panel","password":"bflzefinlh67s","variables":{"subtitle":"Admin Panel"}},
    "mods": [
            ]
  }
...
```


### How do I get results from the SQLite database (flexeval.db) ?

There are 2 ways to **retrieve** the **results**:
1. **directly** on the website, at the **root of the folder** containing the **data**, to retrieve the **flexeval.db** SQLite database,
2. using the FlexEval **administration panel**. In this case, 2 download modes are available:
    * **CSV mode**: download a **zip repository** containing the database dumped in **csv** files and [**blob** files](https://developer.mozilla.org/fr/docs/Web/API/Blob)    .
    * **SQLite mode** : download the **SQLite base**


## Authentication

### What are the authentication possibilities?

### What if I do not want the visitors to authenticate?

### How do I set a fixed list of allowed visitors?

## Tests

### How can I record audio from a visitor?

### How can I record video from a visitor?

## Normal pages

