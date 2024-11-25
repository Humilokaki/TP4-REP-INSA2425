---
jupyter:
  jupytext:
    text_representation:
      extension: .md
      format_name: markdown
      format_version: '1.3'
      jupytext_version: 1.16.4
  kernelspec:
    display_name: Python 3
    language: python
    name: python3
---


# Covid Home Advantage Analysis

## Table showing the difference between points gained at home and away (same with xPoints) from 2014 to 2020 for the 6 championships

### Step 1 : Load and extract the required data
```python
import pandas as pd

# Load the data
data = pd.read_csv('data/understat-football-matches-2014-2020.csv')

# Filter the data to only include matches from 2014 to 2018 seasons
data = data[(data['season'] >= 2014) & (data['season'] <= 2020)]

# Filter the data to only include the championships, season, h_a, pts and xpts columns
data = data[['championship', 'season', 'h_a', 'pts', 'xpts']]

data.head()
```


### Step 2 : Calculate the difference between points gained at home and away for each championship and season
```python
# Total points gained at home and away for each championship and season
diff_pts = data.groupby(['championship', 'season', 'h_a'])['pts'].sum().unstack().fillna(0)
diff_pts['diff_pts'] = diff_pts['h'] - diff_pts['a']
diff_pts = diff_pts.reset_index()

# Same with xPoints
diff_xpts = data.groupby(['championship', 'season', 'h_a'])['xpts'].sum().unstack().fillna(0)
diff_xpts['diff_xpts'] = diff_xpts['h'] - diff_xpts['a']

# Combine the two dataframes by merging on championship, season with points and xPoints differences
data_diff = pd.merge(diff_pts, diff_xpts, on=['championship', 'season'])
```

### Step 3 : Display the table showing the difference
```python
import pandas as pd

# Assuming your data is in `df`
df = data_diff.rename(columns={'championship': 'LEAGUE', 'season': 'YEAR', 'diff_pts': 'DIFF_POINTS_HOMEAWAY', 'diff_xpts': 'DIFF_XPOINTS_HOMEAWAY'})

# Ensure that we're working with only the relevant columns
df = df[['LEAGUE', 'YEAR', 'DIFF_POINTS_HOMEAWAY', 'DIFF_XPOINTS_HOMEAWAY']]

# Round the values to integers
df['DIFF_POINTS_HOMEAWAY'] = df['DIFF_POINTS_HOMEAWAY'].round(0).astype(int)
df['DIFF_XPOINTS_HOMEAWAY'] = df['DIFF_XPOINTS_HOMEAWAY'].round(0).astype(int)

# Use Styler.bar to add horizontal bars to DIFF_POINTS_HOMEAWAY and DIFF_XPOINTS_HOMEAWAY
def add_bars_to_table(df):
    # Apply the bar style to the columns
    styled_df = df.style.bar(subset=['DIFF_POINTS_HOMEAWAY'], color=['red', 'lightgreen'], width=100, align='zero') \
                        .bar(subset=['DIFF_XPOINTS_HOMEAWAY'], color=['red', 'lightgreen'], width=100, align='zero') \
                        .set_table_styles([
                            {'selector': 'thead th', 'props': [('background-color', '#f2f2f2')]},  # Header styling
                            {'selector': 'tbody td', 'props': [('padding', '8px')]},  # Cell padding for better visibility
                            {'selector': 'table', 'props': [('border-collapse', 'collapse')]},  # Table border-collapse
                            {'selector': 'td', 'props': [('min-width', '80px')]}  # Ensure cell width is wide enough
                        ]) \
                        .hide(axis='index')  # Hide the index column for cleaner display
    
    return styled_df

# Display the styled table
styled_table = add_bars_to_table(df)
styled_table
```

### Conclusion

- We can see I have the same results as the paper.  

## Plotting the evolution of mean gained points (per match) for all seasons from 2014 and 2020

### Step 1 : Load and extract the required data


