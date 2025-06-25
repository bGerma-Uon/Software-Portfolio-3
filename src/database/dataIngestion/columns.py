"""
Record Column Names
"""

from enum import StrEnum


class CSVColumns(StrEnum):
    """
    Tracks the column names of the csv file
    """
    TEST_SEGMENT_ID = "test_segment_id"
    FOUND_BY = "found_by"
    PULSE_COUNT = "pulse_count"
    PULSE_COUNTS = "pulse_counts"
    UNIQUE_ID = "unique_id"
    UNIQUE_IDS = "unique_ids"
    TOP_RAIL = "top_rail"
    KEYS = "keys"
    PRIORITY = "priority"


class ColumnExplodeGroup1(StrEnum):
    """
    Tracks the column names of the csv file
    """
    PULSE_COUNTS = CSVColumns.PULSE_COUNTS
    UNIQUE_IDS = CSVColumns.UNIQUE_IDS
    KEYS = CSVColumns.KEYS


class ColumnExplodeGroup2(StrEnum):
    """
    Tracks the column names of the csv file
    """
    FOUND_BY = CSVColumns.FOUND_BY


class ColumnDropGroup(StrEnum):
    """
    Tracks the column names of the csv file
    """
    PULSE_COUNT = CSVColumns.PULSE_COUNT
    UNIQUE_ID = "unique_id"


class NormalizedColumns(StrEnum):
    """
    Tracks the column names of the normalized table
    """
    ID = "id"
    TEST_SEGMENT_ID = "test_segment_id"
    FOUND_BY = "found_by"
    PULSE_COUNTS = "pulse_counts"
    UNIQUE_IDS = "unique_ids"
    TOP_RAIL = "top_rail"
    KEYS = "keys"
    PRIORITY = "priority"
