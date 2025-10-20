import os
import importlib

from pathlib import Path

from config.django.base import BASE_DIR
from .models import Job

from hub_insight.utils.typing import JobDetail


class JobsCommand:
    
    def __load_default_jobs(self,) -> list[tuple]:
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


    # TODO: Save varibales and return_annotation
    def create_new_jobs(self) -> bool:

        new_jobs = []

        for script_filename, detail_func, run_job in self.__load_default_jobs():

            job_detail:JobDetail = detail_func()

            if not Job.objects.filter(name=job_detail["name"]).exists():
                new_jobs.append(
                    Job(name=job_detail["name"],
                        help=job_detail["help"],
                        script_filename=script_filename,
                        version=job_detail.get("version", "v1"))
                )
        
        if new_jobs:
            Job.objects.bulk_create(new_jobs, batch_size=len(new_jobs))

        return True



