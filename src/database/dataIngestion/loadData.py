"""
Script to load and normalize rail defect data from a CSV file into the
database.
"""

# Builtins
import ast
import logging
import uuid
from pathlib import Path
from typing import Any

# External
import pandas

from src.database.dataIngestion.columnConfig import raw_to_normalised_column_map
from src.database.dataIngestion.columns import ColumnDropGroup
from src.database.dataIngestion.columns import ColumnExplodeGroup1
from src.database.dataIngestion.columns import ColumnExplodeGroup2
from src.database.dataIngestion.columns import DataBaseColumns
# Internal
from src.database.management import BASE
from src.database.management import ENGINE


# Logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# CONSTANTS
REPO_ROOT = Path(__file__).parent.parent.parent.parent


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


def normalise_data(csv_path: Path) -> pandas.DataFrame:
    """
    Normalizes the data in a CSV file.

    :param csv_path:
        path to the CSV file
    :return:
        normalized dataframe
    """

    # 2. Read and process data from the CSV file.
    logger.info(f"Reading data from {csv_path}")
    df = pandas.read_csv(csv_path)
    df = df.sample(1000)  # TODO: remove line
    df = df.where(pandas.notna(df), None)
    logger.info(f"Initial dataframe shape: {df.shape}")

    # Drop unnecessary columns
    logger.info(f"Dropping columns: {ColumnDropGroup}")
    df = df.drop(columns=ColumnDropGroup)
    logger.info(f"Shape after dropping columns: {df.shape}")

    # Rename columns
    logger.info("Renaming columns...")
    df = df.rename(columns=raw_to_normalised_column_map)
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
        raise ValueError("DataFrame is empty after processing.")
    return df


def recreate_database() -> None:
    """
    Recreates the database from scratch.
    """
    BASE.metadata.drop_all(ENGINE)
    BASE.metadata.create_all(ENGINE)


def upload_test_segment_to_database(dataframe: pandas.DataFrame) -> None:
    """

    :param dataframe:
    :return:
    """
    # Get table raw values
    test_segment_table = dataframe[["test_segment_id"]].drop_duplicates()

    # Add GUID
    test_segment_table["guid"] = None
    test_segment_table["guid"] = test_segment_table["guid"].apply(
        lambda x: str(uuid.uuid4().hex)
    )

    # Rename to match database
    test_segment_table = test_segment_table.rename(columns={
        "test_segment_id": DataBaseColumns.TEST_SEGMENT_ID
    })

    # Write to database
    test_segment_table.to_sql(
        name='test_segment',
        con=ENGINE,
        if_exists='append',
        index=False,
    )


def upload_player_to_database(dataframe: pandas.DataFrame) -> None:
    """

    :param dataframe:
    :return:
    """
    # Get table raw values
    player_table = dataframe[["player"]].drop_duplicates()

    # Add GUID
    player_table["guid"] = None
    player_table["guid"] = player_table["guid"].apply(
        lambda x: str(uuid.uuid4().hex),
    )

    # Rename to match database
    player_table = player_table.rename(columns={
        "player": DataBaseColumns.PLAYER
    })

    # Write to database
    player_table.to_sql(
        name='player',
        con=ENGINE,
        if_exists='append',
        index=False,
    )


def load_normalized_data_to_database(df: pandas.DataFrame) -> None:
    """
    Loads and normalizes rail defect data from a CSV file into the database.
    """


def main(csv_path: Path):
    """
    Entry point for the script.
    """
    normalised_df = normalise_data(csv_path)
    recreate_database()

    upload_test_segment_to_database(normalised_df)
    upload_player_to_database(normalised_df)

    # load_normalized_data_to_database(normalised_df)


if __name__ == '__main__':
    csv_path = REPO_ROOT / "data" / "found_by_23_July_2022_to_29_July_2022.csv"
    if not csv_path.exists():
        raise FileNotFoundError(f"CSV file not found at: {csv_path}")

    main(csv_path)
