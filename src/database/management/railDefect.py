"""
Defines the RailDefect table model for SQLAlchemy.
"""

# External
from sqlalchemy import Column, Integer, String, Boolean, Text

# Internal
from . import BASE, SqlBaseMixin


class RailDefect(SqlBaseMixin, BASE):
    """
    Represents a record of a rail defect.
    """
    __tablename__ = 'rail_defects'

    id = Column(Integer, primary_key=True)
    test_segment_id = Column(String(50))
    found_by = Column(Text)
    pulse_count = Column(Integer)
    pulse_counts = Column(Text)
    unique_id = Column(String(32))
    unique_ids = Column(Text)
    top_rail = Column(Boolean)
    keys = Column(Text)
    priority = Column(Integer)

    def __repr__(self):
        return (
            f"<RailDefect(id='{self.id}', "
            f"test_segment_id='{self.test_segment_id}', "
            f"priority={self.priority})>"
        )
