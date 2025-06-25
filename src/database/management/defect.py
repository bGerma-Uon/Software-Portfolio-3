"""
Defect Table
"""

# Builtin
pass

# External
from sqlalchemy import Column
from sqlalchemy import ForeignKey
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy import Text
from sqlalchemy.orm import relationship

# Internal
from src.database.management import BASE
from src.database.management import SqlBaseMixin


class Defect(SqlBaseMixin, BASE):
    __tablename__ = 'defects'

    id = Column(String(32), primary_key=True)
    test_segment_id = Column(
        String(50),
        ForeignKey('test_segments.test_segment_id'),
    )
    found_by_id = Column(Integer, ForeignKey('found_by.id'))
    pulse_count = Column(Integer)
    key = Column(Text)

    test_segment = relationship('TestSegment', back_populates='defects')
    found_by_source = relationship('FoundBy', back_populates='defects')
