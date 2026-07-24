"""
Normalization Manager

Public interface for the normalization engine.
"""

from ai.normalization.matcher import RuleMatcher


class NormalizationManager:

    def __init__(self, root="."):

        self.matcher = RuleMatcher(root)

    def normalize(self, problem):

        return self.matcher.match(problem)

    def __call__(self, problem):

        return self.normalize(problem)
