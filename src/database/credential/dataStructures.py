from dataclasses import dataclass
from dataclasses import dataclass
from enum import StrEnum
from enum import StrEnum
from enum import StrEnum
from typing import Optional
from typing import Self
from typing import Self


class DBCredentialsDict(StrEnum):
    """
    Manages Keys for the DB credentials dict
    """
    DEFAULT_PROFILE = "defaultProfile"
    DEFAULT_DATABASE = "defaultDatabase"
    CREDENTIALS = "credentials"


class CredentialDict(StrEnum):
    """
    Manages Keys for the credentials dict
    """
    PROFILE_NAME = "profileName"
    HOST = "host"
    USER = "user"
    PASSWORD = "password"
    DATABASE = "database"
    SSH = "ssh"


class SSHDict(StrEnum):
    """
    Manages Keys for the ssh dict
    """
    HOST = "host"
    USER = "user"
    PASSWORD = "password"


@dataclass
class SSH:
    """
    Wraps the ssh credentials into a dataclass
    """
    host: str
    user: str
    password: str

    @classmethod
    def from_dict(cls, _dict: dict) -> Self:
        """
        Creates an instance of itself from a dict

        :param _dict:
            The dictionary to read values from

        :return:
            An instance of itself
        """
        return cls(
            host=_dict[SSHDict.HOST],
            user=_dict[SSHDict.USER],
            password=_dict[SSHDict.PASSWORD],
        )


@dataclass
class Credential:
    """
    Wraps the DB Credentials into a dataclass
    """
    profile_name: str
    database: str
    host: str
    password: str
    user: str
    ssh: Optional[SSH]

    @classmethod
    def from_dict(cls, _dict: dict) -> Self:
        """
        Creates an instance of itself from a dict

        :param _dict:
            The dictionary to read values from

        :return:
            An instance of itself
        """
        ssh_dict = _dict[CredentialDict.SSH]
        ssh = SSH.from_dict(ssh_dict) if ssh_dict else None

        return cls(
            profile_name=_dict[CredentialDict.PROFILE_NAME],
            database=_dict[CredentialDict.DATABASE],
            host=_dict[CredentialDict.HOST],
            password=_dict[CredentialDict.PASSWORD],
            user=_dict[CredentialDict.USER],
            ssh=ssh,
        )
