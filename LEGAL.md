# LEGAL #

By completing the legal's file (legal.json), FlexEval will generate automatically your CGU and GDPR file.

legal.json need to be place in your instance's repository.

```
 /instance_directory_name
             /structure.json
             /legal.json
```

## legal.json

| Property              | Type     | Required     | Nullable |
| --------------------- | -------- | ------------ | -------- |
| [GDPR](#GDPR) | `object` | **Required** | No  |
| [GCU](#GCU) | `object` |  **Required** | Yes |

## GPDR
In order to be fully GPDR Compliant you need to fill all the fields.

The different fields described in the GPDR field, will be used to generate the GPDR, based on the text written in [legal.tpl](flexeval/templates/legal.tpl).

## data_controller

`data_controller`

- is **required**
- type: `object`

### data_controller Type

`object` with following properties:

| Property        | Type  | Required     |
| --------------- | ----- | ------------ |
| `identity` | string | Additionnal |
| `contact` | object | Additionnal |


#### identity

##### identity Type


#### contact

##### contact Type

`object` with following properties:

| Property        | Type  | Required     |
| --------------- | ----- | ------------ |
| `email` | string | Additionnal |
| `other` | string | Additionnal |


## data_collection

`data_collection`

- is **required**
- type: `object`

### data_collection Type

`object` with following properties:

| Property        | Type  | Required     |
| --------------- | ----- | ------------ |
| `purpose` | string | Additionnal |
| `data` | array[string]| Additionnal |
| `legal_basis` | string | Additionnal |
| `recipients` | array[string] | Additionnal |

#### purpose

##### purpose Type

#### data

##### data Type

#### legal_basis

##### legal_basis Type

#### recipients

##### recipients Type

## data_conservation

`data_conservation`

- is **required**
- type: `object`

### data_conservation Type

`object` with following properties:

| Property        | Type  | Required     |
| --------------- | ----- | ------------ |
| `duration` | integer | Additionnal |
| `criterions_duration` | string| Additionnal |
| `security_measures` | string | Additionnal |


## data_protection_officer

`data_protection_officer`

- is **required**
- type: `object`

### data_protection_officer Type

`object` with following properties:

| Property        | Type  | Required     |
| --------------- | ----- | ------------ |
| `identity` | string | Additionnal |
| `contact` | object| Additionnal |


#### contact

`contact`

- is **required**
- type: `object`

##### contact Type

`object` with following properties:

| Property        | Type  | Required     |
| --------------- | ----- | ------------ |
| `email` | string | Additionnal |
| `phone_number` | object| Additionnal |
| `other` | object| Additionnal |



## CGU
If the field is null, FlexEval will use the default CGU that can be found in [legal.tpl](flexeval/templates/legal.tpl). Beware, that in order to properly generate the CGU you need to complete the minimal requirement for the [GDPR](#GDPR) field.

## Backbone

```

{
  "GDPR":{
    "data_controller":{
      "identity":null,
      "contact":
      {
        "email":null,
        "other":null
      }
    },

    "data_collection":
    {
      "purpose":null,
      "data":[],
      "legal_basis":null,
      "recipients":[]
    },

    "data_conservation":
    {
      "duration":null,
      "criterions_duration":null,
      "security_measures":null
    },

    "data_protection_officer":
    {
      "identity":null,
      "contact":
      {
        "email":null,
        "phone_number":null,
        "other":null
      }
    }
  },

  "GCU":
  {
    "text":null
  }
}
```
