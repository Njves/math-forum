import math

from app.models import Problem


class TokenCalculator:
    def calculate_task_value(self, problem: Problem):
        class_level = problem.class_level * math.sqrt(problem.class_level)
        body_len = len(problem.body)

        return int(class_level * math.sqrt(body_len)) - 100


