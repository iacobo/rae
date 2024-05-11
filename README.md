# CORDE Term Frequency Analysis

This project includes a Python script that performs frequency analysis of terms over time in the Real Academia Española's CORDE (Corpus Diacrónico del Español). The output resembles the Google Ngram Viewer, providing insights into the usage of specific terms across different periods.

## Project Structure

- `corde_freq_analysis.py`: The main Python script for fetching data and generating plots.
- `environment.yml`: Contains the specifications for the Conda environment required to run the script.
- `README.md`: This file, providing documentation for the project.

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

With the environment activated, run the script using:

```bash
python corde_freq_analysis.py
```
This will execute the term frequency analysis and display the resulting plots. The script fetches data from the CORDE, processes it, and plots the frequency of terms over the specified time range.

### Custromisation

You can customize the terms, time range, and other parameters by modifying the following variables in the `corde_freq_analysis.py`:

- `QUERIES`: List of terms to analyze.
- `START_YEAR`, `STOP_YEAR`: The range of years to cover in the analysis.
- `STEP`: Interval of years for querying the corpus.