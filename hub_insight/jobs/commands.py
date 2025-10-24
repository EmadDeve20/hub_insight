import os
import importlib
import inspect

from pathlib import Path

from django.db import transaction

from config.django.base import BASE_DIR
from .models import Job, Variable, MAP_PYTHON_VAR

from hub_insight.utils.typing import JobDetail


def load_default_jobs() -> list[tuple]:
    """
    load default jobs

    
    Returns:
        list[tuple]: list of tuple
        tuple data will be something like this:
        (python_script_filename: (str), job_detail: (function), run_job: (function))
    """

    path = BASE_DIR / Path("hub_insight/default_jobs")

    folder_name = "default_jobs"

    modules = []

    for file in os.listdir(path):
    
        if os.path.isdir(path / Path(str(file))) or file == "__init__.py":
            continue

        module_name = f"hub_insight.{folder_name}.{file[:-3]}"
        module = importlib.import_module(module_name)
        modules.append((file,
                        getattr(module, "job_detail"),
                        getattr(module, "run_job")))

    return modules


class JobsCommand:
    
    load_default_jobs = load_default_jobs()

    saved_jobs_name = []

    def __add_variables_job(self, jobs:list[Job], func_jobs):
        """
        add variables and response for each Job object model

        Args:
            jobs (list[Job]): list of jobs
            func_jobs (_type_): job function for each job
        """

        vars = []

        for job, func_job in zip(jobs, func_jobs):
            func_sign = inspect.signature(func_job)
            for s in func_sign.parameters.items():
                vars.append(
                    Variable(
                        job=job,
                        name=s[0],
                        var_type=MAP_PYTHON_VAR[s[1].annotation],
                        default=s[1].default if s[1].default != inspect._empty else None 
                    )
                )

        if vars:
            Variable.objects.bulk_create(vars, batch_size=len(vars))

    @transaction.atomic
    def create_new_jobs(self) -> bool:
        """
        create new jobs.
        after each load_default_jobs, if save a new job form this, save job will be remove in load_default_jobs.

        Returns:
            bool: return True if everything is ok
        """
        new_jobs = []
        jobs = []

        for script_filename, detail_func, run_job in self.load_default_jobs.copy():

            job_detail:JobDetail = detail_func()
            func_sign = inspect.signature(run_job)


            if not Job.objects.filter(name=job_detail["name"]).exists():
                new_jobs.append(
                    Job(name=job_detail["name"],
                        help=job_detail["help"],
                        script_filename=script_filename,
                        version=job_detail.get("version", "v1"),
                        response_type=MAP_PYTHON_VAR[func_sign.return_annotation],
                        )
                )
                jobs.append(run_job)

                self.load_default_jobs.remove((script_filename, detail_func, run_job))
                self.saved_jobs_name.append(job_detail["name"])

        if new_jobs:
            created_jobs = Job.objects.bulk_create(new_jobs, batch_size=len(new_jobs))

            self.__add_variables_job(created_jobs, jobs)

        return True


    @transaction.atomic
    def update_jobs(self) -> bool:
        """
        update jobs if job`s name exist. this function shoulde use after create_new_jobs function.
        this is better for performance. after update each jobs in load_default_jobs, job will be remove.

        Returns:
            bool: return True if everything is ok
        """

        updated_jobs = []
        selected_jobs = []
        jobs = []

        for script_filename, detail_func, run_job in self.load_default_jobs.copy():

            job_detail:JobDetail = detail_func()

            try:
                currunt_job = Job.objects.get(name=job_detail["name"])
            except Job.DoesNotExist:
                continue

            func_sign = inspect.signature(run_job)

            if currunt_job.version != job_detail["version"]:
                updated_jobs.append(
                    Job(
                        pk=currunt_job.pk,
                        name=job_detail["name"],
                        help=job_detail["help"],
                        script_filename=script_filename,
                        version=job_detail.get("version", "v1"),
                        response_type=MAP_PYTHON_VAR[func_sign.return_annotation],
                        )
                    )

                # Remove variables of this job
                # we will set it again
                currunt_job.variables.all().delete()

                selected_jobs.append(currunt_job)

                jobs.append(run_job)
                

            self.load_default_jobs.remove((script_filename, detail_func, run_job))

            self.saved_jobs_name.append(job_detail["name"])


        if updated_jobs:
            Job.objects.bulk_update(updated_jobs,
                                    fields=["version", "help", "script_filename" ],
                                    batch_size=len(updated_jobs))

            self.__add_variables_job(selected_jobs, jobs)

        return True


    @transaction.atomic
    def delete_jobs(self) -> bool:
        """
        delete jobs.

        this is improtant. use this function after create_new_jobs then after update_jobs function.

        Returns:
            bool: return True if everything is ok
        """

        Job.objects.all().exclude(name__in=self.saved_jobs_name).delete()

        return True


