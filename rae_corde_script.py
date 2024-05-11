"""
Refactored script for comparing frequency of terms in the RAE's CORDE.
Produces graphs similar to Google Ngram Viewer.
"""

from itertools import zip_longest
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
QUERIES = ["vos", "tú", "usted"]
COUNTRIES = [1000]  # 1000 for all countries
START_YEAR = 900
STOP_YEAR = 2000
STEP = 25


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


def main():
    data_frames = []
    for query, country in zip_longest(QUERIES, COUNTRIES, fillvalue=COUNTRIES[-1]):
        data = fetch_data(query, country, START_YEAR, STOP_YEAR, STEP)
        df = pd.DataFrame(list(data.items()), columns=["Year", "Occurrences"])
        df["Query"] = query
        data_frames.append(df)
    plot_data(data_frames)


if __name__ == "__main__":
    main()
