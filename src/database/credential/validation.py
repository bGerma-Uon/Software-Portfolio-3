"""
Validates the database credentials file
"""

# Builtin
import json
import logging
from pathlib import Path

# External
from jsonschema.exceptions import ValidationError
from jsonschema import validate

# Internal
pass


logger = logging.getLogger(__name__)


# Constants
SCHEMAS_DIR = (
    Path(__file__).parent.parent.parent.parent
    / "data" / "schemas" / "database_creds"
)


def get_latest_schema() -> dict:
    """
    Gets the latest schema from the data folder.

    The function finds all schema files, which are expected to be named
    incrementally (e.g., 1.json, 2.json), and returns the contents of the
    schema with the highest number.

    :return:
        A dictionary containing the latest JSON schema.

    :raises FileNotFoundError:
        If no schema files are found in the directory.
    """
    schemas = [
        path for path in SCHEMAS_DIR.iterdir()
        if path.is_file()
        and path.suffix == ".json"
        and path.stem.isdigit()
    ]
    if not schemas:
        raise FileNotFoundError(f"No schema files found in {SCHEMAS_DIR}")

    latest_schema_path = max(schemas, key=lambda path: int(path.stem))

    return json.loads(latest_schema_path.read_text())


def validate_credentials(credentials: dict) -> None:
    """
    Validates the credentials file against the latest schema.

    :param credentials:
        The credentials dictionary to validate.

    :raises ValidationError:
        If the credentials file is invalid.
    """
    schema = get_latest_schema()
    try:
        validate(instance=credentials, schema=schema)
        logger.info("Credentials file validation successful.")
    except ValidationError as e:
        logger.error(f"Credentials file is invalid: {e.message}")
        raise
