"""
TestSegment Table
"""
from sqlalchemy import UniqueConstraint

# Builtin
pass

# External
from sqlalchemy import Column
from sqlalchemy import String
from sqlalchemy.orm import relationship

# Internal
from src.database.management import BASE
from src.database.management import SqlBaseMixin


# CODE


class TestSegment(SqlBaseMixin, BASE):
    __tablename__ = 'test_segment'

    guid = Column(String(32), primary_key=True)
    name = Column(String(50), nullable=False)

    locations = relationship('Location', back_populates='test_segment')

    __table_args__ = (
        UniqueConstraint('name', name='_name_uc'),
    )
