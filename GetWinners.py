import math
import random
from decimal import Decimal

import numpy as np
import pandas as pd


def raffle_for_burners(snapshot_file="DWL_Burners_snapshot.csv", num_winners=35):
    """
    Conducts a weighted raffle where participants with <1 DWL burned
    have a chance proportional to their burned amount.

    Args:
        snapshot_file (str): Path to the DWL_Burners_snapshot.csv file.
        num_winners (int): Number of winners to select from the raffle pool.

    Returns:
        str: Path to the CSV file with the winners.
    """
    df = pd.read_csv(snapshot_file)

    np.random.seed()  # random seed --> you can check the res yourself <3

    df["total_burned"] = df["total_burned"].astype(str).apply(Decimal)
    df["total_burned_dwl"] = df["total_burned"] / Decimal(1e18)

    # Get the guaranteed list // those who burned 1 $DWL or more
    guaranteed_winners = df[df["total_burned_dwl"] >= 1][
        ["sender_address", "total_burned_dwl"]
    ]
    guaranteed_winners["win_type"] = "Guaranteed"

    # Get the raffle pool (those who burned <= 1 $DWL)
    raffle_pool = df[df["total_burned_dwl"] < 1]

    # Calculate weights for the raffle pool
    weights = raffle_pool["total_burned_dwl"]
    weights = weights / weights.sum()

    print(f"Sum of probabilities: {sum(weights)}")

    winners_index = np.random.choice(  # select random winners
        raffle_pool.index, size=num_winners, replace=False, p=weights
    )

    raffle_winners = raffle_pool.loc[
        winners_index, ["sender_address", "total_burned_dwl"]
    ]

    raffle_winners = raffle_winners.sort_values(
        by="total_burned_dwl", ascending=False
    ).reset_index(drop=True)
    raffle_winners["win_type"] = "FCFS"
    raffle_winners.loc[:4, "win_type"] = "GTD"

    final_winners = (
        pd.concat([guaranteed_winners, raffle_winners])
        .sort_values(by="total_burned_dwl", ascending=False)
        .reset_index(drop=True)
    )

    output_file = "winners.csv"
    final_winners.to_csv(output_file, index=False)

    print(f"Raffle completed. Winners saved to {output_file}.")
    return output_file


if __name__ == "__main__":
    raffle_for_burners()
