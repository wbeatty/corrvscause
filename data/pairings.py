import json

import numpy as np
import pandas as pd
from scipy.stats import pearsonr

# TODO:
# Add all datasets to database
# Get all datasets, from generated pairings find object IDs
# With object ID for each dataset in pair, export to json file and save to database


def main():
    print("Input threshold:")
    threshold = float(input()) * 1000
    try:
        with open("data.json", "r") as file:
            data = json.load(file)
            datasets = data["datasets"]
    except FileNotFoundError:
        print("Data file not found")
        return
    df = pd.DataFrame()
    for dataset in datasets:
        df[dataset["id"]] = dataset["values"]
    normalized_df = df.apply(normalize_data)
    pearson_pairs = create_pairs(normalized_df, threshold)
    print("There are", len(pearson_pairs), "pairs above the threshold")

    # print(pearson_pairs)


def normalize_data(series):
    series = np.array(series)
    median = np.median(series)
    mad = np.median(np.abs(series - median))
    if mad == 0:
        return np.zeros_like(series)
    return (series - median) / mad


def create_pairs(df, threshold):
    pairs = []
    for i in range(len(df.columns)):
        for j in range(i + 1, len(df.columns)):
            correlation = calculate_pearson_correlation(df.iloc[:, i], df.iloc[:, j])
            if abs(correlation) >= threshold:
                pairs.append([df.columns[i], df.columns[j], correlation])
    return pairs


def calculate_pearson_correlation(series1, series2):
    correlation_coefficient = pearsonr(series1, series2)[0]

    if np.isnan(correlation_coefficient):
        print("NaN correlation between", series1.name, "and", series2.name)
        return 0

    return int(correlation_coefficient * 1000)


if __name__ == "__main__":
    main()
