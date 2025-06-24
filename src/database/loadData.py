"""
Script to load rail defect data from a CSV file into the database.
"""

# Builtins
import logging
from pathlib import Path

# External
import pandas

# Internal
from src.database.management import (
    BASE,
    ENGINE,
    session_scope,
    RailDefect
)

# --- Configuration ---
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

REPO_ROOT = Path(__file__).parent.parent.parent
CSV_PATH = REPO_ROOT / "data" / "found_by_23_July_2022_to_29_July_2022.csv"


def load_rail_defect_data() -> None:
    """
    Loads rail defect data from a CSV file into the database.
    """
    logger.info("Starting data loading process...")

    # 1. Ensure the table is created.
    logger.info("Dropping and recreating the 'rail_defects' table...")
    BASE.metadata.drop_all(ENGINE)
    BASE.metadata.create_all(ENGINE)

    # 2. Read data from the CSV file.
    logger.info(f"Reading data from {CSV_PATH}")
    if not CSV_PATH.exists():
        logger.error(f"CSV file not found at: {CSV_PATH}")
        return

    logger.info(f"Reading data from {CSV_PATH}")
    df = pandas.read_csv(CSV_PATH)
    df = df.where(pandas.notna(df), None)

    # Add the new id column
    df['id'] = df.index

    # 3. Load data into the database using a session.
    with session_scope() as session:
        logger.info(f"Loading {len(df)} records into the database...")

        if not df.empty:
            df.to_sql(
                name=RailDefect.__tablename__,
                con=ENGINE,
                if_exists='append',
                index=False,
                chunksize=1000  # Insert in chunks for memory management
            )
            logger.info(f"Successfully added {len(df)} new records.")
        else:
            logger.info("No new records to add.")

        logger.info("Data loading complete.")


def main() -> None:
    """"
    """
    load_rail_defect_data()


if __name__ == '__main__':
    main()
