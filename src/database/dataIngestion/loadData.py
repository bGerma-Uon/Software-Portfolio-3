"""
Script to load and normalize rail defect data from a CSV file into the
database.
"""

# Builtins
import ast
import logging
from pathlib import Path
from typing import Any

# External
import pandas

from src.database.dataIngestion.columnConfig import column_mapping
from src.database.dataIngestion.columns import ColumnDropGroup
from src.database.dataIngestion.columns import ColumnExplodeGroup1
from src.database.dataIngestion.columns import ColumnExplodeGroup2
# Internal
from src.database.management import BASE
from src.database.management import Defect
from src.database.management import ENGINE
from src.database.management import FoundBy
from src.database.management import TestSegment
from src.database.management import session_scope


# Logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# CONSTANTS
REPO_ROOT = Path(__file__).parent.parent.parent.parent
CSV_PATH = REPO_ROOT / "data" / "found_by_23_July_2022_to_29_July_2022.csv"
if not CSV_PATH.exists():
    raise FileNotFoundError(f"CSV file not found at: {CSV_PATH}")


def safe_literal_eval(string) -> Any:
    """
    Safely evaluate a string as a Python literal.

    :param string:
        string to evaluate
    :return:
        value of evaluated string
    """
    try:
        return ast.literal_eval(string)
    except (ValueError, SyntaxError):
        return []


def load_normalized_data():
    """
    Loads and normalizes rail defect data from a CSV file into the database.
    """
    logger.info("Starting normalized data loading process...")

    # 1. Drop and recreate tables.
    logger.info("Dropping and recreating normalized tables...")
    BASE.metadata.drop_all(ENGINE)
    BASE.metadata.create_all(ENGINE)

    # 2. Read and process data from the CSV file.
    logger.info(f"Reading data from {CSV_PATH}")
    df = pandas.read_csv(CSV_PATH)
    df = df.sample(1000)  # TODO: remove line
    df = df.where(pandas.notna(df), None)
    logger.info(f"Initial dataframe shape: {df.shape}")

    # Drop unnecessary columns
    logger.info(f"Dropping columns: {ColumnDropGroup}")
    df = df.drop(columns=ColumnDropGroup)
    logger.info(f"Shape after dropping columns: {df.shape}")

    # Rename columns
    logger.info("Renaming columns...")
    df = df.rename(columns=column_mapping)
    logger.info(f"Columns after rename: {df.columns.tolist()}")

    # Convert string-encoded arrays to lists
    logger.info("Converting string-encoded arrays to lists...")
    explosion_columns = list(ColumnExplodeGroup1) + list(ColumnExplodeGroup2)
    df.dropna(subset=explosion_columns, inplace=True)
    logger.info(
        f"Shape after dropping NaNs from explosion columns: {df.shape}",
    )

    df[explosion_columns] = df[explosion_columns].map(safe_literal_eval)
    logger.info("Finished converting columns to lists.")

    # Explode column groups to normalize the data
    logger.info("Exploding column groups...")
    df = df.explode(list(ColumnExplodeGroup1))
    logger.info(f"Shape after exploding group 1 once: {df.shape}")
    df = df.explode(list(ColumnExplodeGroup1))
    logger.info(f"Shape after exploding group 1 twice: {df.shape}")
    df = df.explode(list(ColumnExplodeGroup2))
    logger.info(f"Shape after exploding group 2: {df.shape}")

    if df.empty:
        logger.warning(
            "DataFrame is empty after processing. No data will be loaded.",
        )
        return

    with session_scope() as session:
        # 3. Populate TestSegment and FoundBy tables
        logger.info("Populating TestSegment and FoundBy tables...")

        # Ingest unique TestSegments
        unique_segments_df = df[[
            'test_segment_id',
            'top_rail',
            # 'priority'
        ]].drop_duplicates()
        for row in unique_segments_df.itertuples(index=False):
            segment = TestSegment(
                test_segment_id=row.test_segment_id,
                top_rail=row.top_rail,
                priority=None,  # row.priority todo replace back when fixed
            )
            session.merge(segment)

        # Ingest unique FoundBy names
        unique_found_by_names = df['found_by'].unique()
        for name in unique_found_by_names:
            found_by = FoundBy(name=name)
            session.merge(found_by)

        # Flush to assign IDs before creating Defects
        session.flush()

        # Create a mapping from found_by name to id for quick lookup
        found_by_map = {
            obj.name: obj.id
            for obj in session.query(FoundBy).all()
        }

        # 4. Populate Defect table
        logger.info("Populating Defect table...")
        for row in df:
            defect = Defect(
                id=row["defect_id"],
                test_segment_id=row["test_segment_id"],
                found_by_id=found_by_map[row["found_by"]],
                pulse_count=row["pulse_count"],
                key=row["key"],
            )
            session.merge(defect)

    logger.info("Normalized data loading complete.")


def main():
    """
    Entry point for the script.
    """
    load_normalized_data()


if __name__ == '__main__':
    main()
