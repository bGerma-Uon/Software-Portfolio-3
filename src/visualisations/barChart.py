"""
This module contains functions for creating bar chart visualisations.
"""

# Builtins
from pathlib import Path

# External
import matplotlib.pyplot as plt
import pandas
import seaborn as sns

# Internal
pass


def plot_player_misses(player_misses_df: pandas.DataFrame) -> None:
    """
    Calculates and plots the number of "misses" for each player.

    A "miss" is when a defect is spotted by at least one player in a
    suspect_group, but missed by another player in the same group.

    :param player_misses_df:
        A pandas DataFrame with defect data. Must contain 'player_name',
        'suspect_group', and 'defect_code'.
    """
    player_misses_df = player_misses_df.groupby('player_name')['misses'].sum()
    player_misses_df = player_misses_df.sort_values(ascending=False)
    if player_misses_df.empty:
        print("No misses to plot.")
        return

    # Create the bar plot.
    plt.figure(figsize=(14, 8))
    sns.barplot(
        x=player_misses_df.index,
        y=player_misses_df.values,
        palette='viridis',
        hue=player_misses_df.index,
        legend=False
    )
    plt.title('Number of Defects Missed by Each Player', fontsize=16)
    plt.xlabel('Player Name', fontsize=12)
    plt.ylabel('Number of Misses', fontsize=12)
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()
    plt.show()


def main():
    """
    Main function to run the script.
    """
    # The script is in src/visualisations, data is in analysis/
    csv_path = (
        Path(__file__).resolve().parents[1]
        / 'raw_data'
        / 'player_misses.csv'
    )

    if not csv_path.exists():
        print(f"Error: Data file not found at {csv_path}")
        print("Please run the analysis notebook to generate the defect data.")
        return

    defects_data = pandas.read_csv(csv_path)
    plot_player_misses(defects_data)


if __name__ == '__main__':
    main()
