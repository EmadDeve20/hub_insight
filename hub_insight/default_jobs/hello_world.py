from hub_insight.utils.typing import JobDetail


def job_detail() -> JobDetail:
    detail:JobDetail = {
        "help": "Hello World Job",
        "name": "Hello World",
        "version":"v1"
    }

    return detail


def run_job() -> str:
    """
    print hello world

    Returns:
        str: return 'hello world'
    """
    return  'hello world'


