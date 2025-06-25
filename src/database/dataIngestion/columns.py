"""
Record Column Names
"""

from enum import StrEnum


class CSVColumns(StrEnum):
    """
    Tracks the column names of the csv file
    """
    TEST_SEGMENT_ID = "test_segment_id"
    PLAYER = "found_by"
    PULSE_COUNT = "pulse_count"
    PULSE_COUNTS = "pulse_counts"
    UNIQUE_ID = "unique_id"
    UNIQUE_IDS = "unique_ids"
    TOP_RAIL = "top_rail"
    KEYS = "keys"
    PRIORITY = "priority"


class NormalisedColumns(StrEnum):
    """
    Tracks the column names of the normalized table
    """
    ID = "id"
    TEST_SEGMENT_ID = "test_segment_id"
    PLAYER = "player"
    PULSE_COUNTS = "pulse_counts"
    UNIQUE_IDS = "unique_ids"
    TOP_RAIL = "top_rail"
    KEYS = "keys"
    PRIORITY = "priority"


class DataBaseColumns(StrEnum):
    """
    Database Column Names
    """
    TEST_SEGMENT_ID = "name"
    PLAYER = "name"
    PULSE_COUNT = "pulse_count"
    GROUP = "group"
    TOP_RAIL = "rail"
    KEYS = "code"
    PRIORITY = "level"


class ColumnExplodeGroup1(StrEnum):
    """
    Tracks the column names of the csv file
    """
    PULSE_COUNTS = NormalisedColumns.PULSE_COUNTS
    UNIQUE_IDS = NormalisedColumns.UNIQUE_IDS
    KEYS = NormalisedColumns.KEYS


class ColumnExplodeGroup2(StrEnum):
    """
    Tracks the column names of the csv file
    """
    PLAYER = NormalisedColumns.PLAYER


class ColumnDropGroup(StrEnum):
    """
    Tracks the column names of the csv file
    """
    PULSE_COUNT = CSVColumns.PULSE_COUNT
    UNIQUE_ID = CSVColumns.UNIQUE_ID
