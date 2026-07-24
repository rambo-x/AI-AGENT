"""
TripleSide AI Diagnostic Service

Bridge between Telegram chat and AI Agent reports.

Includes:
- health analysis
- log analysis
- diagnostic memory
- conversation context
"""


import json

from pathlib import Path


from ai.analyzers.health_analyzer import HealthAnalyzer
from ai.analyzers.log_analyzer import LogAnalyzer


from ai.telegram.response_formatter import ResponseFormatter


from ai.memory.context_manager import ContextManager





class DiagnosticService:



    def __init__(
        self,
        root="."
    ):


        self.root = Path(root)


        self.formatter = ResponseFormatter()


        self.context = ContextManager(
            root
        )







    def load_json(
        self,
        file
    ):


        if not file.exists():

            return {}



        try:

            return json.loads(

                file.read_text(
                    encoding="utf-8"
                )

            )


        except Exception:

            return {}








    def run(
        self,
        question: str
    ):


        try:


            # -------------------------
            # Build context
            # -------------------------

            context = self.context.get_context(
                question
            )



            context_summary = self.context.summarize(
                context
            )






            # -------------------------
            # Realtime checks
            # -------------------------

            health_result = HealthAnalyzer(

                self.root

            ).analyze()



            log_result = LogAnalyzer().analyze()







            # -------------------------
            # Load AI reports
            # -------------------------

            reasoning = self.load_json(

                self.root /
                "database/reasoning_report.json"

            )



            decision = self.load_json(

                self.root /
                "database/decision_report.json"

            )







            # -------------------------
            # Format response
            # -------------------------

            if reasoning and decision:


                message = self.formatter.format(

                    reasoning,

                    decision

                )



            else:


                message = (

                    "🧠 TripleSide AI Diagnostic\n\n"

                    f"Pertanyaan: {question}\n\n"

                    f"Status sistem: "
                    f"{health_result.get('health_status','unknown')}\n"

                    f"Error ditemukan: "
                    f"{len(log_result)}"

                )






            # -------------------------
            # Add context information
            # -------------------------

            if context_summary:


                message += "\n\n🧠 Context Memory:\n"


                for item in context_summary:


                    message += (

                        f"• {item}\n"

                    )








            return {


                "status":

                    "diagnostic_complete",



                "question":

                    question,



                "message":

                    message,



                "raw":

                    {

                        "health":

                            health_result,



                        "errors":

                            log_result[:5],



                        "context":

                            context

                    }

            }








        except Exception as error:



            return {


                "status":

                    "diagnostic_failed",



                "question":

                    question,



                "message":

                    "Diagnostic gagal dijalankan.",



                "error":

                    str(error)

            }
