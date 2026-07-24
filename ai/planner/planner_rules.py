"""
Planner Rules

Static recovery plans for known problems.
"""


PLANNER_RULES = {

    "telegram_token": {

        "priority": "high",

        "estimated_time": "2 minutes",

        "steps": [

            "Check TELEGRAM_BOT_TOKEN",

            "Update invalid token",

            "Restart AI Agent",

            "Verify Telegram Bot"

        ],

        "rollback": [

            "Restore previous TELEGRAM_BOT_TOKEN"

        ]

    },


    "connection_refused": {

        "priority": "critical",

        "estimated_time": "5 minutes",

        "steps": [

            "Check target service status",

            "Start the service",

            "Verify connection string",

            "Retest connection"

        ],

        "rollback": [

            "Restore previous configuration"

        ]

    },


    "module_not_found": {

        "priority": "medium",

        "estimated_time": "3 minutes",

        "steps": [

            "Identify missing package",

            "Install dependency",

            "Restart application",

            "Verify import"

        ],

        "rollback": [

            "Remove incompatible package"

        ]

    },


    "disk_full": {

        "priority": "critical",

        "estimated_time": "10 minutes",

        "steps": [

            "Check disk usage",

            "Delete temporary files",

            "Archive old logs",

            "Verify free space"

        ],

        "rollback": [

            "Restore archived files"

        ]

    }

}
