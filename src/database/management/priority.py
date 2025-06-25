"""
Priority Table
"""

# External
from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy import UniqueConstraint

# Internal
from . import BASE
from . import SqlBaseMixin


class Priority(SqlBaseMixin, BASE):
    """
    Represents a record of a rail defect.
    """
    __tablename__ = 'priority'

    guid = Column(String(32), primary_key=True)
    priority = Column(Integer, nullable=False)

    __table_args__ = (
        UniqueConstraint('priority', name='_priority_uc'),
    )
