"""
Configures how the columns map to each other
"""

from .columns import CSVColumns
from .columns import NormalizedColumns


column_mapping = {
    CSVColumns.TEST_SEGMENT_ID: NormalizedColumns.TEST_SEGMENT_ID,
    CSVColumns.FOUND_BY: NormalizedColumns.FOUND_BY,
    CSVColumns.PULSE_COUNTS: NormalizedColumns.PULSE_COUNTS,
    CSVColumns.UNIQUE_IDS: NormalizedColumns.UNIQUE_IDS,
    CSVColumns.TOP_RAIL: NormalizedColumns.TOP_RAIL,
    CSVColumns.KEYS: NormalizedColumns.KEYS,
    CSVColumns.PRIORITY: NormalizedColumns.PRIORITY,
}
