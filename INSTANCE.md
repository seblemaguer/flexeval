# INSTANCE #

FlexEval create a flask's application based on your settings.
An application create by FlexEval is refer as "Instance".
These settings give you the possibility to highly configure your application.
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

More information about [legal compliance](LEGAL.md).

## entrypoint

The first page that any user will see.

`entrypoint`

- is **required**
- type: `string`

### entrypoint Type

The value of entrypoint need to be one of the name defined for one of your [stages](#stages).

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
The admin's field give you the possibility to setup your instance's admin panel.
The admin panel is composed of admin mods (More information about [admin mods](MOD.md/#ADMIN)), that you setup within this field.

If admin is not defined, you will get a 404 error if you try to acces to your admin panel.

`admin`

- is Additional
- type: `object`

### admin Type

`object` with following properties:

| Property        | Type  | Required     |
| --------------- | ----- | ------------ |
| `entrypoint` | object | **Required** |
| `mods` | array | **Required** |


#### entrypoint

`entrypoint`

- is **required**
- type: `object`

##### entrypoint Type

Array type: `object[]`

| Property   | Type   | Required     |
| ---------- | ------ | ------------ |
| `mod`  | string | **Required** |
|*|any|Additional|

###### mod
`mod`

- is **required**
- type: `string`

###### mod Type

mod's value correspond to the name of one of the admin modules available.
More information about the [admin modules](MOD.md#ADMIN).

#### mods

`mods`

- is **required**
- type: `object[]`

##### mods Type

Array type: `object[]`

All items must be of the type: `object` with following properties:

| Property   | Type   | Required     |
| ---------- | ------ | ------------ |
| `mod`  | string | **Required** |
|*|any|Additional|

###### mod
`mod`

- is **required**
- type: `string`

###### mod Type

mod's value correspond to the name of one of the admin modules available.
More information about the [admin modules](MOD.md#ADMIN).



#### stages

`stages`

- is **required**
- type: `object`

##### stages Type

Each property of this object correspond to a stage.
The name of the property correspond to the name assigned to the stage.
It's the name of one of your stages, that you need to assign to the [entrypoint](#entrypoint) field.

| Property   | Type   | Required     |
| ---------- | ------ | ------------ |
|* |object| At least one|

##### *

`*`
The name given to this property correspond to the name of this stage.
- type: `object`

###### stage Type

All items must be of the type: `object` with following properties:

| Property   | Type   | Required     |
| ---------- | ------ | ------------ |
| `type`  | string | **Required** |
| `next`  | string or object | Additional |
|*|any|Additional|

###### type
`type`

- is **required**
- type: `string`

###### type Type

type's value correspond to the name of one of the stage modules available.
More information about the [stage modules](MOD.md#STAGE).

###### next
`next`

- is Additionnal
- type: `string` or `object`

###### next Type

If type is `string`:
  The name of one of the stages, this stage will be display when the user trigger the action to go to the next stage.

If type is `object`:

  Each property is the name of a road.
  The value associate to each property is the name of one of the stages.
  Each road is link to one of the stages.

Example:

  structure.json
  ```
  "stages": {
    "intro":{
              ...
              "next":{"roadToMOS":"test_mos","roadToAB":"test_ab"}
            },
    "test_ab":  {... },
    "test_mos":  {... }
  }

  ```

  someTemplate.tpl
  ```
    ...
  <a class="btn btn-primary" href="{{url_next['roadToAB']}}"> Test AB </a>
  <a class="btn btn-primary" href="{{url_next['roadToMOS']}}"> Test MOS </a>
    ...

  ```



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
