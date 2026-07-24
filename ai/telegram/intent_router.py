"""
TripleSide AI Intent Router

Detect user intention from natural language.
"""


class IntentRouter:


    def __init__(self):

        self.rules = {

            "diagnostic": [

                "cek",
                "check",
                "status",
                "error",
                "masalah",
                "problem",
                "gangguan",
                "kenapa",
                "mengapa",
                "lambat",
                "rusak",
                "down"

            ],


            "report": [

                "laporan",
                "report",
                "ringkasan",
                "summary"

            ],


            "help": [

                "bantuan",
                "help",
                "perintah",
                "command"

            ]

        }




    def detect(
        self,
        message: str
    ):


        text = message.lower()



        for intent, keywords in self.rules.items():

            for keyword in keywords:

                if keyword in text:

                    return {

                        "intent":
                            intent,

                        "confidence":
                            0.8,

                        "source":
                            "keyword"

                    }



        return {

            "intent":
                "unknown",

            "confidence":
                0.0,

            "source":
                "fallback"

        }