```python
import pandas as pd

data = pd.read_csv('data/understat-football-matches-2014-2020.csv')

# We only need the points, xPoints, result_away, xPointsAway, championships and season columns
data = data[['pts', 'xpts', 'h_a', 'championship', 'season']]

# Filter the data to only include matches from 2014 to 2020
data = data[(data['season'] >= 2014) & (data['season'] <= 2020)]

data.head()

```

### Step 2 : Calculate the mean gained points per match for each season


```python
# Calculate the mean gained points and expected points per match for each season by grouping by championship, season, and home/away
mean_stats = data.groupby(['championship', 'season', 'h_a']).agg(
    mean_pts=('pts', 'mean'),
    mean_xpts=('xpts', 'mean')
).unstack().fillna(0)

# Rename columns for clarity
mean_stats.columns = ['result_away', 'result', 'xPointsAway', 'xPoints']

# Reset index to make 'championship' and 'season' columns
mean_stats.reset_index(inplace=True)



mean_stats.head()

```

### Step 3 : Plot the evolution of mean gained points per match for all seasons from 2014 to 2020


```python
import matplotlib.pyplot as plt

# Plot the evolution of mean gained points per match for all seasons

for championship in mean_stats['championship'].unique():
    champ_data = mean_stats[mean_stats['championship'] == championship]
 
    plt.figure(figsize=(12, 6))
    plt.plot(champ_data['season'], champ_data['result'], label='result', marker='o', color='blue')
    plt.plot(champ_data['season'], champ_data['xPoints'], label='xPoints', marker='o', color='orange')
    plt.plot(champ_data['season'], champ_data['result_away'], label='result_away', marker="o", color='green')
    plt.plot(champ_data['season'], champ_data['xPointsAway'], label='xPointsAway', marker='o', color='red')
  
    plt.xlabel('Season')
    plt.ylabel('Mean Points per Match')
    plt.title('Evolution of Mean Gained Points per Match (2014-2020) - ' + championship)
    plt.legend()
    plt.grid(True)
    plt.show()

```


### Conclusion

- We can see that I have the same results as the paper.

## Non-parametrical Wilcoxon Signed-Rank test to assess differences between home and away matches, considering either actual result, xPoints, or xG

### Step 1 : Load and extract the required data

```python
from scipy.stats import wilcoxon
import numpy as np
import pandas as pd

data = pd.read_csv('data/understat-football-matches-2014-2020.csv')

data = data[(data['season'] >= 2014) & (data['season'] <= 2020)]

data = data[['championship', 'season', 'pts', 'xpts', 'xG', 'h_a']]

data.head()
```


### Step 2 : Perform the Wilcoxon Signed-Rank test for each championship and season

```python
# Initialize a list to store Wilcoxon test results
wilcoxon_results = []

# Iterate over championships and seasons to compute Wilcoxon tests
for (championship, season), group in data.groupby(['championship', 'season']):
    home_data = group[group['h_a'] == 'h']
    away_data = group[group['h_a'] == 'a']
    
    # Ensure the datasets have the same length
    if len(home_data) == len(away_data):
        # Wilcoxon test for points
        wilco_points = wilcoxon(home_data['pts'], away_data['pts'])
        
        # Wilcoxon test for xPoints
        wilco_xpoints = wilcoxon(home_data['xpts'], away_data['xpts'])
        
        # Wilcoxon test for xG
        wilco_xg = wilcoxon(home_data['xG'], away_data['xG'])
        
        # Compute effect size (Cohen's d)
        def compute_cohens_d(a, b):
            diff = a.mean() - b.mean()
            pooled_std = np.sqrt(((len(a) - 1) * a.std()**2 + (len(b) - 1) * b.std()**2) / (len(a) + len(b) - 2))
            return diff / pooled_std if pooled_std != 0 else np.nan
        
        cohens_d_points = compute_cohens_d(home_data['pts'], away_data['pts'])
        cohens_d_xpoints = compute_cohens_d(home_data['xpts'], away_data['xpts'])
        cohens_d_xg = compute_cohens_d(home_data['xG'], away_data['xG'])
        
        # Append results to the list
        wilcoxon_results.append({
            'league': championship,
            'season': season,
            'wilco-result': wilco_points.statistic,
            'wilco-result-pvalue': wilco_points.pvalue,
            'result-cohend': cohens_d_points,
            'wilco-xpoint': wilco_xpoints.statistic,
            'wilco-xpoints-pvalue': wilco_xpoints.pvalue,
            'xpoints-cohend': cohens_d_xpoints,
            'wilco-xg': wilco_xg.statistic,
            'wilco-xg-pvalue': wilco_xg.pvalue,
            'xg-cohend': cohens_d_xg
        })

# Convert the results into a DataFrame
wilcoxon_df = pd.DataFrame(wilcoxon_results)
```

