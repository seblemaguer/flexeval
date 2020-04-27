# INSTANCE #

FlexEval create a flask's application based on our settings.
An application create by FlexEval is refer as "Instance".
These settings give you the possibility to highly configure our application.
They are described in a directory refer as "Instance's Repository".

# Instance's Repository

## Minimal Configuration

Structure.json is the only mandatory file in an instance's repository.

```
 /instance_directory_name
             /structure.json
```

### stucture.json

| Property              | Type     | Required     | Nullable |
| --------------------- | -------- | ------------ | -------- |
| [gdpr_compliance](#gdpr_compliance) | `string` | **Required** | No|
| [entrypoint](#entrypoint) | `string` | **Required** | No |
| [variables](#variables) | `object` | Additional | Yes |
| [admin](#admin) | `object` | Additional | No |
| [stages](#stages) | `object` | **Required** | No |

## gdpr_compliance

GDPR Compliance

`gdpr_compliance`

- is **required**
- type: `string`

### gdpr_compliance Type

Two available values:
- strict: The server will start only if all the legal requirement are available.
- relax: The server will start even if all the legal requirement are not available.


## entrypoint

The first page that any user will see.

`entrypoint`

- is **required**
- type: `string`

### entrypoint Type

The value of entrypoint need to be one of the name defined for one of our [stages](#stages).

## variables

All the key defined in variables are available in any template. (More information about [template](TEMPLATE.md))

`variables`

- is Additional
- type: `object`

### variables Type

`object` with following properties:

| Property        | Type  | Required     |
| --------------- | ----- | ------------ |
| `title` | string | Additionnal |
| `description` | string | Additionnal |
| `authors`     | array | Additionnal |

## admin

All the key defined in variables are available in any template. (More information about [admin mods](MODS.md/#ADMIN).)

`variables`

- is Additional
- type: `object`

### admin Type

`object` with following properties:

| Property        | Type  | Required     |
| --------------- | ----- | ------------ |
| `entrypoint` | object | Additionnal |
| `mods` | array | Additionnal |

## Example

```
{
  "gdpr_compliance":"relax",

  "entrypoint": "test_ab",

  "variables":{
    "title":"FlexEval",
    "authors":"Cédric Fayet"
  },

  "admin":{
    "entrypoint":{"mod":"admin_panel","password":"bflzefinlh67s","variables":{"subtitle":"Admin Panel"}},
    "mods": [
              {"mod":"export_bdd","variables":{"subtitle":"Download BDD","subdescription":"Download the database in CSV or SQLite format."}}
            ]
  },

  "stages": {
    "test_ab":  {"type": "test", "template":"ab.tpl", "next":"test_mos","nb_steps":5, "nb_step_intro":2,  "transaction_timeout_seconds":600, "variables":{"subtitle":"Test AB"} },
    "fin_du_test": {"type": "page:user","template":"end.tpl"}
  }
}
```
