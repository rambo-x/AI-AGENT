"""
TripleSide AI Agent

Context Ranker v1.1

Intelligent memory relevance scoring.
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



        text = text.replace(
            "_",
            " "
        )



        return re.findall(
            r"[a-z0-9]+",
            text
        )








    def score(
        self,
        query,
        memory
    ):


        query_words = set(

            self.normalize(
                query
            )

        )



        problem_words = set(

            self.normalize(

                memory.get(
                    "problem",
                    ""
                )

            )

        )



        cause_words = set(

            self.normalize(

                memory.get(
                    "cause",
                    ""
                )

            )

        )



        solution_words = set(

            self.normalize(

                memory.get(
                    "solution",
                    ""
                )

            )

        )



        score = 0.0






        # -----------------------------
        # Problem match
        # -----------------------------

        if problem_words:


            matched = len(

                query_words.intersection(
                    problem_words
                )

            )


            if matched == len(problem_words):


                score += 0.7






        # -----------------------------
        # Cause match
        # -----------------------------

        cause_match = len(

            query_words.intersection(
                cause_words
            )

        )



        if cause_match:


            score += min(

                cause_match * 0.1,

                0.2

            )







        # -----------------------------
        # Solution match
        # -----------------------------

        solution_match = len(

            query_words.intersection(
                solution_words
            )

        )



        if solution_match:


            score += min(

                solution_match * 0.05,

                0.1

            )








        # -----------------------------
        # Resolved memory bonus
        # -----------------------------

        if memory.get(
            "status"
        ) == "resolved":


            score += 0.05






        return round(

            min(

                score,

                1.0

            ),

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



            results.append(

                {

                    "score":

                        self.score(

                            query,

                            memory

                        ),



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
