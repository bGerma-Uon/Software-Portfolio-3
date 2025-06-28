"""
Agreement Table.

This module provides functions to visualise player agreement data.
"""

# Builtins
import matplotlib.pyplot

# External
import pandas
import seaborn

# Internal
pass


def plot_player_agreements(
    player_agreements_df: pandas.DataFrame
) -> None:
    """
    Plots the player agreement table as a heatmap.

    A colour range is used to highlight the gradient of agreement ratios.

    :param player_agreements_df: A square DataFrame where indices and columns
                                 are player names and cells are agreement
                                 ratios.
    """
    figure, axis = matplotlib.pyplot.subplots(figsize=(12, 10))
    seaborn.heatmap(
        player_agreements_df,
        annot=True,
        cmap='YlGnBu',
        fmt=".2f",
        linewidths=.5,
        ax=axis
    )
    title = 'Player Agreement Ratios for Unique Defects in Suspect Groups'
    axis.set_title(title, fontsize=16)
    axis.set_xlabel('Player', fontsize=12)
    axis.set_ylabel('Player', fontsize=12)
    matplotlib.pyplot.xticks(rotation=45, ha='right')
    matplotlib.pyplot.yticks(rotation=0)
    figure.tight_layout()
    matplotlib.pyplot.show()


def main():
    """

    :return:
    """
    # The script is in src/visualisations, data is in analysis/
    from pathlib import Path
    csv_path = (
        Path(__file__).resolve().parents[1]
        / 'raw_data'
        / 'agreement_table.csv'
    )

    if not csv_path.exists():
        print(f"Error: Data file not found at {csv_path}")
        print("Please run the analysis notebook to generate the defect data.")
        return

    agreements_table_df = pandas.read_csv(csv_path)
    agreements_table_df.set_index(
        agreements_table_df.columns[0],
        inplace=True,
        drop=True,
    )
    agreements_table_df.astype(float)
    plot_player_agreements(agreements_table_df)


if __name__ == '__main__':
    main()
