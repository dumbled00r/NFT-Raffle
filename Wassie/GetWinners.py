import math
import random
from decimal import Decimal

import numpy as np
import pandas as pd


def raffle_for_burners(snapshot_file="DWL_Burners_snapshot.csv", num_winners=25):
    """
    Conducts a fully weighted raffle where all participants have a chance proportional to their burned amount.

    Args:
        snapshot_file (str): Path to the DWL_Burners_snapshot.csv file.
        num_winners (int): Number of winners to select from the raffle pool.

    Returns:
        str: Path to the CSV file with the winners.
    """
    df = pd.read_csv(snapshot_file)
    random_seed = random.randint(12, 1231231)
    print(f"Random seed: {random_seed}")
    np.random.seed(random_seed)  # random seed

    df["total_burned"] = df["total_burned"].astype(str).apply(Decimal)
    df["total_burned_dwl"] = df["total_burned"] / Decimal(1e18)

    weights = df["total_burned_dwl"]
    weights = weights / weights.sum()  # normalization

    print(f"Sum of probabilities: {sum(weights)}")

    winners_index = np.random.choice(  # select random winners
        df.index, size=num_winners, replace=False, p=weights
    )

    raffle_winners = df.loc[winners_index, ["sender_address", "total_burned_dwl"]]

    raffle_winners = raffle_winners.sort_values(
        by="total_burned_dwl", ascending=False
    ).reset_index(drop=True)
    raffle_winners["win_type"] = "Weighted Raffle"

    output_file = "winners.csv"
    raffle_winners.to_csv(output_file, index=False)

    print(f"Raffle completed. Winners saved to {output_file}.")
    return output_file


if __name__ == "__main__":
    raffle_for_burners()
