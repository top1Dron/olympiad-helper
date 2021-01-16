from judge.services import execute_solutions
from config.celery import app

# ../../img/textarea_line_numbers.png
@app.task
def task_submit_solution(task_number, programming_language, source_code, solution_id):
    execute_solutions.submit_solution(task_number, programming_language, source_code, solution_id)