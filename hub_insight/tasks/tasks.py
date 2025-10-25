import importlib

from celery import shared_task

from .selectors import get_task_by_name
from .services import create_task_log


@shared_task
def run_job_task(task_name:str):

    task = get_task_by_name(task_name)
    file = task.job.script_filename
    job_version = task.job.version
    job_help = task.job.help
    response_type = task.job.response_type

    try:

        module = importlib.import_module(f"hub_insight.default_jobs.{file[:-3]}")

        job_function = getattr(module, "run_job")

        is_ok, response_value = job_function(**task.variables) 

        create_task_log(
            task=task,
            job_help=job_help,
            job_version=job_version,
            response_type=response_type,
            response_value=None if not is_ok else response_value,
            variables=task.variables,
            error_message=response_value if not is_ok else None,
            is_ok=is_ok
        )

    except Exception:
        create_task_log(
            task=task,
            job_help=job_help,
            job_version=job_version,
            response_type=response_type,
            variables=task.variables,
            error_message="Internal Error!",
            is_ok=False
        )
