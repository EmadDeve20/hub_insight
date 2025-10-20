from django.core.management.base import BaseCommand

from hub_insight.jobs.commands import JobsCommand

class Command(BaseCommand):
    help = "initial system command"

    def handle(self, *args, **options):
        
        job_commands = JobsCommand()

#       ======================================  Jobs  =============================================

        if job_commands.create_new_jobs():
            self.stdout.write(
                self.style.SUCCESS("Successfully create new jobs")
            )
        else:
            self.stdout.write(
                self.style.ERROR("failed to create new jobs!")
            )
        

        if job_commands.update_jobs():
            self.stdout.write(
                self.style.SUCCESS("Successfully update jobs")
            )
        else:
            self.stdout.write(
                self.style.ERROR("failed to update jobs!")
            )
        

        if job_commands.delete_jobs():
            self.stdout.write(
                self.style.SUCCESS("Successfully delete jobs")
            )
        else:
            self.stdout.write(
                self.style.ERROR("failed to delete jobs!")
            )

