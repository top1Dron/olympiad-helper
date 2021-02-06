from judge.services import execute_solutions
from config.celery import app


@app.task
def task_submit_solution(problem_number, programming_language, source_code, solution_id):
    execute_solutions.submit_solution(problem_number, programming_language, source_code, solution_id)