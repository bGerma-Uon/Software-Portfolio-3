"""
Configures how the columns map to each other
"""

from .columns import CSVColumns
from .columns import NormalisedColumns


raw_to_normalised_column_map = {
    CSVColumns.TEST_SEGMENT_ID: NormalisedColumns.TEST_SEGMENT_ID,
    CSVColumns.PLAYER: NormalisedColumns.PLAYER,
    CSVColumns.PULSE_COUNTS: NormalisedColumns.PULSE_COUNTS,
    CSVColumns.UNIQUE_IDS: NormalisedColumns.UNIQUE_IDS,
    CSVColumns.TOP_RAIL: NormalisedColumns.TOP_RAIL,
    CSVColumns.KEYS: NormalisedColumns.KEYS,
    CSVColumns.PRIORITY: NormalisedColumns.PRIORITY,
}
