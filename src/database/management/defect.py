"""
Defect Table
"""

# Builtin
pass

# External
from sqlalchemy import Column
from sqlalchemy import ForeignKey
from sqlalchemy import String
from sqlalchemy.orm import relationship

# Internal
from src.database.management import BASE
from src.database.management import SqlBaseMixin


class Defect(SqlBaseMixin, BASE):
    __tablename__ = 'defect'

    # Key
    guid = Column(String(32), primary_key=True)

    # Columns
    priority_id = Column(
        String(32), ForeignKey('priority.guid'),
    )
    test_segment_id = Column(
        String(32), ForeignKey('test_segment.guid'),
    )
    location_id = Column(
        String(32), ForeignKey('location.guid'),
    )
    player_id = Column(
        String(32), ForeignKey('player.guid'),
    )
    suspect_group_id = Column(
        String(32), ForeignKey('suspect_group.guid'),
    )

    # Relationships
    priority = relationship(
        'Priority', back_populates='defect',
    )
    test_segment = relationship(
        'TestSegment', back_populates='defect',
    )
    location = relationship(
        'Location', back_populates='defect',
    )
    player = relationship(
        'Player', back_populates='defect',
    )
    suspect_group = relationship(
        'SuspectGroup', back_populates='defect',
    )
