# -*- coding: utf-8 -*-
"""
Script for comparing frequency of terms in the RAE's CORDE with command-line arguments.
Produces graphs similar to Google Ngram Viewer.
"""
import argparse
from urllib.parse import quote

import matplotlib.pyplot as plt
import pandas as pd
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException

# Constants
GECKODRIVER_PATH = "C:\\path\\to\\your\\geckodriver.exe"
BASE_URL = "http://corpus.rae.es/cgi-bin/crpsrvEx.dll?MfcISAPICommand=buscar&tradQuery=1&destino=1"
XPATH_SUBMIT = "/html/body/blockquote/table[2]/tbody/tr[5]/td/form/input[5]"
XPATH_TABLE = "/html/body/blockquote/table[2]/tbody/tr/td/table/tbody/tr"


def fetch_data(query, country, start_year, stop_year, step):
    results = {}
    with webdriver.Firefox(executable_path=GECKODRIVER_PATH) as driver:
        for year in range(start_year, stop_year, step):
            sanitized_query = quote(query.encode("latin"))
            url = f"{BASE_URL}&texto={sanitized_query}&ano1={year}&ano2={year+step}&medio=1000&pais={country}&tema=1000"
            driver.get(url)
            try:
                submit_button = driver.find_element_by_xpath(XPATH_SUBMIT)
                submit_button.click()
                table = driver.find_element_by_xpath(XPATH_TABLE)
                rows = table.find_elements_by_class_name("texto")[0].text.split("\n")
                for row in rows[1:]:
                    date, percent, occurrences = row.strip().split()
                    occurrences = int(occurrences)
                    date = str(year + step / 2 + 0.5) if date == "Otros" else date
                    results[date] = max(results.get(date, 0), occurrences)
            except NoSuchElementException:
                continue
    return results


def plot_data(data_frames):
    fig, ax = plt.subplots()
    for df in data_frames:
        df.plot.line(x="Year", y="Query", ax=ax)
    plt.show()


def main(queries, start_year, stop_year, step):
    country = 1000  # Assuming constant country code for all queries
    data_frames = []
    for query in queries:
        data = fetch_data(query, country, start_year, stop_year, step)
        df = pd.DataFrame(list(data.items()), columns=["Year", "Occurrences"])
        df["Query"] = query
        data_frames.append(df)
    plot_data(data_frames)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Perform frequency analysis of terms in RAE's CORDE."
    )
    parser.add_argument(
        "queries", nargs="+", help="Space-separated list of words to search"
    )
    parser.add_argument(
        "--start_year",
        type=int,
        default=900,
        help="Start year of the range (default: 900)",
    )
    parser.add_argument(
        "--stop_year",
        type=int,
        default=2000,
        help="Stop year of the range (default: 2000)",
    )
    parser.add_argument(
        "--step", type=int, default=25, help="Step size for years (default: 25)"
    )
    args = parser.parse_args()

    main(args.queries, args.start_year, args.stop_year, args.step)
