"""
TripleSide AI Agent

Context Manager v2.0

Combines:
- conversation memory
- diagnostic memory
- context ranking

Provides relevant context only.
"""


from ai.memory.conversation_memory import ConversationMemory

from ai.memory.feedback import MemoryFeedback

from ai.memory.context_ranker import ContextRanker






class ContextManager:



    def __init__(
        self,
        root="."
    ):


        self.conversation = ConversationMemory(
            root
        )


        self.diagnostic_memory = MemoryFeedback(
            root
        )


        self.ranker = ContextRanker()







    def get_context(
        self,
        message
    ):


        context = {


            "current_message":
                message,


            "last_conversation":
                None,


            "related_cases":
                []

        }







        # ---------------------------------
        # Get latest conversation
        # ---------------------------------

        last = self.conversation.last()


        if last:


            context["last_conversation"] = last







        # ---------------------------------
        # Search diagnostic memory
        # ---------------------------------

        cases = self.diagnostic_memory.all_cases()






        ranked = self.ranker.rank(

            message,

            cases

        )






        # ---------------------------------
        # Only keep relevant memories
        # ---------------------------------

        relevant = []



        for item in ranked:


            if item.get(
                "score",
                0
            ) >= 0.2:


                memory = item.get(
                    "memory"
                )


                if memory:

                    relevant.append(
                        memory
                    )







        context["related_cases"] = relevant






        return context







    def summarize(
        self,
        context
    ):


        summary = []




        last = context.get(
            "last_conversation"
        )


        if last:


            summary.append(

                "Percakapan sebelumnya: "

                +

                last.get(
                    "question",
                    "-"
                )

            )







        cases = context.get(
            "related_cases",
            []
        )



        if cases:


            summary.append(

                f"Ditemukan {len(cases)} kasus memory relevan."

            )



            for case in cases:


                problem = case.get(
                    "problem",
                    "-"
                )


                status = case.get(
                    "status",
                    ""
                )


                if status:


                    summary.append(

                        f"{problem} status {status}"

                    )

                else:


                    summary.append(

                        f"Kasus: {problem}"

                    )







        return summary
