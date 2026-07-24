"""
Telegram Natural Language Router

Routes free text messages into AI diagnostic services.
"""


import json

from pathlib import Path


from ai.telegram.diagnostic_service import DiagnosticService





class TelegramChatRouter:



    def __init__(self):


        self.base = Path(".")


        self.diagnostic = DiagnosticService()





    def process(
        self,
        message: str
    ):


        text = message.lower()



        diagnostic_keywords = [

            "error",

            "masalah",

            "problem",

            "gangguan",

            "cek",

            "check",

            "kondisi",

            "status",

            "server",

            "sistem",

            "diagnosa",

            "diagnostic"

        ]



        if any(
            keyword in text
            for keyword in diagnostic_keywords
        ):


            return self.diagnostic.run(

                message

            )





        if "report" in text or "laporan" in text:


            return self.read_report()





        return {


            "status":
                "understood",


            "message":

                (

                    "Saya menerima pesan Anda."

                    "\n\n"

                    f"Pertanyaan: {message}"

                    "\n\n"

                    "Saya siap membantu melakukan diagnostic."

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
