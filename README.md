# The Illusion of Transit Equity

**Replication Data and Code Repository**  
This repository contains the spatial analysis workflows, data dictionaries, and replication scripts for the manuscript:  
*"The Illusion of Transit Equity: Evaluating Spatial Poverty Mismatches and Neighboring Transit Supply Across Three U.S. Metropolitan Archetypes"* (Under Review at *Cities*).

## Overview
This study evaluates the local spatial association between Census Block Group (CBG) poverty rates and neighboring public transit supply across three boundary-stable U.S. metropolitan subsets (Chicago, Atlanta, and Houston). The analysis moves beyond global correlation metrics to identify localized spatial outliers—specifically **High-Poverty/Low-Supply** mismatches—using the Bivariate Spatial Association (Lee's $L$) statistic.

## Data Sources
1. **Socio-Economic Data:** U.S. Census Bureau, 2020–2024 American Community Survey (ACS) 5-Year Estimates (Table C17002: Ratio of Income to Poverty Level).
2. **Transit Supply Data:** U.S. Environmental Protection Agency (EPA) Smart Location Database (SLD v3.0, circa 2020 GTFS feeds).
   - Variables used: `D4a` (proximity), `D4c` (frequency), and `D4d` (frequency density), composited into `AuthorComposite_TransitSupply`.

## Methodology & Software
- **Environment:** Python 3.11 / ArcGIS Pro 3.7 (`ArcPy`).
- **Spatial Econometric Statistic:** Bivariate Spatial Association (Lee's $L_i$).
- **Spatial Weights Matrix:** Row-standardized K-Nearest Neighbors ($k=8$ other retained CBGs).
- **Permutations:** 999 conditional random permutations (Two-sided pseudo-$p$, minimum bound = 0.002).
- **Random Seed:** `42` (for absolute reproducibility).

## Repository Contents
- `/scripts`: Contains the automated ArcPy execution script (`bivariate_lees_l_workflow.py`).
- `/data`: (Note: Large shapefiles are excluded to comply with GitHub limits. Analyzed CSVs containing CBG-level outputs and Local Spatial Association Categories are provided).
- `/figures`: Source data tables used to generate the manuscript's charts.

## License
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
