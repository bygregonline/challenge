orders_schema = {
   'type' : 'object',
   'additionalProperties': False,
    'properties':
    {
    'order': {'type': 'array',
               "minItems": 1,
    'items': {
          'properties' : {
                   'uuid':     {'type': 'string',
                                'pattern': '^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$',
                                "minLength": 36,
                                "maxLength": 36  },
                   'quantity': {'type': 'integer',
                                'minimum': 1},

              },
            'required': ['uuid','quantity']
      }
    },
    'info': {
        'type': 'object',
         'properties' : {
              'note': {'type': 'string'},
              'payment': {'type': 'number',
                          'minimum': 0},
            },
        'required': ['note','payment']
    }
}
}
