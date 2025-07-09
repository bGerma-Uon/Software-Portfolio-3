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

# Internal
from src.database.management import BASE
from src.database.management import SqlBaseMixin


# CODE


class Defect(SqlBaseMixin, BASE):
    __tablename__ = 'defect'

    # Key
    guid = Column(String(32), primary_key=True)

    # Columns
    priority = Column(
        Integer, nullable=True,
    )
    location_id = Column(
        String(32), ForeignKey('location.guid'),
    )
    player_id = Column(
        String(32), ForeignKey('player.guid'),
    )
    defect_code_id = Column(
        String(32), ForeignKey('defect_code.guid'),
    )
    suspect_group = Column(
        Integer, nullable=False,
    )
