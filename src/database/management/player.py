"""
FoundBy Table
"""
# Builtin
pass

# External
from sqlalchemy import Column
from sqlalchemy import String
from sqlalchemy import UniqueConstraint

# Internal
from src.database.management import BASE
from src.database.management import SqlBaseMixin


# CODE


class Player(SqlBaseMixin, BASE):
    __tablename__ = 'player'

    guid = Column(String(32), primary_key=True)
    name = Column(String(50), nullable=False)

    __table_args__ = (
        UniqueConstraint('name', name='_name_uc'),
    )
