"""
Function to download defect table from the database
"""

# Builtin
import random

# External
import pandas as pd
from sqlalchemy import distinct
from sqlalchemy import select

# Internal
from src.database.management import Defect
from src.database.management import DefectCode
from src.database.management import Location
from src.database.management import Player
from src.database.management import TestSegment
from src.database.management import session_scope


def download_defect_table(
    limit: int = 10,
) -> pd.DataFrame:
    """
    Downloads the defect table from the database and returns it as a pandas
    DataFrame with all related information (location, test segment, player, 
    defect code).
    
    Returns:
        pandas.DataFrame: The defect table data with related information
    """

    with session_scope() as session:

        # Query
        query = (
            select(
                Defect.guid.label('defect_guid'),
                Defect.priority,
                DefectCode.code.label('defect_code'),
                Player.name.label('player_name'),
                TestSegment.name.label('test_segment_name'),
                Location.rail,
                Location.pulse_count,
                Defect.suspect_group
            )
            .select_from(Defect)
            .join(
                Location,
                Defect.location_id == Location.guid,
                isouter=True
            )
            .join(
                DefectCode,
                Defect.defect_code_id == DefectCode.guid,
                isouter=True
            )
            .join(
                Player,
                Defect.player_id == Player.guid,
                isouter=True
            )
            .join(
                TestSegment,
                Location.test_segment_id == TestSegment.guid,
                isouter=True
            )
            .limit(limit)
        )

        # Get the result
        result = session.execute(query).all()

        # Convert to DataFrame
        defects_df = pd.DataFrame(result)
        return defects_df


def sample_defects_by_group(num_groups=3):
    """
    Samples defects by randomly selecting a specified number of sample groups
    and returns all defects belonging to those groups.
    
    Args:
        num_groups (int): Number of sample groups to randomly select
        
    Returns:
        pandas.DataFrame: Defects from the randomly selected sample groups
    """
    with session_scope() as session:

        # Get all unique suspect_group values
        distinct_groups_query = (
            select(
                distinct(
                    Defect.suspect_group
                )
            )
        )
        all_groups = session.execute(
            distinct_groups_query
        ).scalars().all()

        # Randomly select the specified number of groups
        if num_groups > len(all_groups):
            num_groups = len(all_groups)
        
        selected_groups = random.sample(all_groups, num_groups)

        # Query for all defects in the selected groups
        query = (
            select(
                Defect.guid.label('defect_guid'),
                Defect.priority,
                DefectCode.code.label('defect_code'),
                Player.name.label('player_name'),
                TestSegment.name.label('test_segment_name'),
                Location.rail,
                Location.pulse_count,
                Defect.suspect_group
            )
            .select_from(Defect)
            .join(
                Location,
                Defect.location_id == Location.guid,
                isouter=True
            )
            .join(
                DefectCode,
                Defect.defect_code_id == DefectCode.guid,
                isouter=True
            )
            .join(
                Player,
                Defect.player_id == Player.guid,
                isouter=True
            )
            .join(
                TestSegment,
                Location.test_segment_id == TestSegment.guid,
                isouter=True
            )
            .where(Defect.suspect_group.in_(selected_groups))
        )

        result = session.execute(query).all()

        # Convert to DataFrame
        defects_df = pd.DataFrame(result)
        return defects_df


if __name__ == '__main__':
    defects_df = sample_defects_by_group(1)
    print(defects_df)
