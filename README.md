# Reproducing the article : COVID and Home Advantage in Football: An Analysis of Results and xG Data in European Leagues

## Questions to help understand the subject

### What is the main research question or hypothesis of the paper?

- The main research question is to identify ether yes or not the COVID had an impact on the home advantage in Football.

#### Why is this question significant in its field?

- This question is significant because the home advantage is a well-known phenomenon in football, and it is important to understand if the COVID pandemic has had an impact on it.

### How does it address a gap in existing knowledge?

- The paper addresses a gap in existing knowledge by analyzing the home advantage in football during the COVID pandemic.

### How does this study fit within the broader landscape?


### What prior work does it build upon or differ from?

- This study has been built without looking at existing works in order to have a fresh view of the data used. He sited two articles that are related to this study : https://www.frontiersin.org/articles/10.3389/fspor.2020.593499/full and  https://www.sciencedirect.com/science/article/pii/S0165176520304249?casa_token=9CefrSZOgDwAAAAA:rQmhqD85JHVTWTuaS9OvhzFeMceq1vNHMw3rlijsNftVNeBVsWK3AruPue96CA-mRxQcm4RB3A .

### What are the primary objectives of the study?

- The primary objectives of the study is to show that COVID has had an effect on the home advantage in football.

#### Are there secondary or exploratory questions?

- At the end of the article, the author ask exploratory questions : if tactical approaches have changed or why and what fundamentally changes the way football is played.

---

## Key components for Reproducibility and Replicability

### Data

What data do we have ?

We have access to the understat.com/league data, that regroup a unique feature : expected goals (xG), expected goals against (xGA) and expected points (xPoints). The site reports such metrics for all football matches played since 2014 and in major European leagues such as :  Ligue 1, Liga, Calcio (Serie A), Bundesliga, EPL (Premier League), RFPL (Russian championship).

He consider at the end 14 361 matches and 174 teams in 6 championship.

### Methods and code 

1. Table showing the difference between points gained at home and away (same with xPoints) from 2014 to 2018 for the 6 championships

2. Plotting the evolution of mean gained points (per match) for all seasons from 2014 and 2020

As variables : results, xPoints, result_away and xPointsAway. 

3. Non-parametrical Wilcoxon Signed-Rank test to assess differences between home and away matches, considering either actual result, xPoints, or xG

4. Non-parametrical Mann-Whitney U test to assess differences between seasons (in terms of actual results home and xPoints home)

### Results and Metrics 


