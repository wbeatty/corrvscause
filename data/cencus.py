# 1. Call Cencus Bureau API to get datasets
# 2. Pair datasets based on similarity score
# 3. Save the pairs with higher similarity score to the database


import json
import os
import time

import requests

key = "639d20429682940f88a0e42aed74b63e6d9058a2"

country = "US"


def main():
    datasets = get_all_datasets()
    save_datasets_to_json(datasets)


def get_variables():
    url = "https://api.census.gov/data/timeseries/idb/5year/variables.json"
    response = requests.get(url)
    data = response.json()
    allvar = data["variables"]
    variables = []
    for var_name, var_info in allvar.items():
        group = var_info.get("group", "No group")
        if group == "IDB5YEAR":
            variables.append((var_name, var_info.get("label", "No label")))
    return variables


def get_dataset(var):
    url = (
        "https://api.census.gov/data/timeseries/idb/5year?get="
        + var
        + "&YR=2000:2020&for=genc+standard+countries+and+areas:"
        + country
        + "&key="
        + key
    )
    print(f"Fetching: {url}")

    try:
        response = requests.get(url)
        response.raise_for_status()  # Raise an exception for bad status codes
        data = response.json()

        if not data or len(data) < 2:
            print(f"No data returned for {var}")
            return None

        # Parse the Census API response
        # First row contains headers: [variable_name, "YR", "genc", "time"]
        # Subsequent rows contain: [value, year, country_code, timestamp]

        headers = data[0]
        rows = data[1:]

        # Extract years and values
        years = []
        values = []

        for row in rows:
            try:
                value = float(row[0]) if row[0] not in [None, "", "null"] else 0
                year = int(row[1])
                years.append(year)
                values.append(value)
            except (ValueError, IndexError):
                continue

        # Sort by year to ensure chronological order
        year_value_pairs = list(zip(years, values))
        year_value_pairs.sort(key=lambda x: x[0])
        years, values = zip(*year_value_pairs) if year_value_pairs else ([], [])

        # Get variable label/name
        variables_info = get_variable_info()
        var_name = variables_info.get(var, f"Dataset {var}")

        dataset = {
            "id": var,
            "name": var_name,
            "years": list(years),
            "values": list(values),
        }

        print(
            f"Processed {var}: {len(years)} data points from {min(years) if years else 'N/A'} to {max(years) if years else 'N/A'}"
        )
        return dataset

    except requests.exceptions.RequestException as e:
        print(f"Request failed for {var}: {e}")
        return None
    except json.JSONDecodeError as e:
        print(f"JSON decode error for {var}: {e}")
        return None
    except Exception as e:
        print(f"Unexpected error for {var}: {e}")
        return None


def get_variable_info():
    try:
        url = "https://api.census.gov/data/timeseries/idb/5year/variables.json"
        response = requests.get(url)
        data = response.json()

        variable_names = {}
        for var_name, var_info in data["variables"].items():
            if var_info.get("group") == "IDB5YEAR":
                variable_names[var_name] = var_info.get("label", var_name)

        return variable_names
    except Exception as e:
        print(f"Failed to get variable info: {e}")
        return {}


def save_datasets_to_json(datasets, filename="data/datasets.json"):
    """Save datasets in the format specified by data.json"""

    # Create data directory if it doesn't exist
    os.makedirs(os.path.dirname(filename), exist_ok=True)

    # Format according to data.json structure
    formatted_data = {"datasets": datasets}

    try:
        with open(filename, "w") as f:
            json.dump(formatted_data, f, indent=2)

        print(f"\nSuccessfully saved {len(datasets)} datasets to {filename}")
        print(
            f"Total data points across all datasets: {sum(len(d['years']) for d in datasets)}"
        )

    except Exception as e:
        print(f"Failed to save datasets to {filename}: {e}")


def get_all_datasets():
    """Get all available datasets (use with caution - many API calls)"""
    variables = get_variables()
    datasets = []

    for var_name, var_label in variables:
        try:
            dataset = get_dataset(var_name)
            if dataset:
                datasets.append(dataset)
                print(f"Successfully processed {var_name}")
            time.sleep(0.5)
        except Exception as e:
            print(f"Failed for {var_name}: {e}")
            time.sleep(0.5)

    save_datasets_to_json(datasets)
    return datasets


if __name__ == "__main__":
    main()
