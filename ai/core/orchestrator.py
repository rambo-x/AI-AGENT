"""
AI Agent Orchestrator

Main pipeline controller.
"""

from datetime import datetime
from pathlib import Path
import json


from ai.indexer.scanner import ProjectScanner

from ai.analyzers.project_analyzer import ProjectAnalyzer
from ai.analyzers.dependency_analyzer import DependencyAnalyzer
from ai.analyzers.architecture_analyzer import ArchitectureAnalyzer
from ai.analyzers.log_analyzer import LogAnalyzer
from ai.analyzers.health_analyzer import HealthAnalyzer


from ai.core.decision_engine import DecisionEngine
from ai.core.reasoning import ReasoningEngine


from ai.recommendation.recommendation_engine import RecommendationEngine

from ai.planner.planner_engine import PlannerEngine

from ai.executor.executor_engine import ExecutorEngine


from ai.reporters.report_generator import ReportGenerator

from ai.learning.improvement_engine import ImprovementEngine

from ai.state.state_manager import StateManager


class AgentOrchestrator:


    def __init__(
        self,
        root="."
    ):

        self.root = Path(root)

        self.report = {

            "generated_at":
                datetime.now().isoformat(),

            "status":
                "running",

            "pipeline":
                []

        }


    def run_step(
        self,
        name,
        function
    ):

        try:

            result = function()

            self.report["pipeline"].append({

                "step":
                    name,

                "status":
                    "success",

                "output":
                    result

            })

            return result


        except Exception as error:

            self.report["pipeline"].append({

                "step":
                    name,

                "status":
                    "failed",

                "error":
                    str(error)

            })

            return None



    def run(self):


        self.run_step(
            "project_scanner",
            lambda:
                ProjectScanner(
                    self.root
                ).save()
        )


        self.run_step(
            "project_analyzer",
            lambda:
                ProjectAnalyzer().save()
        )


        self.run_step(
            "dependency_analyzer",
            lambda:
                DependencyAnalyzer().save()
        )


        self.run_step(
            "architecture_analyzer",
            lambda:
                ArchitectureAnalyzer().save()
        )


        self.run_step(
            "log_analyzer",
            lambda:
                LogAnalyzer().save()
        )


        self.run_step(
            "health_analyzer",
            lambda:
                HealthAnalyzer(
                    self.root
                ).save()
        )


        self.run_step(
            "decision_engine",
            lambda:
                DecisionEngine(
                    self.root
                ).save()
        )


        self.run_step(
            "reasoning_engine",
            lambda:
                ReasoningEngine(
                    self.root
                ).save()
        )


        self.run_step(
            "recommendation_engine",
            lambda:
                RecommendationEngine(
                    self.root
                ).recommend(
                    "Telegram authentication failure"
                )
        )


        self.run_step(
            "planner_engine",
            lambda:
                PlannerEngine(
                    self.root
                ).plan(
                    "Telegram authentication failure"
                )
        )


        self.run_step(
            "executor_engine",
            lambda:
                ExecutorEngine(
                    self.root
                ).execute(
                    "Telegram authentication failure"
                )
        )


        self.run_step(
            "report_generator",
            lambda:
                ReportGenerator(
                    self.root
                ).save()
        )


        self.run_step(
            "improvement_engine",
            lambda:
                ImprovementEngine(
                    self.root
                ).save()
        )


        self.run_step(
            "state_manager",
            lambda:
                StateManager(
                    self.root
                ).save()
        )


        self.report["status"] = "completed"


        return self.report



    def save(self):

        result = self.run()


        output = (

            self.root /

            "database/agent_report.json"

        )


        output.write_text(

            json.dumps(

                result,

                indent=4

            )

        )


        return str(output)



if __name__ == "__main__":


    agent = AgentOrchestrator()


    print(

        agent.save()

    )
