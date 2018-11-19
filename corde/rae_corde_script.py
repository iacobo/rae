# -*- coding: utf-8 -*-
"""
Script for comparing frequency of terms in the RAE's CORDE.
Produces graphs similar to Google Ngram.

For keyword argument help, see:
http://corpus.rae.es/ayuda_c.htm
"""

from itertools import zip_longest
from selenium import webdriver
from urllib.request import quote
import pandas as pd
import matplotlib.pyplot as plt

# Parameters
queries = ["vos", "tú", "usted"]
start_year = 900
stop_year = 2000
step = 25 # Gaps n years to search through.
not_spain = "0&pais=1&pais=2&pais=3&pais=4&pais=5&pais=6&pais=7&pais=8&pais=10&pais=11&pais=12&pais=13&pais=14&pais=15&pais=16&pais=17&pais=18&pais=19&pais=20&pais=21&pais=22&pais=23"
all_countries = 1000 # 1000=all countries, 9=Spain
countries = [all_countries]

# Allow plotting of multiple lines on same axis
fig, ax = plt.subplots()

# Container for dataframes for post-analysis
dfs = []

# Location of driver for webdriver. Not needed as param if location in your PATH
geckodriverpath = "C:\\Users\\jacob\\Downloads\\geckodriver-v0.21.0-win64\\geckodriver.exe"
driver = webdriver.Firefox(executable_path=geckodriverpath)

# xpaths for relevant elements on webpages
xpath_submit = "/html/body/blockquote/table[2]/tbody/tr[5]/td/form/input[5]"
xpath_table = "/html/body/blockquote/table[2]/tbody/tr/td/table/tbody/tr"

url_base = "http://corpus.rae.es/cgi-bin/crpsrvEx.dll?MfcISAPICommand=buscar&tradQuery=1&destino=1"

# Zipping queries and country parameter for search
q_c = list(zip_longest(queries, countries, fillvalue=countries[-1]))

for query, country in q_c:
    a = {query: {}}
    
    for year in range(start_year,stop_year,step):
        # Formatting enye, accents etc for url
        sanitised_query = quote(query.encode('latin'))
        url = url_base 
        url += "&texto={}&autor=&titulo=&ano1={}&ano2={}".format(sanitised_query, year, year+step) 
        url += "&medio=1000&pais={}&tema=1000".format(country)
        driver.get(url)
        
        try:
            submit_button = driver.find_element_by_xpath(xpath_submit)
            submit_button.click()
            
            table = driver.find_element_by_xpath(xpath_table)
            rows = table.find_elements_by_class_name("texto")[0]
            rows = rows.text.split("\n")
        
            #[1:] => Ignore header row
            for row in rows[1:]:
                date, percent, occurrences = row.strip().split()
                occurrences = int(occurrences)
                if date == "Otros": 
                    # Averaging date for "Otros" results
                    # 0.5 ensures doesn't replace actual data
                    date = str(year + step/2 + 0.5)
                # Logic for handling occasional errors site produced in results
                if date in a[query]:
                    a[query][date] = max(a[query][date], occurrences)
                else:
                    a[query][date] = occurrences
    
        except: # Except no results for this date range page
            pass
    
    # Creating dataframe of Year and Occurrences for query
    df = pd.DataFrame(data=a)
    # Turning index (Year) into column
    df.reset_index(inplace=True)
    df.rename(columns={'index':'Year'}, inplace=True)
    df = df.apply(pd.to_numeric, errors='ignore')
    dfs.append(df)
    
    try:
        ax = df.plot.line(x="Year", y=query, ax=ax)
    except TypeError:
        pass # No data to plot (i.e. all hits 0)

driver.close()
