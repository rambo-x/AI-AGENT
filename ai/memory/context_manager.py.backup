"""
TripleSide AI Agent
Context Manager v1.0

Combines:
- conversation memory
- diagnostic memory

Provides context awareness.
"""


from ai.memory.conversation_memory import ConversationMemory

from ai.memory.feedback import MemoryFeedback





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





        # last chat context

        last = self.conversation.last()


        if last:


            context["last_conversation"] = last







        # diagnostic memory search

        related = self.diagnostic_memory.search(

            message

        )


        if related:


            context["related_cases"] = related






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

                f"Ditemukan {len(cases)} kasus memory terkait."

            )



        return summary
