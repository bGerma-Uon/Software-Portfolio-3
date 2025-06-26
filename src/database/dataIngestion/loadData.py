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

from src.database.dataIngestion.columnConfig import (
    raw_to_normalised_column_map)
from src.database.dataIngestion.columns import ColumnDropGroup
from src.database.dataIngestion.columns import ColumnExplodeGroup1
from src.database.dataIngestion.columns import ColumnExplodeGroup2
from src.database.dataIngestion.columns import DataBaseColumns
from src.database.dataIngestion.columns import NormalisedColumns
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
    # df = df.sample(1000)  # TODO: remove line
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
    df["suspect_group"] = [i for i in range(df.shape[0])]
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


def upload_test_segment_to_database(
    dataframe: pandas.DataFrame
) -> pandas.DataFrame:
    """
    Uploads unique test segments to the database and replaces the name
    in the main dataframe with the corresponding GUID.

    :param dataframe:
        The main normalised dataframe.
    :return:
        The dataframe with test_segment_id replaced by a GUID.
    """
    # Get table raw values
    test_segment_table = dataframe[[
        NormalisedColumns.TEST_SEGMENT_ID
    ]].drop_duplicates().copy()

    # Add GUID
    test_segment_table["guid"] = [
        str(uuid.uuid4().hex) for _ in range(len(test_segment_table))
    ]

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

    # Merge the GUIDs back into the main dataframe
    dataframe = pandas.merge(
        dataframe,
        test_segment_table,
        left_on="test_segment_id",
        right_on="name",
        how='left'
    )
    dataframe.drop(columns=["name", "test_segment_id"], inplace=True)
    dataframe = dataframe.rename(columns={"guid": "test_segment_id"})

    return dataframe


def upload_player_to_database(dataframe: pandas.DataFrame) -> pandas.DataFrame:
    """
    Uploads unique players to the database and replaces the name
    in the main dataframe with the corresponding GUID.

    :param dataframe:
        The main normalised dataframe.
    :return:
        The dataframe with player replaced by a GUID.
    """
    # Get table raw values
    player_table = dataframe[["player"]].drop_duplicates().copy()

    # Add GUID
    player_table["guid"] = [
        str(uuid.uuid4().hex) for _ in range(len(player_table))
    ]

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

    # Merge the GUIDs back into the main dataframe
    # Merge the GUIDs back into the main dataframe
    dataframe = pandas.merge(
        dataframe,
        player_table,
        left_on="player",
        right_on="name",
        how='left'
    )
    dataframe.drop(columns=["name", "player"], inplace=True)
    dataframe = dataframe.rename(columns={"guid": "player_id"})
    return dataframe


def upload_defect_code_to_database(
    dataframe: pandas.DataFrame
) -> pandas.DataFrame:
    """
    Uploads unique defect codes to the database and replaces the name
    in the main dataframe with the corresponding GUID.

    :param dataframe:
        The main normalised dataframe.
    :return:
        The dataframe with defect code replaced by a GUID.
    """
    # Get table raw values
    defect_code_raw_csv_cols = [
        "keys"
    ]
    defect_code_table = (
        dataframe[defect_code_raw_csv_cols]
        .drop_duplicates()
        .copy()
    )

    # Add GUID
    defect_code_table["guid"] = [
        str(uuid.uuid4().hex) for _ in range(len(defect_code_table))
    ]

    # Rename to match database
    defect_code_table = defect_code_table.rename(
        columns={
            "keys": DataBaseColumns.KEYS
        }
    )

    # Write to database
    defect_code_table.to_sql(
        name='defect_code',
        con=ENGINE,
        if_exists='append',
        index=False,
    )

    # Merge the GUIDs back into the main dataframe
    # Merge the GUIDs back into the main dataframe
    dataframe = pandas.merge(
        dataframe,
        defect_code_table,
        left_on="keys",
        right_on="code",
        how='left'
    )
    dataframe.drop(columns=["keys", "code"], inplace=True)
    dataframe = dataframe.rename(columns={"guid": "defect_code_id"})
    return dataframe


def upload_location_table_to_database(
    dataframe: pandas.DataFrame
) -> pandas.DataFrame:
    """
    Uploads unique locations to the database and adds the location GUID
    to the main dataframe.

    :param dataframe:
        The main normalised dataframe.
    :return:
        The dataframe with an added location_id GUID column.
    """
    # Get table raw values for location
    location_cols = [
        "test_segment_id",
        "top_rail",
        "pulse_counts"
    ]

    location_table = dataframe[location_cols].drop_duplicates().copy()

    # Add GUID
    location_table["guid"] = [
        str(uuid.uuid4().hex) for _ in range(len(location_table))
    ]

    # Rename to match database
    location_table = location_table.rename(columns={
        "top_rail": DataBaseColumns.TOP_RAIL,  # "rail"
        "pulse_counts": DataBaseColumns.PULSE_COUNT  # "pulse_count"
    })

    # Write to database
    location_table.to_sql(
        name='location',
        con=ENGINE,
        if_exists='append',
        index=False,
    )

    # Merge the GUIDs back into the main dataframe
    new_location_cols = [
        "test_segment_id",
        DataBaseColumns.TOP_RAIL,
        DataBaseColumns.PULSE_COUNT,
    ]
    dataframe = pandas.merge(
        dataframe,
        location_table,
        left_on=location_cols,
        right_on=new_location_cols,
        how='left'
    )
    dataframe.drop(
        columns=list(set(location_cols + new_location_cols)),
        inplace=True
    )
    dataframe = dataframe.rename(columns={'guid': 'location_id'})
    return dataframe


def upload_defect_table_to_database(
    dataframe: pandas.DataFrame
) -> pandas.DataFrame:
    """
    Loads and normalizes rail defect data from a CSV file into the database.
    """
    defect_table_cols = [
        "priority",
        "location_id",
        "player_id",
        "defect_code_id",
        "suspect_group",
    ]

    defect_table = dataframe[defect_table_cols]
    defect_table["guid"] = [
        str(uuid.uuid4().hex) for _ in range(len(defect_table))
    ]
    defect_table.to_sql(
        name='defect',
        con=ENGINE,
        if_exists='append',
        index=False,
    )

    return defect_table


def main(csv_path: Path):
    """
    Entry point for the script.
    """
    normalised_df = normalise_data(csv_path)
    recreate_database()

    normalised_df = upload_test_segment_to_database(normalised_df)
    normalised_df = upload_player_to_database(normalised_df)
    normalised_df = upload_location_table_to_database(normalised_df)
    normalised_df = upload_defect_code_to_database(normalised_df)
    _ = upload_defect_table_to_database(normalised_df)


if __name__ == '__main__':
    csv_path = REPO_ROOT / "data" / "found_by_23_July_2022_to_29_July_2022.csv"
    if not csv_path.exists():
        raise FileNotFoundError(f"CSV file not found at: {csv_path}")

    main(csv_path)
