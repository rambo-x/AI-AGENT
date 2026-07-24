"""
TripleSide AI Agent

Context Ranker v1.0

Ranks memories based on relevance.
"""


import re





class ContextRanker:



    def __init__(self):

        pass







    def normalize(
        self,
        text
    ):

        if not text:

            return []


        text = text.lower()


        words = re.findall(
            r"[a-z0-9_]+",
            text
        )


        return words







    def score(
        self,
        query,
        memory_text
    ):


        query_words = set(

            self.normalize(
                query
            )

        )


        memory_words = set(

            self.normalize(
                memory_text
            )

        )



        if not query_words or not memory_words:

            return 0







        overlap = (

            query_words.intersection(
                memory_words
            )

        )



        score = (

            len(overlap)

            /

            len(query_words)

        )



        return round(
            score,
            2
        )








    def rank(
        self,
        query,
        memories,
        limit=5
    ):


        results = []



        for memory in memories:


            text = ""



            if isinstance(
                memory,
                dict
            ):


                text = " ".join(

                    [

                        str(
                            memory.get(
                                "question",
                                ""
                            )
                        ),

                        str(
                            memory.get(
                                "problem",
                                ""
                            )
                        ),

                        str(
                            memory.get(
                                "cause",
                                ""
                            )
                        )

                    ]

                )



            value = self.score(

                query,

                text

            )



            results.append(

                {

                    "score":

                        value,


                    "memory":

                        memory

                }

            )





        results.sort(

            key=lambda x:
                x["score"],

            reverse=True

        )



        return results[:limit]
