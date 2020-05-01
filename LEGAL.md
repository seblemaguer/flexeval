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
