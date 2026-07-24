"""
TripleSide AI Agent
Conversation Memory Layer v1.0

Short term memory for Telegram conversations.

Stores:
- last user question
- detected intent
- last response summary
- timestamp

Storage:
database/conversation_memory.json
"""


import json

from pathlib import Path

from datetime import datetime





class ConversationMemory:



    def __init__(
        self,
        root="."
    ):

        self.root = Path(root)

        self.file = (
            self.root /
            "database/conversation_memory.json"
        )

        self.memory = self.load()





    def load(self):

        if not self.file.exists():

            return {

                "created_at":
                    datetime.now().isoformat(),

                "history":
                    []

            }



        try:

            return json.loads(

                self.file.read_text(
                    encoding="utf-8"
                )

            )

        except Exception:


            return {

                "created_at":
                    datetime.now().isoformat(),

                "history":
                    []

            }







    def save(self):


        self.file.parent.mkdir(

            parents=True,

            exist_ok=True

        )


        self.file.write_text(

            json.dumps(

                self.memory,

                indent=4,

                ensure_ascii=False

            ),

            encoding="utf-8"

        )







    def remember(

        self,

        question,

        intent,

        response

    ):


        item = {


            "timestamp":
                datetime.now().isoformat(),


            "question":
                question,


            "intent":
                intent,


            "response":
                response[:1000]

        }



        self.memory["history"].append(

            item

        )



        # keep last 20 conversations

        self.memory["history"] = (

            self.memory["history"][-20:]

        )



        self.save()


        return item







    def last(self):


        history = self.memory.get(

            "history",

            []

        )


        if not history:

            return None



        return history[-1]







    def search(

        self,

        keyword

    ):


        keyword = keyword.lower()


        results = []



        for item in self.memory.get(

            "history",

            []

        ):


            text = json.dumps(

                item

            ).lower()



            if keyword in text:


                results.append(

                    item

                )



        return results







if __name__ == "__main__":


    memory = ConversationMemory()


    memory.remember(

        "cek server",

        "diagnostic",

        "server healthy"

    )


    print(

        memory.last()

    )
