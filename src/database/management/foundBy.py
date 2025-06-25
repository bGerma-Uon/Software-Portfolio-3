"""
FoundBy Table
"""
# Builtin
pass

# External
from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy import UniqueConstraint
from sqlalchemy.orm import relationship

# Internal
from src.database.management import BASE
from src.database.management import SqlBaseMixin


# CODE


class FoundBy(SqlBaseMixin, BASE):
    __tablename__ = 'found_by'

    id = Column(Integer, primary_key=True)
    name = Column(String(50), nullable=False)

    defects = relationship('Defect', back_populates='found_by_source')

    __table_args__ = (UniqueConstraint('name', name='_name_uc'),)
