"""
TestSegment Table
"""

# Builtin
pass

# External
from sqlalchemy import Boolean
from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy.orm import relationship

# Internal
from src.database.management import BASE
from src.database.management import SqlBaseMixin


# CODE


class TestSegment(SqlBaseMixin, BASE):
    __tablename__ = 'test_segments'

    test_segment_id = Column(String(50), primary_key=True)
    top_rail = Column(Boolean)
    priority = Column(Integer)

    defects = relationship('Defect', back_populates='test_segment')
