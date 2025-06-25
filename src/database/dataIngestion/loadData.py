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

# Internal
from src.database.management import BASE
from src.database.management import ENGINE
from src.database.management import session_scope
from src.database.management import Defect
from src.database.management import FoundBy
from src.database.management import TestSegment

# --- Configuration ---
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

REPO_ROOT = Path(__file__).parent.parent.parent
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
    BASE.metadata.drop_all(ENGINE, checkfirst=True)
    BASE.metadata.create_all(ENGINE)

    # 2. Read data from the CSV file.
    logger.info(f"Reading data from {CSV_PATH}")
    df = pandas.read_csv(CSV_PATH)
    df = df.where(pandas.notna(df), None)

    # 3. Populate FoundBy table
    found_by_set = set()
    # "found_by",
    columns_to_explode = [
        "pulse_counts",
        "unique_ids",
        "keys",
    ]
    df["found_by"] = df["found_by"].dropna()
    df["found_by"] = df["found_by"].apply(safe_literal_eval)

    with session_scope() as session:
        found_by_map = {}
        for name in found_by_set:
            found_by_obj = FoundBy(name=name)
            session.add(found_by_obj)
            session.flush()  # Flush to get the ID
            found_by_map[name] = found_by_obj.id

        # 4. Process and insert data row by row
        for _, row in df.iterrows():
            test_segment_id = row['test_segment_id']

            # Create TestSegment if it doesn't exist
            if not session.query(TestSegment).get(test_segment_id):
                test_segment = TestSegment(
                    test_segment_id=test_segment_id,
                    top_rail=row['top_rail'],
                    priority=row['priority'],
                )
                session.add(test_segment)

            found_by_list = safe_literal_eval(row['found_by'])
            pulse_counts_list = safe_literal_eval(row['pulse_counts'])
            unique_ids_list = safe_literal_eval(row['unique_ids'])
            keys_list = safe_literal_eval(row['keys'])

            for i, source in enumerate(found_by_list):
                found_by_id = found_by_map[source]
                for j, unique_id in enumerate(unique_ids_list[i]):
                    if not session.query(Defect).get(unique_id):
                        defect = Defect(
                            id=unique_id,
                            test_segment_id=test_segment_id,
                            found_by_id=found_by_id,
                            pulse_count=pulse_counts_list[i][j],
                            key=keys_list[i][j],
                        )
                        session.add(defect)

    logger.info("Normalized data loading complete.")


def main():
    """
    Entry point for the script.
    """
    load_normalized_data()


if __name__ == '__main__':
    main()
