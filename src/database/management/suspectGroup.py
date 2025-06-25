"""
SuspectGroup Table
"""

# External
from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy import UniqueConstraint

# Internal
from . import BASE
from . import SqlBaseMixin


class SuspectGroup(SqlBaseMixin, BASE):
    """
    Represents a record of a rail defect.
    """
    __tablename__ = 'suspect_group'

    guid = Column(String(32), primary_key=True)
    group = Column(Integer, nullable=False)

    __table_args__ = (
        UniqueConstraint('group', name='_group_uc'),
    )
