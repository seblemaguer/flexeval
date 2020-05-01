# LEGAL #

By completing the legal's file (legal.json), FlexEval will generate automatically our CGU and GDPR file.

legal.json need to be place in our instance's repository.

```
 /instance_directory_name
             /structure.json
             /legal.json
```

## legal.json

| Property              | Type     | Required     | Nullable |
| --------------------- | -------- | ------------ | -------- |
| [GDPR](#GDPR) | `object` | **Required** | No  |
| [GCU](#GCU) | `object` | Additional | Yes |

## GPDR
In order to be fully GPDR Compliant you need to fill all the fields.

The different fields described in the GPDR field, will be used to generate the GPDR, based on the text written in [legal.tpl](flexeval/templates/legal.tpl).

## data_controller

`data_controller`

- is **required**
- type: `object`

### data_controller Type


## data_collection

`data_collection`

- is **required**
- type: `object`

### data_collection Type


## data_conservation

`data_conservation`

- is **required**
- type: `object`

### data_conservation Type


## data_protection_officer

`data_protection_officer`

- is **required**
- type: `object`

### data_protection_officer Type



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