### Step 3 : Format the results Table


```python
# Highlight p-values < 0.05 and Cohen's d thresholds
def highlight_pval(val):
    return "background-color: red" if val < 0.05 else ""

def highlight_cohens_d(val):
    if val < 0.2:
        return "background-color: yellow"  # Small effect size
    elif 0.2 <= val < 0.5:
        return "background-color: orange"  # Medium effect size
    elif val >= 0.5:
        return "background-color: red"  # Large effect size
    return ""

# Apply highlights to the DataFrame
styled_wilcoxon_df = wilcoxon_df.style.applymap(highlight_pval, subset=['wilco-result-pvalue', 'wilco-xpoints-pvalue', 'wilco-xg-pvalue']) \
                                       .applymap(highlight_cohens_d, subset=['result-cohend', 'xpoints-cohend', 'xg-cohend'])

# Display the styled DataFrame
styled_wilcoxon_df
```

### Conclusion

- Here, there is some differcences with the paper. The cohend d values are the same as the paper but the p-values and the statistics are different. They still are pretty close to the paper's results.

## Non-parametrical Mann-Whitney U test to assess differences between seasons (in terms of actual results home and xPoints home)

### Step 1 : Load and extract the required data

```python
import pandas as pd

df = pd.read_csv('data/understat-football-matches-2014-2020.csv')

df = df[(df['season'] >= 2014) & (df['season'] <= 2020)]

df = df[['championship', 'season', 'xpts', 'h_a']]

# Filter the data to only include home
df = df[df['h_a'] == 'h']
```

### Step 2 : Perform the Mann-Whitney U test for each championship

```python

import pandas as pd
import numpy as np
import scipy.stats as stats

# Assuming 'df' contains your data and includes columns 'league', 'season', and 'xPoints'

# List of leagues
leagues = df['championship'].unique()

# Function to compute Mann-Whitney U test p-values and format them
def compute_mannwhitney_by_league(league, df):
    # Filter data for the league
    league_data = df[df['championship'] == league]
    
    seasons = sorted(league_data['season'].unique())
    
    p_values = []

    # Perform Mann-Whitney U test for each pair of seasons
    for season1 in seasons:
        row = []
        for season2 in seasons:
            # Filter data for the relevant seasons
            data1 = league_data[league_data['season'] == season1]['xpts']
            data2 = league_data[league_data['season'] == season2]['xpts']
            
            # Perform Mann-Whitney U test
            stat, p_value = stats.mannwhitneyu(data1, data2, alternative='two-sided', method='asymptotic')
            
            # Store the p-value in the appropriate cell
            row.append(p_value)
        p_values.append(row)

    # Convert p-values to DataFrame for easy manipulation
    p_value_df = pd.DataFrame(p_values, columns=[str(s) for s in seasons], index=[str(s) for s in seasons])

    # Remove the upper triangular part (above the diagonal) to show only the lower part
    lower_triangular_mask = np.tril(np.ones(p_value_df.shape), k=-1).astype(bool)
    p_value_df = p_value_df.where(lower_triangular_mask)

    def highlight(p_value):
        if p_value < 0.05:
            return 'color: red'
        return ''

    styled_df = p_value_df.style.applymap(highlight)

    return styled_df

# Generate the Mann-Whitney U test table for each league
for league in leagues:
    print(f"\n{league} xPoints Change Significance with Mann-Whitney U Test")
    styled_table = compute_mannwhitney_by_league(league, df)
    
    display(styled_table)

```

### Conclusion


