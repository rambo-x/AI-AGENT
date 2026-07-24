"""
TripleSide AI Diagnostic Service

Bridge between Telegram chat and AI Agent reports.

Integrates:
- Health Analyzer
- Log Analyzer
- Context Memory
- Response Formatter
"""


import json

from pathlib import Path


from ai.analyzers.health_analyzer import HealthAnalyzer

from ai.analyzers.log_analyzer import LogAnalyzer


from ai.memory.context_manager import ContextManager


from ai.telegram.response_formatter import ResponseFormatter







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









    def add_memory_context(
        self,
        message,
        response
    ):


        context = self.context.get_context(

            message

        )



        summary = self.context.summarize(

            context

        )



        if summary:


            response += (


                "\n\n"

                "🧠 Context Memory:\n"

            )



            for item in summary:


                response += (

                    "• "

                    +

                    item

                    +

                    "\n"

                )



        return response










    def run(
        self,
        question: str
    ):


        try:



            # -----------------------------
            # Realtime checks
            # -----------------------------

            health_result = HealthAnalyzer(

                self.root

            ).analyze()



            log_result = LogAnalyzer().analyze()








            # -----------------------------
            # Load reasoning reports
            # -----------------------------

            reasoning = self.load_json(

                self.root /

                "database/reasoning_report.json"

            )



            decision = self.load_json(

                self.root /

                "database/decision_report.json"

            )









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







            # -----------------------------
            # Add memory context
            # -----------------------------

            message = self.add_memory_context(

                question,

                message

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

                        self.context.get_context(

                            question

                        )

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
