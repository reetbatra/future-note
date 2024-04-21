import os


def get_environment(ADDITIONAL_ENVIRONMENT=dict()):
    ENVIRONMENT = {
        "MONGO_USER": os.getenv("MONGO_USER"),
        "MONGO_PWD": os.getenv("MONGO_PWD"),
        "MONGO_URL": os.getenv("MONGO_URL"),
    }
    ENVIRONMENT.update(ADDITIONAL_ENVIRONMENT)

    return ENVIRONMENT
