# CORDE Term Frequency Analysis

This project includes a Python script that performs frequency analysis of terms over time in the Real Academia Española's CORDE (Corpus Diacrónico del Español). The output resembles the Google Ngram Viewer, providing insights into the usage of specific terms across different periods.

## Getting Started

### Prerequisites

- [Conda](https://docs.conda.io/en/latest/): Used for managing the project environment and dependencies. Ensure you have it installed on your system.

### Setting Up Your Environment

1. **Clone the repository** or download the files into a local directory.
2. **Navigate to the project directory** where the `environment.yml` is located.
3. **Create the Conda environment** by running the following command:
   ```bash
   conda env create -f environment.yml
   ```
   This will install Python, Selenium, Pandas, Matplotlib, and other necessary dependencies.
4. Activate the newly created environment:
    ```bash
    conda activate corde-analysis
    ```

### Running the Script

With the environment activated, run the script by specifying the terms you want to analyze and optionally setting the start year, stop year, and step size. Use the following syntax:

```bash
python corde_freq_analysis.py [terms] --start_year [start] --stop_year [stop] --step [step]
```

#### Parameters:

- `[terms]`: Space-separated list of words you want to search in the CORDE database. For example, "vos tú usted".
- `[start]`: (Optional) Start year of the time range for the search. Default is 900.
- `[stop]`: (Optional) Stop year of the time range for the search. Default is 2000.
- `[step]`: (Optional) Interval in years between searches. Default is 25.

#### Example Usage:

To analyze the terms "vos", "tú", and "usted" from the year 1600 to 2000 with a 50-year interval, run:

```bash
python corde_freq_analysis.py vos tú usted --start_year 1600 --stop_year 2000 --step 50
```

This command will fetch the usage frequency of the specified terms over the defined period and generate a plot to visualize the trends.

> [!NOTE]
>
> Ensure you have the required Selenium WebDriver installed and correctly configured to match the browser version on your system. This script is configured to use Firefox and its corresponding GeckoDriver.