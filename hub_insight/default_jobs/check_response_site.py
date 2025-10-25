import requests

from hub_insight.utils.typing import JobDetail



def job_detail() -> JobDetail:
    detail:JobDetail = {
        "help": "check status code of url with get method",
        "name": "Check WebSite Status code",
        "version": "v1",
    }

    return detail


def run_job(url:str) -> int:
    """
    check status code of a website

    Args:
        url (str): url of a site

    Returns:
        int: status code
    """

    try:
        response = requests.get(url=url)

        return True, response.status_code

    except requests.ConnectionError:

        return False, "Connection Error To Website!"
    
    except requests.RequestException:

        return False, "Request Exception!"
    
    except requests.Timeout:
        return False, "Timeout!"
    
    except requests.ConnectTimeout:

        return False, "Connection Timeout!"

    except Exception:

        return False , "Something Wrong!"








