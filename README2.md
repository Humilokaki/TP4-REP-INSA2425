# COVID and Home Advantage in Football: An Analysis of Results and xG Data in European Leagues

## Introduction

This study investigates whether the COVID-19 pandemic had an impact on the home advantage in football. The home advantage is a well-known phenomenon, and understanding its potential alteration during a period without crowds offers unique insights. By analyzing expected goals (xG) and points data across major European leagues, this study sheds light on the broader effects of the pandemic on competitive sports.

## Reproducibility

### How to Reproduce the Results

1. **Requirements**  
   - **System Requirements**: Any operating system that supports Docker.
   - **Dependencies**:  
    - Python: 3.8 
     - Libraries:  
       - pandas: 1.5.2  
       - scipy: 1.6.0
       - matplotlib: 3.7.5  
       - Jinja2: 3.1.4 
       - jupyterlab: 3.5.0
       - ipykernel: 6.21.3 

2. **Setting Up the Environment**  
   Use the provided `Dockerfile` to create a reproducible environment:
   ```bash
   docker build --build-arg MY_PYTHON_VERSION=3.8 --build-arg WORKFLOW=default -t covid-home-advantage .
   docker run -it -p 8888:8888 covid-home-advantage
   ```

3. **Reproducing Results**  
   **Access JupyterLab** **If** you just runned the Dockerfile : 
   1. Open your browser and go to `http://localhost:8888` and use the token displayed in the terminal to log in.
   2. Open `analysis/covid-home-advantage_analysis.ipynb` in your notebook environment with the kernel named `Python 3.8.x (Docker REP project)`
   3. Follow the steps to reproduce the analysis.
   **Else** :
   1. Run this command first and redo the steps above :
    ```bash
      jupyter lab --ip=0.0.0.0 --port=8888 --no-browser --allow-root
    ```
### Encountered Issues and Improvements
- **Challenges**:  
  - Data scraping involved manual extraction of JSON patterns from the website as no API was available.
  - No clear documentation on the data preprocessing steps was provided. 
  - No clear instructions on what versions of libraries were used in the original study.
- **Improvements**:  
  - Introduced a structured data pipeline for efficient preprocessing.
  - Documented the data scraping process for future reference.
### Is the Original Study Reproducible?
The original study's methodology was reproducible with the given data and tools. Our results closely matched those presented in the study, as evidenced by comparison tables and visualizations.

## Results and Metrics

1. **Difference Between Home and Away Points**  
   - Displayed in tables and bar charts across six leagues from 2014–2020.  
   - Example metric: `DIFF_POINTS_HOMEAWAY`, `DIFF_XPOINTS_HOMEAWAY`.

2. **Evolution of Mean Points (Per Match)**  
   - Plotted the seasonal trends for home and away matches.

3. **Statistical Tests**  
   - **Wilcoxon Signed-Rank Test**: Assessed differences between home and away metrics.  
   - **Mann-Whitney U Test**: Compared seasonal variations in home metrics.

### Analyze and Document Reproduced Results
- Results align with the original study's conclusions. COVID-19 had a measurable impact on home advantage across analyzed leagues.
- Supporting visualizations and statistical summaries validate findings.

### Document Any Deviations or Observations
- I noticed a major deviation in the Non-parametrical Wilcoxon Signed-Rank test results. The original study reported a constant p-value for xG of 0.000515 for all leagues. However, my results showed variations across leagues. It might be an error in the original study. Apart from this, most results were consistent.

## Variability Factors
- **Source of Data**: Understat's league data from 2014–2020.
- **Version of Data**: Potential inclusion of a larger dataset for extended analysis by using an other source.
- **Statistical Tests**: Alternative tests for robustness.
- *Environment*: Use of Python 3.9 for enhanced performance and compatibility with newer libraries.

### Draw Conclusions: Is it Reproducible?
Yes, the study is reproducible with the provided tools and data pipeline. The results consistently support the hypothesis that COVID-19 affected home advantage in football.

## Replicability

### Variability Factors
- **Version of Data**: Potential inclusion of a larger dataset for extended analysis by using an other source.
- **Statistical Tests**: Alternative tests for robustness.
- **Parameters**: Different parameters for statistical tests.
- **Environment**: Use of Python 3.9 for enhanced performance and compatibility with newer libraries.

### Variability Factors
- **List of Factors**: Identify all potential sources of variability (e.g., dataset splits, random seeds, hardware).  
  Example table:
  | Variability Factor | Possible Values     | Relevance                                    |
  |--------------------|---------------------|----------------------------------------------|
  | Version of Data    | 2014->2024                | Impacts consistency of random processes      |
  | Statistical Tests  | Test t, permutation_test | May affect computation time and results      |
  | Parameters         |    A voir       | Ensures comparability across experiments     |
  | Version of Python  | 3.9            | Compatibility and performance considerations |

- **Constraints Across Factors**:  


### Replication Execution
1. **Instructions**  
  Use the provided `Dockerfile` to create a replication environment (you can change the name of the image if you want both environments to be available on your machine):
   ```bash
   docker build --build-arg MY_PYTHON_VERSION=3.9 --build-arg WORKFLOW=replicate -t covid-home-advantage .
   docker run -it -p 8888:8888 covid-home-advantage
   ```

2. **Presentation and Analysis of Results**  
   - As we can see on the notebook, the difference in points gained at home and away and the mean points gained at home and away show that more points were gained away on the COVID season than other season on most championship. Moreover, we can see that a lot of statistics at home and away have big differencies except for the 2020 season for most championship. These results can also be linked to the result of the final test were there are big difference between xPoints and actual Points at home for the 2020 season for most championships.  
   - With thes results, we can conclude that, in fact, the COVID season had a negative impact on the home advantage in most championship.

### Does It Confirm the Original Study?
- Each point of the replicated study support the original one, even with others statistical test and the new data added to deepened the comprehension of this effect.

## Conclusion
The study can be reproduce with all the data and tools that have been provided. It can also be replicate with more data and different statistical test ton find the same conclusion.
