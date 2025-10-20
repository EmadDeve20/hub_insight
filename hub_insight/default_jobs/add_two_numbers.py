from .typing import JobDetail


def job_detail() -> JobDetail:
    detail:JobDetail = {
        "help": "This job is for add two numbers. number_one + number_two",
        "name": "Add Two Numbers"
    }

    return detail


def run_job(number_one:int=1, number_two:int=2) -> int:
    """
    add two numbers

    Args:
        number_one (int, optional): number one. Defaults to 1.
        number_two (int, optional): numbert two. Defaults to 2.

    Returns:
        int: return response [number_one + number_two]
    """
    return  number_one + number_two


