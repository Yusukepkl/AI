from config import config


def validate(token: str) -> bool:
    return token == config.AUTH_TOKEN
