"""
Telegram Natural Language Router

Routes free text messages into AI services.

Supports:
- diagnostic
- report
- status
- help
- fallback conversation
"""


import json

from pathlib import Path


from ai.telegram.diagnostic_service import DiagnosticService

from ai.telegram.intent_router import IntentRouter





class TelegramChatRouter:



    def __init__(self):


        self.base = Path(".")


        self.diagnostic = DiagnosticService()


        self.intent_router = IntentRouter()






    def process(
        self,
        message: str
    ):


        intent = self.intent_router.detect(
            message
        )


        intent_name = intent.get(
            "intent"
        )



        # -----------------------------
        # Diagnostic request
        # -----------------------------

        if intent_name == "diagnostic":


            return self.diagnostic.run(
                message
            )





        # -----------------------------
        # Status request
        # -----------------------------

        if intent_name == "status":


            return self.diagnostic.run(
                message
            )





        # -----------------------------
        # Report request
        # -----------------------------

        if intent_name == "report":


            return self.read_report()





        # -----------------------------
        # Help request
        # -----------------------------

        if intent_name == "help":


            return {


                "status":
                    "success",


                "message":
                    (
                        "🧠 TripleSide AI Agent\n\n"

                        "Contoh pertanyaan:\n\n"

                        "• cek server\n"
                        "• apakah ada error?\n"
                        "• kenapa sistem lambat?\n"
                        "• buat laporan\n\n"

                        "Command:\n"
                        "/status\n"
                        "/report\n"
                        "/help"
                    )

            }






        # -----------------------------
        # Unknown conversation
        # -----------------------------

        return {


            "status":
                "understood",



            "message":

                (

                    "🧠 TripleSide AI Agent\n\n"

                    f"Pertanyaan: {message}\n\n"

                    "Saya belum menemukan kategori yang tepat, "
                    "tetapi saya siap membantu diagnostic sistem."

                )

        }






    def read_status(self):


        path = Path(
            "database/state.json"
        )



        if path.exists():


            data = json.loads(

                path.read_text()

            )


            return {


                "status":
                    "success",


                "source":
                    "state",


                "data":
                    data

            }




        return {


            "status":
                "unknown",


            "message":
                "Belum ada state agent."

        }






    def read_report(self):


        path = Path(
            "database/final_report.json"
        )



        if path.exists():


            data = json.loads(

                path.read_text()

            )


            return {


                "status":
                    "success",


                "source":
                    "report",


                "data":
                    data

            }




        return {


            "status":
                "unknown",


            "message":
                "Belum ada report."

        }
