"""
This is the main management module for the database.
"""

# Builtins
import logging
from contextlib import contextmanager

# External
from sqlalchemy import create_engine
from sqlalchemy.engine import URL
from sqlalchemy.orm import sessionmaker, declarative_base, Session
from sqlalchemy.exc import NoResultFound

# Internal
from src.database.credential import get_credential


# --- Logging ---
logger = logging.getLogger(__name__)


# --- Database Configuration ---

# 1. Get database credentials using the provided function.
db_credentials = get_credential()

# 2. Create the database connection URL.
#    Assuming a MySQL database with pymysql driver.
db_url = URL.create(
    drivername="mysql+pymysql",
    username=db_credentials.user,
    password=db_credentials.password,
    host=db_credentials.host,
    database=db_credentials.database,
)

# 3. Engine: Connect to the specified database.
ENGINE = create_engine(db_url, echo=False)

# 4. SessionMaker: A factory for creating new Session objects.
SESSION_MAKER = sessionmaker(bind=ENGINE, autoflush=False, autocommit=False)

# 5. Declarative Base: All mapped classes will inherit from this base.
BASE = declarative_base()


# --- Session Management ---

@contextmanager
def session_scope() -> Session:  # noqa
    """
    Provide a transactional scope around a series of operations.
    """
    session = SESSION_MAKER()
    try:
        yield session  # noqa
        session.commit()
    except Exception:
        session.rollback()
        raise
    finally:
        session.close()


# --- Base Model Mixin ---

class SqlBaseMixin:
    """
        A base mixin class that provides common CRUD operations.
        """
    __abstract__ = True

    @classmethod
    def get_one(cls, session: Session, **kwargs):
        """
        Gets a single object from the database based on filter criteria.
        """
        return session.query(cls).filter_by(**kwargs).one()

    @classmethod
    def get_one_or_create(cls, session: Session, **kwargs):
        """
        Tries to get an object, and if it doesn't exist, creates it.
        """
        try:
            instance = cls.get_one(session, **kwargs)
            return instance, False
        except NoResultFound:
            instance = cls(**kwargs)  # noqa
            session.add(instance)
            return instance, True

    def save(self, session: Session):
        """
        Saves the current instance to the database.
        """
        session.add(self)
        return self

    def delete(self, session: Session):
        """
        Deletes the current instance from the database.
        """
        session.delete(self)


from .testSegment import TestSegment
from .player import Player
from .priority import Priority
from .suspectGroup import SuspectGroup
from .defectCode import DefectCode
from .location import Location
from .defect import Defect
