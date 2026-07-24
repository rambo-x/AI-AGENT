"""
TripleSide AI Telegram Response Formatter

Convert AI reports into human readable Telegram messages.
"""


class ResponseFormatter:



    def format(
        self,
        reasoning,
        decision
    ):


        lines = []


        lines.append(
            "🧠 TripleSide AI Diagnostic"
        )


        lines.append(
            ""
        )


        diagnoses = reasoning.get(
            "diagnoses",
            []
        )


        decisions = decision.get(
            "decisions",
            []
        )


        if diagnoses:


            lines.append(
                "📌 Temuan:"
            )


            for item in diagnoses:


                problem = item.get(
                    "problem",
                    "-"
                )


                confidence = item.get(
                    "confidence",
                    0
                )


                lines.append(

                    f"• {problem} "
                    f"({int(confidence*100)}%)"

                )



        if decisions:


            lines.append(
                ""
            )


            lines.append(
                "🔍 Analisa:"
            )


            for item in decisions:


                root = item.get(
                    "root_cause"
                )


                if root:


                    lines.append(
                        f"• Penyebab: {root}"
                    )



                recommendations = item.get(
                    "recommendation",
                    []
                )


                for rec in recommendations:


                    lines.append(
                        f"  - {rec}"
                    )



        lines.append(
            ""
        )


        lines.append(
            "✅ Diagnostic selesai."
        )


        return "\n".join(lines)
