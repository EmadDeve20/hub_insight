import os
import importlib

from pathlib import Path

from config.django.base import BASE_DIR
from .models import Job

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

    # TODO: Save varibales and return_annotation
    def create_new_jobs(self) -> bool:
        """
        create new jobs.
        after each load_default_jobs, if save a new job form this, save job will be remove in load_default_jobs.

        Returns:
            bool: return True if everything is ok
        """
        new_jobs = []

        for script_filename, detail_func, run_job in self.load_default_jobs.copy():
            

            job_detail:JobDetail = detail_func()

            if not Job.objects.filter(name=job_detail["name"]).exists():
                new_jobs.append(
                    Job(name=job_detail["name"],
                        help=job_detail["help"],
                        script_filename=script_filename,
                        version=job_detail.get("version", "v1"))
                )
                self.load_default_jobs.remove((script_filename, detail_func, run_job))
                self.saved_jobs_name.append(job_detail["name"])

        if new_jobs:
            Job.objects.bulk_create(new_jobs, batch_size=len(new_jobs))

        return True


    # TODO: Save varibales and return_annotation
    def update_jobs(self) -> bool:
        """
        update jobs if job`s name exist. this function shoulde use after create_new_jobs function.
        this is better for performance. after update each jobs in load_default_jobs, job will be remove.

        Returns:
            bool: return True if everything is ok
        """

        updated_jobs = []

        for script_filename, detail_func, run_job in self.load_default_jobs.copy():

            job_detail:JobDetail = detail_func()

            try:
                currunt_job = Job.objects.get(name=job_detail["name"])
            except Job.DoesNotExist:
                continue


            if currunt_job.version != job_detail["version"]:
                updated_jobs.append(
                    Job(
                        pk=currunt_job.pk,
                        name=job_detail["name"],
                        help=job_detail["help"],
                        script_filename=script_filename,
                        version=job_detail.get("version", "v1"))
                    )

            self.load_default_jobs.remove((script_filename, detail_func, run_job))

            self.saved_jobs_name.append(job_detail["name"])


        if updated_jobs:
            Job.objects.bulk_update(updated_jobs, fields=["version", "help", "script_filename" ], batch_size=len(updated_jobs))

        return True


    # TODO: Remove varibales and return_annotation
    def delete_jobs(self) -> bool:
        """
        delete jobs.

        this is improtant. use this function after create_new_jobs then after update_jobs function.

        Returns:
            bool: return True if everything is ok
        """

        Job.objects.all().exclude(name__in=self.saved_jobs_name).delete()

        return True


