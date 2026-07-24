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


class AgentOrchestrator:

    def __init__(self, root="."):

        self.root = Path(root)

        self.report = {
            "generated_at": datetime.now().isoformat(),
            "status": "running",
            "pipeline": []
        }


    def run_step(self, name, function):

        try:

            result = function()

            self.report["pipeline"].append({
                "step": name,
                "status": "success",
                "output": result
            })

            return result

        except Exception as e:

            self.report["pipeline"].append({
                "step": name,
                "status": "failed",
                "error": str(e)
            })

            return None


    def run(self):

        self.run_step(
            "project_scanner",
            lambda: ProjectScanner(
                self.root
            ).save()
        )


        self.run_step(
            "project_analyzer",
            lambda: ProjectAnalyzer(
            ).save()
        )


        self.run_step(
            "dependency_analyzer",
            lambda: DependencyAnalyzer(
            ).save()
        )


        self.run_step(
            "architecture_analyzer",
            lambda: ArchitectureAnalyzer(
            ).save()
        )


        self.run_step(
            "log_analyzer",
            lambda: LogAnalyzer(
            ).save()
        )


        self.run_step(
            "health_analyzer",
            lambda: HealthAnalyzer(
                self.root
            ).save()
        )


        self.run_step(
            "decision_engine",
            lambda: DecisionEngine(
                self.root
            ).save()
        )


        self.run_step(
            "reasoning_engine",
            lambda: ReasoningEngine(
            ).save()
        )


        self.report["status"] = "completed"

        return self.report



    def save(self):

        data = self.run()

        output = (
            self.root /
            "database/agent_report.json"
        )

        output.write_text(
            json.dumps(
                data,
                indent=4
            )
        )

        return str(output)



if __name__ == "__main__":

    agent = AgentOrchestrator()

    print(
        agent.save()
    )
