"""
SuspectGroup Table
"""

# External
from sqlalchemy import Column
from sqlalchemy import ForeignKey
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy.orm import relationship

# Internal
from src.database.management import BASE
from src.database.management import SqlBaseMixin


class Location(SqlBaseMixin, BASE):
    """
    Represents a record of a rail defect.
    """
    __tablename__ = 'location'

    # Primary Key
    guid = Column(String(32), primary_key=True)

    # Columns
    test_segment_id = Column(
        String(32), ForeignKey('test_segment.guid'))
    rail = Column(
        Integer, nullable=False)
    pulse_count = Column(
        Integer, nullable=False)

    # Relationships
    test_segment = relationship(
        'TestSegment', back_populates='location')
