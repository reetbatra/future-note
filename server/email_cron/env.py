import os


def get_environment(ADDITIONAL_ENVIRONMENT=dict()):
    ENVIRONMENT = {
        "MONGO_USER": os.getenv("MONGO_USER"),
        "MONGO_PWD": os.getenv("MONGO_PWD"),
        "MONGO_URL": os.getenv("MONGO_URL"),
        "SENDGRID_API_KEY": os.getenv("SENDGRID_API_KEY"),
        "AWS_ACCESS_ID": os.getenv("AWS_ACCESS_ID"),
        "AWS_ACCESS_KEY_VAL": os.getenv("AWS_ACCESS_KEY_VAL"),
        "AWS_REGION_VAL": os.getenv("AWS_REGION_VAL"),
    }
    ENVIRONMENT.update(ADDITIONAL_ENVIRONMENT)

    return ENVIRONMENT
