"""
Gathers misses from defects dataframe
"""

# Builtins
from pathlib import Path

# External
import pandas

# Internal
pass


def gather_player_misses(defects_df: pandas.DataFrame) -> pandas.DataFrame:
    """
    Gathers misses from defects dataframe

    :param defects_df:
        A pandas DataFrame with defect data. Must contain 'player_name',
        'suspect_group', and 'defect_code'.

    :return:
        A pandas DataFrame with miss data
    """
    players = defects_df['player_name'].unique().tolist()
    miss_df = pandas.DataFrame(
        columns=[
            "player_name",
            "defect_code",
            "suspect_group",
            "misses",
        ],
    )
    for group, suspect_group_df in defects_df.groupby('suspect_group'):
        unique_defects_in_suspect_group = (
            suspect_group_df['defect_code'].unique().tolist()
        )
        for player in players:
            defects_player_spotted = (suspect_group_df[
                suspect_group_df['player_name'] == player
                ])
            unique_defects_player_spotted = (
                defects_player_spotted['defect_code']
                .unique().tolist()
            )
            misses = (
                set(unique_defects_in_suspect_group)
                - set(unique_defects_player_spotted)
            )
            for miss in misses:
                miss_df = pandas.concat([
                    miss_df,
                    pandas.DataFrame([{
                        "player_name":   player,
                        "defect_code":   miss,
                        "suspect_group": group,
                        "misses":        1,
                    }]),
                ], ignore_index=True)

    return miss_df


def main():
    """

    :return:
    """
    # The script is in src/visualisations, data is in analysis/
    csv_path = (
        Path(__file__).resolve().parents[1]
        / 'raw_data'
        / 'defects_table.csv'
    )

    if not csv_path.exists():
        print(f"Error: Data file not found at {csv_path}")
        print("Please run the analysis notebook to generate the defect data.")
        return

    defects_data = pandas.read_csv(csv_path)
    gather_player_misses(defects_data)


if __name__ == '__main__':
    main()
