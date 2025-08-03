import json
import os
import time

import requests


def main():
    datasets = get_all_datasets()
    save_datasets_to_json(datasets)


wb_vars = [
    ("EN.POP.DNST", "Population density (people per sq. km of land area)"),
    ("NY.GDP.PCAP.KD.ZG", "GDP per capita (annual % growth)"),
    ("SG.GEN.PARL.ZS", "Proportion of seats held by women in national parliaments (%)"),
    (
        "SP.M18.2024.FE.ZS",
        "Women who were first married by age 18 (% of women ages 20-24)",
    ),
    ("SH.HIV.INCD.ZS", "Incidence of HIV, ages 15-49 (per 1,000 uninfected population"),
    (
        "ER.PTD.TOTL.ZS",
        "Terrestrial and marine protected areas (% of total territorial area)",
    ),
    ("EN.POP.SLUM.UR.ZS", "Population living in slums (% of urban population)"),
    ("VC.IHR.PSRC.P5", "Intentional homicides (per 100,000 people)"),
    ("IT.NET.USER.ZS", "Individuals using the Internet (% of population)"),
    ("EG.ELC.ACCS.ZS", "Access to electricity (% of population)"),
    (
        "EG.FEC.RNEW.ZS",
        "Renewable energy consumption (% of total final energy consumption)",
    ),
    ("SP.DYN.LE00.IN", "Life expectancy at birth, total (years)"),
    ("SP.DYN.CONU.ZS", "Contraceptive prevalence rate, total (% of women ages 15-49)"),
    ("EG.USE.PCAP.KG.OE", "Electric power consumption (kWh per capita)"),
    ("IT.CEL.SETS.P2", "Mobile cellular subscriptions (per 100 people)"),
    ("SM.POP.NETM", "Net migration"),
    (
        "PV.PER.RNK",
        "Political Stability and Absence of Violence/Terrorism: Percentile Rank",
    ),
    ("MS.MIL.XPND.GD.ZS", "Military expenditure (% of GDP)"),
    ("MS.MIL.XPRT.KD", "Arms exports (SIPRI trend indicator values)"),
    ("IS.RRS.TOTL.KM", "Railways, total (km)"),
    ("IP.JRN.ARTC.SC", "Scientific and technical journal articles"),
    ("IP.PAT.RESD", "Patent applications, residents"),
    ("ST.INT.ARVL", "International tourism, number of arrivals (1000s)"),
    ("ST.INT.DPRT", "International tourism, number of departures (1000s)"),
]


def get_dataset(var):
    wb_url = (
        "https://api.worldbank.org/v2/country/usa/indicator/"
        + var[0]
        + "?date=2000:2020&format=json"
    )
    print(f"Fetching: {wb_url}")

    try:
        response = requests.get(wb_url)
        response.raise_for_status()
        data = response.json()

        if not data or len(data) < 2:
            print(f"No data returned for {var[0]}")
            return None

        data_points = data[1]
        years = []
        values = []
        for point in data_points:
            try:
                value = (
                    float(point["value"])
                    if point["value"] not in [None, "", "null"]
                    else 0
                )
                year = int(point["date"])
                years.append(year)
                values.append(value)
            except (ValueError, IndexError):
                continue

        year_value_pairs = list(zip(years, values))
        year_value_pairs.sort(key=lambda x: x[0])
        years, values = zip(*year_value_pairs) if year_value_pairs else ([], [])

        return {
            "id": var[0],
            "name": var[1],
            "years": list(years),
            "values": list(values),
        }

    except requests.exceptions.RequestException as e:
        print(f"Request failed for {var[0]}: {e}")
        return None
    except json.JSONDecodeError as e:
        print(f"JSON decode error for {var[0]}: {e}")
        return None
    except Exception as e:
        print(f"Unexpected error for {var[0]}: {e}")
        return None


def get_all_datasets():
    datasets = []
    for vars in wb_vars:
        try:
            dataset = get_dataset(vars)
            if dataset:
                datasets.append(dataset)
                print(f"Successfully processed {vars[0]}")
            time.sleep(0.5)
        except Exception as e:
            print(f"Failed for {vars[0]}: {e}")
            time.sleep(0.5)
    return datasets


def save_datasets_to_json(datasets, filename="data/datasets.json"):
    os.makedirs(os.path.dirname(filename), exist_ok=True)
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


if __name__ == "__main__":
    main()
