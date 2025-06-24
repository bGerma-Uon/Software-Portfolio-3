"""
Gets the database credentials from the user store
"""

# Builtin
import json
import logging
from pathlib import Path

# External
from jsonschema import ValidationError
from jsonschema import validate

# Internal
from .dataStructures import Credential
from .dataStructures import CredentialDict
from .dataStructures import DBCredentialsDict
from .validation import get_latest_schema

# Logging
logger = logging.getLogger(__name__)

# Constants
REPO_ROOT = Path(__file__).parent.parent.parent.parent

CREDENTIALS_PATH = REPO_ROOT / "credentials/databaseCreds.json"


def __get_raw_db_credentials_file() -> dict:
    """
    Gets the database credentials and validates them against the schema.

    :return:
        Raw database credentials as json dict

    :raises:
        ValidationError if the credentials file is invalid.
    """
    schema = get_latest_schema()
    credentials = json.loads(CREDENTIALS_PATH.read_text())

    try:
        validate(instance=credentials, schema=schema)
        logger.info("Credentials file validation successful.")
    except ValidationError as e:
        logger.error(f"Credentials file is invalid: {e.message}")
        raise

    return credentials


def __get_db_credentials() -> list[dict]:
    """
    Gets the database credentials

    :return:
        The database credentials dict
    """
    raw_db_credentials = __get_raw_db_credentials_file()

    return raw_db_credentials[
        DBCredentialsDict.CREDENTIALS
    ]


def __get_db_credentials_config() -> dict:
    """
    Gets the database credentials config

    :return:
        Database credentials configuration
    """
    raw_db_credentials = __get_raw_db_credentials_file()

    config_keys = [
        DBCredentialsDict.DEFAULT_PROFILE,
        DBCredentialsDict.DEFAULT_DATABASE,
    ]

    return {key: raw_db_credentials[key] for key in config_keys}


def get_credential(
    database: str = None,
    profile: str = None,
) -> Credential:
    """
    Gets the credentials of the database

    :return:
        The database credentials
    """
    credentials = __get_db_credentials()
    config = __get_db_credentials_config()

    if not database:
        logger.info("No database provided - Using default")
        database = config[DBCredentialsDict.DEFAULT_DATABASE]

    if not profile:
        logger.info("No profile provided - Using default")
        profile = config[DBCredentialsDict.DEFAULT_PROFILE]

    cred_dict = __find_credential(credentials, database, profile)

    return Credential.from_dict(cred_dict)


def __find_credential(
    credentials: list[dict],
    database: str,
    profile: str,
) -> dict:
    """
    Finds a credential

    :param credentials:
        List of credentials
    :param database:
        Name of the database to find
    :param profile:
        Name of the profile to find

    :return:
        Profile credentials
    """
    # Guard statements
    if not __find_credentials_with_database(credentials, database):
        raise ValueError(f"database {database} not found")

    if not __find_credentials_with_profile(credentials, profile):
        raise ValueError(f"profile {profile} not found")

    for credential in credentials:
        if (
            credential[CredentialDict.DATABASE] == database
            and credential[CredentialDict.PROFILE_NAME] == profile
        ):
            return credential
    else:
        raise ValueError(
            f"database {database} in environment {profile} not found",
        )


def __find_credentials_with_database(
    credentials: list[dict],
    database: str,
) -> list[dict]:
    """
    Finds all credentials with the given database

    :param credentials:
        List of credentials
    :param database:
        Name of the database to find

    :return:
        Profile credentials
    """
    credentials_with_database = []
    for credential in credentials:
        if credential[CredentialDict.DATABASE] == database:
            credentials_with_database.append(credential)

    return credentials_with_database


def __find_credentials_with_profile(
    credentials: list[dict],
    profile: str
) -> list[dict]:
    """
    Finds all credentials with the given profile

    :param credentials:
        List of credentials
    :param profile:
        Name of the profile to find

    :return:
        Profile credentials
    """
    credentials_with_profile = []
    for credential in credentials:
        if credential[CredentialDict.PROFILE_NAME] == profile:
            credentials_with_profile.append(credential)

    return credentials_with_profile
