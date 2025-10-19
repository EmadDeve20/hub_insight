from .models import User

def create_user(first_name:str, last_name:str,
username:str, password:str, email:str) -> User:
    """
    create user

    Args:
        first_name (str): first name of user
        last_name (str): last name of user
        username (str): username of user
        password (str): password of user
        email (str): email of user

    Returns:
        User: return created User
    """

    return User.objects.create_user(
        first_name=first_name,
        last_name=last_name,
        password=password,
        email=email,
        username=username
    )

