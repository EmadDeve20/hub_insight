import importlib

from celery import shared_task

from .selectors import get_task_by_name



@shared_task
def run_job_task(task_name:str):

    task = get_task_by_name(task_name)

    file = task.job.script_filename

    module = importlib.import_module(f"hub_insight.default_jobs.{file[:-3]}")

    job_function = getattr(module, "run_job")

    job_response = job_function(**task.variables) 

    # TODO: Save it in a model.
    # make a log model to save response
    with open("test.txt", "a") as file:
        file.write(f"\n{job_response}\n")

