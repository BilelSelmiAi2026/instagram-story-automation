import os

from dotenv import load_dotenv


load_dotenv()


def get_required_environment_variable(
    name: str,
) -> str:
    value = os.getenv(name, "").strip()

    if not value:
        raise ValueError(
            f"Missing environment variable: {name}"
        )

    return value


def get_boolean_environment_variable(
    name: str,
    default: bool = False,
) -> bool:
    value = os.getenv(name)

    if value is None:
        return default

    return value.strip().lower() in {
        "1",
        "true",
        "yes",
        "on",
    }