"""
DefectCode Table
"""

# External
from sqlalchemy import Column
from sqlalchemy import String
from sqlalchemy import UniqueConstraint

# Internal
from . import BASE
from . import SqlBaseMixin


class DefectCode(SqlBaseMixin, BASE):
    """
    Represents a record of a rail defect.
    """
    __tablename__ = 'defect_code'

    guid = Column(String(32), primary_key=True)
    code = Column(String(45), nullable=False)

    __table_args__ = (
        UniqueConstraint('code', name='_defect_code_uc'),
    )
