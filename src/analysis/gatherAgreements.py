"""
Creates agreement ratio table from defects df
"""
import pandas


def gather_agreement_ratio_table(
    defects_df: pandas.DataFrame
) -> pandas.DataFrame:
    """
    Creates a table with the ratios that different players agree on the defects
    present at a suspect group.

    1. Record all the unique defects each player spotted at a suspect
    2. Create two tables of pairings for each player
    3. For each suspect group, calculate the no. of agreements and the no.
        of total defects in the suspect group
    4. At the end of the comparison, divide the "no. of agreements" table by
        the "total number of defects" table.

    :param defects_df:

    :return:

    """

    # Step 1
    players = defects_df['player_name'].unique().tolist()
    import numpy
    agreement_table = pandas.DataFrame(
        columns=players, index=players,
        data=numpy.zeros((len(players), len(players)))
    )
    total_defects_table = pandas.DataFrame(
        columns=players, index=players,
        data=numpy.zeros((len(players), len(players)))
    )

    # Step 1.5
    for player in players:
        agreement_table.loc[player, player] = pandas.NA
        total_defects_table.loc[player, player] = pandas.NA

    # Step 2
    for group, suspect_group_df in defects_df.groupby('suspect_group'):
        for player_1 in players:
            for player_2 in players:
                player_1_defects = suspect_group_df[
                    suspect_group_df['player_name'] == player_1]
                player_2_defects = suspect_group_df[
                    suspect_group_df['player_name'] == player_2]
                player_1_defects = player_1_defects['defect_code']
                player_2_defects = player_2_defects['defect_code']
                player_1_defects = player_1_defects.unique().tolist()
                player_2_defects = player_2_defects.unique().tolist()
                num_agreements = (
                    len(set(player_1_defects) & set(player_2_defects)))
                num_defects = (
                    len(set(player_1_defects) | set(player_2_defects)))
                agreement_table.loc[player_1, player_2] += num_agreements
                total_defects_table.loc[player_1, player_2] += num_defects
                difference = num_defects - num_agreements
                if difference > 0:
                    pass

    # Step 3
    agreement_ratio_table = agreement_table.divide(total_defects_table)

    return agreement_ratio_table


def main():
    """"
    """
    from pathlib import Path
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
    gather_agreement_ratio_table(defects_data)


if __name__ == '__main__':
    main()
