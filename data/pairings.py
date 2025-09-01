import json

import numpy as np
import pandas as pd
import requests
from scipy.stats import pearsonr

# TODO:
# Automate adding new data and automatically comparing with existing datasets
# Be able to compare datasets where timeframes may be subsets of each other


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
    print("Would you like to upload the pairings to the database? (y/n)")
    upload = input()
    if upload == "y":
        upload_pairings(pearson_pairs)

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


def upload_pairings(pairings):
    url = "http://localhost:3000/api/datasets"
    datasets = requests.get(url)
    datasets = datasets.json()
    postURL = "http://localhost:3000/api/pairings"
    for pairing in pairings:
        dataset1 = next((d for d in datasets if d["id"] == pairing[0]), None)
        dataset1ID = dataset1["_id"]
        dataset2 = next((d for d in datasets if d["id"] == pairing[1]), None)
        dataset2ID = dataset2["_id"]
        pairing = requests.post(
            postURL,
            json={
                "dataset1": dataset1ID,
                "dataset2": dataset2ID,
                "similarityScore": pairing[2],
            },
        )
        print(pairing.text)


if __name__ == "__main__":
    main()
