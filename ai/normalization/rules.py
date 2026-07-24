"""
Normalization Rules

Built-in normalization signatures.
These rules are used as defaults before loading
custom rules from database/normalization_rules.json.
"""


DEFAULT_RULES = {

    "telegram_token": [

        "telegram authentication failure",

        "telegram.error.invalidtoken",

        "invalid telegram bot token",

        "telegram_invalid_token",

        "telegram token",

        "telegram bot token"

    ],

    "connection_refused": [

        "connection refused",

        "database connection refused",

        "mongodb connection refused",

        "cannot connect",

        "econnrefused",

        "service unavailable"

    ],

    "module_not_found": [

        "modulenotfounderror",

        "module not found",

        "no module named"

    ],

    "disk_full": [

        "disk full",

        "disk is full",

        "no space left",

        "storage full"

    ],

    "permission_denied": [

        "permission denied",

        "access denied",

        "operation not permitted"

    ]

}
